##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test add-form"""
import unittest

from zope.browser.interfaces import IAdding
from zope.component import getMultiAdapter
from zope.component.eventtesting import PlacelessSetup as EventPlacelessSetup
from zope.component.eventtesting import getEvents
from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.formlib.widget import CustomWidgetFactory
from zope.interface import Interface
from zope.interface import implementer
from zope.interface.interfaces import IComponentLookup
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine
from zope.schema import accessors
from zope.security.checker import CheckerPublic
from zope.site.site import SiteManagerAdapter

import zope.app.form.testing as ztapi
from zope.app.form.browser import TextWidget as Text
from zope.app.form.browser.add import AddView
from zope.app.form.browser.add import AddViewFactory
from zope.app.form.browser.metaconfigure import AddFormDirective
from zope.app.form.browser.submit import Update
# Foo needs to be imported as globals() are checked
from zope.app.form.browser.tests.test_editview import Foo
from zope.app.form.browser.tests.test_editview import FooBarAdapter
from zope.app.form.browser.tests.test_editview import IBar
from zope.app.form.browser.tests.test_editview import IFoo


class PlacelessSetup(CAPlacelessSetup, EventPlacelessSetup):

    def setUp(self, doctesttest=None):
        CAPlacelessSetup.setUp(self)
        EventPlacelessSetup.setUp(self)


class Context:

    def action(self, discriminator, callable, args=(), kw={}):
        self.last_action = (discriminator, callable, args, kw)


class ITest(Interface):

    name = TextLine()
    first = TextLine()
    last = TextLine()
    email = TextLine()
    address = TextLine()
    getfoo, setfoo = accessors(TextLine())
    extra1 = TextLine()
    extra2 = TextLine(required=False)


@implementer(ITest)
class C:

    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    def getfoo(self): return self._foo
    def setfoo(self, v): self._foo = v


class V:
    name_widget = CustomWidgetFactory(Text)
    first_widget = CustomWidgetFactory(Text)
    last_widget = CustomWidgetFactory(Text)
    email_widget = CustomWidgetFactory(Text)
    address_widget = CustomWidgetFactory(Text)
    getfoo_widget = CustomWidgetFactory(Text)
    extra1_widget = CustomWidgetFactory(Text)
    extra2_widget = CustomWidgetFactory(Text)


class FooV:
    bar_widget = CustomWidgetFactory(Text)


class SampleData:

    name = "foo"
    first = "bar"
    last = "baz"
    email = "baz@dot.com"
    address = "aa"
    getfoo = "foo"
    extra1 = "extra1"
    extra2 = "extra2"


class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        self._context = Context()
        super().setUp()
        ztapi.provideAdapter(IFoo, IBar, FooBarAdapter)

    def _invoke_add(self, schema=ITest, name="addthis",
                    permission="zope.Public",
                    label="Add this", content_factory=C, class_=V,
                    arguments=['first', 'last'], keyword_arguments=['email'],
                    set_before_add=['getfoo'], set_after_add=['extra1'],
                    fields=None):
        """Call the 'add' factory to process arguments into 'args'."""
        AddFormDirective(self._context,
                         schema=schema,
                         name=name,
                         permission=permission,
                         label=label,
                         content_factory=content_factory,
                         class_=class_,
                         arguments=arguments,
                         keyword_arguments=keyword_arguments,
                         set_before_add=set_before_add,
                         set_after_add=set_after_add,
                         fields=fields
                         )()

    def test_add_no_fields(self):
        _context = self._context
        self._invoke_add()
        result1 = _context.last_action
        self._invoke_add(
            fields=[
                "name",
                "first",
                "last",
                "email",
                "address",
                "getfoo",
                "extra1",
                "extra2",
            ]
        )
        result2 = _context.last_action

        self.assertEqual(result1, result2)

    def test_add_error_handling(self):
        # cannot use a field in arguments if it is not mentioned in fields
        self.assertRaises(ValueError, self._invoke_add,
                          fields="first email getfoo extra1".split())

        # cannot use a field in keyword_arguments if it is not
        # mentioned in fields

        self.assertRaises(ValueError, self._invoke_add,
                          fields="first last getfoo extra1".split())

        # cannot use a field in set_before_add if it is not mentioned in fields
        self.assertRaises(ValueError, self._invoke_add,
                          fields="first last email extra1".split())

        # cannot use a field in set_after_add if it is not mentioned in fields
        self.assertRaises(ValueError, self._invoke_add,
                          fields="first last email getfoo".split())

        # cannot use an optional field in arguments
        self.assertRaises(ValueError, self._invoke_add, arguments=["extra2"])

    def test_add(self, args=None):
        self._invoke_add()
        (descriminator, callable, args, kw) = self._context.last_action

        self.assertEqual(descriminator,
                         ('view', IAdding, 'addthis', IBrowserRequest,
                          IDefaultBrowserLayer))

        self.assertEqual(callable, AddViewFactory)

        (name, schema, label, permission, layer, template,
         default_template, bases, for_, fields, content_factory,
         arguments, keyword_arguments, set_before_add,
         set_after_add) = args

        self.assertEqual(name, 'addthis')
        self.assertEqual(schema, ITest)
        self.assertEqual(label, 'Add this')
        self.assertEqual(permission, CheckerPublic)  # 'zope.Public' translated
        self.assertEqual(layer, IDefaultBrowserLayer)
        self.assertEqual(template, 'add.pt')
        self.assertEqual(default_template, 'add.pt')
        self.assertEqual(bases, (V, AddView, ))
        self.assertEqual(for_, IAdding)
        self.assertEqual(" ".join(fields),
                         "name first last email address getfoo extra1 extra2")
        self.assertEqual(content_factory, C)
        self.assertEqual(" ".join(arguments),
                         "first last")
        self.assertEqual(" ".join(keyword_arguments),
                         "email")
        self.assertEqual(" ".join(set_before_add),
                         "getfoo")
        self.assertEqual(" ".join(set_after_add),
                         "extra1 name address extra2")

    def test_add_content_factory_id(self, args=None):
        self._invoke_add(content_factory='C')
        (descriminator, callable, args, kw) = self._context.last_action

        self.assertEqual(descriminator,
                         ('view', IAdding, 'addthis', IBrowserRequest,
                          IDefaultBrowserLayer))

        self.assertEqual(callable, AddViewFactory)

        (name, schema, label, permission, layer, template,
         default_template, bases, for_, fields, content_factory,
         arguments, keyword_arguments, set_before_add,
         set_after_add) = args

        self.assertEqual(name, 'addthis')
        self.assertEqual(schema, ITest)
        self.assertEqual(label, 'Add this')
        self.assertEqual(permission, CheckerPublic)  # 'zope.Public' translated
        self.assertEqual(layer, IDefaultBrowserLayer)
        self.assertEqual(template, 'add.pt')
        self.assertEqual(default_template, 'add.pt')
        self.assertEqual(bases, (V, AddView, ))
        self.assertEqual(for_, IAdding)
        self.assertEqual(" ".join(fields),
                         "name first last email address getfoo extra1 extra2")
        self.assertEqual(content_factory, 'C')
        self.assertEqual(" ".join(arguments),
                         "first last")
        self.assertEqual(" ".join(keyword_arguments),
                         "email")
        self.assertEqual(" ".join(set_before_add),
                         "getfoo")
        self.assertEqual(" ".join(set_after_add),
                         "extra1 name address extra2")

    def test_create(self):

        @implementer(IAdding)
        class Adding:

            def __init__(self, test):
                self.test = test

            def add(self, ob):
                self.ob = ob
                self.test.assertEqual(
                    ob.__dict__,
                    {'args': ("bar", "baz"),
                     'kw': {'email': 'baz@dot.com'},
                     '_foo': 'foo',
                     })
                return ob

            def nextURL(self):
                return "."

        adding = Adding(self)
        self._invoke_add()
        (descriminator, callable, args, kw) = self._context.last_action
        AddViewFactory(*args)
        request = TestRequest()
        view = getMultiAdapter((adding, request), name='addthis')
        content = view.create('a', 0, abc='def')

        self.assertIsInstance(content, C)
        self.assertEqual(content.args, ('a', 0))
        self.assertEqual(content.kw, {'abc': 'def'})

    def test_create_content_factory_id(self):

        @implementer(IAdding)
        class Adding:

            def __init__(self, test):
                self.test = test

            def add(self, ob):
                self.ob = ob
                self.test.assertEqual(
                    ob.__dict__,
                    {'args': ("bar", "baz"),
                     'kw': {'email': 'baz@dot.com'},
                     '_foo': 'foo',
                     })
                return ob

            def nextURL(self):
                return "."

        # register content factory for content factory id lookup
        ztapi.provideAdapter(None, IComponentLookup, SiteManagerAdapter)
        ztapi.provideUtility(IFactory, Factory(C), name='C')

        adding = Adding(self)
        self._invoke_add(content_factory='C')
        (descriminator, callable, args, kw) = self._context.last_action
        AddViewFactory(*args)
        request = TestRequest()
        view = getMultiAdapter((adding, request), name='addthis')
        content = view.create('a', 0, abc='def')

        self.assertIsInstance(content, C)
        self.assertEqual(content.args, ('a', 0))
        self.assertEqual(content.kw, {'abc': 'def'})

    def test_createAndAdd(self):

        @implementer(IAdding)
        class Adding:

            def __init__(self, test):
                self.test = test

            def add(self, ob):
                self.ob = ob
                self.test.assertEqual(
                    ob.__dict__,
                    {'args': ("bar", "baz"),
                     'kw': {'email': 'baz@dot.com'},
                     '_foo': 'foo',
                     })
                return ob

            def nextURL(self):
                return "."

        adding = Adding(self)
        self._invoke_add()
        (descriminator, callable, args, kw) = self._context.last_action
        AddViewFactory(*args)
        request = TestRequest()
        view = getMultiAdapter((adding, request), name='addthis')

        view.createAndAdd(SampleData.__dict__)

        self.assertEqual(adding.ob.extra1, "extra1")
        self.assertEqual(adding.ob.extra2, "extra2")
        self.assertEqual(adding.ob.name, "foo")
        self.assertEqual(adding.ob.address, "aa")
        self.assertEqual(len(getEvents(IObjectCreatedEvent)), 1)
        self.assertEqual(len(getEvents(IObjectModifiedEvent)), 1)

    def test_createAndAdd_w_adapter(self):

        @implementer(IAdding)
        class Adding:

            def __init__(self, test):
                self.test = test

            def add(self, ob):
                self.ob = ob
                self.test.assertEqual(ob.__dict__, {'foo': 'bar'})
                return ob

            def nextURL(self):
                return "."

        adding = Adding(self)
        self._invoke_add(
            schema=IBar, name="addthis", permission="zope.Public",
            label="Add this", content_factory=Foo, class_=FooV,
            arguments=None, keyword_arguments=None,
            set_before_add=["bar"], set_after_add=None,
            fields=None
        )
        (descriminator, callable, args, kw) = self._context.last_action
        AddViewFactory(*args)
        request = TestRequest()
        view = getMultiAdapter((adding, request), name='addthis')

        view.createAndAdd({'bar': 'bar'})

    def test_hooks(self):

        @implementer(IAdding)
        class Adding:
            pass

        adding = Adding()
        self._invoke_add()
        (descriminator, callable, args, kw) = self._context.last_action
        AddViewFactory(*args)
        request = TestRequest()

        request.form.update({
            "field.%s" % k: v
            for (k, v) in dict(SampleData.__dict__).items()
        })
        request.form[Update] = ''
        view = getMultiAdapter((adding, request), name='addthis')

        # Add hooks to V

        l_ = [None]

        def add(aself, ob):
            l_[0] = ob
            self.assertEqual(
                ob.__dict__,
                {'args': ("bar", "baz"),
                 'kw': {'email': 'baz@dot.com'},
                 '_foo': 'foo',
                 })
            return ob

        V.add = add

        V.nextURL = lambda self: 'next'

        try:
            self.assertEqual(view.update(), '')

            self.assertEqual(view.errors, ())

            self.assertEqual(l_[0].extra1, "extra1")
            self.assertEqual(l_[0].extra2, "extra2")
            self.assertEqual(l_[0].name, "foo")
            self.assertEqual(l_[0].address, "aa")

            self.assertEqual(request.response.getHeader("Location"), "next")

            # Verify that calling update again doesn't do anything.
            l_[0] = None
            self.assertEqual(view.update(), '')
            self.assertEqual(l_[0], None)

        finally:
            # Uninstall hooks
            del V.add
            del V.nextURL


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(Test)

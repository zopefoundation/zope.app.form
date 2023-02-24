#############################################################################
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
"""Form Directives Tests"""
import unittest
from io import StringIO

from zope.component.testing import PlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.configuration.xmlconfig import xmlconfig
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.browser import TestRequest
from zope.schema import Int
from zope.schema import TextLine
from zope.traversing.interfaces import TraversalError

from zope import component
from zope.app.form.browser import TextWidget
from zope.app.form.tests import utils


template = """<configure
   xmlns='http://namespaces.zope.org/zope'
   xmlns:browser='http://namespaces.zope.org/browser'
   i18n_domain='zope'>
   %s
   </configure>"""


request = TestRequest()


class Schema(Interface):

    text = TextLine(
        title='Text',
        description='Nice text',
        required=False)


class IC(Schema):
    pass


@implementer(IC)
class Ob:
    pass


unwrapped_ob = Ob()
ob = utils.securityWrap(unwrapped_ob, IC)


class ISomeWidget(Interface):
    displayWidth = Int(
        title="Display Width",
        default=20,
        required=True)


@implementer(ISomeWidget)
class SomeWidget(TextWidget):
    pass


class Test(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super().setUp()
        import zope.component
        XMLConfig('meta.zcml', zope.component)()
        import zope.app.form.browser
        XMLConfig('meta.zcml', zope.app.form.browser)()
        import zope.browsermenu
        XMLConfig('meta.zcml', zope.browsermenu)()

        from zope.traversing.adapters import DefaultTraversable
        from zope.traversing.interfaces import ITraversable

        component.provideAdapter(DefaultTraversable, (None,), ITraversable)

    def testAddForm(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='add.html'),
            None)
        xmlconfig(StringIO(template % ("""
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.formlib.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:addform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="add.html"
              label="Add a ZPT page"
              fields="text"
              permission="zope.Public" />
            """)))

        v = component.getMultiAdapter((ob, request), name='add.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testEditForm(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='edit.html'),
            None)
        xmlconfig(StringIO(template % ("""
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.formlib.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:editform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="edit.html"
              label="Edit a ZPT page"
              fields="text"
              permission="zope.Public" />
            """)))

        v = component.getMultiAdapter((ob, request), name='edit.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testEditFormWithMenu(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='edit.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <browser:menu id="test_menu" title="Test menu"/>
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.formlib.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />
          <browser:editform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="edit.html"
              label="Edit a ZPT page"
              fields="text"
              permission="zope.Public"
              menu="test_menu"
              title="Test View"
              />
            ''')))

        v = component.queryMultiAdapter((ob, request), name='edit.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testSchemaDisplay(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='view.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.IField"
              provides="zope.formlib.interfaces.IDisplayWidget"
              factory="zope.app.form.browser.DisplayWidget"
              permission="zope.Public"
              />

          <browser:schemadisplay
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="view.html"
              label="View a ZPT page"
              fields="text"
              permission="zope.Public" />
            ''')))

        v = component.queryMultiAdapter((ob, request), name='view.html')
        # expect to fail as standard macros are not configured
        self.assertRaises(TraversalError, v)

    def testAddFormWithWidget(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='add.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.formlib.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:addform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="add.html"
              label="Add a ZPT page"
              fields="text"
              permission="zope.Public">

            <widget
                field="text"
                class="zope.app.form.browser.tests.test_directives.SomeWidget"
                displayWidth="30"
                extra="foo"
                />

          </browser:addform>
            ''')), )

        view = component.queryMultiAdapter((ob, request), name='add.html')
        self.assertTrue(hasattr(view, 'text_widget'))
        self.assertTrue(isinstance(view.text_widget, SomeWidget))
        self.assertEqual(view.text_widget.extra, 'foo')
        self.assertEqual(view.text_widget.displayWidth, 30)

    def testEditFormWithWidget(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='edit.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.ITextLine"
              provides="zope.formlib.interfaces.IInputWidget"
              factory="zope.app.form.browser.TextWidget"
              permission="zope.Public"
              />

          <browser:editform
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="edit.html"
              label="Edit a ZPT page"
              fields="text"
              permission="zope.Public">

            <widget
                field="text"
                class="zope.app.form.browser.tests.test_directives.SomeWidget"
                displayWidth="30"
                extra="foo"
                />

          </browser:editform>
            ''')), )

        view = component.queryMultiAdapter((ob, request), name='edit.html')
        self.assertTrue(hasattr(view, 'text_widget'))
        self.assertTrue(isinstance(view.text_widget, SomeWidget))
        self.assertEqual(view.text_widget.extra, 'foo')
        self.assertEqual(view.text_widget.displayWidth, 30)

    def testSchemaDisplayWithWidget(self):
        self.assertEqual(
            component.queryMultiAdapter((ob, request), name='view.html'),
            None)
        xmlconfig(StringIO(template % ('''
          <view
              type="zope.publisher.interfaces.browser.IBrowserRequest"
              for="zope.schema.interfaces.IField"
              provides="zope.formlib.interfaces.IDisplayWidget"
              factory="zope.app.form.browser.DisplayWidget"
              permission="zope.Public"
              />

          <browser:schemadisplay
              for="zope.app.form.browser.tests.test_directives.IC"
              schema="zope.app.form.browser.tests.test_directives.Schema"
              name="view.html"
              label="View a ZPT page"
              fields="text"
              permission="zope.Public">

            <browser:widget
                field="text"
                class="zope.app.form.browser.tests.test_directives.SomeWidget"
                displayWidth="30"
                extra="foo"
                />
          </browser:schemadisplay>
            ''')))

        view = component.queryMultiAdapter((ob, request), name='view.html')
        self.assertTrue(hasattr(view, 'text_widget'))
        self.assertTrue(isinstance(view.text_widget, SomeWidget))
        self.assertEqual(view.text_widget.extra, 'foo')
        self.assertEqual(view.text_widget.displayWidth, 30)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

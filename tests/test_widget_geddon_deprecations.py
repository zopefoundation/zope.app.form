##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""XXX short summary goes here.

$Id: test_widget_geddon_deprecations.py,v 1.1 2003/06/05 20:13:09 jim Exp $
"""

from zope.testing.doctestunit import DocTestSuite
from zope.publisher.browser import TestRequest
from zope.app.form import utility
from zope.app.form.widget import Widget, CustomWidget
from zope.schema import Text
from zope.schema.interfaces import IText
from zope.app.tests.placelesssetup import setUp, tearDown
from zope.component.view import provideView
from zope.publisher.interfaces.browser import IBrowserPresentation
import warnings

class TestView:

    bar = CustomWidget(Widget, uncle='bob')
    
    def __init__(self, context, request):
        self.context, self.request = context, request

class TestWidget:
    
    def __init__(self, context, request):
        self.context, self.request = context, request

    def __call__(self):
        return '42'

theField = Text(__name__="foo")


def test_widget_in_wrong_name():
    """
    >>> warned = None
    >>> def fakewarn(*args, **kw):
    ...     global warned
    ...     warned = args

    >>> utility.warn = fakewarn
    
    >>> request = TestRequest()
    >>> view = TestView(None, request)
    >>> view.foo = Widget(theField, request)
    >>> int(hasattr(view, 'foo_widget'))
    0

    >>> warned
    >>> utility.setUpWidget(view, 'foo', Text())

    >>> print warned[0]
    View (TestView) saved a widget (foo) without a '_widget' suffix.
    Url: http://127.0.0.1

    >>> warned[1].__name__
    'DeprecationWarning'

    >>> int(hasattr(view, 'foo_widget'))
    1

    >>> utility.warn = warnings.warn
    """

def test_widget_gets_warning_w_custom_widget_in_wrong_name():
    """
    >>> warned = None
    >>> def fakewarn(*args, **kw):
    ...     global warned
    ...     warned = args

    >>> utility.warn = fakewarn

    >>> request = TestRequest()
    >>> view = TestView(None, request)
    >>> int(hasattr(view, 'bar_widget'))
    0


    >>> warned
    >>> utility.setUpWidget(view, 'bar', Text())

    >>> print warned[0]
    View (TestView) saved a widget (bar) without a '_widget' suffix.
    Url: http://127.0.0.1

    >>> warned[1].__name__
    'DeprecationWarning'

    >>> view.bar_widget.uncle
    'bob'

    Make sure we updated the old attr:

    >>> view.bar.uncle
    'bob'

    >>> utility.warn = warnings.warn
    """

def test_clients_using_wrong_name():
    """
    >>> warned = None
    >>> def fakewarn(*args, **kw):
    ...     global warned
    ...     warned = args

    >>> utility.warn = fakewarn

    >>> setUp()
    >>> provideView(IText, 'test', IBrowserPresentation, TestWidget)

    >>> request = TestRequest()
    >>> view = TestView(None, request)
    >>> utility.setUpWidget(view, 'foo', Text(), vname='test')
    >>> view.foo_widget()
    '42'
    >>> warned
    >>> view.foo()
    '42'

    >>> print warned[0]
    View (TestView) saved a widget (foo) without a '_widget' suffix.
    Url: http://127.0.0.1

    >>> warned[1].__name__
    'DeprecationWarning'
    
    >>> tearDown()
    """

def test_suite(): return DocTestSuite()
if __name__ == '__main__': unittest.main()
##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Radio Widget Functional Tests

$Id: $
"""
import unittest
from persistent import Persistent
import transaction

from support import *

from zope.interface import Interface
from zope.interface import implements

from zope.schema import Bool

from zope.app.traversing.api import traverse

from zope.app.testing.functional import BrowserTestCase


class IFoo(Interface):

    bar = Bool(title=u'Bar')

registerEditForm(IFoo, widgets={
    'bar': { 'class': 'zope.app.form.browser.BooleanRadioWidget' }})


class Foo(Persistent):

    implements(IFoo)

    def __init__(self):
        self.bar = True

defineSecurity(Foo, IFoo)


class Test(BrowserTestCase):


    def test_display_editform(self):
        self.getRootFolder()['foo'] = Foo()
        transaction.commit()

        # display edit view
        response = self.publish('/foo/edit.html')
        self.assertEqual(response.getStatus(), 200)
        
        # bar field should be displayed as two radio buttons
        self.assert_(patternExists(
            '<input .*checked="checked".*name="field.bar".*type="radio".*'
            'value="on".* />',
            response.getBody()))
        self.assert_(patternExists(
            '<input .*name="field.bar".*type="radio".*value="off".* />',
            response.getBody()))

        # a hidden element is used to note that the field is present
        self.assert_(patternExists(
            '<input name="field.bar-empty-marker" type="hidden" value="1".* />',
            response.getBody()))


    def test_submit_editform(self):
        self.getRootFolder()['foo'] = Foo()
        transaction.commit()

        # submit edit view
        response = self.publish('/foo/edit.html', form={
            'UPDATE_SUBMIT' : '',
            'field.bar' : 'off'})
        self.assertEqual(response.getStatus(), 200)
        self.assert_(updatedMsgExists(response.getBody()))

        # check new values in object
        object = traverse(self.getRootFolder(), 'foo')
        self.assertEqual(object.bar, False)


    def test_missing_value(self):
        self.getRootFolder()['foo'] = Foo()
        transaction.commit()
        
        # temporarily make bar field not required
        IFoo['bar'].required = False

        # submit missing value for bar
        response = self.publish('/foo/edit.html', form={
            'UPDATE_SUBMIT' : '',
            'field.bar-empty-marker' : '' })
        self.assertEqual(response.getStatus(), 200)
        self.assert_(updatedMsgExists(response.getBody()))

        # confirm use of missing_value as new object value
        self.assert_(IFoo['bar'].missing_value is None)
        object = traverse(self.getRootFolder(), 'foo')
        self.assert_(object.bar is None)
        
        # restore bar required state
        IFoo['bar'].required = True


    def test_required_validation(self):
        self.getRootFolder()['foo'] = Foo()
        transaction.commit()
        
        self.assert_(IFoo['bar'].required)

        # submit missing value for required field bar
        response = self.publish('/foo/edit.html', form={
            'UPDATE_SUBMIT' : '',
            'field.bar-empty-marker' : '1'})
        self.assertEqual(response.getStatus(), 200)
        
        # confirm error msgs
        self.assert_(missingInputErrorExists('bar', response.getBody()))


    def test_invalid_allowed_value(self):
        self.getRootFolder()['foo'] = Foo()
        transaction.commit()

        # submit a value for bar isn't allowed
        response = self.publish('/foo/edit.html', form={
            'UPDATE_SUBMIT' : '',
            'field.bar' : 'bogus' })
        self.assertEqual(response.getStatus(), 200)

        self.assert_(validationErrorExists('bar', 'Invalid value',
            response.getBody()))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')

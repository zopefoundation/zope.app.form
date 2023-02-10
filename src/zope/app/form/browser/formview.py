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
"""Form View Classes"""
__docformat__ = 'restructuredtext'

import transaction
from zope.formlib.interfaces import IInputWidget
from zope.formlib.interfaces import WidgetsError

from zope.app.form.browser.editview import EditView
from zope.app.form.browser.i18n import _
from zope.app.form.browser.submit import Update
from zope.app.form.utility import applyWidgetsChanges
from zope.app.form.utility import setUpWidgets


class Data(dict):
    """Dictionary wrapper to make keys available as attributes."""

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


class FormView(EditView):

    def getData(self):
        """Get the data for the form.

        This method should return a dictionary mapping field names to values.
        """
        raise NotImplementedError(
            'Must be implemented by a specific form class')

    def setData(self, data):
        """Set the data gotten from a form.

        The data will be a dictionary of fieldnames to values.

        May return a status message.
        """
        raise NotImplementedError(
            'Must be implemented by a specific form class')

    def _setUpWidgets(self):
        self.data = Data(self.getData())
        setUpWidgets(
            self, self.schema, IInputWidget, initial=self.data,
            names=self.fieldNames)

    def update(self):
        if self.update_status is not None:
            # We've been called before. Just return the status we previously
            # computed.
            return self.update_status

        status = ''

        if Update in self.request:
            try:
                changed = applyWidgetsChanges(
                    self, self.schema, target=self.data, names=self.fieldNames)
            except WidgetsError as errors:  # pragma: no cover
                self.errors = errors
                status = _("An error occurred.")
                transaction.doom()
            else:
                if changed:
                    status = self.setData(self.data)
                setUpWidgets(
                    self, self.schema, IInputWidget, initial=self.data,
                    ignoreStickyValues=True, names=self.fieldNames)

        self.update_status = status
        return status

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
"""Edit View Classes"""
__docformat__ = 'restructuredtext'

import datetime
import sys

import transaction
import zope.component
from zope.browserpage import ViewPageTemplateFile
from zope.browserpage.simpleviewclass import SimpleViewClass
from zope.event import notify
from zope.formlib.interfaces import WidgetsError
from zope.interface import Interface
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import getFieldNamesInOrder
from zope.security.checker import NamesChecker
from zope.security.checker import defineChecker

from zope.app.form.browser.i18n import _
from zope.app.form.browser.submit import Update
from zope.app.form.utility import applyWidgetsChanges
from zope.app.form.utility import setUpEditWidgets


PY310_OR_OLDER = sys.version_info < (3, 11)


class EditView(BrowserView):
    """Simple edit-view base class

    Subclasses should provide a `schema` attribute defining the schema
    to be edited.

    The automatically generated widgets are available by name through
    the attributes `*_widget`.
    (E.g. ``view.title_widget for the title widget``)
    """

    errors = ()
    update_status = None
    label = ''

    # Fall-back field names computes from schema
    fieldNames = property(lambda self: getFieldNamesInOrder(self.schema))
    # Fall-back template
    generated_form = ViewPageTemplateFile('edit.pt')

    def __init__(self, context, request):
        super().__init__(context, request)
        self._setUpWidgets()

    def _setUpWidgets(self):
        self.adapted = self.schema(self.context)
        setUpEditWidgets(self, self.schema, source=self.adapted,
                         names=self.fieldNames)

    def setPrefix(self, prefix):
        for widget in self.widgets():
            widget.setPrefix(prefix)

    def widgets(self):
        return [getattr(self, name + '_widget')
                for name in self.fieldNames]

    def changed(self):
        # This method is overridden to execute logic *after* changes
        # have been made.
        pass

    def update(self):
        if self.update_status is not None:
            # We've been called before. Just return the status we previously
            # computed.
            return self.update_status

        status = ''

        content = self.adapted

        if Update in self.request:
            changed = False
            try:
                changed = applyWidgetsChanges(
                    self, self.schema,
                    target=content, names=self.fieldNames)
                # We should not generate events when an adapter is used.
                # That's the adapter's job.
                if changed and self.context is self.adapted:
                    description = Attributes(self.schema, *self.fieldNames)
                    notify(ObjectModifiedEvent(content, description))
            except WidgetsError as errors:
                self.errors = errors
                status = _("An error occurred.")
                transaction.doom()
            else:
                setUpEditWidgets(self, self.schema, source=self.adapted,
                                 ignoreStickyValues=True,
                                 names=self.fieldNames)
                if changed:
                    self.changed()
                    formatter = self.request.locale.dates.getFormatter(
                        'dateTime', 'medium')
                    if PY310_OR_OLDER:
                        now = datetime.datetime.now(datetime.timezone.utc)
                    else:
                        now = datetime.datetime.now(datetime.UTC)

                    status = _("Updated on ${date_time}",
                               mapping={'date_time':
                                        formatter.format(now)})

        self.update_status = status
        return status


def EditViewFactory(name, schema, label, permission, layer,
                    template, default_template, bases, for_, fields,
                    fulledit_path=None, fulledit_label=None):

    class_ = SimpleViewClass(template, used_for=schema, bases=bases, name=name)
    class_.schema = schema
    class_.label = label
    class_.fieldNames = fields

    class_.fulledit_path = fulledit_path
    if fulledit_path and (fulledit_label is None):
        fulledit_label = "Full edit"

    class_.fulledit_label = fulledit_label

    class_.generated_form = ViewPageTemplateFile(default_template)

    defineChecker(class_,
                  NamesChecker(("__call__", "__getitem__",
                                "browserDefault", "publishTraverse"),
                               permission))
    if layer is None:
        layer = IDefaultBrowserLayer

    s = zope.component.getGlobalSiteManager()
    s.registerAdapter(class_, (for_, layer), Interface, name)

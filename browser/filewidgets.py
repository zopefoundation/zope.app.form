##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors.
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
"""Browser widgets with file-based input

$Id:$
"""
__docformat__ = 'restructuredtext'


from zope.interface import implements

from zope.app.form.interfaces import IInputWidget, ConversionError
from zope.app.form.browser.widget import SimpleInputWidget, renderElement
from zope.app.form.browser.widget import DisplayWidget
from zope.app.form.browser.textwidgets import escape



class FileWidget(SimpleInputWidget):
    """File Widget"""

    type = 'file'

    default = ''
    displayWidth = 20
    displayMaxWidth = ""
    extra = ''
    style = ''
    convert_missing_value = True

    def __call__(self):
        displayMaxWidth = self.displayMaxWidth or 0
        if displayMaxWidth > 0:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 size=self.displayWidth,
                                 maxlength=displayMaxWidth,
                                 extra=self.extra)
        else:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 size=self.displayWidth,
                                 extra=self.extra)

    def _toFieldValue(self, input):
        if input == '':
            return self.context.missing_value
        try:
            seek = input.seek
            read = input.read
        except AttributeError, e:
            raise ConversionError('Form input is not a file object', e)
        else:
            seek(0)
            data = read()
            if data or getattr(input, 'filename', ''):
                return data
            else:
                return self.context.missing_value


class MimeWidget(SimpleInputWidget):
    u"""Mime file upload widget"""

    type = 'file'

    default = ''
    displayWidth = 20
    displayMaxWidth = ""
    extra = ''
    style = ''
    convert_missing_value = True

    def __call__(self):
        # XXX set the width to 40 to be sure to recognize this widget
        displayMaxWidth = self.displayMaxWidth or 0
        if displayMaxWidth > 0:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 size=40,
                                 maxlength=40,
                                 extra=self.extra)
        else:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 size=40,
                                 extra=self.extra)

    def _toFieldValue(self, input):
        if input == '':
            return self.context.missing_value
        try:
            seek = input.seek
            read = input.read
        except AttributeError, e:
            raise ConversionError('Form input is not a file object', e)
        else:
            # if the FileUpload instance has no filename set, there is
            # no upload.
            if getattr(input, 'filename', ''):
                return input
            else:
                return self.context.missing_value

    def applyChanges(self, content):
        field = self.context
        value = self.getInputValue()
        # need to test for value, as an empty field is not an error, but
        # the current file should not be replaced.
        if value and (field.query(content, self) != value):
            field.set(content, value)
            return True
        else:
            return False


class MimeDisplayWidget(DisplayWidget):
    """Mime data display widget."""
    # There need to be probably some widget options to determine how
    # the file is displayed, e.g. as a download link.

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default

        show = u"Filename %s, size in bytes: %s" (content.filename,
                                                  content.getSize())
        return renderElement("span", contents=escape(show))

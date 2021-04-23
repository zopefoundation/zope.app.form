##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""API Documentation macros"""
__docformat__ = 'restructuredtext'

from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface.common.mapping import IItemMapping
from zope.publisher.browser import BrowserView


@implementer(IItemMapping)
class FormMacros(BrowserView):

    macro_pages = (
        'view_macros',
        'widget_macros',
        'addform_macros',
    )
    aliases = {
        'view': 'page',
        'dialog': 'page',
        'addingdialog': 'page',
    }

    def __getitem__(self, key):
        key = self.aliases.get(key, key)
        context = self.context
        request = self.request
        for name in self.macro_pages:
            page = getMultiAdapter((context, request), name=name)
            try:
                v = page[key]
            except KeyError:
                pass
            else:
                return v
        raise KeyError(key)

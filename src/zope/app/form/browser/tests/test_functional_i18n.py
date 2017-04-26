##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
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
"""Test form i18n

$Id$
"""

import re
import unittest
import doctest
from persistent import Persistent
from zope.testing import renormalizing
from zope.interface import Interface, implementer
from zope.schema import TextLine, Text, Int, List
from zope.i18nmessageid import MessageFactory

from zope.app.wsgi.testlayer import http
from zope.app.wsgi.testlayer import FakeResponse
from zope.app.form.testing import AppFormLayer


_ = MessageFactory('formtest')

__docformat__ = "reStructuredText"


class IFieldContent(Interface):

    title = TextLine(
        title=_(u"Title"),
        description=_(u"A short description of the event."),
        default=u"",
        required=True
        )

    description = Text(
        title=_(u"Description"),
        description=_(u"A long description of the event."),
        default=u"",
        required=False
        )

    somenumber = Int(
        title=_(u"Some number"),
        default=0,
        required=False
        )

    somelist = List(
        title=_(u"Some List"),
        value_type=TextLine(title=_(u"Some item")),
        default=[],
        required=False
        )

@implementer(IFieldContent)
class FieldContent(Persistent):
    pass


checker = renormalizing.RENormalizing([
    (re.compile(r"HTTP/1\.0 200 .*"), "HTTP/1.1 200 OK"),
    ])

class _FakeResponse(FakeResponse):
    if str is bytes:
        # Up through at least 4.0.0 of zope.app.wsgi, Py2 has a bug,
        # assuming headers are in unicode already, or are decodable
        # implicitly to ascii
        def getHeaders(self):
            headers = super(_FakeResponse, self).getHeaders()
            result = []
            for key, value in headers:
                assert isinstance(key, str)
                assert isinstance(value, str)
                result.append((key.decode('latin-1'),
                               value.decode('latin-1')))
            return result

        # we also need to ensure we get something that can be printed
        # in ascii and produce the same output as Py3.
        def __str__(self):
            return self.getOutput().decode('latin-1').encode("utf-8")



def test_suite():
    def setUp(test):
        wsgi_app = AppFormLayer.make_wsgi_app()
        def _http(query_str, *args, **kwargs):
            # Strip leading \n
            query_str = query_str.lstrip()
            if not isinstance(query_str, bytes):
                query_str = query_str.encode("ascii")
            response = http(wsgi_app, query_str, *args, **kwargs)
            response.__class__ = _FakeResponse
            return response

        test.globs['http'] = _http

    i18n = doctest.DocFileSuite('../i18n.rst',
                                setUp=setUp,
                                checker=checker,
                                optionflags=doctest.ELLIPSIS
                                | doctest.REPORT_NDIFF
                                | doctest.NORMALIZE_WHITESPACE)
    i18n.layer = AppFormLayer
    return unittest.TestSuite([
        i18n,
    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

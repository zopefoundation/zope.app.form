##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""
$Id: metadirectives.py,v 1.2 2004/03/20 19:52:45 srichter Exp $
"""

from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Tokens, Path, \
     Bool, PythonIdentifier, MessageID
from zope.schema import Text, TextLine, Id
from zope.app.publisher.interfaces.browser import IUsage
from zope.app.security.fields import Permission

class ICommonInformation(IUsage):
    """
    Common information for all successive directives
    """

    name = TextLine(
        title=u"Name",
        description=u"The name of the generated view.",
        required=True
        )

    schema = GlobalObject(
        title=u"Schema",
        description=u"The schema from which the form is generated.",
        required=True
        )

    for_ = GlobalObject(
        title=u"Interface",
        description=u"""
        The interface this page (view) applies to.

        The view will be for all objects that implement this
        interface. The schema is used if the for attribute is not
        specified.

        If the for attribute is specified, then the objects views must
        implement or be adaptable to the schema.""",
        required=False
        )

    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=True
        )

    layer = TextLine(
        title=u"Layer",
        description=u"The later the view is in. Default: 'default'",
        required=False
        )

    template = Path(
        title=u"Template",
        description=u"An alternate template to use for the form.",
        required=False
        )

    class_ = GlobalObject(
        title=u"Class",
        description=u"""
        A class to provide custom widget definitions or methods to be
        used by a custom template.

        This class is used as a mix-in class. As a result, it needn't
        subclass any special classes, such as BrowserView.""",
        required=False
        )


class ICommonFormInformation(ICommonInformation):
    """
    Common information for browser forms
    """

    label = MessageID(
        title=u"Label",
        description=u"A label to be used as the heading for the form.",
        required=False
        )

    menu = TextLine(
        title=u"The browser menu to include the form in.",
        description=u"""
        Many views are included in menus. It's convenient to name the
        menu in the page directive, rather than having to give a
        separate menuItem directive.""",
        required=False
        )

    title = MessageID(
        title=u"Menu title",
        description=u"The browser menu label for the form.",
        required=False
        )

    fields = Tokens(
        title=u"Fields",
        description=u"""
        The fields and the order in which to display them.  If this is
        not specified, all schema fields will be displayed in the
        order specified in the schema itself.""",
        required=False,
        value_type=PythonIdentifier()
        )

class ICommonWizardInformation(ICommonInformation):
    """
    Common information for browser wizards
    """

    menu = TextLine(
        title=u"The browser menu to include the form in.",
        description=u"""
        Many views are included in menus. It's convenient to name the
        menu in the page directive, rather than having to give a
        separate menuItem directive.""",
        required=False
        )

    title = MessageID(
        title=u"Menu title",
        description=u"The browser menu label for the form.",
        required=False
        )

    description = MessageID(
        title=u"A longer description of the add form.",
        description=u"""
        A UI may display this with the item or display it when the
        user requests more assistance.""",
        required=False
        )

    use_session = Bool(
        title=u"Use session",
        description=u"""
        If 'no', hidden input controls are used to maintain state
        between panes in the wizard. Only simple data types can
        be propagated with this method.

        Defaults to 'yes'.""",
        required=False
        )

class ICommonAddInformation(Interface):
    """
    Common information for add forms/wizards
    """

    content_factory = GlobalObject(
        title=u"Content factory",
        description=u"""
        An object to call to create new content objects.

        This attribute isn't used if a class is specified that
        implements createAndAdd.""",
        required=False
        )

    arguments = Tokens(
        title=u"Arguments",
        description=u"""
        A list of field names to supply as positional arguments to the
        factory.""",
        required=False,
        value_type=PythonIdentifier()
        )

    keyword_arguments = Tokens(
        title=u"Keyword arguments",
        description=u"""
        A list of field names to supply as keyword arguments to the
        factory.""",
        required=False,
        value_type=PythonIdentifier()
        )

    set_before_add = Tokens(
        title=u"Set before add",
        description=u"""
        A list of fields to be assigned to the newly created object
        before it is added.""",
        required=False,
        value_type=PythonIdentifier(),
        )

    set_after_add = Tokens(
        title=u"Set after add",
        description=u"""
        A list of fields to be assigned to the newly created object
        after it is added.""",
        required=False,
        value_type=PythonIdentifier()
        )

class IAddWizardDirective(ICommonWizardInformation, ICommonAddInformation):
    """
    Define an automatically generated add wizard (multi-page form)

    The addwizard directive creates and registers a view for adding an
    object based on a schema.

    Adding an object is a bit trickier than editing an object, because
    the object the schema applies to isn't available when forms are
    being rendered.  The addwizard directive provides an customization
    interface to overcome this difficulty.

    See zope.app.browser.form.interfaces.IAddFormCustomization.
    """

class IEditWizardDirective(ICommonWizardInformation):
    """
    Define an automatically generated edit wizard (multi-page form).

    The editwizard directive creates and register's a view for editing
    an object based on a schema.
    """

    title = MessageID(
        title=u"The browser menu label for the edit form",
        description=u"This attribute defaults to 'Edit'.",
        required=False
        )

class IPaneSubdirective(Interface):
    """
    Define a Pane (page) of the wizard
    """

    label = MessageID(
        title=u"Label",
        description=u"The label used as the heading on this pane",
        required=False,
        )

    fields = Tokens(
        title=u"Fields",
        description=u"The fields to display on this pane of the wizard",
        required=True,
        value_type=PythonIdentifier()
        )

class IEditFormDirective(ICommonFormInformation):
    """
    Define an automatically generated edit form

    The editform directive creates and register's a view for editing
    an object based on a schema.
    """

class ISubeditFormDirective(ICommonInformation):
    """
    Define a subedit form
    """

    label = TextLine(
        title=u"Label",
        description=u"A label to be used as the heading for the form.",
        required=False
        )

    fulledit_path = TextLine(
        title=u"Path (relative URL) to the full edit form",
        required=False
        )

    fulledit_label = MessageID(
        title=u"Label of the full edit form",
        required=False
        )

class IAddFormDirective(ICommonFormInformation, ICommonAddInformation):
    """
    Define an automatically generated add form

    The addform directive creates and registers a view for adding an
    object based on a schema.

    Adding an object is a bit trickier than editing an object, because
    the object the schema applies to isn't available when forms are
    being rendered.  The addform directive provides an customization
    interface to overcome this difficulty.

    See zope.app.browser.form.interfaces.IAddFormCustomization.
    """

    description = Text(
        title=u"A longer description of the add form.",
        description=u"""
        A UI may display this with the item or display it when the
        user requests more assistance.""",
        required=False
        )

class ISchemaDisplayDirective(ICommonFormInformation):
    """
    Define an automatically generated display form.

    The schemadisplay directive creates and register's a view for
    displaying an object based on a schema.
    """

    title = MessageID(
        title=u"The browser menu label for the edit form",
        description=u"This attribute defaults to 'Edit'.",
        required=False
        )

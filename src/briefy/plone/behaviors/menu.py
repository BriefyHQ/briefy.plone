# -*- coding: utf-8 -*-
"""Site menu behaviour."""
from briefy.plone import _
from briefy.plone.config import DEFAULT_MENU_FOOTER
from briefy.plone.config import DEFAULT_MENU_HEADER
from briefy.plone.config import DEFAULT_MENU_LOGIN
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import provider

import json


@provider(IFormFieldProvider)
class IMenu(model.Schema):
    """Behavior interface to control menu options for the site."""

    model.fieldset(
        'menu',
        label=_(u'Menu'),
        fields=[
            'menu_header',
            'menu_login',
            'menu_footer'
        ]
    )

    menu_header = schema.Text(
        title=_(u'Header menu'),
        description=_(
            u'JSON construct with a list of objects.'
            u'i.e: [{path: "/about", title: "About", internal: true},].'
        ),
        required=False
    )

    menu_header = schema.Text(
        title=_(u'Header menu'),
        description=_(
            u'JSON construct with a list of objects.'
            u'i.e: [{path: "/about", title: "About", internal: true},].'
        ),
        required=True
    )

    menu_login = schema.Text(
        title=_(u'Login menu'),
        description=_(
            u'JSON construct with a list of objects.'
            u'i.e: [{path: "https://business.briefy.co", title: "Business", internal: false},].'
        ),
        required=True
    )

    menu_footer = schema.Text(
        title=_(u'Footer menu'),
        description=_(
            u'JSON construct with a list of objects.'
            u'i.e: [{title: "Discover", items: {path: "/business-solutions", ...}},]'
        ),
        required=True
    )


@implementer(IMenu)
class Menu(object):
    """Store menu info on an annotation."""

    def __init__(self, context):
        """Initialize the behavior factory."""
        self.context = context

    @property
    def __annotations(self):
        annotations = IAnnotations(self.context)
        return annotations

    def _format_value(self, value):
        """Format a JSON value."""
        try:
            value_obj = json.loads(value)
            value = json.dumps(value_obj, ident=2, sort_keys=True)
        except ValueError:
            raise ValueError('Invalid value for menu header')
        return value

    def _getter(self, key, default):
        """Getter for annotation values."""
        value = self.__annotations.get(key, None)
        return value if value else default

    def _setter(self, key, value):
        """Setter for annotation values."""
        attr = getattr(self, key)
        if value != attr:
            # Save only if the value is not the same and it is a valid json
            value = self._format_value(value)
            self.__annotations[key] = value
        value = self.__annotations.get(key, None)

    @property
    def menu_header(self):
        """Getter for menu_header."""
        return self._getter('menu_header', DEFAULT_MENU_HEADER)

    @menu_header.setter
    def menu_header(self, value):
        """Setter for menu_header."""
        self._setter('menu_header', value)

    @property
    def menu_login(self):
        """Getter for menu_login."""
        return self._getter('menu_login', DEFAULT_MENU_LOGIN)

    @menu_login.setter
    def menu_login(self, value):
        """Setter for menu_login."""
        self._setter('menu_login', value)

    @property
    def menu_footer(self):
        """Getter for menu_footer."""
        return self._getter('menu_footer', DEFAULT_MENU_FOOTER)

    @menu_footer.setter
    def menu_footer(self, value):
        """Setter for menu_footer."""
        self._setter('menu_footer', value)

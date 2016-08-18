# -*- coding: utf-8 -*-
"""Composite page content type."""
from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class ICompositePage(Interface):
    """Interface for a Composite Page."""


@implementer(ICompositePage)
class CompositePage(Container):
    """A Composite Page."""

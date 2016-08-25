# -*- coding: utf-8 -*-
"""Composite page content type."""
from briefy.plone.content.interfaces import IBriefyContent
from plone.dexterity.content import Container
from zope.interface import implementer


class ICompositePage(IBriefyContent):
    """Interface for a Composite Page."""


@implementer(ICompositePage)
class CompositePage(Container):
    """A Composite Page."""

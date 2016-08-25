# -*- coding: utf-8 -*-
"""Team Gallery content type."""
from briefy.plone.content.interfaces import IBriefyContent
from plone.dexterity.content import Container
from zope.interface import implementer


class IGallery(IBriefyContent):
    """Interface for a Showcase Gallery."""


@implementer(IGallery)
class Gallery(Container):
    """A Showcase Gallery."""

# -*- coding: utf-8 -*-
"""Base block for a Composite page."""
from briefy.plone.content.interfaces import IBriefyContent
from plone.dexterity.content import Container
from zope.interface import implementer


class IBlock(IBriefyContent):
    """Interface for a block object to be added to a Composite Page."""


@implementer(IBlock)
class Block(Container):
    """A Block object to be added to a Composite Page."""

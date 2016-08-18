# -*- coding: utf-8 -*-
"""Base block for a Composite page."""
from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IBlock(Interface):
    """Interface for a block object to be added to a Composite Page."""


@implementer(IBlock)
class Block(Container):
    """A Block object to be added to a Composite Page."""

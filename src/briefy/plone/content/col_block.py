# -*- coding: utf-8 -*-
"""Row block base class."""
from briefy.plone.content.block import Block
from briefy.plone.content.block import IBlock
from zope.interface import implementer


class IColBlock(IBlock):
    """Interface for a Block to be added inside another block."""


@implementer(IColBlock)
class ColBlock(Block):
    """A Block to be added inside another block."""

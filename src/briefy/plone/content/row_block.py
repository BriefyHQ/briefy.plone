# -*- coding: utf-8 -*-
"""Row block base class."""
from briefy.plone.content.block import Block
from briefy.plone.content.block import IBlock
from zope.interface import implementer


class IRowBlock(IBlock):
    """Interface for a Block to be added inside another block."""


@implementer(IRowBlock)
class RowBlock(Block):
    """A Block to be added inside another block."""

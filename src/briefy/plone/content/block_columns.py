# -*- coding: utf-8 -*-
"""Block checker content type."""
from briefy.plone.content.block import Block
from briefy.plone.content.block import IBlock
from zope.interface import implementer


class IBlockColumns(IBlock):
    """Interface for a Block with many columns."""


@implementer(IBlockColumns)
class BlockColumns(Block):
    """A Block with many columns."""

# -*- coding: utf-8 -*-
"""Block checker content type."""
from briefy.plone.content.block import Block
from briefy.plone.content.block import IBlock
from zope.interface import implementer


class IBlockChecker(IBlock):
    """Interface for a Block with checkered pattern."""


@implementer(IBlockChecker)
class BlockChecker(Block):
    """A Block with checkered pattern."""

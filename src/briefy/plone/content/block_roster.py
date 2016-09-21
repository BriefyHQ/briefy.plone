# -*- coding: utf-8 -*-
"""Team Roster block to be included in a composite page."""
from briefy.plone.content.block import Block
from briefy.plone.content.block import IBlock
from zope.interface import implementer


class IBlockRoster(IBlock):
    """Interface for a Team Roster to be included in a composite page."""


@implementer(IBlockRoster)
class BlockRoster(Block):
    """A Team Roster to be included in a composite page."""

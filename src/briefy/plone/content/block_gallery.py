# -*- coding: utf-8 -*-
"""Gallery block to be included in a composite page."""
from briefy.plone.content.block import Block
from briefy.plone.content.block import IBlock
from zope.interface import implementer


class IBlockGallery(IBlock):
    """Interface for a Gallery to be included in a composite page."""


@implementer(IBlockGallery)
class BlockGallery(Block):
    """A Gallery to be included in a composite page."""

# -*- coding: utf-8 -*-
"""Team Roster content type."""
from briefy.plone.content.interfaces import IBriefyContent
from plone.dexterity.content import Container
from zope.interface import implementer


class IRoster(IBriefyContent):
    """Interface for a Team Roster."""


@implementer(IRoster)
class Roster(Container):
    """A Team Roster."""

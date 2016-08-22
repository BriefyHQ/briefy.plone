# -*- coding: utf-8 -*-
"""Team Roster content type."""
from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IRoster(Interface):
    """Interface for a Team Roster."""


@implementer(IRoster)
class Roster(Container):
    """A Team Roster."""

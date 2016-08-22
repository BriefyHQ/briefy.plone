# -*- coding: utf-8 -*-
"""Team Member content type."""
from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class ITeamMember(Interface):
    """Interface for a Team Member."""


@implementer(ITeamMember)
class TeamMember(Container):
    """A Team Member."""

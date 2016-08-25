# -*- coding: utf-8 -*-
"""Team Member content type."""
from briefy.plone.content.interfaces import IBriefyContent
from plone.dexterity.content import Container
from zope.interface import implementer


class ITeamMember(IBriefyContent):
    """Interface for a Team Member."""


@implementer(ITeamMember)
class TeamMember(Container):
    """A Team Member."""

# -*- coding: utf-8 -*-
"""Form content type."""
from briefy.plone.content.interfaces import IBriefyContent
from plone.dexterity.content import Container
from zope.interface import implementer


class IForm(IBriefyContent):
    """Interface for a Composite Page."""


@implementer(IForm)
class Form(Container):
    """A Form."""

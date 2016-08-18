# -*- coding: utf-8 -*-
"""Canonical url behavior."""
from briefy.plone import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ICanonicalURL(model.Schema):
    """Behavior interface to add a Canonical URL to contents."""

    model.fieldset(
        'seo',
        label=_(u'SEO'),
        fields=['canonical_url']
    )

    canonical_url = schema.URI(
        title=_(u'Canonical URL'),
        description=_(u'Inform the canonical url for this content.'),
        required=False
    )

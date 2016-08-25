# -*- coding: utf-8 -*-
"""Canonical url behavior."""
from briefy.plone import _
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
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


@implementer(ICanonicalURL)
class CanonicalURL(object):
    """Store canonical_url in an annotation."""

    def __init__(self, context):
        """Initialize the behavior factory."""
        self.context = context

    @property
    def __annotations(self):
        annotations = IAnnotations(self.context)
        return annotations

    @property
    def canonical_url(self):
        """Getter for canonical_url."""
        value = self.__annotations.get('canonical_url', None)
        if not value:
            context_view = api.content.get_view(
                name='plone_context_state',
                context=self.context,
                request=self.context.REQUEST
            )
            value = context_view.canonical_object_url()
        return value

    @canonical_url.setter
    def canonical_url(self, value):
        """Setter for canonical_url."""
        if value != self.canonical_url:
            # Save only if the value is not the same
            self.__annotations['canonical_url'] = value

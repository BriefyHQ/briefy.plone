# -*- coding: utf-8 -*-
"""Robots metatag behavior."""
from briefy.plone import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


metarobots_vocabulary = SimpleVocabulary([
    SimpleTerm('noindex', 'noindex', u'noindex'),
    SimpleTerm('nofollow', 'nofollow', u'nofollow'),
    SimpleTerm('none', 'none', u'none'),
    SimpleTerm('noarchive', 'noarchive', u'noarchive'),
    SimpleTerm('nosnippet', 'nosnippet', u'nosnippet'),
    SimpleTerm('noodp', 'noodp', u'noodp'),
    SimpleTerm('notranslate', 'notranslate', u'notranslate'),
    SimpleTerm('noimageindex', 'noimageindex', u'noimageindex'),
    SimpleTerm('unavailable_after', 'unavailable_after', u'unavailable after expiration'),
])


@provider(IFormFieldProvider)
class IMetaRobots(model.Schema):
    """Behavior interface to configure the robots metatag."""

    model.fieldset(
        'seo',
        label=_(u'SEO'),
        fields=['robots']
    )

    robots = schema.List(
        title=_(u'Metatag Robots'),
        description=_(u'Select the options to be added to the robots metatag.'),
        value_type=schema.Choice(
            title=_(u'Available options'),
            vocabulary=metarobots_vocabulary
        ),
    )

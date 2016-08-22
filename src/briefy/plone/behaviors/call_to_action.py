# -*- coding: utf-8 -*-
"""Call to action behaviour."""
from briefy.plone import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


cta_types_vocabulary = SimpleVocabulary([
    SimpleTerm('button', 'button', u'button'),
    SimpleTerm('link', 'link', u'link')
])


@provider(IFormFieldProvider)
class ICallToAction(model.Schema):
    """Behavior interface to add a call to action fieldset to a block."""

    model.fieldset(
        'call_to_action',
        label=_(u'Call to Action'),
        fields=[
            'call_to_action_text',
            'call_to_action_url',
            'call_to_action_type'
        ]
    )

    call_to_action_text = schema.TextLine(
        title=_(u'Text'),
        description=_(u'Text to be displayed on the call to action.'),
        required=False
    )

    call_to_action_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u'.'),
        required=False
    )

    call_to_action_type = schema.Choice(
        title=_(u'Type'),
        description=_(u'Call to action type.'),
        vocabulary=cta_types_vocabulary,
        required=False
    )

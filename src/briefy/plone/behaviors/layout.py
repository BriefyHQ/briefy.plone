# -*- coding: utf-8 -*-
"""Layout behaviour."""
from briefy.plone import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ILayout(model.Schema):
    """Behavior interface to add a Layout fieldset to a block."""

    model.fieldset(
        'layout',
        label=_(u'Layout'),
        fields=[
            'css_class',
            'style_color',
            'style_padding',
            'style_margin',
            'style_background_color',
            'style_background_width',
            'style_background_height',
        ]
    )

    css_class = schema.TextLine(
        title=_(u'CSS Class'),
        description=_(u'Set a css class to this element.'),
        required=False
    )

    style_color = schema.TextLine(
        title=_(u'Text color'),
        description=_(u'If set, override default text color.'),
        required=False
    )

    style_padding = schema.TextLine(
        title=_(u'Padding'),
        description=_(u'If set, overrides default setting for padding.'),
        required=False
    )

    style_margin = schema.TextLine(
        title=_(u'Margin'),
        description=_(u'If set, override default margin settings for this element.'),
        required=False
    )

    style_background_color = schema.TextLine(
        title=_(u'Background color'),
        description=_(u'If set, override the background color for this element.'),
        required=False
    )

    style_background_width = schema.TextLine(
        title=_(u'Background width'),
        description=_(u'If set, override the background width for this element.'),
        required=False
    )

    style_background_height = schema.TextLine(
        title=_(u'Background height'),
        description=_(u'If set, override the background height for this element.'),
        required=False
    )

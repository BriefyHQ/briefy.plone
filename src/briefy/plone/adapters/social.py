# -*- coding: utf-8 -*-
"""Social Metadata adapter."""
from briefy.plone.imaging import get_scales
from plone.app.contenttypes.behaviors.leadimage import ILeadImage


class SocialMetadata(object):
    """Return social metadata info for an object."""

    def __init__(self, context):
        """Initialize the behavior factory."""
        self.context = context

    def _get_locale(self):
        """Return a proper locale based on content language."""
        context = self.context
        locales = {
            'en': 'en_GB',
            'de': 'de_DE'
        }
        language = context.language if context.language else 'en'
        return locales.get(language)

    def _get_image_url(self, context):
        if context.image:
            width, height = context.image.getImageSize()
            scales = get_scales(context, 'image', width, height)
            return scales.get('social-full', scales.get('large'))

    def _get_image(self):
        context = self.context
        url = ''
        if ILeadImage.providedBy(context):
            url = self._get_image_url(context)
        else:
            for child in context.objectValues():
                url = self._get_image_url(child) if ILeadImage.providedBy(child) else ''
                if url:
                    break
        return url

    def __call__(self):
        """Social metada information."""
        context = self.context
        properties = []
        names = []
        created_at = context.Date()
        updated_at = context.ModificationDate()
        base = {
            'title': context.title,
            'description': context.description,
            'image': self._get_image(),
            'author': 'Briefy Team',  # HACK
            'created_at': created_at,
            'updated_at': updated_at if updated_at else created_at,
            'locale': self._get_locale(),
        }
        # Open Graph
        properties.append(('og:title', base['title']))
        properties.append(('og:description', base['description']))
        properties.append(('og:image', base['image']))
        properties.append(('og:locale', base['locale']))
        if context.portal_type == 'News Item':
            # http://ogp.me/#type_article
            properties.append(('og:type', 'article'))
            properties.append(('og:article:author', base['author']))
            properties.append(('og:article:published_time', base['created_at']))
            properties.append(('og:article:modified_time', base['updated_at']))
            for tag in context.subject:
                properties.append(('og:article:tag', tag))
        else:
            properties.append(('og:type', 'website'))

        # Twitter Cards
        names.append(('twitter:card', 'summary_large_image'))
        names.append(('twitter:title', base['title']))
        names.append(('twitter:description', base['description']))
        names.append(('twitter:image', base['image']))
        metadata = (
            [{'name': k, 'content': v} for k, v in names] +
            [{'property': k, 'content': v} for k, v in properties]
        )
        return metadata

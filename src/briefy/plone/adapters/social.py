# -*- coding: utf-8 -*-
"""Social Metadata adapter."""
from briefy.plone.imaging import get_scales
from briefy.plone.behaviors.canonical import ICanonicalURL
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
        tmp_url = ''
        children = context.objectValues()
        elements = [context, ]
        if children:
            elements.extend(children)
        for item in elements:
            tmp_url = self._get_image_url(item) if ILeadImage.providedBy(item) else ''
            # We ignore gradient images if possible
            if tmp_url and 'gradient' in tmp_url.lower():
                continue
            url = tmp_url
            if url:
                break
        url = url if url else tmp_url
        return url

    def __call__(self):
        """Social metada information."""
        context = self.context
        properties = []
        names = []
        created_at = context.Date()
        updated_at = context.ModificationDate()
        canonical = ICanonicalURL(context, None)
        url = context.absolute_url()
        if canonical:
            url = canonical.canonical_url
        base = {
            'url': url,
            'title': context.title,
            'description': context.description,
            'image': self._get_image(),
            'author': 'Briefy Team',  # HACK
            'created_at': created_at,
            'updated_at': updated_at if updated_at else created_at,
            'locale': self._get_locale(),
        }
        # Open Graph
        properties.append(('og:url', base['url']))
        properties.append(('og:title', base['title']))
        properties.append(('og:description', base['description']))
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
        if base['image']:
            properties.append(('og:image', base['image']))
            names.append(('twitter:image', base['image']))
        metadata = (
            [{'name': k, 'content': v} for k, v in names] +
            [{'property': k, 'content': v} for k, v in properties]
        )
        return metadata

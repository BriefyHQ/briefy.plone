# -*- coding: utf-8 -*-
"""JSON Serializer for Contents."""
from briefy.plone.interfaces import IBriefyPloneJSONLayer
from briefy.plone.imaging import get_scales
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import INamedImageField
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import ImageFieldSerializer
from zope.component import adapter
from zope.interface import implementer


@implementer(IFieldSerializer)
@adapter(INamedImageField, IDexterityContent, IBriefyPloneJSONLayer)
class ImageFieldSerializer(ImageFieldSerializer):
    """Serialize an Image field."""

    def __call__(self):
        """."""
        image = self.field.get(self.context)
        if not image:
            return None

        url = '/'.join((self.context.absolute_url(), '@@images', self.field.__name__))

        width, height = image.getImageSize()
        scales = get_scales(self.context, self.field, width, height)
        result = {
            'filename': image.filename,
            'content-type': image.contentType,
            'size': image.getSize(),
            'download': url,
            'width': width,
            'height': height,
            'scales': scales
        }
        return json_compatible(result)

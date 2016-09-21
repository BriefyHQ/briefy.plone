# -*- coding: utf-8 -*-
"""Imaging support for briefy.plone."""
from briefy.plone.adapters.storages import IAlternateStorageLocation
from briefy.plone.adapters.storages import S3Adapter
from briefy.plone.config import logger
from briefy.plone.imaging.urls import generate_url
from briefy.plone.utils.fields import get_image_fields
from plone.restapi.imaging import get_actual_scale
from plone.restapi.imaging import get_scale_infos


THUMBOR_IMAGE_SIZES = (
    (u'original', 0, 0),
    (u'jumbotron', 1400, 800),
    (u'portrait', 320, 320),
    (u'gallery-full', 1074, 716),
    (u'gallery-thumb', 80, 80),
    (u'gallery-mobile', 400, 266)
)


def scale_info(name, context, s3_path, field_name, width, height, cache=False):
    """Return scale info."""
    url = u'{0}/@@images/{1}/{2}'.format(context.absolute_url(), field_name, name)

    if s3_path:
        url = generate_url(s3_path, width, height, cache)

    return {
        u'download': url,
        u'width': width,
        u'height': height
    }


def get_scales(context, field, width, height, cache=False):
    """Return a dictionary of available scales for an image field."""
    scales = {}

    field_name = field.__name__
    alternate_storage = IAlternateStorageLocation(context)

    s3_path = alternate_storage.get_field(field_name) if alternate_storage else ''

    for name, scale_width, scale_height in get_scale_infos():
        bbox = scale_width, scale_height
        width, height = get_actual_scale((width, height), bbox)
        scales[name] = scale_info(name, context, s3_path, field_name, width, height, cache)

    if s3_path:
        for name, width, height in THUMBOR_IMAGE_SIZES:
            scales[name] = scale_info(name, context, s3_path, field_name, width, height, cache)

    return scales


def store_image_field_on_s3(obj):
    """Given an object, storage all image fields on S3."""
    fields = get_image_fields(obj)
    if fields:
        logger.debug('Subscriber for image storage: {0}'.format(obj.absolute_url()))
        s3_store = S3Adapter(obj)
        s3_store.store_fields(fields)
        # TODO: Async calls to cache all images with Thumbor

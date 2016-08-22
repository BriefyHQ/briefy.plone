# -*- coding: utf-8 -*-
"""Imaging support for briefy.plone."""
from plone.restapi.imaging import get_actual_scale
from plone.restapi.imaging import get_scale_infos


def get_scales(context, field, width, height):
    """Return a dictionary of available scales for an image field."""
    scales = {}
    absolute_url = context.absolute_url()

    for name, scale_width, scale_height in get_scale_infos():
        bbox = scale_width, scale_height
        actual_width, actual_height = get_actual_scale((width, height), bbox)
        url = u'{0}/@@images/{1}/{2}'.format(
            absolute_url, field.__name__, name
        )

        scales[name] = {
            u'download': url,
            u'width': actual_width,
            u'height': actual_height
        }

    return scales

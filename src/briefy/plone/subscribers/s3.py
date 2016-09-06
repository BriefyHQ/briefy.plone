# -*- coding: utf-8 -*-
"""Subscriber that uploads image data from content to Amazon S3."""
from briefy.plone.config import logger
from briefy.plone.imaging import store_image_field_on_s3
from zope.container.interfaces import IContainerModifiedEvent


def dx_handler(obj, event):
    """Subscriber for image storage.

    :param obj: Plone content object
    :type obj: object
    :param event: Event
    :type event: event
    """
    if IContainerModifiedEvent.providedBy(event):
        # This object is not wrapped in acquisition so we fail silently
        logger.debug('Object {0} not wrapped in acquisition'.format(str(obj)))
        return

    store_image_field_on_s3(obj)

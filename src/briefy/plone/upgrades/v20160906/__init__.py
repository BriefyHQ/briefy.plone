# -*- coding: utf-8 -*-
"""Upgrade briefy.plone to v20160831."""
from briefy.plone.config import PROJECTNAME
from briefy.plone.imaging import store_image_field_on_s3
from plone import api

import logging

logger = logging.getLogger(PROJECTNAME)


def images_s3(context):
    """Upload existing images to S3."""
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog()
    logger.info('There are {0} objects on the database'.format(len(results)))
    for brain in results:
        obj = brain.getObject()
        logger.info('Processing {0}'.format(obj.absolute_url()))
        store_image_field_on_s3(obj)

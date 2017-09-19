# -*- coding: utf-8 -*-
"""Upgrade briefy.plone to v20161018."""
from briefy.plone.config import PROFILE_ID
from briefy.plone.config import PROJECTNAME
from plone import api
from plone.app.textfield.value import RichTextValue

import logging


logger = logging.getLogger(PROJECTNAME)


def data_migration(context):
    """Migrate data from description field to text field."""
    ct = api.portal.get_tool('portal_catalog')
    results = ct.searchResults({'portal_type': 'row_block_checker'})
    for brain in results:
        obj = brain.getObject()
        description = obj.description
        obj.text = RichTextValue(description, 'text/plain', 'text/html')
        obj.reindexObject()
    logger.info('Run data migration')


def types_registration(context):
    """Register new types."""
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    logger.info('Run types registration')

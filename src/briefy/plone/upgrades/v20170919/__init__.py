# -*- coding: utf-8 -*-
"""Upgrade briefy.plone to v20170919."""
from briefy.plone.config import PROJECTNAME
from plone import api

import logging


logger = logging.getLogger(PROJECTNAME)


def upgrade_plone_restapi(context):
    """Upgrade plone rest api."""
    profile = 'plone.restapi:default'
    setup = api.portal.get_tool('portal_setup')
    setup.upgradeProfile(profile)
    logger.info('Upgrade plone_restapi')


def remove_blocks_from_search(context):
    """Remove blocks from search."""
    record = 'plone.types_not_searched'
    to_remove = (
        'block_breezy',
        'block_checker',
        'block_columns',
        'block_gallery',
        'block_header',
        'block_image',
        'block_jumbotron',
        'block_jumbotron_video',
        'block_page',
        'block_roster',
        'col_block_item',
        'Discussion Item',
        'Image',
        'Plone Site',
        'row_block_checker',
        'team_member',
        'TempFolder'
    )
    api.portal.set_registry_record(record, to_remove)
    logger.info('Blocks removed')

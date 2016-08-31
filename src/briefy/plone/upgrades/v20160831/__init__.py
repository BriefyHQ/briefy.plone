# -*- coding: utf-8 -*-
"""Upgrade briefy.plone to v20160831."""
from briefy.plone.config import PROFILE_ID
from briefy.plone.config import PROJECTNAME
from plone import api

import logging

logger = logging.getLogger(PROJECTNAME)


def types_registration(context):
    """Register new types."""
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    logger.info('Run types registration')


def add_gallery_to_navigation(context):
    """Add gallery to navigation."""
    displayed_types = list(
        api.portal.get_registry_record(
            'plone.displayed_types'
        )
    )
    displayed_types.append('gallery')
    api.portal.set_registry_record(
        'plone.displayed_types', tuple(displayed_types)
    )
    logger.info('Added gallery to navigation')


def add_theme(context):
    """Add css_resources."""
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.theming')
    logger.info('Added theme')

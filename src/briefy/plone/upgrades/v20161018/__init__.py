# -*- coding: utf-8 -*-
"""Upgrade briefy.plone to v20161018."""
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

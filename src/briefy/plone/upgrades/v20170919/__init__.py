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

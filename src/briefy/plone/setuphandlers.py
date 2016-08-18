# -*- coding: utf-8 -*-
"""Setup handlers for Briefy CMS."""
from briefy.plone.config import logger
from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite


def set_folder_title_description(obj):
    """Fix the title and description of this Language Root Folder.

    :param obj: Language Root Folder
    :type obj: plone.dexterity.content.Container
    """
    # Change title of the language folder
    current_title = obj.title
    title = u'Briefy {title} site'.format(title=current_title)
    obj.title = title
    description = u'Content for the Briefy {title} site needs to be put here'.format(
        title=current_title
    )
    obj.description = description


def run_after(context):
    """Executed after briefy.plone installation."""
    site = api.portal.get()
    setupTool = SetupMultilingualSite()
    output = setupTool.setupSite(site)
    results = api.content.find(site, portal_type='LRF')
    for brain in results:
        set_folder_title_description(brain.getObject())
    logger.debug(output)

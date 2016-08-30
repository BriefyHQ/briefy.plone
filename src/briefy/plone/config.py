# -*- coding: utf-8 -*-
"""Configuration and settings for the package."""
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer

import logging

PROJECTNAME = 'briefy.plone'
PROFILE_ID = 'briefy.plone:default'

logger = logging.getLogger(PROJECTNAME)


BLACKLISTED = [
    '@@search',
    'folder_contents',
    'manage',
    'manage_main',
    'sitemap.xml.gz',
]


ANON_WHITE_LISTED = (
    '++plone',
    '++resource',
    '++theme',
    '@@site-logo',
    '@@sitemap.json',
    'sitemap.json',
    'acl_users',
    'config.js',
    'login',
    'mail_password_form',
    'passwordreset',
    'plonejsi18n',
    'pwreset_form',
)

SEARCH_BLACKLIST = (
    'Discussion Item',
    'Image',
    'Plone Site',
    'TempFolder',
)


@implementer(qi_interfaces.INonInstallable)
class HiddenProducts(object):
    """List of packages to be hidden in control panel and new site screen."""

    def getNonInstallableProducts(self):  # noqa
        """Return a list of packages that will not be listed."""
        return [
            'archetypes.multilingual',
        ]


@implementer(INonInstallable)
class HiddenProfiles(object):
    """List of profiles to be hidden in control panel and new site screen."""

    def getNonInstallableProfiles(self):  # noqa
        """Return a list of profiles that will not be listed."""
        return [
            'archetypes.multilingual:default',
            'archetypes.multilingual:uninstall',
            'plone.app.caching:default',
            'plone.app.contenttypes:default',
            'plone.app.iterate:default',
            'plone.app.iterate:plone.app.iterate',
            'plone.app.iterate:uninstall',
            'plone.app.multilingual:default',
            'plone.app.openid:default',
            'plone.app.widgets:default',
            'plone.restapi:default',
            'plone.restapi:performance',
            'plone.session:default',
            'plone.session:uninstall',
            'plonetheme.barceloneta:default',
            'plonetheme.barceloneta:registerless',
            'Products.ATContentTypes:base',
            'Products.ATContentTypes:content',
            'Products.ATContentTypes:default',
            'Products.CMFPlacefulWorkflow:base',
        ]

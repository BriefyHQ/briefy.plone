# -*- coding: utf-8 -*-
"""Configuration and settings for the package."""
from os import environ as env
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer

import logging


PROJECTNAME = 'briefy.plone'
PROFILE_ID = 'briefy.plone:default'

logger = logging.getLogger(PROJECTNAME)

ENV = env.get('ENV', 'dev')

_BASE_URLS = {
    'dev': 'http://localhost:8080',
    'stg': 'https://www.stg.briefy.co',
    'live': 'https://briefy.co',
}

BASE_URL = _BASE_URLS.get(ENV, _BASE_URLS['dev'])

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
    'mail_password',
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

# Thumbor integration
S3_BUCKET = env.get('S3_BUCKET', 'images.stg.briefy.co')
S3_PATH = env.get('S3_PATH', 'source/cms/')
S3_REGION = env.get('S3_REGION', 'us-east-1')

THUMBOR_PATH = env.get('THUMBOR_PATH', 'cms/')
THUMBOR_KEY = env.get('THUMBOR_PATH', 'dMXlEkjuSz3VoIn9THJOROfMPZa4FqSvDl3jXwN9')
THUMBOR_BASE_URL = env.get('THUMBOR_BASE_URL', 'https://images.stg.briefy.co')
THUMBOR_CACHE_URL = env.get(
    'THUMBOR_CACHE_URL',
    'http://briefy-thumbor.briefy-thumbor.svc.cluster.local'
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


DEFAULT_MENU_HEADER = """[
    {"path": "/about", "title": "About", "internal": true},
    {"path": "/creatives", "title": "Creatives", "internal": true},
    {"path": "/business-solutions", "title": "Business Solutions", "internal": true}
]
"""


DEFAULT_MENU_LOGIN = """[
    {"path": "https://business.briefy.co", "title": "Business", "internal": false},
    {"path": "https://professionals.briefy.co", "title": "Photographers", "internal": false}
]
"""


DEFAULT_MENU_FOOTER = """[
    {
      "title": "Discover",
      "items": [
        {"path": "/business-solutions", "title": "Business solutions", "internal": true},
        {"path": "/business-solutions/quote", "title": "Get a quote", "internal": true},
        {"path": "/business-solutions/gallery", "title": "Sample Work", "internal": true},
        {"path": "/creatives", "title": "Creatives", "internal": true},
        {"path": "https://plone.org", "title": "Plone", "internal": false}
      ]
    },
    {
      "title": "Company",
      "items": [
        {"path": "/about", "title": "About", "internal": true},
        {"path": "/careers", "title": "Careers", "internal": true},
        {"path": "https://medium.com/@briefytalks", "title": "Blog", "internal": false}
      ]
    },
    {
      "title": "Important",
      "items": [
        {"path": "/imprint", "title": "Imprint", "internal": true},
        {"path": "/contact", "title": "Contact", "internal": true}
      ]
    },
    {
      "title": "",
      "items": []
    }
]
"""

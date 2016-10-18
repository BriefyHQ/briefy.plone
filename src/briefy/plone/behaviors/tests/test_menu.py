# -*- coding: utf-8 -*-
"""Test IMenu behavior."""
from briefy.plone.behaviors.menu import IMenu
from briefy.plone.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest2 as unittest


class IMenuTest(unittest.TestCase):
    """Test case for IMenu behavior."""

    layer = INTEGRATION_TESTING
    behavior_name = 'briefy.plone.behaviors.canonical.IMenu'

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        fti = queryUtility(IDexterityFTI, name='Document')
        behaviors = list(fti.behaviors)
        behaviors.append(self.behavior_name)
        fti.behaviors = tuple(behaviors)

    def test_registration(self):
        """Assert registration of the behavior."""
        registration = queryUtility(IBehavior, name=self.behavior_name)
        self.assertIsNotNone(registration)

    def test_adapt_content(self):
        """Assert behavior can adapt a content."""
        api.content.create(
            type='Document',
            id='doc-1',
            container=self.portal
        )
        doc = self.portal['doc-1']
        behavior = IMenu(doc)
        self.assertIsNotNone(behavior)

    def test_menu(self):
        """Test behavior work as expected."""
        import json

        api.content.create(
            type='Document',
            id='doc-1',
            container=self.portal
        )
        doc = self.portal['doc-1']
        behavior = IMenu(doc)

        # Return default content
        self.assertIn(
            '"/creatives"',
            behavior.menu_header
        )
        self.assertIn(
            'business.briefy.co',
            behavior.menu_login
        )
        self.assertIn(
            '/imprint',
            behavior.menu_footer
        )

        footer = [
            {
                'title': 'Menu',
                'items': [
                    {
                        'path': '/item-1',
                        'title': 'Menu item 1',
                        'internal': True,
                    }
                ],
            }
        ]
        data = json.dumps(footer)
        behavior.menu_footer = data

        self.assertIn(
            '/item-1',
            behavior.menu_footer
        )

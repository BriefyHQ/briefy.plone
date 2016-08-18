# -*- coding: utf-8 -*-
"""Test ILayout behavior."""
from briefy.plone.behaviors.layout import ILayout
from briefy.plone.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest2 as unittest


class ILayoutTest(unittest.TestCase):
    """Test case for ILayout behavior."""

    layer = INTEGRATION_TESTING
    behavior_name = 'briefy.plone.behaviors.layout.ILayout'

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
        behavior = ILayout(doc)
        self.assertIsNotNone(behavior)

    def test_fields(self):
        """Test behavior work as expected."""
        api.content.create(
            type='Document',
            id='doc-1',
            container=self.portal
        )
        doc = self.portal['doc-1']
        behavior = ILayout(doc)
        self.assertEqual(behavior.css_class, None)
        behavior.css_class = u'page'
        self.assertEqual(behavior.css_class, u'page')

# -*- coding: utf-8 -*-
"""Test Serializer."""
from briefy.plone.interfaces import IBriefyPloneJSONLayer
from briefy.plone.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJson
from zope.component import getMultiAdapter
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides

import unittest2 as unittest


class TestSerialization(unittest.TestCase):
    """Test case for ISerializeToJson adapters."""

    layer = INTEGRATION_TESTING

    def _create_content(self, portal):
        """Create dummy content for our tests."""
        en = portal['en']
        home = en['home']
        self.composite = home
        api.content.create(
            type='block_checker',
            id='block_1',
            container=home,
            title='Checker',
            description='Checker'
        )
        self.block_checker = home['block_1']
        for idx in range(1, 4):
            api.content.create(
                type='row_block_checker',
                id='row_{0}'.format(idx),
                container=self.block_checker,
                title='Row {0}'.format(idx),
                description='Row {0}'.format(idx)
            )

    def setUp(self):
        """Setup testcase."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self._create_content(self.portal)

    def serialize(self, content):
        """Run the serializer for this content."""
        ifaces = [IBriefyPloneJSONLayer, ] + list(
            directlyProvidedBy(self.request)
        )
        directlyProvides(self.request, *ifaces)
        serializer = getMultiAdapter(
            (content, self.request), ISerializeToJson
        )
        return serializer()

    def test_composite(self):
        """Test serialization of a Composite Page."""
        content = self.composite
        data = self.serialize(content)
        self.assertEqual(data['@type'], 'composite')
        self.assertEqual(data['id'], 'home')
        self.assertEqual(data['items_total'], 1)
        self.assertIsNotNone(data['breadcrumbs'])
        # Style
        self.assertTrue(data['display_header'])
        self.assertTrue(data['display_footer'])
        # SEO
        self.assertEqual(
            data['canonical_url'],
            'http://localhost:8080/home'
        )
        self.assertEqual(data['robots'], 'index')

    def test_block_checker(self):
        """Test serialization of a Block Checker."""
        content = self.block_checker
        data = self.serialize(content)
        self.assertEqual(data['@type'], 'block_checker')
        self.assertEqual(data['title'], 'Checker')
        self.assertEqual(data['items_total'], 3)
        self.assertIsNotNone(data['breadcrumbs'])
        # Style
        self.assertIsNone(data['css_class'])
        self.assertIsNone(data['style_background_color'])
        self.assertIsNone(data['style_color'])
        self.assertIsNone(data['style_margin'])
        self.assertIsNone(data['style_padding'])

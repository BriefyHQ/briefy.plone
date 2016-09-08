# -*- coding: utf-8 -*-
"""Test fields helpers."""
from briefy.plone.testing import INTEGRATION_TESTING
from briefy.plone.utils.fields import get_all_fields_from_object
from briefy.plone.utils.fields import get_image_fields
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


import unittest2 as unittest


class BaseTestCase(unittest.TestCase):
    """Base test case."""

    layer = INTEGRATION_TESTING

    def _create_content(self, portal):
        """Create dummy content for our tests."""
        en = portal['en']
        home = en['home']
        self.composite = home
        api.content.create(
            type='block_jumbotron',
            id='block_1',
            container=home,
            title='Jumbotron',
            description='jumbotron'
        )
        self.block = home['block_1']

    def setUp(self):
        """Setup testcase."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self._create_content(self.portal)


class TestFieldsFromObject(BaseTestCase):
    """Test case for get_all_fields_from_object."""

    def test_get_all_fields_from_composite_page(self):
        """Test listing of all field names for an object."""
        content = self.composite
        fields = get_all_fields_from_object(content)
        self.assertIn('title', fields)
        self.assertIn('description', fields)
        self.assertNotIn('image', fields)
        self.assertIn('display_footer', fields)
        self.assertIn('display_header', fields)
        self.assertIn('canonical_url', fields)
        self.assertIn('robots', fields)

    def test_get_all_fields_from_block_jumbotron(self):
        """Test listing of all field names for an object."""
        content = self.block
        fields = get_all_fields_from_object(content)
        self.assertIn('title', fields)
        self.assertIn('description', fields)
        self.assertIn('image', fields)
        self.assertNotIn('display_footer', fields)
        self.assertNotIn('display_header', fields)
        self.assertIn('css_class', fields)


class TestGetImageFields(BaseTestCase):
    """Test case for has_image_field."""

    def test_has_image_field_composite_page(self):
        """Test if composite page has an image field."""
        content = self.composite
        fields = get_image_fields(content)
        self.assertFalse(fields)

    def test_has_image_field_block_jumbotron(self):
        """Test if block jumbotron has an image field."""
        content = self.block
        fields = get_image_fields(content)
        self.assertTrue(fields)

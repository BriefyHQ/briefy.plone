# -*- coding: utf-8 -*-
"""Test url generation."""
from briefy.plone.imaging import urls
import unittest


class TestURLS(unittest.TestCase):
    """Test url generation."""

    def test_prepare_image_url(self):
        """Test image_url path."""
        func = urls._prepare_image_url
        self.assertEqual(func(u'source/cms/foo/bar.jpg'), u'cms/foo/bar.jpg')
        self.assertEqual(func(u'source/cms/foo/image/foo.jpg'), u'cms/foo/image/foo.jpg')

    def test_generate_url(self):
        """Test image_url path."""
        from briefy.plone.config import THUMBOR_BASE_URL
        func = urls.generate_url
        self.assertIn(
            u'100x100/smart/cms/foo/bar.jpg',
            func(u'source/cms/foo/bar.jpg', 100, 100)
        )
        self.assertIn(
            u'150x100/smart/cms/foo/bar.jpg',
            func(u'source/cms/foo/bar.jpg', 150, 100)
        )
        self.assertTrue(
            func(u'source/cms/foo/bar.jpg', 150, 100).startswith(THUMBOR_BASE_URL)
        )

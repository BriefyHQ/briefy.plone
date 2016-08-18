# -*- coding: utf-8 -*-
"""Test utils."""
from briefy.plone import utils
import unittest


class TestNormalizer(unittest.TestCase):
    """Test filename normalizer."""

    def test_normalize_filename(self):
        """Test filename normalizer."""
        func = utils.normalize_filename
        self.assertEqual(func(u'picture.jpeg'), u'picture.jpeg')
        self.assertEqual(func(u'Picture.jpeg'), u'picture.jpeg')
        self.assertEqual(func(u'Picture.JpEG'), u'picture.jpeg')
        self.assertEqual(func(u'ÅÄÖrjy.JpEG'), u'aaorjy.jpeg')
        self.assertEqual(func(u'ÅÄÖrjy.png'), u'aaorjy.png')
        self.assertEqual(func(u'ÅÄÖrjy-gif'), u'aaorjy-gif')
        self.assertEqual(func(u'Photo of Åadvaark-.gif'), u'photo-of-aadvaark.gif')
        self.assertEqual(func(u'Photo of Åadvaark-gif'), u'photo-of-aadvaark-gif')

# -*- coding: utf-8 -*-
"""Test S3 Image upload."""
from briefy.plone.config import S3_BUCKET
from briefy.plone.adapters.storages import IAlternateStorageLocation
from briefy.plone.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobImage

import boto3
import os
import unittest


TEST_JPEG_FILE = open(
    os.path.sep.join(__file__.split(os.path.sep)[:-1] + ['image.jpg', ]),
    'rb'
).read()


class IntegrationTest(unittest.TestCase):
    """S3 Image upload integration test."""

    layer = INTEGRATION_TESTING

    def _image_value(self, filename=u'image.jpg'):
        """Create an image value."""
        return NamedBlobImage(data=TEST_JPEG_FILE, filename=filename)

    def setUp(self):
        """Setup testing environment."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_subscriber_image_on_s3(self):
        """Upload image field from Image content type to Amazon."""
        ctype = 'Image'

        # Create connection to S3
        resource = boto3.resource('s3')
        resource.create_bucket(Bucket=S3_BUCKET)

        content = api.content.create(
            type=ctype, id='image.jpg', container=self.portal, image=self._image_value()
        )
        data = IAlternateStorageLocation(content)
        self.assertIn('image', data.fields)
        self.assertEqual(data.get_field('image'), 'source/cms/image.jpg')
        for fieldname, path in data.items():
            obj = resource.Object(S3_BUCKET, path)
            self.assertEqual(obj.content_length, 128827)

    def test_subscriber_news_item_on_s3(self):
        """Upload image field from News Item content type to Amazon."""
        ctype = 'News Item'

        # Create connection to S3
        resource = boto3.resource('s3')
        resource.create_bucket(Bucket=S3_BUCKET)

        content = api.content.create(
            type=ctype, id='interesting-news', container=self.portal, image=self._image_value()
        )
        data = IAlternateStorageLocation(content)
        self.assertIn('image', data.fields)
        self.assertEqual(data.get_field('image'), 'source/cms/interesting-news/image/image.jpg')
        for fieldname, path in data.items():
            obj = resource.Object(S3_BUCKET, path)
            self.assertEqual(obj.content_length, 128827)

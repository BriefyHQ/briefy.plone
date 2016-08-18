# -*- coding: utf-8 -*-
"""Test upgrade steps."""
from briefy.plone.config import PROJECTNAME
from briefy.plone.testing import INTEGRATION_TESTING


import unittest


class UpgradesTestCase(unittest.TestCase):
    """Ensure product upgrades work."""

    layer = INTEGRATION_TESTING
    profile = PROJECTNAME + ':default'

    def setUp(self):
        """Setup testing environment."""
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']

    def test_latest_version(self):
        """Test latest version of profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile(self.profile)[0],
            u'20160816'
        )

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item['source'] == source and item['dest'] == dest

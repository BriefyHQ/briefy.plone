# -*- coding: utf-8 -*-
"""Test upgrade steps."""
from briefy.plone.config import PROJECTNAME
from briefy.plone.testing import INTEGRATION_TESTING
from Products.GenericSetup.upgrade import listUpgradeSteps

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
            u'20161101'
        )

    def _match(self, item, source, dest):
        source, dest = tuple([source]), tuple([dest])
        return item['source'] == source and item['dest'] == dest

    def test_20160825_available(self):
        """Test upgrade step 20160825 is available."""
        steps = listUpgradeSteps(self.setup, self.profile, '20160816')
        steps = [s for s in steps if self._match(s[0], '20160816', '20160825')]
        self.assertEqual(len(steps), 1)

    def test_20160831_available(self):
        """Test upgrade step 20160831 is available."""
        steps = listUpgradeSteps(self.setup, self.profile, '20160825')
        steps = [s for s in steps if self._match(s[0], '20160825', '20160831')]
        self.assertEqual(len(steps), 1)

    def test_20160906_available(self):
        """Test upgrade step 20160906 is available."""
        steps = listUpgradeSteps(self.setup, self.profile, '20160831')
        steps = [s for s in steps if self._match(s[0], '20160831', '20160906')]
        self.assertEqual(len(steps), 1)

    def test_20160922_available(self):
        """Test upgrade step 20160906 is available."""
        steps = listUpgradeSteps(self.setup, self.profile, '20160906')
        steps = [s for s in steps if self._match(s[0], '20160906', '20160922')]
        self.assertEqual(len(steps), 1)

    def test_20161018_available(self):
        """Test upgrade step 20161018 is available."""
        steps = listUpgradeSteps(self.setup, self.profile, '20160922')
        steps = [s for s in steps if self._match(s[0], '20160922', '20161018')]
        self.assertEqual(len(steps), 1)

    def test_20161101_available(self):
        """Test upgrade step 20161101 is available."""
        steps = listUpgradeSteps(self.setup, self.profile, '20161018')
        steps = [s for s in steps if self._match(s[0], '20161018', '20161101')]
        self.assertEqual(len(steps), 1)

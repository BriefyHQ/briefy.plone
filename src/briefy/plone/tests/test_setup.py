# -*- coding: utf-8 -*-
"""Test briefy.plone setup."""
from briefy.plone.config import PROJECTNAME
from briefy.plone.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


class TestInstall(unittest.TestCase):
    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Setup testing environment."""
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        """Test if package is installed."""
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        """Test if Interface Layer is present."""
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IBriefyPloneLayer', layers)

    def test_dependencies_are_installed(self):
        """Validate profile has been run and the product dependencies have been installed."""
        installed = [p['id'] for p in self.qi.listInstalledProducts()]
        self.assertIn('plone.restapi', installed)
        self.assertIn('plone.app.contenttypes', installed)
        self.assertIn('plone.app.multilingual', installed)

    def test_default_object_creation(self):
        """Validate if default CMS structure was created."""
        portal = self.portal
        # Language folders
        self.assertIn('en', portal.objectIds())
        self.assertIn('de', portal.objectIds())

        # English Root folder
        en = portal['en']
        self.assertEqual(en.title, 'Briefy English site')
        self.assertIsNotNone(api.group.get('en_editors'))
        self.assertIn('home', en.objectIds())
        self.assertIn('team', en.objectIds())
        self.assertIn('blog', en.objectIds())
        self.assertIn('media', en.objectIds())

        # Deutsch Root folder
        de = portal['de']
        self.assertEqual(de.title, 'Briefy Deutsch site')
        self.assertIsNotNone(api.group.get('de_editors'))
        self.assertIn('home', de.objectIds())
        self.assertIn('team', de.objectIds())
        self.assertIn('blog', de.objectIds())
        self.assertIn('media', de.objectIds())


class TestDefaultSettings(unittest.TestCase):
    """Default settings should have been set."""

    layer = INTEGRATION_TESTING

    def test_title(self):
        """Test title is set."""
        key = api.portal.get_registry_record(
            'plone.site_title'
        )
        self.assertEqual(u'Briefy CMS', key)

    def test_email_address(self):
        """Test email address is set."""
        key = api.portal.get_registry_record(
            'plone.email_from_address'
        )
        self.assertEqual(u'site@briefy.co', key)

    def test_email_name(self):
        """Test email name is set."""
        key = api.portal.get_registry_record(
            'plone.email_from_name'
        )
        self.assertEqual(u'Briefy CMS', key)

    def test_smtp_host(self):
        """Test if smtp_host is set."""
        key = api.portal.get_registry_record(
            'plone.smtp_host'
        )
        self.assertEqual(u'smtp.gmail.com', key)

    def test_smtp_port(self):
        """Test if smtp_port is set."""
        key = api.portal.get_registry_record(
            'plone.smtp_port'
        )
        self.assertEqual(587, key)

    def test_logo(self):
        """Test if logo is set."""
        key = api.portal.get_registry_record(
            'plone.site_logo'
        )
        self.assertIsNotNone(key)


class TestUninstall(unittest.TestCase):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Setup testing environment."""
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        """Test package is uninstalled."""
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        """Test Interface layer is removed."""
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IBriefyPloneLayer', layers)

# -*- coding: utf-8 -*-
"""Test traversal hooks."""
from briefy.plone.interfaces import IBriefyPloneLayer
from briefy.plone.testing import FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser
from zope.interface.declarations import directlyProvides

import transaction
import unittest


class TraversalTestCase(unittest.TestCase):
    """Traversal hooks Integration test."""

    layer = FUNCTIONAL_TESTING

    def setup_content(self):
        """Setup base content for tests."""
        with api.env.adopt_roles(['Manager', 'Reviewer']):
            privacy = api.content.create(
                type='Document',
                id='privacy',
                container=self.portal
            )
            privacy.title = u'Privacy policy'
            privacy.description = u'This is our privacy policy'
            privacy.subjects = ['Foo', 'Bar']
        return privacy

    def setUp(self):  # noqa
        """Setup testing environment."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.request, IBriefyPloneLayer)
        self.portal.portal_workflow.setChainForPortalTypes(
            ['Document', ],
            ['one_state_workflow'],
        )
        self.page = self.setup_content()
        self.browser = Browser(self.layer['app'])
        transaction.commit()

    def test_no_json_mark_interface_applied(self):
        """Test json mark interface is not applied by default."""
        page = self.page
        browser = self.browser
        browser.open('{0}'.format(page.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        # Redirect to login form
        self.assertIn('text/html', browser.headers['content-type'])
        self.assertIn('<html', browser.contents)
        self.assertIn('You must enable cookies before you can log in', browser.contents)

    def test_json_mark_interface_applied(self):
        """Test json mark interface is applied if header present."""
        import json
        page = self.page
        browser = self.browser
        browser.addHeader('Accept', 'application/json')
        browser.open('{0}'.format(page.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        # A normal html response from Plone
        self.assertIn('application/json', browser.headers['content-type'])
        json_body = json.loads(browser.contents)
        self.assertIsInstance(json_body, dict)
        self.assertIn('@id', json_body)

    def test_unauthorized_when_accessing_blocked_views(self):
        """Test unauthorized is raised when accessing blocked views."""
        from zExceptions.unauthorized import Unauthorized
        # A normal access will not raise an exception
        browser = self.browser
        browser.open('{0}/@@search'.format(self.portal.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertIn('text/html', browser.headers['content-type'])
        self.assertIn('<html', browser.contents)

        # with the Accept header applied we should not be able to
        # use the @@search view
        browser = self.browser
        browser.handleErrors = False
        browser.addHeader('Accept', 'application/json')
        try:
            browser.open('{0}/@@search'.format(self.portal.absolute_url()))
        except Unauthorized:
            pass

    def test_authorized_when_accessing_whitelisted_views(self):
        """Test unauthorized is not raised when accessing whitelisted views."""
        from zExceptions.unauthorized import Unauthorized
        setRoles(self.portal, TEST_USER_ID, [])
        browser = self.browser
        browser.open('{0}/mail_password_form'.format(self.portal.absolute_url()))
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertIn('text/html', browser.headers['content-type'])
        self.assertIn('<html', browser.contents)

        try:
            browser.open('{0}/@@search'.format(self.portal.absolute_url()))
        except Unauthorized:
            pass

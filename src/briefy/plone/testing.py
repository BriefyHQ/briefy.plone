# -*- coding: utf-8 -*-
"""Fixtures for briefy.plone testing."""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import botocore.endpoint
import os


def get_url():
    """Return the url for the SQS server."""
    host = os.environ.get('S3_IP', 'localhost')
    port = os.environ.get('S3_PORT', '5000')
    return 'http://{0}:{1}'.format(host, port)


class Fixture(PloneSandboxLayer):
    """Testing fixture."""

    defaultBases = (PLONE_FIXTURE,)

    def mock_s3(self):
        """Mock S3 communication."""
        class MockEndpoint(botocore.endpoint.Endpoint):
            def __init__(self, host, *args, **kwargs):
                super(MockEndpoint, self).__init__(get_url(), *args, **kwargs)

        botocore.endpoint.Endpoint = MockEndpoint

    def setUpZope(self, app, configurationContext):  # noqa
        """Setup the application server."""
        # Load ZCML
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        import plone.app.caching
        self.loadZCML(package=plone.app.caching)
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes)
        import briefy.plone
        self.loadZCML(package=briefy.plone)

        # Mock S3
        self.mock_s3()

    def setUpPloneSite(self, portal):  # noqa
        """Setup the Plone site."""
        self.applyProfile(portal, 'plone.app.contenttypes:default')
        self.applyProfile(portal, 'briefy.plone:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='briefy.plone:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='briefy.plone:Functional')

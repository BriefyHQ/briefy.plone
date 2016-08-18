# -*- coding: utf-8 -*-
"""Fixtures for briefy.plone testing."""
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class Fixture(PloneSandboxLayer):
    """Testing fixture."""

    defaultBases = (PLONE_FIXTURE,)

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

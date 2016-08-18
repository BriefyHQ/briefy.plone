# -*- coding: utf-8 -*-
"""Implement a sitemap service."""
from plone import api
from plone.restapi.services import Service


class SitemapGet(Service):
    """Sitemap service GET handler."""

    def get_all_entries(self):
        """Return a list of objects.

        :returns: List of contentobjects
        :rtype: list
        """
        request = self.request
        context = self.context
        view = api.content.get_view(
            name='sitemap.xml.gz',
            context=context,
            request=request
        )
        objects = [o for o in view.objects()]
        return objects

    def reply(self):
        """Response for a sitemap request."""
        return self.get_all_entries()

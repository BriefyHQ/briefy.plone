# -*- coding: utf-8 -*-
"""JSON view for sitemaps."""
from plone.app.layout.sitemap.sitemap import SiteMapView

import json


class SitemapJSONView(SiteMapView):
    """Browser view that returns a list of objects that should be indexed."""

    def __init__(self, context, request):
        """Initialize the view.

        :param context: Context object
        :type context: object
        :param request: Request object
        :type request: request
        """
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):
        """Return a JSON response."""
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        request = self.request
        response = request.response
        data = self.get_response_body()
        response.setHeader('Access-Control-Allow-Origin', '*')
        response.setHeader('Access-Control-Allow-Headers', 'X-Locale')
        response.setHeader('Content-Type', 'application/json;charset=utf-8')
        return data

    def get_all_entries(self):
        """Return a list of objects.

        :returns: List of contentobjects
        :rtype: list
        """
        objects = [o for o in self.objects()]
        return objects

    def get_response_body(self):
        """Return a JSON body for this content."""
        return json.dumps(self.get_all_entries())


# -*- coding: utf-8 -*-
"""JSON view for sitemaps."""
from BTrees.OOBTree import OOBTree
from plone import api
from plone.app.layout.sitemap.sitemap import SiteMapView
from Products.CMFPlone.interfaces import IPloneSiteRoot

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

    def objects(self):
        """Returns the data to create the sitemap."""
        query = {}
        catalog = api.portal.get_tool('portal_catalog')
        utils = api.portal.get_tool('plone_utils')
        query['portal_type'] = utils.getUserFriendlyTypes()
        typesUseViewActionInListings = api.portal.get_registry_record(
            'plone.types_use_view_action_in_listings'
        )
        is_plone_site_root = IPloneSiteRoot.providedBy(self.context)
        if not is_plone_site_root:
            query['path'] = '/'.join(self.context.getPhysicalPath())
        query['is_default_page'] = True
        default_page_modified = OOBTree()
        keywords = {}
        print(query, keywords)
        for item in catalog.searchResults(query, **keywords):
            key = item.getURL().rsplit('/', 1)[0]
            value = (item.modified.micros(), item.modified.ISO8601())
            default_page_modified[key] = value
        # The plone site root is not catalogued.
        if is_plone_site_root:
            loc = self.context.absolute_url()
            date = self.context.modified()
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            yield {
                'loc': loc,
                'lastmod': lastmod,
            }

        query['is_default_page'] = False
        print(query, keywords)
        for item in catalog.searchResults(query, **keywords):
            loc = item.getURL()
            date = item.modified
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            if item.portal_type in typesUseViewActionInListings:
                loc += '/view'
            yield {
                'loc': loc,
                'lastmod': lastmod
            }

    def get_all_entries(self):
        """Return a list of objects.

        :returns: List of contentobjects
        :rtype: list
        """
        objects = [o for o in self.objects()]
        print(len(objects))
        return objects

    def get_response_body(self):
        """Return a JSON body for this content."""
        return json.dumps(self.get_all_entries())

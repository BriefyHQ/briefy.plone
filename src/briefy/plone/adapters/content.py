# -*- coding: utf-8 -*-
"""JSON Serializer for Contents."""
from briefy.plone.adapters.social import SocialMetadata
from briefy.plone.behaviors.menu import IMenu
from briefy.plone.content.block_checker import IBlockChecker
from briefy.plone.content.block_columns import IBlockColumns
from briefy.plone.content.block_gallery import IBlockGallery
from briefy.plone.content.block_roster import IBlockRoster
from briefy.plone.content.composite import ICompositePage
from briefy.plone.content.gallery import IGallery
from briefy.plone.content.roster import IRoster
from briefy.plone.interfaces import IBriefyPloneJSONLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityContainer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson as BaseSerializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer

import json


def get_children_of_folderish(context):
    """Return a list of children object of a folder."""
    brains = api.content.find(
        context=context,
        depth=1,
        sort_on='getObjPositionInParent'
    )
    results = [b.getObject() for b in brains]
    return results


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IBriefyPloneJSONLayer)
class SerializeToJson(BaseSerializer):
    """Serialize Briefy CMS objects to JSON."""

    def __call__(self, version=None):
        """Execute the serialization."""
        result = super(SerializeToJson, self).__call__(version=version)
        # Remove parent and review_state keys
        keys = ('parent', 'review_state')
        for key in keys:
            if key in result:
                del(result[key])
        return result


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IBriefyPloneJSONLayer)
class SerializeFolderishToJson(SerializeToJson):
    """Serialize a Briefy Folderish object to JSON."""

    def _getObjects(self):
        return get_children_of_folderish(self.context)

    def get_breadcrumbs(self):
        """Return breadcrumbs for this content."""
        breadcrumbs_view = getMultiAdapter((self.context, self.request), name='breadcrumbs_view')
        result = []
        for crumb in breadcrumbs_view.breadcrumbs():
            result.append({
                'title': crumb['Title'],
                'url': crumb['absolute_url']
            })
        return result

    def get_items(self, batch):
        """Remove not needed items from summary."""
        result = []
        for obj in batch:
            item = getMultiAdapter((obj, self.request), ISerializeToJson)()
            if 'social_metadata' in item:
                del(item['social_metadata'])
            if 'breadcrumbs' in item:
                del(item['breadcrumbs'])
            result.append(item)
        return result

    def get_menu(self):
        """Return meu for this content."""
        nav_root = api.portal.get_navigation_root(self.context)
        menu = IMenu(nav_root, None)
        result = {}
        if menu:
            result['menu'] = {
                'header': json.loads(menu.menu_header),
                'footer': json.loads(menu.menu_footer),
                'login': json.loads(menu.menu_login),
            }
        return result

    def __call__(self, version=None):
        """Execute the serialization."""
        folder_metadata = super(SerializeFolderishToJson, self).__call__(version=version)
        breadcrumbs = self.get_breadcrumbs()

        batch = self._getObjects()

        result = folder_metadata
        result['@id'] = self.context.absolute_url()
        result['items_total'] = len(batch)

        result['items'] = self.get_items(batch)
        result['breadcrumbs'] = breadcrumbs
        result['social_metadata'] = SocialMetadata(self.context)()
        result['creators'] = 'Briefy Team'  # HACK
        # menu = self.get_menu()
        # if menu:
        #     keys = [k for k in result.keys() if k.startswith('menu')]
        #     for key in keys:
        #         del(result[key])
        #     result.update(menu)
        return result


@implementer(ISerializeToJson)
@adapter(ICompositePage, IBriefyPloneJSONLayer)
class SerializeCompositeToJson(SerializeFolderishToJson):
    """Serialize a Composite Page to JSON."""


@implementer(ISerializeToJson)
@adapter(IBlockChecker, IBriefyPloneJSONLayer)
class SerializeBlockCheckerToJson(SerializeFolderishToJson):
    """Serialize a Block checker to JSON."""


@implementer(ISerializeToJson)
@adapter(IBlockColumns, IBriefyPloneJSONLayer)
class SerializeBlockColumnsToJson(SerializeFolderishToJson):
    """Serialize a Block columns to JSON."""


@implementer(ISerializeToJson)
@adapter(IRoster, IBriefyPloneJSONLayer)
class SerializeRosterToJson(SerializeFolderishToJson):
    """Serialize a Roster to JSON."""


@implementer(ISerializeToJson)
@adapter(IGallery, IBriefyPloneJSONLayer)
class SerializeGalleryToJson(SerializeFolderishToJson):
    """Serialize a Gallery to JSON."""


@implementer(ISerializeToJson)
@adapter(IBlockRoster, IBriefyPloneJSONLayer)
class SerializeBlockRosterToJson(SerializeFolderishToJson):
    """Serialize a Block Roster to JSON."""

    def _getObjects(self):
        context = self.context
        roster = context.roster
        if roster:
            context = roster.to_object
            return get_children_of_folderish(context)


@implementer(ISerializeToJson)
@adapter(IBlockGallery, IBriefyPloneJSONLayer)
class SerializeBlockGalleryToJson(SerializeFolderishToJson):
    """Serialize a Block Gallery to JSON."""

    def _getObjects(self):
        context = self.context
        gallery = context.gallery
        if gallery:
            context = gallery.to_object
            return get_children_of_folderish(context)

# -*- coding: utf-8 -*-
"""JSON Serializer for Contents."""
from briefy.plone.adapters.social import SocialMetadata
from briefy.plone.content.block_checker import IBlockChecker
from briefy.plone.content.block_columns import IBlockColumns
from briefy.plone.content.block_gallery import IBlockGallery
from briefy.plone.content.block_roster import IBlockRoster
from briefy.plone.content.composite import ICompositePage
from briefy.plone.content.gallery import IGallery
from briefy.plone.content.roster import IRoster
from briefy.plone.interfaces import IBriefyPloneJSONLayer
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityContainer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson as BaseSerializer
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IBriefyPloneJSONLayer)
class SerializeToJson(BaseSerializer):
    """Serialize Briefy CMS objects to JSON."""

    def __call__(self):
        """Execute the serialization."""
        result = super(SerializeToJson, self).__call__()
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
        context = self.context
        return context.objectValues()

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

    def __call__(self):
        """Execute the serialization."""
        folder_metadata = super(SerializeFolderishToJson, self).__call__()
        breadcrumbs = self.get_breadcrumbs()

        batch = self._getObjects()

        result = folder_metadata
        result['@id'] = self.context.absolute_url()
        result['items_total'] = len(batch)

        result['items'] = [
            getMultiAdapter((obj, self.request), ISerializeToJson)()
            for obj in batch
        ]
        result['breadcrumbs'] = breadcrumbs
        result['social_metadata'] = SocialMetadata(self.context)()
        result['creators'] = 'Briefy Team'  # HACK
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
            return context.objectValues()


@implementer(ISerializeToJson)
@adapter(IBlockGallery, IBriefyPloneJSONLayer)
class SerializeBlockGalleryToJson(SerializeFolderishToJson):
    """Serialize a Block Gallery to JSON."""

    def _getObjects(self):
        context = self.context
        gallery = context.gallery
        if gallery:
            context = gallery.to_object
            return context.objectValues()

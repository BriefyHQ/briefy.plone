# -*- coding: utf-8 -*-
"""JSON Serializer for Contents."""
from briefy.plone.content.block_checker import IBlockChecker
from briefy.plone.content.block_columns import IBlockColumns
from briefy.plone.content.composite import ICompositePage
from briefy.plone.content.gallery import IGallery
from briefy.plone.content.roster import IRoster
from briefy.plone.interfaces import IBriefyPloneJSONLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityContainer
from plone.restapi.batching import HypermediaBatch
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

    def _build_query(self):
        path = '/'.join(self.context.getPhysicalPath())
        query = {'path': {
            'depth': 1,
            'query': path,
            'sort_on': 'getObjPositionInParent'}
        }
        return query

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
        query = self._build_query()
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(query)

        batch = HypermediaBatch(self.request, brains)

        result = folder_metadata
        result['@id'] = self.context.absolute_url()
        result['items_total'] = batch.items_total
        if batch.links:
            result['batching'] = batch.links

        result['items'] = [
            getMultiAdapter((brain.getObject(), self.request), ISerializeToJson)()
            for brain in batch
        ]
        result['breadcrumbs'] = breadcrumbs
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

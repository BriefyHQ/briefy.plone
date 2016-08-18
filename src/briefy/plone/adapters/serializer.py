# -*- coding: utf-8 -*-
"""JSON Serializer for Composite Page."""
from briefy.plone.content.block_checker import IBlockChecker
from briefy.plone.content.composite import ICompositePage
from briefy.plone.interfaces import IBriefyPloneLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.batching import HypermediaBatch
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IBriefyPloneLayer, Interface)
class DXSerializeToJson(SerializeToJson):
    """Serialize Briefy CMS objects to JSON."""

    def __call__(self):
        """Execute the serialization."""
        result = super(DXSerializeToJson, self).__call__()
        return result


class SerializeFolderishToJson(DXSerializeToJson):
    """Serialize a Briefy Folderish object to JSON."""

    def _build_query(self):
        path = '/'.join(self.context.getPhysicalPath())
        query = {'path': {
            'depth': 1,
            'query': path,
            'sort_on': 'getObjPositionInParent'}
        }
        return query

    def __call__(self):
        """Execute the serialization."""
        folder_metadata = super(SerializeFolderishToJson, self).__call__()

        query = self._build_query()

        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(query)

        batch = HypermediaBatch(self.request, brains)

        result = folder_metadata
        result['@id'] = batch.canonical_url
        result['items_total'] = batch.items_total
        if batch.links:
            result['batching'] = batch.links

        result['items'] = [
            getMultiAdapter((brain.getObject(), self.request), ISerializeToJson)()
            for brain in batch
        ]
        return result


@implementer(ISerializeToJson)
@adapter(ICompositePage, Interface)
class SerializeCompositeToJson(SerializeFolderishToJson):
    """Serialize a Composite Page to JSON."""


@implementer(ISerializeToJson)
@adapter(IBlockChecker, Interface)
class SerializeBlockCheckerToJson(SerializeFolderishToJson):
    """Serialize a Block checker to JSON."""

# -*- coding: utf-8 -*-
"""S3 storage adapter for drivejoy.cms."""
from briefy.plone import utils
from briefy.plone.config import logger
from briefy.plone.config import S3_BUCKET
from briefy.plone.config import S3_PATH
from persistent.mapping import PersistentMapping
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import boto3
import StringIO


IMAGES_KEY = 'briefy.plone.storage'


class IAlternateStorageLocation(Interface):
    """Alternate location for image Fields."""

    def fields():
        """List of fields stored remotely."""

    def get_field(fieldname):  # noqa
        """Return the path for the stored remotely."""

    def set_field(fieldname, path):  # noqa
        """Set the path for the data of fieldname stored remotely."""

    def items():
        """Return all values in key, value tuples."""


@implementer(IAlternateStorageLocation)
@adapter(IDexterityContent)
class AlternateStorageLocation(object):
    """Alternate location for image Fields."""

    def __init__(self, context):
        """Initialize the AlternateStorageLocation.

        :param context: Plone content type
        :type context: object
        """
        self.context = context
        annotations = self.__annotations
        annotations.setdefault(IMAGES_KEY, PersistentMapping())

    @property
    def __annotations(self):
        annotations = IAnnotations(self.context)
        if IMAGES_KEY in annotations:
            annotations = annotations[IMAGES_KEY]
        return annotations

    @property
    def fields(self):
        """List of fields stored in S3."""
        return self.__annotations.keys()

    def get_field(self, fieldname):  # noqa
        """Return the path for a field in S3."""
        return self.__annotations.get(fieldname)

    def set_field(self, fieldname, path):  # noqa
        """Set the path for the data of fieldname stored on S3."""
        self.__annotations[fieldname] = path

    def items(self):
        """Return all fielname and paths."""
        return [(k, v) for k, v in self.__annotations.items() if k and v]


class S3Adapter(object):
    """S3 storage adapter for briefy.plone."""

    _storage = None

    def __init__(self, obj):
        """Initialize the S3Adapter.

        :param obj: Plone content type
        :type obj: object
        """
        self.site = api.portal.get()
        self.obj = obj

    @property
    def storage(self):
        """Return a S3 resource object."""
        if not self._storage:
            s3 = boto3.resource('s3')
            self._storage = s3.Bucket(S3_BUCKET)
        return self._storage

    def _annotate_object(self, fieldname, s3_path):
        """Annotate the object with the path to the field content on Amazon S3.

        :param fieldname: Fieldname for the content
        :type fieldname: str
        :param s3_path: Path to the content on Amazon S3
        :type s3_path: str
        """
        obj = self.obj
        data = IAlternateStorageLocation(obj)
        data.set_field(fieldname, s3_path)

    def _write_to_storage(self, data, path):
        """Write data to the storage.

        :param data: Data to be stored
        :type data: str
        :param path: Path to the content on Amazon S3
        :type path: str
        """
        status = True
        storage = self.storage
        # Create a file like object
        fh = StringIO.StringIO(data)
        fh.seek(0)
        # Store the data on Amazon
        try:
            storage.put_object(Key=path, Body=data)
        except Exception as e:
            logger.info('Exception: {0}'.format(e.message))
            status = False
        return status

    def _generate_path(self, fieldname, filename):
        """Generate path on Amazon S3 given a fieldname and a filename.

        :param fieldname: Name of the field containing the data to stored
        :type fieldname: str
        :param filename: Filename of the data
        :type filename: str
        """
        obj = self.obj
        obj_id = obj.id
        site_path = self.site.getPhysicalPath()
        obj_path = obj.getPhysicalPath()
        path = u'{0}{1}'.format(S3_PATH, '/'.join(obj_path[len(site_path):]))

        # If filename and obj_id are the same, we do not need to add the fieldname
        if not (filename == obj_id):
            filename = utils.normalize_filename(filename)
            path = u'{0}/{1}/{2}'.format(path, fieldname, filename)
        return path

    def _store_field(self, fieldname, field):
        """Generate path on Amazon S3 given a fieldname and a filename.

        :param fieldname: Name of the field containing the data to be stored
        :type fieldname: str
        :param field: Field to use
        :type field: object
        :returns: Status of the action
        :rtype: str
        """
        value = field.get(self.obj)
        if not value:
            return
        filename = value.filename
        data = value.data
        path = self._generate_path(fieldname, filename)
        status = self._write_to_storage(data, path)
        if status:
            # Annotate the object with the path to the image on S3
            self._annotate_object(fieldname, path)
            logger.debug('Field {0}: {1}'.format(fieldname, path))
        return '{0}: {1}'.format(fieldname, status)

    def store_fields(self, fields):
        """Store given fields on Amazon S3.

        :param fields: Name of the field containing the data to be stored
        :type fields: str
        """
        logger.info('Storing fields: {0}'.format(''.join([f[0] for f in fields])))
        results = []
        for fieldname, field in fields:
            results.append(self._store_field(fieldname, field))
        return results

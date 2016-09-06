# -*- coding: utf-8 -*-
"""Helpers to deal with fields for content objects."""
from plone.behavior.interfaces import IBehaviorAssignable
from plone.namedfile.file import NamedBlobImage
from zope.schema import getFieldsInOrder


def _get_all_fields_from_object(obj):
    """Return all fields and values of an object.

    :param obj: Plone content type object
    :type obj: object
    :returns: List of fields and values for that object
    :rtype: list
    """
    all_fields = [(k, v) for k, v in getFieldsInOrder(obj.getTypeInfo().lookupSchema())]
    behavior_assignable = IBehaviorAssignable(obj)
    if behavior_assignable:
        for behavior in behavior_assignable.enumerateBehaviors():
            all_fields += [(k, v) for k, v in getFieldsInOrder(behavior.interface)]
    return all_fields


def get_all_fields_from_object(obj):
    """Return all fields and transformed values of an object.

    :param obj: Plone content type object
    :type obj: object
    :returns: List of field names for the object
    :rtype: dict
    """
    fields = []
    for key, value in _get_all_fields_from_object(obj):
        fields.append(key)

    return fields


def get_image_fields(obj):
    """Check if image field is available for this object.

    :param obj: Plone content type object
    :type obj: object
    :returns: Boolean indicating if an image field is available for this object.
    :rtype: bool
    """
    fields = _get_all_fields_from_object(obj)
    image_fields = [(k, v) for k, v in fields if v._type is NamedBlobImage]

    return image_fields

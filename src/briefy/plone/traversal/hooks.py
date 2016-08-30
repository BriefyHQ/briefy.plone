# -*- coding: utf-8 -*-
"""This module marks requests to be served as JSON."""
from briefy.plone.config import ANON_WHITE_LISTED
from briefy.plone.config import BLACKLISTED
from briefy.plone.config import logger
from briefy.plone.interfaces import IBriefyPloneJSONLayer
from plone import api
from zExceptions.unauthorized import Unauthorized
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides


def _is_request_for_image_scale(physical_path):
    """Check if this request is for an image scale.

    :param physical_path: Plone content object
    :type physical_path: object
    :returns: Returns is this request is for an image scale
    :rtype: bool
    """
    return '@@images' in physical_path


def mark_json_request(obj, event):
    """Mark the request if we receive the proper header.

    :param obj: Plone content object
    :type obj: object
    :param event: Event
    :type event: event
    """
    request = event.request
    accept = request.get_header('HTTP_ACCEPT')
    if accept == 'application/json':
        # Also add our marker interface to the top of the list
        ifaces = [IBriefyPloneJSONLayer, ] + list(directlyProvidedBy(request))
        directlyProvides(request, *ifaces)
    else:
        try:
            event.request.post_traverse(reject_anonymous, (obj, event.request))
        except RuntimeError:
            # Make this work in a testrunner
            pass


def unauthorized_access_to_blacklisted(event):
    """Raise unauthorized to views that are BLACKLISTED.

    :param event: Event
    :type event: event
    """
    request = event.request
    if not IBriefyPloneJSONLayer.providedBy(request):
        return
    blacklisted = request.get('PATH_INFO').split('/')[-1] in BLACKLISTED
    if blacklisted:
        raise Unauthorized()


def reject_anonymous(obj, request):
    """Raise an Unauthorized exception if the request is made by an Anonymous user.

    :param obj: Plone content object
    :type obj: object
    :param event: Event
    :type event: event
    """
    if api.user.is_anonymous():
        portal = api.portal.get()
        portal_path = portal.getPhysicalPath()
        physical_path = request.physicalPathFromURL(request['URL'])
        is_image_scale = _is_request_for_image_scale(physical_path)
        if is_image_scale:
            # HACK: We should not block images
            return None
        url = physical_path[len(portal_path):]
        if url[-1] == 'index_html':
            url.pop()
        item_id = url[0]
        if not item_id.startswith(ANON_WHITE_LISTED):
            logger.debug(
                'Anonymous access to {0}'.format(item_id),
                extra=request
            )
            raise Unauthorized('Anonymous rejected')

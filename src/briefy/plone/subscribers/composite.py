# -*- coding: utf-8 -*-
"""Subscribers to LRF content events."""
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility


def remove_portlets(obj, event):
    """Remove portlets from Composite page.

    :param obj: Composite page
    :type obj: briefy.plone.content.composite.CompositePage
    :param event: Event
    :type event: event
    """
    # Get the proper portlet manager
    for manager_id in ('plone.leftcolumn', 'plone.rightcolumn'):
        manager = getUtility(IPortletManager, name=manager_id)

        # Get the current blacklist for the location
        blacklist = getMultiAdapter((obj, manager), ILocalPortletAssignmentManager)

        # Turn off the manager
        blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

# -*- coding: utf-8 -*-
"""Subscribers to LRF content events."""
from plone import api
from plone.app.dexterity.behaviors import constrains
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes


def create_groups(obj, event):
    """Create group for content managers in this Language Root Folder.

    :param obj: Language Root Folder
    :type obj: plone.dexterity.content.Container
    :param event: Event
    :type event: event
    """
    # Create Editors' group
    groupname = '{0}_editors'.format(obj.id)
    api.group.create(
        groupname=groupname,
        title='{0} Editors'.format(obj.title),
        description='{0} Content Editors'.format(obj.title),
        roles=[],
        groups=[],
    )
    # Set editor and contributor's role for the newly
    # created group on the current object
    api.group.grant_roles(
        groupname=groupname,
        roles=['Editor', 'Contributor', 'Reviewer'],
        obj=obj
    )


def create_home(obj, event):
    """Create a composite object named home inside the Language Root Folder.

    :param obj: Language Root Folder
    :type obj: plone.dexterity.content.Container
    :param event: Event
    :type event: event
    """
    home_id = 'home'
    home_title = u'Briefy: Coming Soon to Connect Businesses with Photographers'
    home_description = (
        u'Briefy is a Berlin based startup building the first intelligent '
        u'and worldwide marketplace for businesses to list photography jobs '
        u'and hire local professional photographers'
    )
    home_tags = [
        'photographer',
        'photography',
        'photographers',
        'jobs',
        'find',
        'search',
        'hire',
        'compare',
        'professional',
        'worldwide',
        'images',
        'photos',
        'startup',
        'berlin'
    ]
    if home_id not in obj.objectIds():
        # Create composite object
        api.content.create(
            type='composite', id=home_id, container=obj,
            title=home_title, description=home_description,
            subject=home_tags
        )

    # Set default page
    # obj.setDefaultPage('home')


def create_roster(obj, event):
    """Create a Team roster with id team inside the Language Root Folder.

    :param obj: Language Root Folder
    :type obj: plone.dexterity.content.Container
    :param event: Event
    :type event: event
    """
    id = 'team'
    title = u'Our Team'
    description = (
        u'This is our amazing team.'
    )
    tags = [
        'team',
        'briefy',
        'berlin',
        'startup',
    ]
    if id not in obj.objectIds():
        # Create roster object
        api.content.create(
            type='roster', id=id, container=obj,
            title=title, description=description,
            subject=tags
        )

    # No more rosters to be added here
    obj.manage_permission('Briefy: Add Roster', roles=[])


def create_blog(obj, event):
    """Create a blog folder inside this Language Root Folder.

    :param obj: Language Root Folder
    :type obj: plone.dexterity.content.Container
    :param event: Event
    :type event: event
    """
    blog_id = 'blog'
    blog_title = u'Briefy Blog'
    blog_description = u'Briefy Blog'
    if blog_id not in obj.objectIds():
        # Create blog folder
        api.content.create(
            type='Folder', id=blog_id, container=obj,
            title=blog_title, description=blog_description
        )
    blog = obj['blog']
    # We need to have a Collection named blog in here.
    if 'blog' not in blog.objectIds():
        aggregator = api.content.create(
            type='Collection', id=blog_id, container=blog,
            title=blog_title, description=blog_description
        )
        # Set the Collection criteria.
        #: Sort on the Effective date
        aggregator.sort_on = u'effective'
        aggregator.sort_reversed = True
        #: Query by Type and Review State
        aggregator.query = [
            {'i': u'portal_type',
             'o': u'plone.app.querystring.operation.selection.any',
             'v': [u'News Item'],
             },
            {'i': u'review_state',
             'o': u'plone.app.querystring.operation.selection.any',
             'v': [u'published'],
             },
            {u'i': u'path',
             u'o': u'plone.app.querystring.operation.string.path',
             u'v': u''
             }
        ]
        aggregator.setLayout('summary_view')

    # Constrain types
    allowed_types = ['News Item', ]
    behavior = ISelectableConstrainTypes(blog)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setImmediatelyAddableTypes(allowed_types)

    # Set default page
    blog.setDefaultPage('blog')

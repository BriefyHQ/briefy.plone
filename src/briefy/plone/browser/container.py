# -*- coding: utf-8 -*-
from plone.dexterity.browser.view import DefaultView
from plone import api


class BriefyView(DefaultView):
    """The default view for Dexterity content."""

    @property
    def contents(self):
        """Return list of contents available in this folderish."""
        all_content = api.content.find(
            context=self.context,
            depth=1,
            sort_on='getObjPositionInParent'
        )
        return all_content

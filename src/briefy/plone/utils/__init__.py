# -*- coding: utf-8 -*-
"""General utilities used by briefy.plone."""
from plone.i18n.normalizer import idnormalizer


def normalize_filename(value):
    """Normalize a filename.

    :param value: Filename
    :type value: str
    :returns: normalized filename
    :rtype: unicode
    """
    pieces = value.split('.')
    name = value
    ext = '.{0}'.format(pieces[-1]) if pieces and len(pieces) > 1 else u''
    if ext:
        name = value.replace(ext, u'')
        ext = '.{0}'.format(idnormalizer.normalize(ext))
    return u'{0}{1}'.format(idnormalizer.normalize(name), ext)

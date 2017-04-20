# -*- coding: utf-8 -*-
"""Vocabularies used by CMS."""

from zope.schema.vocabulary import SimpleVocabulary


form_vocabulary = SimpleVocabulary.fromItems([('Professional Lead', 'professional-lead'),
                                              ('Customer Quote', 'customer-quote')])

# -*- coding: utf-8 -*-
"""Imaging support for briefy.plone."""
from briefy.plone.config import S3_PATH
from briefy.plone.config import THUMBOR_BASE_URL
from briefy.plone.config import THUMBOR_KEY
from briefy.plone.config import THUMBOR_CACHE_URL
from briefy.plone.config import THUMBOR_PATH
from libthumbor import CryptoURL


_crypto = CryptoURL(key=THUMBOR_KEY)


def _prepare_image_url(s3_path):
    """Given the path of an image on S3, we return the thumbor path to this image.

    :param s3_path: Path to the image on S3
    :type s3_path: str
    :returns: Path to the image on Thumbor
    :rtype: str
    """
    return s3_path.replace(S3_PATH, THUMBOR_PATH)


def generate_url(s3_path, width, height, smart=True, cache=False):
    """Generate a signed url."""
    prefix = THUMBOR_CACHE_URL if cache else THUMBOR_BASE_URL
    image_url = _prepare_image_url(s3_path)
    encrypted_url = _crypto.generate(
        width=width,
        height=height,
        smart=smart,
        image_url=image_url
    )
    return '{base_url}{encrypted_url}'.format(
        base_url=prefix, encrypted_url=encrypted_url
    )

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://www.mangaeden.com'
uriRegex = '/[^/]+/([^/]+\-manga)/([^/]+)/?'


def get_main_content(url, get=None, post=None):
    result = re.search(uriRegex, url)
    groups = result.groups()
    return get('{}/en/{}/{}/'.format(domainUri, groups[0], groups[1]))


def get_volumes(content=None, url=None, get=None, post=None):
    volumes = document_fromstring(content).cssselect('a.chapterLink')
    return [domainUri + i.get('href') for i in volumes]


def get_archive_name(volume, index: int = None):
    name = re.search('\-manga/[^/]+/(\d+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return '{:0>3}'.format(name.groups()[0])


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    result = re.search('var\s+pages\s+=\s+(\[{.+}\])', content)
    items = []
    if not result:
        return []
    for i in json.loads(result.groups()[0]):
        items.append('https:' + i['fs'])
    return items


def get_manga_name(url, get=None):
    result = re.search(uriRegex, url)
    if not result:
        raise UrlParseError()
    return result.groups()[1]

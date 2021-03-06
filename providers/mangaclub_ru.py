#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'https://mangaclub.ru'
uriRegex = '\\.ru(?:/manga/view)?/(\d+\-[^/]+)/?'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}.html'.format(domainUri, name)
    return get(url)


def get_volumes(content: str, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.manga-ch-list a.col-sm-10')
    if not parser:
        return []
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    result = re.search('/manga/view/.+/([^.]+).html', volume)
    return result.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('.manga-lines-page a.manga-lines')
    return [i.get('data-i') for i in result]


def get_manga_name(url, get=None):  # todo: refactoring it!
    test = re.search(uriRegex + '\\.html', url)
    if test:
        return test.groups()[0]
    return re.search(uriRegex, url).groups()[0]

# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import requests


APP_VIEW_API = 'https://public.api.bsky.app'


def get_profiles(actors: list):
    """
    Retrieves the profiles of the list of actors.

    :param actors: list of at-identifiers (dids or handles).
    :return: list of profiles
    """
    if len(actors) <= 25:
        response = requests.get(
            url=APP_VIEW_API + '/xrpc/app.bsky.actor.getProfiles',
            params={'actors': actors}
        )
        response.raise_for_status()
        return response.json()['profiles']
    else:
        raise Exception('Too many actors.')


def feed(feed: dict = None, cursor: str = None, **kwargs):
    """
    feedContext:
        t-nature
        t-science
        t-tv
        t-music
        nettop
    """
    if not feed:
        feed = {'id': '3ld6okch7p32l', 'pinned': True, 'type': 'feed',
                'value': 'at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot'}  # default feed
    response = requests.get(
        url=APP_VIEW_API + '/xrpc/app.bsky.feed.getFeed',
        params={
            'feed': feed['value'],
            'limit': 50,
            'cursor': cursor
        }
    )
    response.raise_for_status()
    res = response.json()
    return res


def list_feed(list: dict = None, cursor: str = None, **kwargs):
    """
    feedContext:
        t-nature
        t-science
        t-tv
        t-music
        nettop
    """
    if not list:
        raise RuntimeError('No list specified.')
    response = requests.get(
        url=APP_VIEW_API + '/xrpc/app.bsky.feed.getFeed',
        params={
            'list': list['uri'],
            'limit': 50,
            'cursor': cursor
        }
    )
    response.raise_for_status()
    res = response.json()
    return res


def search_actors(query: dict):
    """ Search for actors. Parameters:

        q: string (required) Search query string; syntax, phrase, boolean, and faceting is unspecified, but Lucene query syntax is recommended.

        limit: integer (optional) Possible values: >= 1 and <= 100. Default value: 25

        cursor: string (optional)Optional pagination mechanism; may not necessarily allow scrolling through entire result set.

        Some recommendations can be found here: https://bsky.social/about/blog/05-31-2024-search
    """

    actors = []
    still_some = True
    cursor = None
    while still_some:
        response = requests.get(
            url=APP_VIEW_API + '/xrpc/app.bsky.actor.searchActors',
            params={
                'q': query,
                'limit': 50,
                'cursor': cursor}
        )
        response.raise_for_status()
        res = response.json()
        actors.extend(res['actors'])
        if 'cursor' in res:
            cursor = res['cursor']
        else:
            still_some = False
    return actors


def search_100_posts(query: dict):
    """
    Search a maximum of 100 posts.
    Parameters of the query:

        q: string (required) Search query string; syntax, phrase, boolean, and faceting is unspecified, but Lucene query syntax is recommended.

        sort: string (optional) Possible values: [top, latest]. Specifies the ranking order of results. Default value: latest.

        since: string (optional) Filter results for posts after the indicated datetime (inclusive). Expected to use 'sortAt' timestamp, which may not match 'createdAt'. A datetime.

        until: string (optional) Filter results for posts before the indicated datetime (not inclusive). Expected to use 'sortAt' timestamp, which may not match 'createdAt'. A datetime.

        mentions: at-identifier (optional) Filter to posts which mention the given account. Handles are resolved to DID before query-time. Only matches rich-text facet mentions.

        author: at-identifier (optional) Filter to posts by the given account. Handles are resolved to DID before query-time.

        lang: language (optional) Filter to posts in the given language. Expected to be based on post language field, though server may override language detection.

        domain: string (optional) Filter to posts with URLs (facet links or embeds) linking to the given domain (hostname). Server may apply hostname normalization.

        url: uri (optional) Filter to posts with links (facet links or embeds) pointing to this URL. Server may apply URL normalization or fuzzy matching.

        tag: string[] Possible values: <= 640 characters. Filter to posts with the given tag (hashtag), based on rich-text facet or tag field. Do not include the hash (#) prefix. Multiple tags can be specified, with 'AND' matching.

        limit: integer (optional) Possible values: >= 1 and <= 100. Default value: 25

        cursor: string (optional)Optional pagination mechanism; may not necessarily allow scrolling through entire result set.

        Some recommendations can be found here: https://bsky.social/about/blog/05-31-2024-search
    """
    response = requests.get(
        url=APP_VIEW_API + '/xrpc/app.bsky.feed.searchPosts',
        params=query
    )
    response.raise_for_status()
    return response.json()['posts']


if __name__ == '__main__':
    # Quick tests
    query = {
        'q': 'game theory',
        'sort': 'latest',
        'since': '2024-11-05T21:44:46Z',
        'until': '2024-12-10T21:44:46Z',
        'limit': 100
    }
    # found_posts = search_100_posts(query)
    feed = feed()
    # returns
    list_of_dictionaries   = feed['feed']
    cursor                 = feed['cursor']  # str
    # Every post dictionary consists of
    feedContext = list_of_dictionaries[0]['feedContext']
    post        = list_of_dictionaries[0]['post']
    # Every post dictionary contains:
    uri   = post['uri']
    cid   = post['cid']
    author  = post['author']
    record  = post['record']
    # Record consists of
    text    = record['text']
    # other fields of a post...
    embed   = post['embed']
    labels  = post['labels']
    threadgate = post['threadgate']
    # 'createdAt': '2024-11-05T21:44:46Z'
    ...
import unittest
from unittest.mock import AsyncMock

from twikit.client.client import Client
from twikit.user import User


def user_data(entities):
    legacy = {
        'created_at': 'Mon Jan 01 00:00:00 +0000 2024',
        'profile_image_url_https': 'https://example.test/a',
        'location': '', 'description': 'synthetic', 'pinned_tweet_ids_str': [],
        'verified': False, 'possibly_sensitive': False, 'can_dm': False,
        'can_media_tag': False, 'want_retweets': False, 'default_profile': False,
        'default_profile_image': False, 'has_custom_timelines': False,
        'followers_count': 0, 'fast_followers_count': 0, 'normal_followers_count': 0,
        'friends_count': 0, 'favourites_count': 0, 'listed_count': 0,
        'media_count': 0, 'statuses_count': 0, 'is_translator': False,
        'translator_type': 'none', 'entities': entities,
    }
    return {'rest_id': 'u1', 'core': {'name': 'Core name', 'screen_name': 'core_name'}, 'legacy': legacy, 'is_blue_verified': False}


def bookmark_payload(entities):
    tweet = {'rest_id': 't1', 'legacy': {'created_at': 'Mon Jan 01 00:00:00 +0000 2024',
        'full_text': 'synthetic post', 'lang': 'en', 'is_quote_status': False,
        'reply_count': 0, 'favorite_count': 0, 'favorited': False, 'retweet_count': 0,
        'entities': {}}, 'core': {'user_results': {'result': user_data(entities)}}}
    entries = [
        {'entryId': 'tweet-1', 'content': {'itemContent': {'tweet_results': {'result': tweet}}}},
        {'entryId': 'cursor-top', 'content': {'value': 'previous-cursor'}},
        {'entryId': 'cursor-bottom', 'content': {'value': 'next-cursor'}},
    ]
    return {'data': {'timeline': {'instructions': [{'entries': entries}]}}}


class BookmarkUserEntitiesTests(unittest.IsolatedAsyncioTestCase):
    async def test_get_bookmarks_description_without_urls_and_two_cursors(self):
        client = Client.__new__(Client)
        client.gql = type('GQL', (), {'bookmarks': AsyncMock(return_value=(bookmark_payload({'description': {}}), None))})()
        result = await client.get_bookmarks()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].user.description_urls, [])
        self.assertEqual(result[0].user.name, 'Core name')
        self.assertEqual(result[0].user.screen_name, 'core_name')
        self.assertEqual(result.next_cursor, 'next-cursor')
        self.assertEqual(result.previous_cursor, 'previous-cursor')

    def test_legacy_description_urls_are_preserved(self):
        urls = [{'url': 'https://example.test', 'expanded_url': 'https://example.test'}]
        user = User(None, user_data({'description': {'urls': urls}}))
        self.assertEqual(user.description_urls, urls)


if __name__ == '__main__':
    unittest.main()

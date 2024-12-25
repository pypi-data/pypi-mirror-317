import os
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from http.cookiejar import MozillaCookieJar
from unittest.mock import MagicMock, patch
import logging
from typing import List

from pararamio import Group
from pararamio.chat import Chat
from pararamio.client import Pararamio
from pararamio.deferred_post import DeferredPost
from pararamio.exceptions import (
    PararamioException,
    PararamioHTTPRequestException,
    PararamioValidationException,
)
from pararamio.post import Post
from pararamio.user import User
from pararamio.activity import ActivityAction
from pararamio.team import Team
from pararamio.bot import PararamioBot
from pararamio.poll import Poll
from tests.integrations._base import BasePararamioTest


RESOURCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../resources')
SKIP_AUTH_TESTS = bool(int(os.getenv('SKIP_AUTH_TESTS', '1')))


class PararamioClientTest(BasePararamioTest):
    def setUp(self):
        super().setUp()
        if int(os.environ.get('DEBUG', 0)):
            logging.basicConfig(level=logging.DEBUG)
        self.recipient_email = os.environ.get('PARARAMIO_RECIPIENT_EMAIL', '')
        self.recipient_chat_id = int(os.environ.get('PARARAMIO_RECIPIENT_CHAT_ID', 0))
        self.org_id = int(os.environ.get('PARARAMIO_ORG_ID', 0))
        self.bot = PararamioBot(os.environ.get('PARARAMIO_TEST_BOT_KEY', ''))
        if not self.recipient_email:
            self.skipTest('env variable PARARAMIO_RECIPIENT_EMAIL is not set')
        if not self.recipient_chat_id:
            self.skipTest('env variable PARARAMIO_RECIPIENT_CHAT_ID is not set')
        if not self.org_id:
            self.skipTest('env variable PARARAMIO_ORG_ID is not set')
        if not self.bot.key:
            self.skipTest('env variable PARARAMIO_TEST_BOT_KEY is not set')

    def test_001_login_without_cookie(self):
        if SKIP_AUTH_TESTS:
            self.skipTest('set env variable SKIP_AUTH_TESTS to 0 to run this test')
        client = Pararamio(**self.user1)
        self.assertIsNotNone(client.profile)

    def test_002_login_with_cookie(self):
        if SKIP_AUTH_TESTS:
            self.skipTest('set env variable SKIP_AUTH_TESTS to 0 to run this test')
        with tempfile.NamedTemporaryFile(suffix='.cookie') as tmp:
            MozillaCookieJar(tmp.name).save()
            client = Pararamio(**self.user1, cookie_path=tmp.name)
            self.assertIsNotNone(client.profile, 'Authentication failed')
            self.assertTrue(os.path.exists(tmp.name), 'Cookie path is not found')
            del client
            client = Pararamio(login='', password='', key='', cookie_path=tmp.name)
            self.assertIsNotNone(client.profile, 'Cookie authentication failed')

    def test_003_login_with_broken_cookie(self):
        if SKIP_AUTH_TESTS:
            self.skipTest('set env variable SKIP_AUTH_TESTS to 0 to run this test')
        with tempfile.NamedTemporaryFile(suffix='.cookie') as tmp:
            tmp.write('broken_cookie'.encode())
            client = Pararamio(**self.user1, cookie_path=tmp.name, ignore_broken_cookie=True)
            self.assertIsNotNone(client.profile, 'Authentication failed')
            self.assertTrue(os.path.exists(tmp.name), 'Cookie path is not found')

    def test_004_profile(self):
        self.assertEqual(self.client.profile.get('email'), self.user1['login'])

    def test_005_send_delete_file(self):
        d = {'size': 23050, 'type': 'image/png', 'filename': 'test.png'}
        post = None
        chat = Chat(self.client, self.recipient_chat_id)
        file = chat.upload_file(file=os.path.join(RESOURCES_PATH, 'test.png'))
        chat.load()
        post = Post(chat, post_no=chat.posts_count)
        self.assertEqual(post.file.guid, file.guid)
        self.assertEqual(post.file.filename, d['filename'])
        self.assertIsNotNone(file)
        file.download('test 1.png')
        file.delete()
        self.assertDictEqual(
            {'size': file.size, 'type': post.file._data['mime_type'], 'filename': file.filename}, d
        )

    def test_006_list_own_threads(self):
        chats = self.client.list_chats()
        self.assertIsNotNone(chats)
        chat = next(chats)
        chat_ = Chat(self.client, chat.id)
        chat_.load()
        self.assertTrue(chat == chat_)

    def test_007_list_posts(self):
        chat = Chat(self.client, self.recipient_chat_id)
        self.assertTrue(chat.posts(-10, -1))
        self.assertTrue(chat.posts(0, 1))
        chat.load()
        exception = False
        try:
            chat.posts(1, 0)
        except PararamioValidationException:
            exception = True
        self.assertTrue(exception, 'posts load with invalid start end position')
        exception = False
        try:
            chat.posts(-1, -10)
        except PararamioValidationException:
            exception = True
        self.assertTrue(exception, 'posts load with invalid start end position')

    def test_008_search_user(self):
        self.assertIsNotNone(self.client.search_user('tamtambottester2@gmail.com'))
        self.assertIsNotNone(self.client.search_user('tamtambottester2'))
        self.assertIsNotNone(self.client.search_user('tamtam_bot_tester2'))

    def test_009_reply_to_post(self):
        chat = Chat(self.client, self.recipient_chat_id)
        post = chat.post('test')
        reply = post.reply('ReplyTest')
        self.assertEqual(post.post_no, reply.reply_no)

    def test_010_search_group(self):
        self.assertIsNotNone(self.client.search_group('test'))

    def test_011_list_users(self):
        u = User(self.client, 58)
        u.load()

        self.assertTrue(u.unique_name)

    def test_012_chat_load(
        self,
    ):
        u = self.client.search_user(self.recipient_email)[0]
        chat = u.get_pm_thread()
        chat.load()
        pc = chat.posts_count
        u.post('text')
        chat.load()
        self.assertTrue(chat.posts_count == pc + 1)

    def test_013_read_status(self):
        u = self.client.search_user(self.recipient_email)[0]
        chat = u.get_pm_thread()
        chat.load()
        post = chat.post('test')
        chat.read_status(post.post_no + 1)
        self.assertTrue(chat.last_read_post_no == post.in_thread_no)

    def test_014_edit(self):
        u = self.client.search_user(self.recipient_email)[0]
        post = u.post('test')
        post.edit(text='TestTestStringString')
        chat = u.get_pm_thread()
        np = Post(chat, post.post_no)
        np.load()
        self.assertEqual('TestTestStringString', np.text)

    def test_015_send_and_delete_private_message(self):
        u = self.client.search_user(self.recipient_email)[0]
        post = u.post('test')
        self.assertIsNotNone(post)
        self.assertIsNotNone(post.delete())

    def test_016_send_and_delete_thread_message(self):
        chat = Chat(self.client, self.recipient_chat_id)
        post = chat.post('test')
        self.assertIsNotNone(post)
        self.assertIsNotNone(post.delete())

    def test_017_chat_methods(self):
        d = {
            'title': 'Test Create Chat',
            'users': [self.client.profile['id']],
            'pm': False,
            'member_ids': [self.client.profile['id']],
        }
        chat = Chat.create(self.client2, **d)
        self.assertTrue(
            Post(
                chat,
                post_no=1,
            )
            in chat
        )
        self.assertFalse(Post(Chat(self.client, id=100), post_no=1) in chat)
        self.assertTrue(
            chat.id in [ch.id for ch in self.client.list_chats()], 'Thread is not created'
        )
        chat.add_admins([self.client.profile['id']])
        chat.load()
        chat2 = Chat(self.client, chat.id).load()
        self.assertTrue(chat2.adm_flag, 'Admin is not set')
        time.sleep(5)
        chat.delete_admins([self.client.profile['id']])
        chat2.load()
        self.assertFalse(chat2.adm_flag, 'User is still admin')
        self.assertFalse(Chat(self.client, chat.id).pm)
        chat.delete()
        self.assertFalse(
            chat.id in [tr.id for tr in self.client.list_chats()], 'Thread is still exists'
        )

    def test_018_deferred_posts(self):
        time_sending = datetime.now(tz=timezone.utc) + timedelta(days=1)
        text = f'{time_sending.timestamp()}: test deferred posts !'
        result = DeferredPost.create(self.client, self.recipient_chat_id, text, time_sending)
        self.assertTrue(result)
        posts = DeferredPost.get_deferred_posts(self.client)
        post = [p for p in posts if p.text == text]
        self.assertTrue(bool(post), 'Post is empty')
        self.assertTrue(post[0].text == text, 'text is not match')
        self.assertTrue(int(post[0].time_sending.timestamp()) == int(time_sending.timestamp()))
        post[0].delete()

    def test_019_posts_tree(self):
        chat = Chat(self.client, self.recipient_chat_id, posts_count=100)
        with patch.object(
            Post,
            'rerere',
            return_value=[
                Post(chat, post_no=96, text='post no 96', reply_no=None),
                Post(chat, post_no=99, text='post no 99', reply_no=96),
                Post(chat, post_no=100, text='post no 100', reply_no=99, meta={}),
            ],
        ):
            with patch.object(
                chat,
                '_lazy_posts_loader',
                return_value=iter(
                    [
                        Post(chat, post_no=96, text='post no 96', reply_no=None),
                        Post(chat, post_no=97, text='post no 97', reply_no=None),
                        Post(chat, post_no=98, text='post no 98', reply_no=96),
                        Post(chat, post_no=99, text='post no 99', reply_no=96),
                    ]
                ),
            ):
                post = Post(chat, post_no=100, text='post no 100', reply_no=99, meta={})
                self.assertListEqual([96, 98, 99, 100], list(post.get_tree().keys()))
        many_fake_posts = [
            Post(chat, post_no=1, text='post no 1', reply_no=None),
            *[Post(chat, text=f'post no {i}', post_no=i, reply_no=i - 1) for i in range(2, 2000)],
            Post(chat, post_no=2000, text='post no 2000', reply_no=1999, meta={}),
        ]

        def _load_posts_side_effect(start, end):
            return iter(many_fake_posts[start:end])

        with patch.object(
            Post, 'rerere', return_value=[many_fake_posts[0], *many_fake_posts[1000:]]
        ):
            chat._load_posts = MagicMock(side_effect=_load_posts_side_effect)
            posts = list(many_fake_posts[-1].get_tree().keys())
            self.assertListEqual(
                [many_fake_posts[0].post_no, *[p.post_no for p in many_fake_posts[1000:]]], posts
            )

        with patch.object(Post, 'rerere', return_value=[]):
            chat._load_posts = MagicMock(side_effect=lambda a, b: [])
            self.assertListEqual([2000], list(many_fake_posts[-1].get_tree().keys()))

    def test_020_send_and_delete_message_by_email(self):
        text = 'test by mail'
        try:
            self.client.post_private_message_by_user_email(self.recipient_email + '1111', text)
            self.assertTrue(False, 'the message cannot be sent to a non-existent email')
        except PararamioException:
            pass
        post = self.client.post_private_message_by_user_email(self.recipient_email, text)
        self.assertIsNotNone(post)
        self.assertTrue(post.text == text)
        self.assertIsNotNone(post.delete())

    def test_021_send_and_delete_message_by_id(self):
        text = 'test by mail'
        try:
            self.client.post_private_message_by_user_email(-1, text)
            self.assertTrue(False, 'the message cannot be sent to a non-existent id')
        except PararamioException:
            pass
        post = self.client.post_private_message_by_user_id(self.client2.profile['id'], text)
        self.assertIsNotNone(post)
        self.assertTrue(post.text == text)
        self.assertIsNotNone(post.delete())

    def test_022_activity_loading(self):
        u1 = User(self.client, self.client.profile['id']).load()
        u2 = self.client.search_user(self.recipient_email)[0]
        post = u2.post('test')
        time.sleep(10)
        start = datetime.now(tz=timezone.utc).replace(tzinfo=timezone.utc) - timedelta(minutes=5)
        end = datetime.now(tz=timezone.utc).replace(tzinfo=timezone.utc)
        self.assertTrue(bool(u1.get_activity(start, end)), 'all activity list is empty')
        acts = u1.get_activity(start, end, [ActivityAction.POST])
        self.assertTrue(bool(acts), 'post activity list is empty')
        for act in acts:
            self.assertTrue(
                act.action == ActivityAction.POST, 'post activity list contains another action'
            )
        self.assertTrue(
            int(post.time_created.timestamp()) == int(acts[-1].time.timestamp()),
            'last post action time not match last post time',
        )

    def test_023_set_org_status(self):
        team = Team(self.client, self.org_id)
        team_member = team.member_info(self.client.profile['id'])
        new_status = f'Status test {datetime.now(tz=timezone.utc)}'
        self.assertTrue(team_member.add_status(new_status), 'add team status failed')
        self.assertTrue(team_member.get_last_status().status == new_status)

    def test_024_is_bot_meta(self):
        bot_post = self.bot.post_private_message_by_user_id(
            self.client.profile['id'], 'test message from bot'
        )
        chat = Chat(self.client, bot_post['chat_id'])
        post = chat.posts(bot_post['post_no'], bot_post['post_no'])[0]
        self.assertTrue(
            'is_bot' in post.meta.get('user', {}), 'meta.user.is_bot not found in received post'
        )
        self.assertTrue(
            post.meta.get('user', {}).get('is_bot') is True,
            'meta.user.is_bot is not True for post from bot',
        )

    def _poll_create(self, question: str, mode: str, anonymous: bool, options: List[str]) -> 'Poll':
        chat = Chat(self.client, self.recipient_chat_id)
        poll = Poll.create(chat, question=question, mode=mode, anonymous=anonymous, options=options)
        self.assertEqual(poll.question, question, 'poll question')
        self.assertEqual(poll.mode, mode, 'poll mode')
        self.assertEqual(poll.anonymous, anonymous, 'poll anonymous')
        self.assertEqual(poll.chat_id, self.recipient_chat_id, 'poll chat_id')
        self.assertListEqual([opt.text for opt in poll.options], options)
        return poll

    def test_025_single_poll(self):
        question = 'test anonymous single poll?'
        options = ['option 1', 'option 2', 'option 3']
        poll = self._poll_create(question, mode='one', anonymous=True, options=options)
        poll = poll.vote(0)
        self.assertEqual([opt.count for opt in poll.options], [1, 0, 0], 'poll vote')
        poll = poll.retract()
        self.assertTrue(all(opt.count == 0 for opt in poll.options), 'poll retract')
        exception = False
        try:
            poll.vote(4)
        except PararamioValidationException:
            exception = True
        self.assertTrue(exception, 'poll vote with incorrect option')
        exception = False
        try:
            poll.vote_multi([1, 2])
        except PararamioValidationException:
            exception = True
        self.assertTrue(exception, 'multi vote on single option poll')

    def test_026_multi_poll(self):
        question = 'test anonymous multi poll?'
        options = ['option 1', 'option 2', 'option 3']
        poll = self._poll_create(question, mode='more', anonymous=False, options=options)
        poll = poll.vote(1)
        self.assertEqual([opt.count for opt in poll.options], [0, 1, 0], 'poll vote')
        poll = poll.retract()
        self.assertTrue(all(opt.count == 0 for opt in poll.options), 'poll retract')
        poll = poll.vote_multi([1, 2])
        self.assertEqual([opt.count for opt in poll.options], [0, 1, 1], 'poll multi vote')
        exception = False
        try:
            poll.vote(4)
        except PararamioValidationException:
            exception = True
        self.assertTrue(exception, 'poll vote with incorrect option')
        exception = False
        try:
            poll.vote_multi([0, 4])
        except PararamioValidationException:
            exception = True
        self.assertTrue(exception, 'poll multi vote with incorrect option')

    def test_027_test_file(self):
        d = {'size': 23050, 'type': 'image/png', 'filename': 'test.png'}
        file_path = os.path.join(RESOURCES_PATH, 'test.png')
        chat = Chat(self.client, self.recipient_chat_id)
        file = chat.upload_file(file=file_path)
        file.delete()
        self.assertDictEqual(
            {'size': file.size, 'type': file.mime_type, 'filename': file.filename}, d
        )
        with self.assertRaises(PararamioValidationException):
            with open(file_path, 'rb') as f:
                chat.upload_file(file=f)
        with open(file_path, 'rb') as f:
            file2 = chat.upload_file(file=f, filename=d['filename'])
        file2.delete()
        self.assertDictEqual(
            {'size': file2.size, 'type': file2.mime_type, 'filename': file2.filename}, d
        )

    def test_028_test_mentions(self):
        u = self.client.search_user(self.recipient_email)[0]
        post = u.get_pm_thread().post('test @' + self.client2.profile.get('unique_name'))
        ## TODO: Uncomment this when the bug is fixed
        # self.assertTrue(post.is_mention)
        # self.assertTrue(post.mentions[0]['name'] == 'tamtambottester2')
        # self.assertTrue(post.mentions[0]['id'] == self.client.search_user('tamtambottester2')[0].id)
        # self.assertTrue(post.mentions[0]['value'] == '@tamtambottester2')

    def test_029_test_group_operations(self):
        grp = Group.create(self.client, organization_id=self.org_id, name='test_group')
        grp.delete()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('test.cookie'):
            os.remove('test.cookie')
        if os.path.exists('test.cookie2'):
            os.remove('test.cookie2')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(PararamioClientTest)


if __name__ == '__main__':
    unittest.main()

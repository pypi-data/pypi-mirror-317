from collections import OrderedDict
from typing import Any, cast, Dict, Iterable, List, Optional, Set, Tuple, TYPE_CHECKING
from uuid import uuid4
from pararamio._base import BaseLoadedAttrPararamObject
from pararamio.exceptions import (
    PararamioRequestException,
    PararamNoNextPost,
    PararamNoPrevPost,
)
from pararamio.file import File
from pararamio.utils.helpers import (
    encode_digit,
    parse_iso_datetime,
    rand_id,
)

if TYPE_CHECKING:
    from pararamio.chat import Chat
    from pararamio.client import Pararamio
    from pararamio._types import PostMention, FormatterT, PostMetaT, TextParsedT
    from datetime import datetime

__all__ = ('Post',)


def get_post_mention(data: 'TextParsedT') -> Optional['PostMention']:
    id, name, value = (
        data.get('id', None),
        data.get('name', None),
        data.get('value', None),
    )
    if id is None and name is None and value is None:
        return None
    return cast('PostMention', {'id': id, 'name': name, 'value': value})


class Post(BaseLoadedAttrPararamObject):
    _data: Dict[str, Any]
    _chat: 'Chat'
    chat_id: int
    event: Optional[Dict[str, Any]]
    id: Optional[int]
    is_deleted: bool
    meta: 'PostMetaT'
    post_no: int
    reply_no: Optional[int]
    text: str
    text_parsed: List['TextParsedT']
    time_created: 'datetime'
    time_edited: Optional['datetime']
    user_id: int
    uuid: Optional[str]
    ver: Optional[int]

    _attr_formatters: 'FormatterT' = {
        'post_no': lambda data, key: int(data[key]),
        'time_edited': parse_iso_datetime,
        'time_created': parse_iso_datetime,
    }

    def __init__(
        self,
        chat: 'Chat',
        post_no: int,
        load_on_key_error: bool = True,
        **kwargs: Any,
    ) -> None:
        self._chat = chat
        if post_no is None:
            post_no = kwargs['in_thread_no']
        self.post_no = post_no
        self._data = {**kwargs, 'post_no': post_no}
        self._load_on_key_error = load_on_key_error

    def __repr__(self) -> str:
        return (
            f'<Post(client={hex(id(self.client))}, '
            f'chat_id={self.chat_id}, post_no={self.post_no}) {hex(id(self))}>'
        )

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other) -> bool:
        if not isinstance(other, Post):
            return id(other) == id(self)
        return self._chat == other._chat and self.post_no == other.post_no

    def _compare_validations(self, other: 'Post') -> None:
        if not isinstance(other, Post):
            raise ValueError(f'can not compare post and {other.__class__.__name__}')
        if self._chat != other._chat:
            raise ValueError('can not compare posts from different chats')

    def __ge__(self, other: 'Post') -> bool:
        self._compare_validations(other)
        # noinspection PyUnresolvedReferences
        return self.post_no >= other.post_no  # type: ignore[operator]

    def __gt__(self, other: 'Post') -> bool:
        self._compare_validations(other)
        # noinspection PyUnresolvedReferences
        return self.post_no > other.post_no  # type: ignore[operator]

    def __lt__(self, other: 'Post') -> bool:
        self._compare_validations(other)
        # noinspection PyUnresolvedReferences
        return self.post_no < other.post_no  # type: ignore[operator]

    def __le__(self, other: 'Post') -> bool:
        self._compare_validations(other)
        # noinspection PyUnresolvedReferences
        return self.post_no <= other.post_no  # type: ignore[operator]

    @property
    def in_thread_no(self) -> int:
        return self.post_no

    @property
    def file(self) -> Optional[File]:
        _file = self.meta.get('file', None)
        if not _file:
            return None
        return File(self._chat._client, **_file)

    @property
    def is_reply(self) -> bool:
        return self.reply_no is not None

    @property
    def chat(self) -> 'Chat':
        return self._chat

    @property
    def client(self) -> 'Pararamio':
        return self._chat.client

    @property
    def is_bot(self) -> bool:
        is_bot = self.meta.get('user', {}).get('is_bot', False)
        if is_bot is None:
            raise PararamioRequestException('failed to load data for post')
        return is_bot

    @property
    def is_file(self) -> bool:
        return 'file' in self.meta

    @property
    def is_event(self) -> bool:
        """
        Returns whether there is an event.
        """
        return bool(self.event)

    @property
    def mentions(self) -> List['PostMention']:
        text_parsed = self.text_parsed
        if text_parsed is None:
            return []
        mentions_: List['PostMention'] = []
        for item in text_parsed:
            if item.get('type', '') == 'mention':
                mention = get_post_mention(item)
                if not mention:
                    continue
                mentions_.append(mention)
        return mentions_

    @property
    def user_links(self) -> List['PostMention']:
        if not self.text_parsed:
            return []
        links: List['PostMention'] = []
        for item in self.text_parsed:
            if item.get('type', '') == 'user_link':
                mention = get_post_mention(item)
                if not mention:
                    continue
                links.append(mention)
        return links

    @property
    def is_mention(self) -> bool:
        if not self.text_parsed:
            return False
        for item in self.text_parsed:
            if item.get('type', '') == 'mention' and item.get(
                'id', None
            ) == self.client.profile.get('id', -1):
                return True
        return False

    def load(self) -> 'Post':
        url = f'/msg/post?ids={encode_digit(self.chat.id)}-{encode_digit(self.post_no)}'
        res = self.client.api_get(url).get('posts', [])
        if len(res) != 1:
            raise PararamioRequestException(
                f'failed to load data for post_no {self.post_no} in chat {self._chat.id}'
            )
        self._data = res[0]
        return self

    @property
    def replies(self) -> List[int]:
        url = f'/msg/post/{self._chat.id}/{self.post_no}/replies'
        return self.client.api_get(url).get('data', [])

    def reply(self, text: str, quote: Optional[str] = None) -> 'Post':
        _url = f'/amsg/post/{self._chat.id}'
        res = self.client.api_post(
            _url,
            {'uuid': rand_id(), 'text': text, 'quote': quote, 'reply_no': self.post_no},
        )
        return Post(self._chat, res['post_no'], load_on_key_error=self._load_on_key_error).load()

    def rerere(self) -> Iterable['Post']:
        url = f'/msg/post/{self._chat.id}/{self.post_no}/rerere'
        res = self.client.api_get(url)

        def make_post_from_re(post_no):
            return Post(self._chat, post_no, load_on_key_error=self._load_on_key_error).load()

        return map(make_post_from_re, res['data'])

    def get_tree(self, load_limit: int = 1000) -> 'OrderedDict[int, Post]':
        posts = {self.post_no: self}
        for post in self.rerere():
            posts[post.post_no] = post
        first = posts[min(posts.keys())]
        tree = OrderedDict(sorted(posts.items()))  # type: ignore
        load_start = first.post_no + 1
        if self.post_no - first.post_no > load_limit:
            load_start = self.post_no - load_limit
        for post in self.chat._lazy_posts_loader(*sorted([load_start, self.post_no - 1])):
            posts[post.post_no] = post

        for post in sorted(posts.values()):
            if post.reply_no is None or post.reply_no not in tree:
                continue
            tree[post.post_no] = post
        return OrderedDict(sorted(tree.items()))  # type: ignore

    def get_reply_to_post(self) -> Optional['Post']:
        reply_no = self.reply_no
        if reply_no is not None:
            return Post(self._chat, reply_no, load_on_key_error=self._load_on_key_error).load()
        return None

    def next(self, skip_event: bool = True) -> 'Post':
        """
        get next post or throw PararamNoNextPost

        :param bool skip_event: Skip message if this is an event
        """
        _next = self.post_no + 1
        if _next > self._chat.posts_count:
            raise PararamNoNextPost()
        post = Post(self._chat, _next)
        if skip_event and post.is_event:
            return post.next()
        return post

    def prev(self, skip_event: bool = True) -> 'Post':
        """
        get previous post or throw PararamNoPrevPost

        :param bool skip_event: Skip message if this is an event
        """
        _prev = self.post_no - 1
        if _prev <= 0:
            raise PararamNoPrevPost()
        post = Post(self._chat, _prev)
        if skip_event and post.is_event:
            return post.prev()
        return post

    def who_read(self) -> List[int]:
        url = f'/activity/who-read?thread_id={self._chat.id}&post_no={self.post_no}'
        return self.client.api_get(url).get('users', [])

    def mark_read(self) -> bool:
        return self.chat.read_status(self.post_no)

    def edit(self, text: str, quote: Optional[str] = None, reply_no: Optional[int] = None) -> bool:
        """

        Updates the content of a post with new text, optional quote, and optional reply number.

        Parameters:
            text (str): The new text content for the post.
            quote (Optional[str]): An optional quote to include in the post.
            reply_no (Optional[int]): An optional reply number for the post.

        Returns:
            bool: True if the post was successfully updated, False otherwise.
        """
        url = f'/amsg/post/{self._chat.id}/{self.post_no}'

        res = self.client.api_put(
            url,
            {
                'uuid': self._data.get('uuid', rand_id()),
                'text': text,
                'quote': quote,
                'reply_no': reply_no,
            },
        )
        if res.get('ver'):
            self.load()
            return True
        return False

    def delete(self) -> bool:
        url = f'/amsg/post/{self._chat.id}/{self.post_no}'
        res = self.client.api_delete(url)
        if res.get('ver'):
            self.load()
            return True
        return False

    def _find_attachment(
        self,
        attachments: Set[str],
        start: int,
        end: int,
    ) -> Tuple[List[File], Set[str]]:
        results = []
        found = set()
        for post in self.chat._lazy_posts_loader(start, end):
            if post.uuid in attachments:
                found.add(post.uuid)
            file = post.file
            if file is not None:
                results.append(file)
        return results, found

    def load_attachments(self, max_deep: int = 100, raise_if_not_found: bool = True) -> List[File]:
        attachments = self.meta.get('attachments', [])
        if not attachments:
            return []
        attachments_ = set(attachments)
        start, end = self.post_no - len(attachments), self.post_no
        results, found = self._find_attachment(attachments_, start, end)
        if len(found) == len(attachments_):
            return results
        results_fb, found_fb = self._find_attachment(attachments_, end - 1 - max_deep, end - 1)
        results.extend(results_fb)
        if not raise_if_not_found or len(found_fb) + len(found) == len(attachments_):
            return results
        raise PararamioRequestException('can not find all attachments')

    @property
    def attachments(self) -> List[File]:
        return self.load_attachments()

    @classmethod
    def create(
        cls,
        chat: 'Chat',
        text: str,
        reply_no: Optional[int] = None,
        quote: Optional[str] = None,
        uuid: Optional[str] = None,
        attachments: Optional[List[str]] = None,
    ) -> 'Post':
        url = f'/amsg/post/{chat.id}'
        data: Dict[str, Any] = {
            'uuid': uuid or str(uuid4().hex),
            'text': text,
            'quote': quote,
            'reply_no': reply_no,
        }
        if attachments:
            data['attachments'] = attachments
        res = chat._client.api_post(url, data)
        if not res:
            raise PararamioRequestException('Failed to create post')
        return cls(chat, post_no=res['post_no']).load()

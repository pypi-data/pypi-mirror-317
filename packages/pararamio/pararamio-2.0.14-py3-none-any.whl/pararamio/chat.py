from datetime import datetime
from io import BytesIO
from os import PathLike
from typing import Any, BinaryIO, cast, Dict, Iterable, List, Optional, Tuple, TYPE_CHECKING, Union
from urllib.parse import quote_plus
from pararamio.attachment import Attachment
from pararamio.constants import POSTS_LIMIT
from pararamio.exceptions import (
    PararamioLimitExceededException,
    PararamioMethodNotAllowed,
    PararamioRequestException,
    PararamioValidationException,
)
from pararamio.post import Post
from pararamio.utils.helpers import (
    encode_chats_ids,
    format_datetime,
    join_ids,
    parse_iso_datetime,
)
from ._base import BaseClientObject, BaseLoadedAttrPararamObject

if TYPE_CHECKING:
    from pararamio.client import Pararamio
    from pararamio.file import File
    from pararamio._types import (
        FormatterT,
        QuoteRangeT,
    )

__all__ = ('Chat',)

ATTR_FORMATTERS: 'FormatterT' = {
    'time_edited': parse_iso_datetime,
    'time_updated': parse_iso_datetime,
    'time_created': parse_iso_datetime,
    'user_time_edited': parse_iso_datetime,
}


def check_result(result: dict) -> bool:
    return 'chat_id' in result


def validate_post_load_range(start_post_no: int, end_post_no: int) -> None:
    if (start_post_no < 0 <= end_post_no) or (start_post_no >= 0 > end_post_no):
        raise PararamioValidationException(
            'start_post_no and end_post_no can only be negative or positive at the same time'
        )
    if 0 > start_post_no > end_post_no:
        raise PararamioValidationException('range start_post_no must be greater then end_post_no')
    if 0 <= start_post_no > end_post_no:
        raise PararamioValidationException('range start_post_no must be smaller then end_post_no')


class Chat(BaseLoadedAttrPararamObject, BaseClientObject):
    id: int
    title: str
    history_mode: str
    description: Optional[str]
    posts_count: int
    pm: bool
    e2e: bool
    time_created: datetime
    time_updated: datetime
    time_edited: Optional[datetime]
    author_id: int
    two_step_required: bool
    org_visible: bool
    organization_id: Optional[int]
    posts_live_time: Optional[int]
    allow_api: bool
    read_only: bool
    tnew: bool
    adm_flag: bool
    custom_title: Optional[str]
    is_favorite: bool
    inviter_id: Optional[int]
    tshow: bool
    user_time_edited: datetime
    history_start: int
    pinned: List[int]
    thread_groups: List[int]
    thread_users: List[int]
    thread_admins: List[int]
    thread_users_all: List[int]
    last_msg_author_id: Optional[int]
    last_msg_author: str
    last_msg_bot_name: str
    last_msg_text: str
    last_msg: str
    last_read_post_no: int
    thread_guests: List[int]
    _data: Dict[str, Any]
    _attr_formatters = ATTR_FORMATTERS

    def __init__(
        self,
        client: 'Pararamio',
        id: Optional[int] = None,
        load_on_key_error: bool = True,
        **kwargs: Any,
    ) -> None:
        if id is None:
            id = kwargs.get('chat_id', None)
            if id is None:
                id = kwargs['thread_id']
        self.id = int(id)
        self._data = {}
        if kwargs:
            self._data = {**kwargs, 'id': id}
        self._load_on_key_error = load_on_key_error
        self._client = client

    def __str__(self) -> str:
        title = self._data.get('title', '')
        id_ = self.id or ''
        return f'{id_} - {title}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chat):
            return id(other) == id(self)
        return self.id == other.id

    def __contains__(self, item: 'Post') -> bool:
        if isinstance(item, Post):
            return item.chat == self
        return False

    def load(self) -> 'Chat':
        if self.id is None:
            raise PararamioMethodNotAllowed(f'Load is not allow for new {self.__class__.__name__}')
        chats = self.load_chats(self._client, [self.id])
        if len(chats) != 1:
            raise PararamioRequestException(f'failed to load data for chat id {self.id}')
        self._data = chats[0]._data
        return self

    def edit(self, **kwargs) -> None:
        """
        Updates the attributes of a chat instance with the provided keyword arguments.

        Parameters:
          kwargs: Arbitrary keyword arguments specifying the attributes to update.

        Returns:
          None

        Raises:
          Various exceptions based on the response from the API PUT request.
        """
        url = f'/core/chat/{self.id}'
        check_result(self._client.api_put(url, data=kwargs))

    def transfer(self, org_id: int) -> bool:
        url = f'/core/chat/{self.id}/transfer/{org_id}'
        return check_result(self._client.api_post(url, {}))

    def delete(self):
        url = f'/core/chat/{self.id}'
        return check_result(self._client.api_delete(url))

    def hide(self) -> bool:
        url = f'/core/chat/{self.id}/hide'
        return check_result(self._client.api_post(url))

    def show(self) -> bool:
        url = f'/core/chat/{self.id}/show'
        return check_result(self._client.api_post(url))

    def favorite(self) -> bool:
        url = f'/core/chat/{self.id}/favorite'
        return check_result(self._client.api_post(url))

    def unfavorite(self) -> bool:
        url = f'/core/chat/{self.id}/unfavorite'
        return check_result(self._client.api_post(url))

    def enter(self) -> bool:
        url = f'/core/chat/{self.id}/enter'
        return check_result(self._client.api_post(url))

    def quit(self) -> bool:
        url = f'/core/chat/{self.id}/quit'
        return check_result(self._client.api_post(url))

    def set_custom_title(self, title: str) -> bool:
        url = f'/core/chat/{self.id}/custom_title'
        return check_result(self._client.api_post(url, {'title': title}))

    def add_users(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/user/{join_ids(ids)}'
        return check_result(self._client.api_post(url))

    def delete_users(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/user/{join_ids(ids)}'
        return check_result(self._client.api_delete(url))

    def add_admins(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/admin/{join_ids(ids)}'
        return check_result(self._client.api_post(url))

    def delete_admins(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/admin/{join_ids(ids)}'
        return check_result(self._client.api_delete(url))

    def add_groups(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/group/{join_ids(ids)}'
        return check_result(self._client.api_post(url))

    def delete_groups(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/group/{join_ids(ids)}'
        return check_result(self._client.api_delete(url))

    def _load_posts(
        self,
        start_post_no: int = -50,
        end_post_no: int = -1,
        limit: int = POSTS_LIMIT,
    ) -> List['Post']:
        url = f'/msg/post?chat_id={self.id}&range={start_post_no}x{end_post_no}'
        validate_post_load_range(start_post_no, end_post_no)
        _absolute = abs(end_post_no - start_post_no)
        if start_post_no < 0:
            _absolute = +1
        if _absolute >= limit:
            raise PararamioLimitExceededException(f'max post load limit is {limit - 1}')
        res = self._client.api_get(url).get('posts', [])
        if not res:
            return []
        return [Post(chat=self, **post) for post in res]

    def _lazy_posts_loader(
        self, start_post_no: int = -50, end_post_no: int = -1, limit: int = POSTS_LIMIT
    ) -> Iterable['Post']:
        validate_post_load_range(start_post_no, end_post_no)
        absolute = abs(end_post_no - start_post_no)
        start, end = start_post_no, end_post_no
        if absolute > limit:
            end = start_post_no + limit - 1
        posts = iter(self._load_posts(start, end))
        counter = 0
        for _ in range(start_post_no, end_post_no):
            try:
                yield next(posts)
            except StopIteration:
                counter += 1
                res = self._load_posts(start + limit * counter, end + limit * counter)
                if not res:
                    return
                posts = iter(res)

    def posts(self, start_post_no: int = -50, end_post_no: int = -1) -> List['Post']:
        return self._load_posts(start_post_no=start_post_no, end_post_no=end_post_no)

    def read_status(self, post_no: int) -> bool:
        return self.mark_read(post_no)

    def mark_read(self, post_no: Optional[int] = None) -> bool:
        url = f'/msg/lastread/{self.id}'
        data: Dict[str, Union[int, bool]] = {'read_all': True}
        if post_no is not None:
            data = {'post_no': post_no}
        res = self._client.api_post(url, data)
        if 'post_no' in res:
            self._data['last_read_post_no'] = res['post_no']
        if 'posts_count' in res:
            self._data['posts_count'] = res['posts_count']
        return True

    def post(
        self,
        text: str,
        quote_range: Optional['QuoteRangeT'] = None,
        reply_no: Optional[int] = None,
        attachments: Optional[List['Attachment']] = None,
    ) -> 'Post':
        if self.id is None:
            raise ValueError('can not post file to new chat')
        _attachments = []
        for attachment in attachments or []:
            _attachments.append(
                self.upload_file(
                    attachment.fp,
                    filename=attachment.guess_filename,
                    content_type=attachment.guess_content_type,
                    reply_no=reply_no,
                )
            )
        return Post.create(
            self,
            text=text,
            reply_no=reply_no,
            quote=cast(str, quote_range['text']) if quote_range else None,
            attachments=[attach.guid for attach in _attachments],
        )

    def upload_file(
        self,
        file: Union[str, BytesIO, BinaryIO, PathLike],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        reply_no: Optional[int] = None,
        quote_range: Optional[str] = None,
    ) -> 'File':
        if self.id is None:
            raise ValueError('can not upload file to new chat')
        if not isinstance(file, (str, PathLike)) and not filename:
            raise PararamioValidationException('can not determine filename for BinaryIO')
        attachment = Attachment(file, filename=filename, content_type=content_type)
        return self._client.upload_file(
            file=attachment.fp,
            chat_id=self.id,
            filename=attachment.guess_filename,
            content_type=attachment.guess_content_type,
            reply_no=reply_no,
            quote_range=quote_range,
        )

    @classmethod
    def load_chats(cls, client: 'Pararamio', ids: List[int]) -> List['Chat']:
        url = f'/core/chat?ids={join_ids(ids)}'
        res = client.api_get(url)
        if res and 'chats' in res:
            return [cls(client, **data) for data in client.api_get(url).get('chats', [])]
        raise PararamioRequestException(
            f'failed to load data for chats ids: {",".join(map(str, ids))}'
        )

    @classmethod
    def post_search(
        cls,
        client: 'Pararamio',
        q: str,
        order_type: str = 'time',
        page: int = 1,
        chat_id: Optional[int] = None,
        limit: Optional[int] = POSTS_LIMIT,
    ) -> Tuple[int, Iterable['Post']]:
        if not limit:
            limit = POSTS_LIMIT
        url = f'/posts/search?q={quote_plus(q)}&order_type={order_type}&page={page}&limit={limit}'
        if chat_id is not None:
            url += f'&th_id={chat_id}'

        res = client.api_get(url)
        if 'posts' not in res:
            raise PararamioRequestException('failed to perform search')
        created_chats = {}

        def create_post(data):
            nonlocal created_chats
            _chat_id = data['thread_id']
            post_no = data['post_no']
            if _chat_id not in created_chats:
                created_chats[_chat_id] = cls(client, id=_chat_id)
            return Post(created_chats[_chat_id], post_no=post_no)

        return res['count'], map(create_post, res['posts'])

    @classmethod
    def create(
        cls,
        client: 'Pararamio',
        title: str,
        description: str = '',
        users: Optional[List[int]] = None,
        groups: Optional[List[int]] = None,
        **kwargs,
    ) -> 'Chat':
        """

        Creates a new chat instance in the Pararamio application.

        Args:
            cls: The class itself (implicit first argument for class methods).
            client (Pararamio): An instance of the Pararamio client.
            title (str): The title of the chat.
            description (str, optional): A description of the chat. Default is an empty string.
            users (Optional[List[int]], optional): A list of user IDs to be added to the chat.
                                                   Default is None.
            groups (Optional[List[int]], optional): A list of group IDs to be added to the chat.
                                                    Default is None.
            **kwargs: Additional keyword arguments to be included in the chat creation data.

        Returns:
            Chat: An instance of the Chat class representing the newly created chat.
        """
        if users is None:
            users = []
        if groups is None:
            groups = []
        data = {
            'title': title,
            'description': description,
            'users': users,
            'groups': groups,
            **kwargs,
        }

        res = client.api_post('/core/chat', data)
        id_: int = res['chat_id']
        return cls(client, id_)

    @classmethod
    def create_private_chat(cls, client: 'Pararamio', user_id: int) -> 'Chat':
        url = f'/core/chat/pm/{user_id}'
        res = client.api_post(url)
        id_: int = res['chat_id']
        return cls(client, id=id_)

    @staticmethod
    def sync_chats(
        client: 'Pararamio',
        chats_ids: List[Tuple[int, int, int]],
        sync_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        url = '/core/chat/sync'
        data = {'ids': encode_chats_ids(chats_ids)}
        if sync_time:
            data['sync_time'] = format_datetime(sync_time)
        return client.api_post(url)

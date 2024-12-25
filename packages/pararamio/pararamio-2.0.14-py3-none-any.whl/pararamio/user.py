from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, TypedDict
from pararamio.activity import Activity, ActivityAction

from pararamio.exceptions import PararamNotFound
from pararamio.utils.helpers import unescape_dict

from .chat import Chat
from ._base import BaseLoadedAttrPararamObject, BaseClientObject

if TYPE_CHECKING:
    from ._types import QuoteRangeT
    from pararamio.client import Pararamio
    from pararamio.post import Post
    from datetime import datetime

__all__ = ('User', 'UserSearchResult', 'UserInfoParsedItem')


@dataclass
class UserSearchResult:
    id: int
    avatar: Optional[str]
    name: str
    unique_name: str
    custom_name: Optional[str]
    time_created: str
    time_updated: str
    other_blocked: bool
    pm_thread_id: Optional[int]
    is_bot: bool
    user: 'User'

    @property
    def has_pm(self) -> bool:
        return self.pm_thread_id is not None

    def get_pm_thread(self) -> 'Chat':
        if self.pm_thread_id is not None:
            chat = Chat(self.user._client, self.pm_thread_id)
            return chat
        return Chat.create_private_chat(self.user._client, self.id)

    def post(
        self,
        text: str,
        quote_range: Optional['QuoteRangeT'] = None,
        reply_no: Optional[int] = None,
    ) -> 'Post':
        chat = self.get_pm_thread()
        return chat.post(text=text, quote_range=quote_range, reply_no=reply_no)


class UserInfoParsedItem(TypedDict):
    type: str
    value: str


INTERSECTION_KEYS = (
    'id',
    'name',
    'unique_name',
    'time_created',
    'time_updated',
    'is_bot',
)


class User(BaseLoadedAttrPararamObject, BaseClientObject):
    id: int
    name: str
    name_trans: str
    info: str
    unique_name: str
    deleted: bool
    active: bool
    time_updated: str
    time_created: str
    is_bot: bool
    alias: Optional[None]
    timezone_offset_minutes: int
    owner_id: Optional[None]
    organizations: List[int]
    info_parsed: List[UserInfoParsedItem]
    _data: Dict[str, Any]

    def __init__(self, client, id: int, load_on_key_error: bool = True, **kwargs):
        self._client = client
        self.id = id
        self._data = {'id': id, **kwargs}
        self._load_on_key_error = load_on_key_error

    def __eq__(self, other):
        if not isinstance(other, User):
            return id(other) == id(self)
        return self.id == other.id

    def load(self) -> 'User':
        resp = self._client.get_users_by_ids([self.id])
        if len(resp) != 1:
            raise PararamNotFound()
        self._data = next(iter(resp))._data
        return self

    @classmethod
    def load_users(cls, client, ids: List[int]) -> List['User']:
        return client.get_users_by_ids(ids)

    def post(
        self,
        text: str,
        quote_range: Optional['QuoteRangeT'] = None,
        reply_no: Optional[int] = None,
    ) -> 'Post':
        for res in self.search(self._client, self.unique_name):
            if res.unique_name == self.unique_name:
                return res.post(text=text, quote_range=quote_range, reply_no=reply_no)
        raise PararamNotFound(f'User {self.unique_name} not found')

    def __str__(self):
        if 'name' not in self._data:
            self.load()
        return self._data.get('name')

    @classmethod
    def search(cls, client: 'Pararamio', search_string: str) -> List[UserSearchResult]:
        url = f'/users?flt={search_string}'
        result: List[UserSearchResult] = []
        for response in client.api_get(url).get('users', []):
            data = unescape_dict(response, keys=['name'])
            data['user'] = cls(client, **{k: data[k] for k in INTERSECTION_KEYS})
            result.append(UserSearchResult(**data))
        return result

    def _activity_page_loader(self) -> Callable[..., Dict[str, Any]]:
        def loader(action: Optional[ActivityAction] = None, page: int = 1) -> Dict[str, Any]:
            action_ = action.value if action else ''
            url = f'/activity?user_id={self.id}&action={action_}&page={page}'
            return self._client.api_get(url)

        return loader

    def get_activity(
        self,
        start: 'datetime',
        end: 'datetime',
        actions: Optional[List[ActivityAction]] = None,
    ) -> List[Activity]:
        """get user activity

        :param start: start time
        :param end: end time
        :param actions: list of action types (all actions if None)
        :returns: activity list
        """
        return Activity.get_activity(self._activity_page_loader(), start, end, actions)

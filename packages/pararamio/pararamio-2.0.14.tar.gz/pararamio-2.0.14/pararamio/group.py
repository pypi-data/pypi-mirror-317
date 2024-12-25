from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pararamio.exceptions import PararamNotFound
from pararamio.utils import parse_iso_datetime
from ._base import BaseLoadedAttrPararamObject, BaseClientObject

if TYPE_CHECKING:
    from pararamio.client import Pararamio
    from pararamio._types import FormatterT

__all__ = ('Group',)

ATTR_FORMATTERS: 'FormatterT' = {
    'post_no': lambda data, key: int(data[key]),
    'time_edited': parse_iso_datetime,
    'time_created': parse_iso_datetime,
}
EDITABLE_FIELDS = ('unique_name', 'name', 'description', 'email_domain')


class Group(BaseLoadedAttrPararamObject, BaseClientObject):
    id: int
    unique_name: str
    name: str
    description: str
    email_domain: str
    organization_id: int
    time_updated: datetime
    time_created: datetime
    threads: List[int]
    users: List[int]
    admins: List[int]
    adm_flag: bool
    _data: Dict[str, Any]

    def __init__(
        self,
        client: 'Pararamio',
        id: int,
        load_on_key_error: bool = True,
        **kwargs: Any,
    ):
        self.id = id
        self._data = {}
        if kwargs:
            self._data = {'id': id, **kwargs}
        self._client = client
        self._load_on_key_error = load_on_key_error

    def __str__(self) -> str:
        name = self.name or 'New'
        id_ = self.id or ''
        return f'[{id_}] {name}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Group):
            return id(other) == id(self)
        return self.id == other.id

    @classmethod
    def create(
        cls,
        client: 'Pararamio',
        organization_id: int,
        name: str,
        description: Optional[str] = None,
    ) -> 'Group':
        resp = client.api_post(
            '/core/group',
            data={
                'organization_id': organization_id,
                'name': name,
                'description': description or '',
            },
        )
        return cls(client, id=resp['group_id'])

    def edit(self, changes: Dict[str, Optional[str]], reload: bool = True) -> None:
        if any(key not in self._data for key in EDITABLE_FIELDS):
            self.load()
        data = {k: changes.get(k, self._data[k]) for k in EDITABLE_FIELDS}
        self._client.api_put(f'/core/group/{self.id}', data=data)
        self._data.update(data)
        if reload:
            self.load()

    def delete(self) -> None:
        self._client.api_delete(f'/core/group/{self.id}')

    def remove_member(self, user_id: int, reload: bool = True) -> None:
        url = f'/core/group/{self.id}/users/{user_id}'
        self._client.api_delete(url)
        self._data['users'] = [user for user in self.users if user != user_id]
        self._data['admins'] = [admin for admin in self.admins if admin != user_id]
        if reload:
            self.load()

    def add_member(self, user_id: int, reload: bool = True) -> None:
        url = f'/core/group/{self.id}/users/{user_id}'
        self._client.api_post(url)
        self._data['users'].append(user_id)
        if reload:
            self.load()

    def add_admins(self, user_id: int, reload: bool = True) -> None:
        url = f'/core/group/{self.id}/admins/{user_id}'
        self._client.api_post(url)
        if user_id not in self._data['users']:
            self._data['users'].append(user_id)
        self._data['admins'].append(user_id)
        if reload:
            self.load()

    def load(self) -> 'Group':
        resp = self._client.get_groups_by_ids([self.id])
        if not resp:
            raise PararamNotFound(f'failed to load group {self.id}')
        self._data = next(iter(resp))._data
        return self

    @classmethod
    def search(cls, client: 'Pararamio', search_string: str) -> List['Group']:
        url = f'/users?flt={search_string}'
        return [cls(client, **group) for group in client.api_get(url).get('groups', [])]

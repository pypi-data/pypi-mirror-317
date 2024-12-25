import logging
import os
from http.cookiejar import CookieJar, FileCookieJar, LoadError, MozillaCookieJar
from io import BytesIO
from typing import (
    Any,
    BinaryIO,
    Callable,
    cast,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

from pararamio._types import ProfileTypeT, SecondStepFnT
from pararamio.chat import Chat
from pararamio.constants import XSRF_HEADER_NAME
from pararamio.exceptions import (
    PararamioAuthenticationException,
    PararamioHTTPRequestException,
    PararamioValidationException,
)
from pararamio.file import File
from pararamio.group import Group
from pararamio.post import Post
from pararamio.user import User, UserSearchResult
from pararamio.utils.authentication import (
    authenticate,
    do_second_step,
    do_second_step_with_code,
    get_xsrf_token,
)
from pararamio.utils.helpers import (
    check_login_opts,
    get_empty_vars,
    lazy_loader,
    unescape_dict,
)
from pararamio.utils.requests import (
    api_request,
    delete_file,
    download_file,
    xupload_file,
)

__all__ = ('Pararamio',)
log = logging.getLogger('pararamio.client')


class Pararamio:
    """Pararamio client class.

    This class provides a client interface for interacting with the Pararamio API.

    Parameters:
        login: Optional string for the login name.
        password: Optional string for the password.
        key: Optional string for an authentication key.
        cookie: Optional CookieJar object for handling cookies.
        cookie_path: Optional string specifying the path to the cookie file.
        ignore_broken_cookie: Boolean flag to ignore broken cookie errors if set to True.
    """

    _login: Optional[str]
    _password: Optional[str]
    _key: Optional[str]
    _authenticated: bool
    _cookie: Union[CookieJar, FileCookieJar]
    __profile: Optional[ProfileTypeT]
    __headers: Dict[str, str]
    __user: dict

    def __init__(
        self,
        login: Optional[str] = None,
        password: Optional[str] = None,
        key: Optional[str] = None,
        cookie: Optional[CookieJar] = None,
        cookie_path: Optional[str] = None,
        ignore_broken_cookie: bool = False,
    ):
        self._login = login
        self._password = password
        self._key = key
        self.__headers = {}
        self.__profile = None
        self._authenticated = False
        if cookie is not None:
            self._cookie = cookie
        elif cookie_path is not None:
            self._cookie = MozillaCookieJar(cookie_path)
            if os.path.exists(cookie_path):
                if not os.path.isfile(cookie_path):
                    raise OSError(f'path {cookie_path} is directory')
                if not os.access(cookie_path, os.R_OK):
                    raise OSError(f'file {cookie_path} is not readable')
                if not os.access(cookie_path, os.W_OK):
                    raise OSError(f'file {cookie_path} is not writable')
                try:
                    self._cookie.load(ignore_discard=True)
                    self._authenticated = True
                except LoadError as e:
                    log.error('failed to load cookie from file %s', cookie_path)
                    if not ignore_broken_cookie:
                        raise OSError(e) from e
        else:
            self._cookie = CookieJar()
        for cj in self._cookie:
            if cj.name == '_xsrf':
                self.__headers[XSRF_HEADER_NAME] = str(cj.value)
                break

    @property
    def cookies(self) -> Union[CookieJar, FileCookieJar]:
        """

        Property for retrieving the cookie jar containing authentication cookies.

        Checks if the user is authenticated, and if not, performs the authentication process first.
        Once authenticated, returns the cookie jar.

        Returns:
            Union[CookieJar, FileCookieJar]: The cookie jar containing authentication cookies.
        """
        if not self._authenticated:
            self.authenticate()
        return self._cookie

    @property
    def headers(self) -> Dict[str, str]:
        """
        @property
        def headers(self) -> Dict[str, str]:
            Checks if the user is authenticated, performs authentication if not authenticated,
            and returns the headers.

            Returns:
                Dict[str, str]: The headers to be used in the request.
        """
        if not self._authenticated:
            self.authenticate()
        return self.__headers

    def _save_cookie(self) -> None:
        """
        _save_cookie:
            Saves the cookies in the FileCookieJar instance, if applicable.
            Ensures that cookies are saved persistently by ignoring the discard attribute.
        """
        if isinstance(self._cookie, FileCookieJar):
            self._cookie.save(ignore_discard=True)

    def _profile(self, raise_on_error: bool = False) -> 'ProfileTypeT':
        """

        Fetches the user profile data from the API.

        Parameters:
        - raise_on_error (bool): If set to True, an error will be raised in case of a failure.
                                 Defaults to False.

        Returns:
        - ProfileTypeT: The unescaped user profile data retrieved from the API.

        """
        return cast(
            'ProfileTypeT',
            unescape_dict(
                self.api_get('/user/me', raise_on_error=raise_on_error),
                keys=['name'],
            ),
        )

    def _do_auth(
        self,
        login: str,
        password: str,
        cookie_jar: CookieJar,
        headers: Dict[str, str],
        second_step_fn: SecondStepFnT,
        second_step_arg: str,
    ) -> None:
        """
        Authenticate the user and set the necessary headers for future requests.

        Args:
            login (str): The user's login name.
            password (str): The user's password.
            cookie_jar (CookieJar): The cookie jar to store cookies.
            headers (Dict[str, str]): The headers to be included in the request.
            second_step_fn (SecondStepFnT): The function to handle
                                            the second step of authentication if required.
            second_step_arg (str): An argument for the second step function.

        Returns:
            None

        Sets:
            self._authenticated (bool): True if authentication is successful, False otherwise.
            self.__headers[XSRF_HEADER_NAME] (str): The XSRF token if authentication is successful.
        """
        self._authenticated, _, xsrf = authenticate(
            login, password, cookie_jar, headers, second_step_fn, second_step_arg
        )
        if self._authenticated:
            self.__headers[XSRF_HEADER_NAME] = xsrf
            self._save_cookie()

    def _authenticate(
        self,
        second_step_fn: SecondStepFnT,
        second_step_arg: str,
        login: Optional[str] = None,
        password: Optional[str] = None,
    ) -> bool:
        """
        Authenticate the user with the provided login and password,
        performing a secondary step if necessary.

        Arguments:
        second_step_fn: Function to execute for the second step of the authentication process
        second_step_arg: Argument to pass to the second step function
        login: Optional login name. If not provided,
               it will use login stored within the class instance.
        password: Optional password. If not provided,
                  it will use the password stored within the class instance.

        Returns:
        bool: True if authentication is successful, False otherwise

        Raises:
        PararamioAuthenticationException: If login or password is not provided or empty

        Exceptions:
        PararamioHTTPRequestException:
                        Raised if there is an error during the HTTP request in the profile check.

        """
        login = login or self._login or ''
        password = password or self._password or ''
        if not check_login_opts(login, password):
            raise PararamioAuthenticationException(
                f'{get_empty_vars(login=login, password=password)} must be set and not empty'
            )
        if not self._cookie:
            self._do_auth(
                login,
                password,
                self._cookie,
                self.__headers,
                second_step_fn,
                second_step_arg,
            )
        try:
            self._authenticated = True
            self._profile(raise_on_error=True)
        except PararamioHTTPRequestException:
            self._authenticated = False
            self._do_auth(
                login,
                password,
                self._cookie,
                self.__headers,
                second_step_fn,
                second_step_arg,
            )
        return self._authenticated

    def authenticate(
        self,
        login: Optional[str] = None,
        password: Optional[str] = None,
        key: Optional[str] = None,
    ) -> bool:
        """
        Authenticate a user using either a login and password or a key.

        This method attempts to authenticate a user through provided login credentials
        or a predefined key. If the key is not provided, it will use the instance key
        stored in `self._key`.

        Args:
            login (str, optional): The user's login name. Defaults to None.
            password (str, optional): The user's password. Defaults to None.
            key (str, optional): A predefined key for authentication. Defaults to None.

        Returns:
            bool: True if authentication is successful, False otherwise.

        Raises:
            PararamioAuthenticationException: If no key is provided.

        """
        key = key or self._key
        if not key:
            raise PararamioAuthenticationException('key must be set and not empty')
        return self._authenticate(do_second_step, key, login, password)

    def authenticate_with_code(
        self,
        code: str,
        login: Optional[str] = None,
        password: Optional[str] = None,
    ) -> bool:
        """

        Authenticates a user using a provided code and optionally login and password.

        Parameters:
          code (str): The authentication code. Must be set and not empty.
          login (str, optional): The user login. Default is None.
          password (str, optional): The user password. Default is None.

        Returns:
          bool: True if authentication is successful, otherwise raises an exception.

        Raises:
          PararamioAuthenticationException: If the code is not provided or is empty.
        """
        if not code:
            raise PararamioAuthenticationException('code must be set and not empty')
        return self._authenticate(do_second_step_with_code, code, login, password)

    def _api_request(
        self,
        url: str,
        method: str = 'GET',
        data: Optional[dict] = None,
        callback: Callable = lambda rsp: rsp,
        raise_on_error: bool = False,
    ) -> Any:
        """
        Performs an authenticated API request with XSRF token management and error handling.

        Args:
            url (str): The API endpoint URL to which the request is made.
            method (str): The HTTP method to use for the request. Defaults to 'GET'.
            data (Optional[dict]): The data payload for the request, if applicable.
                                   Defaults to None.
            callback (Callable): A callback function to process the response.
                                 Defaults to a lambda that returns the response.
            raise_on_error (bool): Flag to determine if exceptions should be raised.
                                   Defaults to False.

        Returns:
            Any: The result of the callback processing on the API request response.

        Raises:
            PararamioHTTPRequestException:
                                         If an HTTP error occurs and raise_on_error is set to True.

        Notes:
            - The function ensures that the user is authenticated before making the request.
            - Manages the XSRF token by retrieving and saving it as needed.
            - Handles specific error cases by attempting re-authentication or
              renewing the XSRF token.
        """
        if not self._authenticated:
            self.authenticate()
        if not self.__headers.get(XSRF_HEADER_NAME, None):
            self.__headers[XSRF_HEADER_NAME] = get_xsrf_token(self._cookie)
            self._save_cookie()
        try:
            return callback(
                api_request(url, method, data, cookie_jar=self._cookie, headers=self.__headers)
            )
        except PararamioHTTPRequestException as e:
            if raise_on_error:
                raise
            if e.code == 401:
                self._authenticated = False
                return self._api_request(
                    url=url,
                    method=method,
                    data=data,
                    callback=callback,
                    raise_on_error=True,
                )
            message = e.message
            if message == 'xsrf':
                log.info('xsrf is expire, invalid or was not set, trying to get new one')
                self.__headers[XSRF_HEADER_NAME] = ''
                return self._api_request(
                    url=url,
                    method=method,
                    data=data,
                    callback=callback,
                    raise_on_error=True,
                )
            raise

    def api_get(self, url: str, raise_on_error: bool = False) -> dict:
        """

        Handles HTTP GET requests to the specified API endpoint.

        Arguments:
        url (str): The URL of the API endpoint.

        raise_on_error (bool): If set to True, an exception will be raised
                               if the API response indicates an error. Defaults to False.

        Returns:
        dict: The JSON response from the API, parsed into a Python dictionary.

        """
        return self._api_request(url, raise_on_error=raise_on_error)

    def api_post(
        self,
        url: str,
        data: Optional[Dict[Any, Any]] = None,
        raise_on_error: bool = False,
    ) -> dict:
        """
        Sends a POST request to the specified URL with the given data.

        Parameters:
        url (str): The endpoint URL where the POST request should be sent.
        data (Optional[Dict[Any, Any]], optional): The payload to be sent in the POST request body.
                                                   Defaults to None.
        raise_on_error (bool, optional): Whether to raise an exception if the request fails.
                                         Defaults to False.

        Returns:
        dict: The response from the server as a dictionary.
        """
        return self._api_request(url, method='POST', data=data, raise_on_error=raise_on_error)

    def api_put(
        self,
        url: str,
        data: Optional[Dict[Any, Any]] = None,
        raise_on_error: bool = False,
    ) -> dict:
        """
        Sends a PUT request to the specified URL with the provided data.

        Parameters:
        - url: The URL to send the PUT request to.
        - data: Optional dictionary containing the data to include in the request body.
        - raise_on_error: Boolean flag indicating whether to raise an exception
                          if the request results in an error.

        Returns:
        A dictionary containing the server's response to the PUT request.
        """
        return self._api_request(url, method='PUT', data=data, raise_on_error=raise_on_error)

    def api_delete(
        self,
        url: str,
        data: Optional[Dict[Any, Any]] = None,
        raise_on_error: bool = False,
    ) -> dict:
        """
        Sends a DELETE request to the specified URL with optional data.

        Parameters:
        url (str): The URL to send the DELETE request to.
        data (Optional[Dict[Any, Any]], optional): Optional payload to include in the request.
        raise_on_error (bool, optional): Determines whether an exception should be raised
                                         on request failure.

        Returns:
        dict: The response from the API request.
        """
        return self._api_request(url, method='DELETE', data=data, raise_on_error=raise_on_error)

    def _upload_file(
        self,
        file: Union[BinaryIO, BytesIO],
        chat_id: int,
        filename: Optional[str] = None,
        type_: Optional[str] = None,
        organization_id: Optional[int] = None,
        reply_no: Optional[int] = None,
        quote_range: Optional[str] = None,
    ) -> Tuple[dict, dict]:
        """
        _upload_file is a method for uploading a file to a specified chat or organization.

        Arguments:
            file: A binary stream of the file to be uploaded.
            chat_id: The ID of the chat where the file will be uploaded.
            filename: An optional parameter that specifies the name of the file.
            type_: An optional parameter that specifies the type of file being uploaded.
                   If not provided, it will be inferred from the filename.
            organization_id: An optional parameter that specifies the ID of the organization
                             if the file is an organization avatar.
            reply_no: An optional parameter that specifies the reply number
                      associated with the file.
            quote_range: An optional parameter that specifies the range
                         of quotes associated with the file.

        Returns:
            A tuple containing a dictionary with the response from the xupload_file function
            and a dictionary of the fields used during the upload.

        Raises:
            PararamioValidationException: If filename is not set when type is None,
            or if organization_id is not set when type is organization_avatar,
            or if chat_id is not set when type is chat_avatar.

        Notes:
            This method ensures that the necessary headers and
            tokens are set before attempting the file upload.
        """
        if type_ is None and not filename:
            raise PararamioValidationException('filename must be set when type is None')
        if not self._authenticated:
            self.authenticate()
        if not self.__headers.get(XSRF_HEADER_NAME, None):
            self.__headers[XSRF_HEADER_NAME] = get_xsrf_token(self._cookie)
        if type_ == 'organization_avatar' and organization_id is None:
            raise PararamioValidationException(
                'organization_id must be set when type is organization_avatar'
            )
        if type_ == 'chat_avatar' and chat_id is None:
            raise PararamioValidationException('chat_id must be set when type is chat_avatar')
        content_type = None
        if type_ not in ('organization_avatar', 'chat_avatar'):
            content_type = type_
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0, 0)
        fields: List[Tuple[str, Union[str, int, None]]] = [
            ('type', type_),
            ('filename', filename),
            ('size', file_size),
            ('chat_id', chat_id),
            ('organization_id', organization_id),
            ('reply_no', reply_no),
            ('quote_range', quote_range),
        ]
        return xupload_file(
            fp=file,
            fields=fields,
            filename=filename,
            content_type=content_type,
            headers=self.__headers,
            cookie_jar=self._cookie,
        ), dict(fields)

    def upload_file(
        self,
        file: Union[str, BytesIO, BinaryIO, os.PathLike],
        chat_id: int,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        reply_no: Optional[int] = None,
        quote_range: Optional[str] = None,
    ) -> File:
        """
        upload_file uploads a file to a specified chat.

        Parameters:
        file: Union[str, BytesIO, os.PathLike] The file to be uploaded. It can be a file path,
              a BytesIO object, or an os.PathLike object.
        chat_id: int
            The ID of the chat where the file should be uploaded.
        filename: Optional[str]
            The name of the file.
            If not specified and the file is a path, the basename of the file path will be used.
        content_type: Optional[str]
            The MIME type of the file.
        reply_no: Optional[int]
            The reply number in the chat to which this file is in response.
        quote_range: Optional[str]
            The range of messages being quoted.

        Returns:
        File
            An instance of the File class representing the uploaded file.
        """
        if isinstance(file, (str, os.PathLike)):
            filename = filename or os.path.basename(file)
            with open(file, 'rb') as f:
                res, extra = self._upload_file(
                    file=f,
                    chat_id=chat_id,
                    filename=filename,
                    type_=content_type,
                    reply_no=reply_no,
                    quote_range=quote_range,
                )
        else:
            res, extra = self._upload_file(
                file=file,
                chat_id=chat_id,
                filename=filename,
                type_=content_type,
                reply_no=reply_no,
                quote_range=quote_range,
            )
        return File(self, guid=res['guid'], mime_type=extra['type'], **extra)

    def delete_file(self, guid: str) -> dict:
        """
        Deletes a file identified by the provided GUID.

        Args:
            guid (str): The globally unique identifier of the file to be deleted.

        Returns:
            dict: The result of the deletion operation.

        """
        return delete_file(guid, headers=self.__headers, cookie_jar=self._cookie)

    def download_file(self, guid: str, filename: str) -> BytesIO:
        """
        Downloads and returns a file as a BytesIO object given its unique identifier and filename.

        Args:
            guid (str): The unique identifier of the file to be downloaded.
            filename (str): The name of the file to be downloaded.

        Returns:
            BytesIO: A BytesIO object containing the downloaded file content.
        """
        return download_file(guid, filename, headers=self.__headers, cookie_jar=self._cookie)

    @property
    def profile(self) -> 'ProfileTypeT':
        """

        Provides access to the profile property. If the profile is not
        yet initialized, this method will initialize it by calling the
        _profile method.

        Returns:
            ProfileTypeT: The profile object.
        """
        if not self.__profile:
            self.__profile = self._profile()
        return self.__profile

    def search_user(self, query: str) -> List[UserSearchResult]:
        """
        search_user(query: str) -> List[User]

        Searches for users based on the given query string.

        Parameters:
        query (str): The search query used to find matching users.

        Returns:
        List[User]: A list of User objects that match the search query.
        """
        return User.search(self, query)

    def search_group(self, query: str) -> List[Group]:
        """
        Performs a search for groups based on a given query string.

        Arguments:
        query (str): The search term used to find matching groups.

        Returns:
        List[Group]: A list of Group objects that match the search criteria.
        """
        return Group.search(self, query)

    def search_posts(
        self,
        query: str,
        order_type: str = 'time',
        page: int = 1,
        chat_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterable[Post]]:
        """

        search_posts searches for posts based on a given query and various optional parameters.

        Arguments:
        - query: The search term used to find posts.
        - order_type: Specifies the order of the search results. Default is 'time'.
        - page: The page number of the search results to retrieve. Default is 1.
        - chat_id: Optional ID of the chat to search within. If None, search in all chats.
        - limit: The maximum number of posts to return. If None, use the default limit.

        Returns:
        - A tuple containing the total number of posts matching
          the search query and an iterable of Post objects.
        """
        return Chat.post_search(
            self, query, order_type=order_type, page=page, chat_id=chat_id, limit=limit
        )

    def list_chats(self) -> Iterable[Chat]:
        """
        Returns iterable that yields chat objects in a lazy-loading manner.
        The chats are fetched from the server using the specified URL and are returned in batches.

        Returns:
            Iterable: An iterable that yields chat objects.
        """
        url = '/core/chat/sync'
        chats_per_load = 50
        ids = self.api_get(url).get('chats', [])
        return lazy_loader(self, ids, Chat.load_chats, per_load=chats_per_load)

    def get_groups_by_ids(self, ids: List[int]) -> Iterable[Group]:
        """

        Fetches a list of Group objects based on provided group ids.

        Args:
         ids (List[int]): A list of group IDs to fetch.

        Returns:
         Iterable[Group]: An iterable of Group objects corresponding to the provided IDs.

        """
        url = '/core/group?ids=' + ','.join(map(str, ids))
        return [Group(self, **data) for data in self.api_get(url).get('groups', [])]

    def get_users_by_ids(self, ids: List[int]) -> List[User]:
        """
        Retrieve a list of User objects by their IDs.

        Arguments:
        ids -- a list of user ID integers.

        Returns:
        A list of User objects corresponding to the provided IDs.
        """
        url = '/user/list?ids=' + ','.join(map(str, ids))
        return [
            User(self, **unescape_dict(data, ['name']))
            for data in self.api_get(url).get('users', [])
        ]

    def post_private_message_by_user_email(self, email: str, text: str) -> Post:
        """

        Posts a private message to a user identified by their email address.

        :param email: The email address of the user to whom the message will be sent.
        :type email: str
        :param text: The content of the message to be posted.
        :type text: str
        :return: A Post object representing the posted message.
        :rtype: Post
        """
        url = '/msg/post/private'
        resp = self._api_request(url, method='POST', data={'text': text, 'user_email': email})
        return Post(Chat(self, resp['chat_id']), resp['post_no'])

    def post_private_message_by_user_id(self, user_id: int, text: str) -> Post:
        """
        Send a private message to a specific user.

        Parameters:
        user_id (int): The ID of the user to whom the message will be sent.
        text (str): The content of the message to be sent.

        Returns:
        Post: The Post object containing information about the scent message.
        """
        url = '/msg/post/private'
        resp = self._api_request(url, method='POST', data={'text': text, 'user_id': user_id})
        return Post(Chat(self, resp['chat_id']), resp['post_no'])

    def post_private_message_by_user_unique_name(self, unique_name: str, text: str) -> Post:
        """
        Post a private message to a user identified by their unique name.

        Parameters:
        unique_name (str): The unique name of the user to whom the private message is to be sent.
        text (str): The content of the private message.

        Returns:
        Post: An instance of the Post class representing the posted message.
        """
        url = '/msg/post/private'
        resp = self._api_request(
            url, method='POST', data={'text': text, 'user_unique_name': unique_name}
        )
        return Post(Chat(self, resp['chat_id']), resp['post_no'])

    def mark_all_messages_as_read(self, org_id: Optional[int] = None) -> bool:
        """

        Marks all messages as read for the organization or everywhere if org_id is None.

        Parameters:
        org_id (Optional[int]): The ID of the organization. This parameter is optional.

        Returns:
        bool: True if the operation was successful, False otherwise.
        """
        url = '/msg/lastread/all'
        data = {}
        if org_id is not None:
            data['org_id'] = org_id
        return self.api_post(url, data=data).get('result', None) == 'OK'

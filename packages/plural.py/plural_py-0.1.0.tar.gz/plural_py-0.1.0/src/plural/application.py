from typing import overload, Literal

from .enums import Intents
from .models import Message
from .user import User


class Application:
    def __init__(self, token: str, intents: Intents = Intents.NONE) -> None:
        self.token = token
        self.intents = intents

    def as_user(self, user_id: int) -> User:
        '''
        Return a user object for the given user ID.

        Intended for sending requests on behalf of a user. e.g. `await app.as_user(123).fetch_member(456)`

        :param user_id: The user ID to act as.
        :type user_id: int
        '''
        return User(user_id=user_id, application=self)

    @overload
    async def fetch_message(
        self,
        message_id: int,
        only_check_existence: Literal[True],
        max_wait: float = 10.0
    ) -> bool:
        ...

    @overload
    async def fetch_message(
        self,
        message_id: int,
        only_check_existence: Literal[False],
        max_wait: float = 10.0
    ) -> Message:
        ...

    async def fetch_message(
        self,
        message_id: int,
        only_check_existence: bool = False,
        max_wait: float = 10.0
    ) -> Message | bool:
        '''
        Fetch a message by either original or proxied ID.

        :param message_id: The original or proxied message ID.
        :type message_id: `int`
        :param only_check_existence: Whether to only check if the message exists. If `True`, the return type will be `bool`.
        :type only_check_existence: `bool`
        :param max_wait: The maximum time to wait for a response. Defaults to 10 seconds.
        :type max_wait: `float`
        :return: `bool` if `only_check_existence` is `True`, otherwise `Message`.
        '''

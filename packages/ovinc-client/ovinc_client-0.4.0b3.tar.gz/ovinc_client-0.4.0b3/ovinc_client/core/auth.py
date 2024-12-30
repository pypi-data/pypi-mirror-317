from typing import Tuple, Union

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from pydantic import BaseModel as PydanticBaseModel
from rest_framework.authentication import SessionAuthentication

from ovinc_client import OVINCClient
from ovinc_client.constants import ResponseData
from ovinc_client.core.exceptions import LoginRequired
from ovinc_client.core.logger import logger

USER_MODEL = get_user_model()


class UserInfo(PydanticBaseModel):
    username: str
    nick_name: str
    user_type: str
    last_login: str = ""


class SessionAuthenticate(SessionAuthentication):
    """
    Session Auth
    """

    async def authenticate(self, request) -> Union[Tuple[USER_MODEL, None], None]:
        user = getattr(request._request, "user", None)  # pylint: disable=W0212
        if await self.check_user(user):
            return None
        return user, None

    @database_sync_to_async
    def check_user(self, user):
        return user is None or not user.is_active


class LoginRequiredAuthenticate(SessionAuthenticate):
    """
    Login Required Authenticate
    """

    async def authenticate(self, request) -> (USER_MODEL, None):
        user_tuple = await super().authenticate(request)
        if user_tuple is None or await self.check_user(user_tuple[0]):
            raise LoginRequired()
        return user_tuple


class OAuthBackend(BaseBackend):
    """
    OAuth
    """

    def authenticate(self, request, **kwargs) -> USER_MODEL | None:
        # load ticket
        ticket = request.COOKIES.get(getattr(settings, "OVINC_TICKET_COOKIE_NAME", "ovinc-api-sessionid"))
        if not ticket:
            return None
        # Union API Auth
        try:
            # request
            client = OVINCClient(
                app_code=settings.APP_CODE, app_secret=settings.APP_SECRET, union_api_url=settings.OVINC_API_DOMAIN
            )
            resp: ResponseData = async_to_sync(client.auth.verify_ticket)({"ticket": ticket})
            if not resp.result:
                logger.info("[UnionAuthFailed]")
                return None
            # parse user
            user_info = UserInfo.model_validate(resp.data.get("data", {}))
            user: USER_MODEL = USER_MODEL.objects.get_or_create(username=user_info.username)[0]
            if (
                not user.nick_name
                or not user.user_type
                or user_info.nick_name.lower() != user.nick_name.lower()
                or user_info.user_type.lower() != user.user_type.lower()
            ):
                user.nick_name = user_info.username
                user.user_type = user_info.user_type
                user.last_login = user_info.last_login
                user.save(update_fields=["nick_name", "user_type"])
            return user
        except Exception as err:  # pylint: disable=W0718
            logger.exception(err)
            return None

    def get_user(self, user_id: str) -> USER_MODEL:
        return USER_MODEL.objects.get_or_create(username=user_id)[0]

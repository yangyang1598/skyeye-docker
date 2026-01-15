from urllib import parse
import logging
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from rest_framework.response import Response
from rest_framework import status

db_logger = logging.getLogger('db')

@database_sync_to_async
def get_user_from_headers_or_queries(scope):
    """
    function to get the `User` object
    from his headers or queries as well.
    :return object of `User` or None
    """
    try:
        headers = dict(scope["headers"])
    except KeyError as error:
        headers = {}
        db_logger.error(error)

    try:
        params = dict(parse.parse_qsl(scope["query_string"].decode("utf8")))
    except KeyError as error:
        params = {}
        db_logger.warning(error)

    token_key = None
    token_is_found = False

    if b"authorization" in headers:
        # 1. get from authorization headers
        token_name, token_key = headers[b"authorization"].decode().split()
        if token_name == "Token":  # nosec: B105 (just checking the token name)
            token_is_found = True
    else:
        # 2. get from token params
        token_key = params.get("token")
        token_is_found = True if token_key else False
    if token_is_found:
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            pass  # AnonymousUser
    return None


class TokenAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        user = await get_user_from_headers_or_queries(scope)
        if user is not None:
            scope["user"] = user
            return await self.app(scope, receive, send)
        else:
            # print("Fail")
            return Response(user, status=status.HTTP_401_UNAUTHORIZED)


# Handy shortcut for applying all three layers at once
def TokenAuthMiddlewareStack(inner):
    """
    middleware to support websocket ssh connection
    from both session or by queries
    """
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))

from typing import TYPE_CHECKING

from fastapi import Request
from fastapi.responses import Response
from fastapi.security import APIKeyCookie

from fastauth.schema import TokenResponse
from fastauth.transport.base import TokenTransport

if TYPE_CHECKING:
    from fastauth.fastauth import FastAuth


class CookieTransport(TokenTransport):
    def schema(self, request: Request, refresh: bool = False):
        if refresh:
            return APIKeyCookie(
                name=self._config.COOKIE_REFRESH_TOKEN_NAME, auto_error=False
            )
        return APIKeyCookie(
            name=self._config.COOKIE_ACCESS_TOKEN_NAME, auto_error=False
        )

    async def login_response(
        self,
        security: "FastAuth",
        content: TokenResponse,
        response: Response | None = None,
    ) -> Response:
        if response:
            response = security.set_access_cookie(content.access_token, response)
            if content.refresh_token is not None:  # pragma: no cover
                response = security.set_refresh_cookie(content.refresh_token, response)
            return response

        response = Response(status_code=204)
        return await self.login_response(security, content, response)

    async def logout_response(
        self, security: "FastAuth", response: Response | None = None
    ) -> Response:
        res = response or Response(status_code=204)
        return security.remove_cookies(res)

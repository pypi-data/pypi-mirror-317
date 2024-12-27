from typing import TYPE_CHECKING

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from fastauth.schema import TokenResponse
from fastauth.transport.base import TokenTransport

if TYPE_CHECKING:
    from fastauth.fastauth import FastAuth


class BearerTransport(TokenTransport):
    def schema(self, request: Request, refresh: bool = False) -> OAuth2PasswordBearer:
        token_url = (
            f"{self._config.ROUTER_AUTH_DEFAULT_PREFIX}{self._config.TOKEN_LOGIN_URL}"
        )
        return OAuth2PasswordBearer(token_url, auto_error=False)

    async def login_response(
        self,
        security: "FastAuth",
        content: TokenResponse,
        response: Response | None = None,
    ) -> Response:
        content = content.model_dump()
        if response:
            response.body = response.render(content)
            response.init_headers()  # call to recalculate Content-Length header
            return response
        return JSONResponse(content=content)

    async def logout_response(
        self, security: "FastAuth", response: Response | None = None
    ) -> Response:
        return response or Response(status_code=204)

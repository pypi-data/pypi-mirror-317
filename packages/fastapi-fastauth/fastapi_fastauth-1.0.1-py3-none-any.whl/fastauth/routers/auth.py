from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from fastauth.fastauth import FastAuth
from fastauth.schema import TokenResponse
from fastauth.transport import get_login_response, get_logout_response


def get_auth_router(security: FastAuth):
    config = security.config
    router = APIRouter(prefix=config.ROUTER_AUTH_DEFAULT_PREFIX)

    @router.post(config.TOKEN_LOGIN_URL)
    async def login(
        request: Request,
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service=security.AUTH_MANAGER,
        strategy=security.TOKEN_STRATEGY,
    ):
        tokens: TokenResponse = await auth_service.password_login(
            credentials, strategy, request
        )
        return await get_login_response(security, tokens)

    @router.post(
        config.TOKEN_LOGOUT_URL,
        dependencies=[Depends(security.access_token_required())],
    )
    async def logout(request: Request):
        return await get_logout_response(security)

    if config.ENABLE_REFRESH_TOKEN:  # pragma: no cover

        @router.post(config.TOKEN_REFRESH_URL)
        async def refresh(
            request: Request,
            token=security.REFRESH_TOKEN,
            auth_service=security.AUTH_MANAGER,
            strategy=security.TOKEN_STRATEGY,
        ):
            uid = token.get("sub")
            user = await auth_service.get_user(uid)

            access_token = await strategy.write_token(user, "access")
            refresh_token = await strategy.write_token(user, "refresh")

            tokens = TokenResponse(
                access_token=access_token, refresh_token=refresh_token
            )

            return await get_login_response(security, tokens)

    return router

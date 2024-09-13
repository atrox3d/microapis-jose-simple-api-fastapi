# print('SERVER | ------- START ----------')
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from auth import decode_and_validate_token
import jwt

server = FastAPI(debug=True)

public_pem = 'public_key.pem'
audience = 'http://localhost:8000/orders'

class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    # async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> api.Response:
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # return await super().dispatch(request, call_next)
        if request.url in [ 'docs', '/openapi.json']:
            return await call_next(request)
        if request.method == 'OPTIONS':
            return await call_next(request)

        bearer_header = request.headers.get('Authorization')
        if not bearer_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content = {
                    'detail': 'missing access token',
                    'content': 'missing access token',
                }
            )
        try:
            _, auth_token = bearer_header.split()
            auth_token = auth_token.strip()
            token_payload = decode_and_validate_token(auth_token, public_pem, audience)
        except (
            jwt.exceptions.ExpiredSignatureError,
            jwt.exceptions.ImmatureSignatureError,
            jwt.exceptions.InvalidAlgorithmError,
            jwt.exceptions.InvalidAudienceError,
            jwt.exceptions.InvalidKeyError,
            jwt.exceptions.InvalidTokenError,
            jwt.exceptions.MissingRequiredClaimError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'detail':str(error), 'content':str(error)}
            )
        else:
            request.state.user_id = token_payload['sub']
        return await call_next(request)
    


# print('SERVER | ---- import api -----')
import api

# print('SERVER | ------- END ----------')

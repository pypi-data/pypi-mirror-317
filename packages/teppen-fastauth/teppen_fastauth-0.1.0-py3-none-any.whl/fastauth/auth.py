from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError, PyJWKSetError, InvalidAudienceError

from .decode import decode_access_token_using_jwks
from .exceptions import NoTokenException


def get_bearer_access_token_decode(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
):
    if authorization is None:
        raise HTTPException(401, "トークンがありません。")
    
    try:
        token = authorization.credentials
        return decode_access_token_using_jwks(token)
    except InvalidSignatureError:
        print("InvalidSignatureError")
        raise HTTPException(400, "署名が不正です。")
    except ExpiredSignatureError:
        print("ExpiredSignatureError")
        raise HTTPException(401, "トークンの期限が切れています。")
    except InvalidAudienceError:
        print("InvalidAudienceError")
        raise HTTPException(400, "InvalidAudienceError: aud が不正です。")
    except PyJWKSetError as e:
        print(e)
        print("PyJWKSetError")
        raise HTTPException(401)
    except NoTokenException:
        print("NoTokenException")
        raise HTTPException(401, "トークンがありません。")
    except Exception as e:
        print(e)
        raise HTTPException(500, "予期せぬエラーが発生しました。")

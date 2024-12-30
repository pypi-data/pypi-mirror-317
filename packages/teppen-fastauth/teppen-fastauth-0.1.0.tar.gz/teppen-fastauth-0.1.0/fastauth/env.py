import os

JWKS_ENDPOINT = os.getenv("JWKS_ENDPOINT", "http://nginx/api/tokens/jwks")
JWT_ALGHORITHM = "RS256"
HOST_RESOURCE_APP = os.getenv("HOST_RESOURCE_APP")

if HOST_RESOURCE_APP is None:
    raise Exception("環境変数 HOST_RESOURCE_APP は必須です。")

JWT_AUDIENCE = ["localhost:81", HOST_RESOURCE_APP]

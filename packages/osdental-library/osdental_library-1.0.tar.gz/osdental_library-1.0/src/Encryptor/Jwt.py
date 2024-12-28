import jwt
from Exception.Exception import JWTokenException
from Helpers.Message import JWT_GENERATE_FAILED, JWT_FAILED
from Helpers.Constant import STATUS_ERROR

class JWT:

    @staticmethod
    def generate_token(payload: dict, jwt_secret_key:str) -> str:
        try:
            token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
            return token

        except Exception as e:
            raise JWTokenException(message=JWT_GENERATE_FAILED, error=str(e), status_code=STATUS_ERROR) from e


    @staticmethod
    def extract_payload(jwt_token: str, jwt_secret_key:str) -> dict:
        try:
            payload = jwt.decode(jwt_token, jwt_secret_key, algorithms=['HS256'])
            return payload

        except Exception as e:
            raise JWTokenException(message=JWT_FAILED, error=str(e), status_code=STATUS_ERROR) from e
import hashlib
import hmac
import base64
import json
import time
from .config import settings

class AuthSystem:
    def generate_jwt(self, payload, secret=None):
        secret = secret or settings.JWT_SECRET
        header = {"alg": "HS256", "typ": "JWT"}
        segments = []
        for obj in (header, payload):
            raw = json.dumps(obj, separators=(',', ':')).encode()
            segment = base64.urlsafe_b64encode(raw).rstrip(b'=')
            segments.append(segment)
        signing_input = b'.'.join(segments)
        signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
        segments.append(base64.urlsafe_b64encode(signature).rstrip(b'='))
        return b'.'.join(segments).decode()

    def verify_jwt(self, token, secret=None):
        secret = secret or settings.JWT_SECRET
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts
        signing_input = (header_b64 + '.' + payload_b64).encode()
        check_sig = base64.urlsafe_b64encode(
            hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
        ).rstrip(b'=')
        if check_sig.decode() != sig_b64:
            return None

        payload_bytes = base64.urlsafe_b64decode(payload_b64 + '==')
        payload = json.loads(payload_bytes)

        if "exp" in payload and payload["exp"] < time.time():
            return None

        return payload

    def authenticate(self, credentials):
        if credentials.get("username") == "test" and credentials.get("password") == "1234":
            payload = {
                "user_id": 1,
                "username": "test",
                "exp": time.time() + 3600
            }
            token = self.generate_jwt(payload)
            return {"token": token, "user_id": 1}
        return None

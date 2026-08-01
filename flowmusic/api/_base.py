import requests
import json
import base64
from typing import Dict, Any

class BaseAPI:
    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def _get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, **kwargs)
        response.raise_for_status()
        return response.json()

def get_user_id_from_token(token: str) -> str:
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT token")
    
    payload_b64 = parts[1]
    payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
    
    payload = json.loads(base64.b64decode(payload_b64).decode('utf-8'))
    return payload.get('sub')

from typing import List, Optional
from ._base import BaseAPI, get_user_id_from_token
from ..models.user import User

class UserAPI(BaseAPI):
    def get_users(self, user_ids: List[str]) -> List[User]:
        """Возвращает публичную информацию о пользователях."""
        data = self._post("users", json={"user_ids": user_ids})
        return [User(**u) for u in data.get("data", [])]

    def get_me(self) -> Optional[User]:
        """Возвращает информацию о текущем пользователе по токену."""
        token = self.session.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return None
        user_id = get_user_id_from_token(token)
        users = self.get_users([user_id])
        return users[0] if users else None

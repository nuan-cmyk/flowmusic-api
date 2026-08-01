from ._base import BaseAPI
from ..models.user import UserLevel, UserScores

class PersonalizeAPI(BaseAPI):
    def get_level(self) -> UserLevel:
        """Получить информацию об уровне подписки пользователя."""
        data = self._post("personalize/level", json={})
        return UserLevel(**data)

    def get_scores(self, user_id: str) -> UserScores:
        """Получить игровые очки/скоры пользователя."""
        data = self._post("personalize/scores", json={"user_ids": [user_id]})
        scores_data = data.get("scores", {}).get(user_id)
        if not scores_data:
            raise ValueError(f"Scores for user {user_id} not found in response")
        return UserScores(**scores_data)

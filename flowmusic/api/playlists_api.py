from typing import Dict, Any, Optional
from ._base import BaseAPI

class PlaylistsAPI(BaseAPI):
    def create(self, name: str, description: Optional[str] = "") -> Dict[str, Any]:
        """Создает новый плейлист."""
        payload = {
            "name": name,
            "description": description,
            "image_id": None
        }
        data = self._post("playlists", json=payload)
        return data.get("playlist", {})

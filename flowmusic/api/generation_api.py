import json
import time
import sseclient
from typing import List, Dict, Optional
from ._base import BaseAPI
from ..models.audio import Clip, ClipResponse
from ..models.chat import ConversationResponse

class GenerationAPI(BaseAPI):
    def upload_image(self, file_path: str, file_type: str = "image/png") -> Dict[str, str]:
        """Загружает картинку и возвращает id и url."""
        import os
        url = f"{self.base_url}/producer/upload"
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            files = {
                "file": (filename, f, file_type),
                "file_type": (None, file_type)
            }
            # We don't use _post because we need files= instead of json=
            response = self.session.post(url, files=files)
            response.raise_for_status()
            return response.json()

    def start_conversation(self, prompt: str, image_info: Optional[Dict[str, str]] = None, model: str = "producer:standard", mode: str = "standard", selected_model: Optional[str] = None) -> str:
        """Начинает генерацию и возвращает job_id (conversation_id)."""
        parts = []
        if image_info:
            import uuid
            tool_call_id = str(uuid.uuid4())
            parts.extend([
                {
                    "tool_name": "synthetic__upload_image",
                    "args": {
                        "id": image_info["id"],
                        "url": image_info["url"],
                        "name": "image.png",
                        "instructions": "Tool indicating that the user has uploaded an image file.\n\nNOTE: The agent does not have access to this tool directly."
                    },
                    "tool_call_id": tool_call_id,
                    "part_kind": "tool-call"
                },
                {
                    "tool_name": "synthetic__upload_image",
                    "content": None,
                    "tool_call_id": tool_call_id,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                    "part_kind": "tool-return"
                }
            ])
            parts.append({
                "content": [
                    prompt,
                    {
                        "url": image_info["url"],
                        "identifier": image_info["id"],
                        "kind": "image-url",
                        "media_type": "image/png",
                        "force_download": True
                    }
                ],
                "part_kind": "user-prompt"
            })
        else:
            parts.append({"content": prompt, "part_kind": "user-prompt"})

        payload = {
            "parts": parts,
            "client_context": {
                "song_queue": [],
                "selected_model": selected_model,
                "lyrics_id_map": {},
                "ghostwriter_version": "standard"
            },
            "model_name": model,
            "mode": mode
        }
        data = self._post("conversation", json=payload)
        return data.get("job_id")

    def get_clips_info(self, clip_ids: List[str]) -> Dict[str, Clip]:
        """Получает информацию о клипах по их ID."""
        data = self._post("clips", json={"clip_ids": clip_ids})
        return {k: Clip(**v) for k, v in data.get("clips", {}).items()}

    def get_clip_status(self, operation_id: str) -> str:
        """Получает статус операции генерации трека."""
        data = self._get(f"audio-create-song-status/{operation_id}")
        return data.get("status", "unknown")

    def generate_music(self, prompt: str, image_path: Optional[str] = None, model: str = "producer:standard", mode: str = "standard", selected_model: Optional[str] = None, timeout: int = 120, poll_interval: int = 5) -> List[Clip]:
        """Удобный метод: отправляет запрос, ждет SSE-события и возвращает готовые треки."""
        image_info = None
        if image_path:
            image_info = self.upload_image(image_path)
            
        job_id = self.start_conversation(prompt, image_info, model, mode, selected_model)
        
        # Подключаемся к SSE-стриму
        url = f"{self.base_url}/messages/{job_id}/stream?last_id=0"
        # Для SSE нужно использовать requests со stream=True
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        client = sseclient.SSEClient(response)
        
        clip_ids = []
        for event in client.events():
            if event.event == "part":
                data = json.loads(event.data)
                part = data.get("part", {})
                if part.get("part_kind") == "tool-return" and part.get("tool_name") == "audio__create_song":
                    content = part.get("content", {})
                    if content.get("status") == "success":
                        clip_id = content.get("clip_id")
                        if clip_id:
                            clip_ids.append(clip_id)
            elif event.event == "final" or event.event == "complete":
                pass # Стрим может закончиться
                
            # Если получили 2 клипа (обычно генерируется 2), можно выходить из стрима
            if len(clip_ids) >= 2:
                response.close()
                break
                
        if not clip_ids:
            raise RuntimeError("Не удалось получить clip_id из стрима")

        # Теперь поллим статусы
        start_time = time.time()
        ready_clips = []
        
        while time.time() - start_time < timeout:
            clips_dict = self.get_clips_info(clip_ids)
            all_ready = True
            for cid, clip in clips_dict.items():
                status = clip.duration.status
                if status == "completed":
                    if clip not in ready_clips:
                        ready_clips.append(clip)
                else:
                    all_ready = False
            
            if all_ready and len(ready_clips) == len(clip_ids):
                return ready_clips
                
            time.time() # just for IDE
            time.sleep(poll_interval)
            
        raise TimeoutError("Время ожидания генерации истекло")

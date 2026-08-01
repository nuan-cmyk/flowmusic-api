import requests
from .api.billing_api import BillingAPI
from .api.user_api import UserAPI
from .api.personalize_api import PersonalizeAPI
from .api.generation_api import GenerationAPI
from .api.playlists_api import PlaylistsAPI

class FlowMusicClient:
    """
    Главный клиент для работы с неофициальным API Flow Music (flowmusic.app).
    """

    def __init__(self, token: str):
        """
        Инициализация клиента.
        
        :param token: JWT токен пользователя (из заголовка Authorization, без 'Bearer ')
        """
        self.base_url = "https://www.flowmusic.app/__api"
        self.session = requests.Session()
        
        # Устанавливаем базовые заголовки
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.flowmusic.app",
            "Referer": "https://www.flowmusic.app/"
        })
        
        # Инициализация модулей API
        self.billing = BillingAPI(self.session, self.base_url)
        self.users = UserAPI(self.session, self.base_url)
        self.personalize = PersonalizeAPI(self.session, self.base_url)
        self.generation = GenerationAPI(self.session, self.base_url)
        self.playlists = PlaylistsAPI(self.session, self.base_url)

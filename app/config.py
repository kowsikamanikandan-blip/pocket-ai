from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name:str='PocketSmart AI'; environment:str='development'
    secret_key:str=Field(default='change-me-development-secret',min_length=16)
    database_url:str='sqlite:///./pocketsmart.db'; gemini_api_key:str=''; gemini_model:str='gemini-2.5-flash'
    frontend_origins:str='http://127.0.0.1:8000,http://localhost:8000'
    access_token_expire_minutes:int=120; max_image_size_mb:int=5
    model_config=SettingsConfigDict(env_file='.env',env_file_encoding='utf-8',case_sensitive=False,extra='ignore')
    @property
    def origins(self): return [x.strip() for x in self.frontend_origins.split(',') if x.strip()]
@lru_cache
def get_settings(): return Settings()

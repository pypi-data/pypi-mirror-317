import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key1: str
    anthropic_api_key: str
    agentops_api_key: str
    serper_api_key: str
    google_service_account_json_string_2: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def google_service_account_json_dict(self) -> dict:
        return json.loads(self.google_service_account_json_string_2)


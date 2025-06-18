from pydantic_settings import BaseSettings


class WSSettings(BaseSettings):
    CONECTION_LIMIT = 1024


ws_settings = WSSettings()

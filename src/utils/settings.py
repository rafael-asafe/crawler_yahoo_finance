"""Configurações da aplicação via variáveis de ambiente.

Utiliza ``pydantic-settings`` para carregar e validar variáveis de ambiente,
com suporte a arquivo ``.env``. Todos os campos sem valor padrão são obrigatórios.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações carregadas do ambiente ou arquivo ``.env``.

    Attributes:
        LOG_LEVEL: Nível de log do Python (ex: ``"INFO"``, ``"DEBUG"``).
        CONSOLE_LOG: Se ``True``, habilita handler de log para ``stdout``.
        LOG_FILE: Caminho para arquivo de log. ``None`` desabilita o handler de arquivo.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LOG_LEVEL: str
    CONSOLE_LOG: bool | None = False
    LOG_FILE: str | None = None
    DATA_PATH: str
    CSV_NAME: str
    URL: str
    REGION: str


settings = Settings()

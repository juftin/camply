"""
Gunicorn Configuration
"""

from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class GunicornConfig(BaseSettings):
    """
    Gunicorn Configuration Namespace
    """

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="GUNICORN_",
        case_sensitive=True,
    )

    WORKERS: int = 1
    WORKER_CLASS: str = "uvicorn_worker.UvicornWorker"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    TIMEOUT: int = 30
    RELOAD: bool = False
    PRELOAD: bool = True
    LOG_LEVEL: str = "info"
    ACCESS_LOG: str = "-"
    ERROR_LOG: str = "-"
    ACCESS_LOG_FORMAT: str = (
        '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s'
    )


# Configuration Instance
conf = GunicornConfig()
# Configuration Values
workers: int = conf.WORKERS
worker_class: str = conf.WORKER_CLASS
bind: str = f"{conf.HOST}:{conf.PORT}"
timeout: int = conf.TIMEOUT
reload: bool = conf.RELOAD
preload_app: bool = conf.PRELOAD
loglevel: str = conf.LOG_LEVEL
accesslog: str = conf.ACCESS_LOG
errorlog: str = conf.ERROR_LOG
access_log_format: str = conf.ACCESS_LOG_FORMAT

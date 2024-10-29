import logging
import os

from dataclasses import dataclass

env = os.environ.get("ENV", "local")
log_level = os.environ.get("LOG_LEVEL", "debug").upper()

#https://www.uvicorn.org/deployment/
#server settings options

def get_log_level():
    match log_level:
        case "ERROR":
            return logging.ERROR
        case "INFO":
            return logging.INFO
        case _:
            return logging.DEBUG
    
@dataclass(repr=False)
class BaseConfig:
    reload: bool = True
    use_colors: bool = True
    log_level = logging.getLevelName(logging.INFO)

@dataclass
class LocalConfig(BaseConfig):
    host: str = "127.0.0.1"
    port: int = 8310
    log_level = logging.getLevelName(logging.DEBUG)

@dataclass
class DevConfig(BaseConfig):
    host: str = "foobar"
    log_level = logging.getLevelName(get_log_level())

@dataclass
class StagingConfig(BaseConfig):
    host: str = "staging.milestones.blueboard.com"
    #workers: int = multiprocessing.cpu_count()
    log_level = logging.getLevelName(get_log_level())

@dataclass
class ProdConfig(BaseConfig):
    host: str = "milestones.blueboard.com"
    #workers: int = multiprocessing.cpu_count()
    log_level = logging.getLevelName(get_log_level())

configs = {
    "local" : LocalConfig(),
    "dev" : DevConfig(),
    "staging" : StagingConfig(),
    "prod" : ProdConfig()
}

run_config = configs[env]

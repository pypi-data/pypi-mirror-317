import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from caasm_tool.config import Config


@dataclass
class BaseCaasmConfig(Config):
    DB_SETTINGS: Dict = None
    SOCKS_PROXIES: List = None

    FETCH_SIZE_MAP: Dict = None
    FETCH_WORKER_MAP: Dict = None
    FETCH_FAILED_TIMES: int = None
    FETCH_RETRY_TIMES: int = None
    FETCH_RETRY_WAIT_TIME: int = None
    FETCH_TYPE_MAPPER: Dict = None
    FETCH_DATA_TYPE_MAPPER: Dict = None

    DEFAULT_LOG: List = None

    # 适配器相关
    FILE_PARSER_DIR: str = None
    FILE_PARSER_BUFFER_SIZE: int = None
    DATABASE_PARSER_DIR: str = None
    FTP_PARSER_DIR = None
    SMB_PARSER_DIR = None

    ADAPTER_TYPES: List[int] = None

    # kafka相关
    KAFKA_INSTANCES: Dict[str, Dict] = None
    KAFKA_PARSER_POINTS: List[str] = None
    KAFKA_CONSUMER_MAP: Dict = None

    # 爬虫驱动相关
    CHROME_DRIVER_PATH: str = None

    @property
    def base_config_path(self) -> Path:
        return Path(os.path.dirname(os.path.abspath(__file__))) / "default.yml"

    @property
    def config_path(self) -> Path:
        return self.ROOT_DIR / "config.yml"

    @property
    def default_config_path(self) -> Path:
        return self.ROOT_DIR / "caasm_config" / "default.yml"

    @property
    def data_path(self):
        return self.ROOT_DIR / "caasm_data"

    @property
    def prop_mapper(self) -> Dict:
        return {
            "DB_SETTINGS": "db.settings",
            "SOCKS_PROXIES": "proxy.socks5",
            "FETCH_FAILED_TIMES": "fetch.failed.times",
            "FETCH_SIZE_MAP": "fetch.size_map",
            "FETCH_WORKER_MAP": "fetch.worker_map",
            "FETCH_RETRY_TIMES": "fetch.retry.times",
            "FETCH_RETRY_WAIT_TIME": "fetch.retry.wait",
            "FETCH_TYPE_MAPPER": "fetch.type_mapper",
            "FETCH_DATA_TYPE_MAPPER": "fetch.data_type_mapper",
            "DEFAULT_LOG": "log.default",
            "FILE_PARSER_DIR": "adapter.file.parser_dir",
            "FTP_PARSER_DIR": "adapter.ftp.parser_dir",
            "SMB_PARSER_DIR": "adapter.smb.parser_dir",
            "DATABASE_PARSER_DIR": "adapter.database.parser_dir",
            "FILE_PARSER_BUFFER_SIZE": "adapter.file.buffer_size",
            "ADAPTER_TYPES": "adapter.type",
            "KAFKA_INSTANCES": "kafka.instances",
            "KAFKA_CONSUMER_MAP": "kafka.consumer_map",
            "KAFKA_PARSER_POINTS": "kafka.parser.points",
            "CHROME_DRIVER_PATH": "spider.chrome_driver_path",
        }

    # 一些常用的配置

    @property
    def mongo_conn(self):
        return self.db_conn("mongo")

    @property
    def mongo_default_database(self):
        return self.db_info("mongo", "default_database")

    # 公共方法
    def db_conn(self, db_name) -> Optional[Dict]:
        return self.db_info(db_name, "conn")

    def db_info(self, db_name, config_name):
        return self.DB_SETTINGS.get(db_name, {}).get(config_name)

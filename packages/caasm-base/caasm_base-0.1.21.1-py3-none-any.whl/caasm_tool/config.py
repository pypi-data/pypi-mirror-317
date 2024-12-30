import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from caasm_tool.util import load_yaml_content, Singleton, extract, restore

log = logging.getLogger()


@dataclass
class Config(metaclass=Singleton):
    def __post_init__(self):
        self.install()

    def install(self, install_hook=True):
        # 解析配置
        base_config_mapper = self._parse_base_config()
        default_config_mapper = self._parse_default_config()
        develop_config_mapper = self._parse_develop_config()
        config_mapper = self._parse_config()
        customer_config_mapper = self._parse_customer_config()

        # 融合配置
        configs = [
            #   开发配置
            develop_config_mapper,
            #   定制化配置
            customer_config_mapper,
            #   部署目录下配置
            config_mapper,
            #   代码默认配置
            default_config_mapper,
            #   基础库配置
            base_config_mapper,
        ]
        result_mapper = self._mix_up(*configs)

        self._install_common(result_mapper, install_hook=install_hook)

    def _parse_default_config(self):
        return self.__parse_common(self.default_config_path)

    def _parse_develop_config(self):
        return self.__parse_common(self.develop_config_path)

    def _parse_config(self):
        return self.__parse_common(self.config_path)

    def _parse_base_config(self):
        return self.__parse_common(self.base_config_path)

    def _parse_customer_config(self):
        return self.__parse_common(self.customer_config_path)

    def _mix_up(self, *config_mappers):
        config_mappers = list(config_mappers)

        result_mapper = {}
        old_mapper = config_mappers.pop()
        while config_mappers:
            new_mapper = config_mappers.pop()

            tmp_mapper = self.__mix_up(new_mapper, old_mapper)
            result_mapper = self.__mix_up(tmp_mapper, result_mapper)

            old_mapper = result_mapper

        return result_mapper

    def _install_common(self, result, install_hook=True):
        for key_name, key_define in self.prop_mapper.items():
            self.__dict__[key_name] = extract(result, key_define)
        self.check()
        if install_hook:
            self.install_hook()

    def install_hook(self):
        pass

    def check(self):
        pass

    @classmethod
    def __parse_common(cls, path):
        result = {}
        if not path:
            return result
        if not path.exists():
            return result
        return load_yaml_content(path)

    def __mix_up(self, new_mapper, old_mapper):
        """
        融合两个字典，当字段冲突的时候以new_mapper为主
        :param new_mapper:
        :param old_mapper:
        :return:
        """
        result = {}

        for prop_name, config_define in self.prop_mapper.items():
            new_config = extract(new_mapper, config_define)
            old_config = extract(old_mapper, config_define)

            config = None
            if old_config is not None:
                config = old_config
            if new_config is not None:
                config = new_config

            if config is None:
                continue

            restore(config_define, config, result)
        return result

    @property
    def ROOT_DIR(self):
        return Path()

    @property
    def base_config_path(self) -> Path:
        return None

    @property
    def config_path(self) -> Path:
        return None

    @property
    def develop_config_path(self) -> Path:
        return None

    @property
    def default_config_path(self) -> Path:
        return None

    @property
    def customer_config_path(self) -> Path:
        return None

    @property
    def prop_mapper(self) -> Dict:
        """
        属性转换器
        例如：
            属性a 对应yml文件中的 c.d.f.g
            则
            {
                "a": "c.d.f.g"
            }
        :return:
        """
        raise NotImplementedError

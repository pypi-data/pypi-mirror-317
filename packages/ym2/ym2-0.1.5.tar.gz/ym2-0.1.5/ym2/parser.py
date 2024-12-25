from omegaconf import OmegaConf, DictConfig, ListConfig
from pathlib import Path
from typing import List, Any, Union, Optional, Dict
import yaml
import argparse
import re

class OverrideParser:
    def __init__(self, conf: DictConfig):
        self.conf = conf

    @staticmethod
    def is_overrided(value: Any) -> bool:
        return isinstance(value, str) and ',' in value and ':' not in value

    @staticmethod
    def is_nested(value: Any) -> bool:
        return isinstance(value, DictConfig)

    @staticmethod
    def split_overrided(key: str, value: str) -> List[str]:
        return [f'{key}={val}' for val in value.split(',') if val]

    def parse_overrides(self) -> List[List[str]]:
        overrides = []
        stack = [(self.conf, '', '.')]
        while stack:
            conf, parent_key, sep = stack.pop()
            for key, value in conf.items():
                new_key = parent_key + sep + key if parent_key else key
                if self.is_nested(value):
                    stack.append((value, new_key, sep))
                elif self.is_overrided(value):
                    overrides.append(self.split_overrided(new_key, value))
        return overrides


class ConfigParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='ym2',
            description='A framework to configure complex AI/ML projects'
        )
        parser.add_argument('config_file', type=str, help='config file')
        parser.add_argument('--version', action='version', version='%(prog)s 0.1.5')
        args, cli_args = parser.parse_known_args()

        self.yaml_file = args.config_file
        self.cli_args = cli_args

    def parse_yaml(self) -> DictConfig:
        data = yaml.safe_load(Path(self.yaml_file).open())
        return OmegaConf.create(data)

    def parse_cli(self, return_dotlist: bool = False) -> Union[List[str], DictConfig]:
        dotlist = []
        for arg in self.cli_args:
            matches = re.match(r'^([^=]+)=([^=]+)$', arg)
            if matches is None:
                raise ValueError(f'Invalid argument `{arg}`. Please use the format key=value')
            dotlist.append(arg)
        if return_dotlist:
            return dotlist
        return OmegaConf.from_dotlist(dotlist)

    @staticmethod
    def _find_dependency(yaml_dir: Path, k: str, v: Any) -> Optional[Dict]:
        if not isinstance(v, str) or '\n' in v:
            return None
        file = yaml_dir / k / f'{v}.yaml'
        if not file.exists():
            file = yaml_dir / f'{v}.yaml'
        if not file.exists():
            return None
        return yaml.safe_load(file.open())

    def parse_dependencies(self, conf: DictConfig) -> DictConfig:
        new_conf = {}
        yaml_dir = Path(self.yaml_file).parent
        for k, v in conf.items():
            if (data := self._find_dependency(yaml_dir, k, v)) is not None:
                new_conf[k] = data

            if isinstance(v, ListConfig):
                new_conf[k] = v
                for idx, sub_v in enumerate(v):
                    if (data := self._find_dependency(yaml_dir, k, sub_v)) is not None:
                        new_conf[k][idx] = data
        return OmegaConf.create(new_conf)

    def parse(self) -> DictConfig:
        yaml_conf = self.parse_yaml()
        cli_conf = self.parse_cli()
        return OmegaConf.merge(yaml_conf, cli_conf)

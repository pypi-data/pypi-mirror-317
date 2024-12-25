from itertools import product
from typing import List, Tuple
from omegaconf import DictConfig, OmegaConf
from copy import deepcopy
from .parser import OverrideParser

class Sweeper:
    def __init__(self, conf: DictConfig):
        parser = OverrideParser(conf)
        overrides = parser.parse_overrides()

        self.conf = conf
        self.overrides = overrides

    def sweep(self) -> List[Tuple]:
        if not self.overrides:
            return [[self.conf, '']]
        ret = []
        for override in product(*self.overrides):
            copy_conf = deepcopy(self.conf)
            override_conf = OmegaConf.from_dotlist(override)
            merged_conf = OmegaConf.merge(copy_conf, override_conf)
            ret.append([merged_conf, ';'.join(override)])
        return ret

from typing import List, Tuple, Callable, Any, Dict
from omegaconf import OmegaConf, DictConfig
from pathlib import Path
from multiprocessing import Process
from dataclasses import dataclass, asdict
import traceback
import string
import json
import time
import random
import os

@dataclass
class Stat:
    running_dir: str
    curr: int
    total: int
    config: Dict
    override: str
    term: str
    status: str
    started: int
    duration: int
    pid: int

class Worker:
    def __init__(self, conf: Dict, override: str, curr: int, total: int, term: str):
        self.curr = curr
        self.total = total
        self.conf = conf
        self.override = override
        self.term = term
        self.pid = os.getpid()
        self.seek_pos = None
        self.has_error = False
        self.stat = None

    def setup(self):
        options = string.ascii_lowercase + string.digits
        random_name = ''.join(random.choices(options, k=8))

        self.output_dir = Path.cwd() / 'outputs'
        self.running_dir = self.output_dir / random_name
        self.stat_file = self.output_dir / 'stat.jsonl'

        self.output_dir.mkdir(parents=True, exist_ok=True)

        with open(self.stat_file, 'a') as file:
            self.stat = Stat(
                running_dir=str(self.running_dir),
                curr=self.curr,
                total=self.total,
                config=OmegaConf.to_object(self.conf),
                override=self.override,
                term=self.term,
                status='running',
                started=int(time.time()),
                duration=0,
                pid=self.pid,
            )
            self.seek_pos = file.tell()
            file.write(json.dumps(asdict(self.stat)) + '\n')

    def run(self, cls: Any):
        try:
            conf = {k: v for k, v in self.conf.items() if k != '_cls_'}
            obj = cls(**conf)
            obj.main(stat=self.stat)
        except Exception as e:
            self.has_error = True
            traceback.print_exc()

    def teardown(self):
        with open(self.stat_file, 'r+') as file:
            assert self.seek_pos is not None
            self.stat.status = 'finished' if not self.has_error else 'error'
            self.stat.duration = int(time.time()) - self.stat.started

            file.seek(self.seek_pos)
            file.truncate()
            file.write(json.dumps(asdict(self.stat)) + '\n')

class Launcher:
    def __init__(self, cls: Callable, confs: List[Tuple], term: str):
        self.cls = cls
        self.confs = confs
        self.term = term

    def worker(self, conf: DictConfig, override: str, curr: int, total: int):
        w = Worker(conf, override, curr, total, self.term)
        w.setup()
        w.run(self.cls)
        w.teardown()

    def launch_seq(self):
        total = len(self.confs)
        print(f'[*] Launch {total} tasks locally.')
        for curr, (conf, override) in enumerate(self.confs):
            OmegaConf.resolve(conf)
            process = Process(
                target=self.worker,
                args=(conf, override, curr + 1, total)
            )
            process.start()
            process.join()
            print(f'[+] Process {process.pid} completed and cleaned up.')

    def launch(self):
        self.launch_seq()

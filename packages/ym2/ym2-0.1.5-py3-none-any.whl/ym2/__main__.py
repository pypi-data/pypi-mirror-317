from omegaconf import OmegaConf
from .parser import ConfigParser 
from .sweeper import Sweeper
from .importer import import_class
from .launcher import Launcher

def main():
    parser = ConfigParser()
    conf = parser.parse()
    dotlist = parser.parse_cli(return_dotlist=True)

    sweeper = Sweeper(conf)
    confs = sweeper.sweep()

    # Resolve all deps
    for idx in range(len(confs)):
        raw_conf = confs[idx][0]
        dep_conf = parser.parse_dependencies(raw_conf)
        confs[idx][0] = OmegaConf.merge(raw_conf, dep_conf)

    # Import class and launch processes
    cls = import_class(conf.get('_cls_', None))
    launcher = Launcher(cls, confs, ';'.join(dotlist))
    launcher.launch()


if __name__ == '__main__':
    main()

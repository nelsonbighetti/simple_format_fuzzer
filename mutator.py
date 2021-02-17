from file_parser import *
from executable import *


class MutatorConfig:
    executable_path = None
    file_path = None
    file_name = None
    regex = None
    timeout = None
    args = None


class Mutator:
    cfg = None
    parser = None
    executable = None

    def __init__(self, config):
        logging.debug('Mutator initialized')
        self.cfg = config
        self.parser = FileParser(self.cfg.file_path, self.cfg.file_name)
        self.parser.splitToChunks(self.cfg.regex)
        self.executable = Executable(self.cfg.executable_path, self.cfg.timeout, self.cfg.args)

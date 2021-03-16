from file_parser import *
from executable import *
from mutations import *
from itertools import *
from random import shuffle
import threading
from shutil import copyfile
import itertools

class Mutator:
    cfg = None
    parser = None
    executable = None
    tasks_pool = None
    num = None
    mutations_pool_sequential = None
    mutations_pool_one_shot = None
    reporter = None
    thread_workspace = None

    def __init__(self, reporter, config, num, tasks_pool, thread_workspace):
        logging.debug('Mutator %s initialized', num)
        self.num = num
        self.tasks_pool = copy.deepcopy(tasks_pool)
        self.cfg = config
        self.reporter = reporter
        self.thread_workspace = thread_workspace
        self.parser = FileParser(self.cfg.file_path, self.cfg.file_name)
        self.parser.splitToChunks(self.cfg.regex)
        self.executable = Executable(self.cfg.executable_path + self.cfg.executable_name,
                                     self.cfg.executable_path,
                                     self.cfg.timeout,
                                     self.cfg.args)

        self.mutations_pool_sequential = []

        if self.cfg.mutation_intensity == 0:
            logging.critical('Error: mutation intensity must be > 0')
            exit(0)

        mutations_list_sequential = list(mutationsMapSequential)

        for mutation_i in range(1, len(mutations_list_sequential) + 1):
            for i in combinations(list(mutations_list_sequential), r=mutation_i):
                self.mutations_pool_sequential.append(list(i))

        self.mutations_pool_one_shot = list(mutationsMapOneShot)

    # No deepcopy
    def applyEachMutationToChunk(self, current_sequence, chunk_id, mutations_set):
        for mutation in mutations_set:
            mutationsMapSequential[mutation](current_sequence[chunk_id], self.cfg.mutation_intensity)

    def loop(self):
        logging.debug('Mutator %s loop started', self.num)
        original_sequence = copy.deepcopy(self.parser.getOriginalFileSequence())

        for task in self.tasks_pool:
            for mutations_set_sequential in self.mutations_pool_sequential:
                for mutation_one_shot in self.mutations_pool_one_shot:
                    mutation_types_list = list(mutationTypesMap)
                    mutations_types_pool = [list(p) for p in
                                            [p for p in itertools.product(mutation_types_list, repeat=len(task))]]
                    for mutation_types_set in mutations_types_pool:
                        current_sequence = copy.deepcopy(original_sequence)
                        for chunk_i in range(len(task)):
                            if mutation_types_set[chunk_i] == "sequential":
                                self.applyEachMutationToChunk(current_sequence, task[chunk_i], mutations_set_sequential)
                            else:
                                mutationsMapOneShot[mutation_one_shot](current_sequence[task[chunk_i]])

                        self.parser.emplaceOriginalFile(current_sequence)
                        output = self.executable.execute()
                        if not self.executable.isMatchOriginalOutput(output):
                            logging.debug('Found output inconsistency [Thr: %s]', self.num)
                            self.reporter.writeReport(self.executable.getOriginalOutput(),
                                                      output,
                                                      self.cfg.workspace + r'\\' + self.thread_workspace,
                                                      mutation_types_set,
                                                      mutations_set_sequential,
                                                      mutation_one_shot,
                                                      self.cfg,
                                                      current_sequence
                                                      )


def mutatorWorker(reporter, cfg, num, tasks_pool):
    config = copy.deepcopy(cfg)
    thread_workspace = "ws_" + str(int(time.time())) + "_thr_" + str(num)
    try:
        os.mkdir(config.workspace + thread_workspace)
        logging.warning('Created workspace for thread: %s', str(num))
    except:
        logging.critical('Cannot create workspace for thread')
        exit(1)

    exePathOriginal = config.executable_path + config.executable_name
    configPathOriginal = config.file_path + config.file_name
    exePathCopy = config.workspace + thread_workspace + r'\\' + config.executable_name
    configPathCopy = config.workspace + thread_workspace + r'\\' + config.file_name

    try:
        copyfile(exePathOriginal, exePathCopy)
    except:
        logging.critical('Cannot copy executable to workspace')
        exit(1)

    try:
        for f in cfg.additional_files:
            file_path = config.executable_path + f
            newpath = config.workspace + thread_workspace + r'\\' + f
            copyfile(file_path, newpath)
    except:
        logging.critical('Cannot copy additional files')
        exit(1)

    try:
        copyfile(configPathOriginal, configPathCopy)
    except:
        logging.critical('Cannot copy input file to workspace')
        exit(1)

    config.executable_path = config.workspace + thread_workspace + r'\\'
    config.file_path = config.workspace + thread_workspace + r'\\'

    mutator = Mutator(reporter, config, num, tasks_pool, thread_workspace)
    mutator.loop()


class MutatorsPool:
    cfg = None
    workersThreads = None
    reporter = None

    def __init__(self, config):
        logging.debug('Mutators pool initialized')
        self.cfg = config
        self.parser = FileParser(self.cfg.file_path, self.cfg.file_name, False)
        self.parser.splitToChunks(self.cfg.regex)
        self.reporter = Reporter(self.cfg)

    def initPool(self):
        chunks_count = self.parser.getContentsChunksCount()
        variants = []
        for chunk_i in range(1, chunks_count + 1):
            for i in combinations(range(chunks_count), r=chunk_i):
                variants.append(list(i))

        shuffle(variants)

        thrNum = self.cfg.threads
        tasks_pool = []
        for i in range(thrNum):
            lo = i * (len(variants) // thrNum)
            hi = (i + 1) * (len(variants) // thrNum)
            if i == thrNum - 1:
                hi = len(variants)
            tasks_pool.append(variants[lo:hi])

        tasks_pool = [[[1]]]
        self.workersThreads = []
        for i in range(len(tasks_pool)):
            self.workersThreads.append(
                threading.Thread(target=mutatorWorker, args=(self.reporter, self.cfg, i, tasks_pool[i])))

        for thr in self.workersThreads:
            thr.start()

        for thr in self.workersThreads:
            thr.join()
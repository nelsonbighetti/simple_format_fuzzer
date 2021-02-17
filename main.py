from mutator import *


def tests():
    # FIXME
    print('Fixme')
    # fp = FileParser(cfg.file_path, cfg.file_name)
    # fp.splitToChunks(cfg.regex)
    # print(fp.getBytes())
    # print(fp.getContentsChunksCount())
    # print(fp[5])

    # mutator = Mutator(cfg)
    # mutator.loop()


def main():
    # initLogging(logging.DEBUG)

    initLogging(logging.CRITICAL)
    cfg = MutatorConfig()
    cfg.executable_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.executable_name = r"sample.exe"
    cfg.file_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.file_name = r"sample_config.txt"
    cfg.regex = b";"
    cfg.timeout = 1
    cfg.args = ""
    cfg.threads = 1
    cfg.workspace = r"C:\Users\79313\Documents\repos\APS.L1\exe\workspace\\"
    cfg.mutation_intensity = 50

    pool = MutatorsPool(cfg)
    pool.initPool()

if __name__ == '__main__':
    main()

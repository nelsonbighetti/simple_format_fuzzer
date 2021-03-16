from mutator import *
from mutator_config import *


def exec(cfg):
    executable = Executable(cfg.executable_path + cfg.executable_name,
                            cfg.executable_path,
                            cfg.timeout,
                            cfg.args)
    out = executable.execute()
    print(out)


def main():
    initLogging(logging.WARNING)
    cfg = MutatorConfig()
    cfg.executable_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.executable_name = r"vuln5.exe"
    cfg.additional_files = ["func.dll"]
    cfg.file_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.file_name = r"config_3"
    cfg.regex = b"\/start"
    cfg.timeout = 100
    cfg.args = ""
    cfg.threads = 1
    cfg.workspace = r"C:\Users\79313\Documents\repos\APS.L1\exe\workspace\\"
    cfg.mutation_intensity = 500
    cfg.stop_on_first_crash = False
    cfg.reports = r"C:\Users\79313\Documents\repos\APS.L1\exe\reports\\"
    # cfg.output_comparison_modes = [ComparisonMode.STDOUT, ComparisonMode.STDERR, ComparisonMode.RETCODE]
    cfg.output_comparison_modes = [ComparisonMode.RETCODE]
    cfg.max_reports = 1000

    # exec(cfg)
    pool = MutatorsPool(cfg)
    pool.initPool()

if __name__ == '__main__':
    main()

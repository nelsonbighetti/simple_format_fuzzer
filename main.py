from mutator import *
from mutator_config import *

def main():
    initLogging(logging.WARNING)
    cfg = MutatorConfig()
    cfg.executable_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.executable_name = r"vuln6.exe"
    cfg.additional_files = ["func.dll"]
    cfg.file_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.file_name = r"config_5"
    cfg.regex = b";"
    cfg.timeout = 10
    cfg.args = ""
    cfg.threads = 8
    cfg.workspace = r"C:\Users\79313\Documents\repos\APS.L1\exe\workspace\\"
    cfg.mutation_intensity = 50
    cfg.stop_on_first_crash = False
    cfg.reports = r"C:\Users\79313\Documents\repos\APS.L1\exe\reports\\"
    # cfg.output_comparison_modes = [ComparisonMode.STDOUT, ComparisonMode.STDERR, ComparisonMode.RETCODE]
    cfg.output_comparison_modes = [ComparisonMode.RETCODE]
    cfg.max_reports = 10

    pool = MutatorsPool(cfg)
    pool.initPool()

if __name__ == '__main__':
    main()

from mutator import *

def main():
    initLogging()
    cfg = MutatorConfig()
    cfg.executable_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\sample.exe"
    cfg.file_path = r"C:\Users\79313\Documents\repos\APS.L1\exe\\"
    cfg.file_name = r"sample_config.txt"
    cfg.regex = b"\x01"
    cfg.timeout = 1
    cfg.args = ""

    mutator = Mutator(cfg)

if __name__ == '__main__':
    main()

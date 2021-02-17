from executable import *
from config_parser import *
from logs import *

LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"


def main():
    # r"C:\Users\79313\Documents\repos\APS.L1\exe\sample.exe"
    # Executable(r"C:\Users\79313\Documents\repos\APS.L1\exe\sample.exe")
    # config = ConfigParser(r"C:\Users\79313\Desktop\Учеба 10s\АБП (Жуковский)\ЛР 1-2\vuln\\", r"config_5")
    initLogging()
    config = ConfigParser(r"C:\Users\79313\Documents\repos\APS.L1\exe\\", r"sample_config.txt")
    config.splitToChunks(b"\x01")

    # print('here')
    # seq = Sequence()

    # print(seq.getBytes())'


if __name__ == '__main__':
    main()

from executable import *
from sequence import *


def main():
    # r"C:\Users\79313\Documents\repos\APS.L1\exe\sample.exe"
    Executable(r"C:\Users\79313\Documents\repos\APS.L1\exe\sample.exe")
    Config(r"C:\Users\79313\Desktop\Учеба 10s\АБП (Жуковский)\ЛР 1-2\vuln\\", r"config_5")
    print('here')
    seq = Sequence()

    print(seq.getBytes())


if __name__ == '__main__':
    main()

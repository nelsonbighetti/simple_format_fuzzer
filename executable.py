import subprocess
import copy


class Output:
    stdout = None
    stderr = None

    def __init__(self, stdout, stderr):
        self.stdout = copy.deepcopy(stdout)
        self.stderr = copy.deepcopy(stderr)

    def __str__(self):
        return str([self.stdout, self.stderr])

    def __eq__(self, other):
        return (self.stderr == other.stderr and self.stdout == other.stdout)

    def __ne__(self, other):
        return not self.__eq__(other)

class Executable:
    __path__ = None
    __args__ = None
    __default__ = None

    def __init__(self, path, args=""):
        self.__path__ = path
        self.__args__ = args
        self.storeDefaultOutput()

    def storeDefaultOutput(self):
        result = subprocess.Popen([self.__path__, self.__args__], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()
        stdout = result[0]
        stderr = result[1]
        self.__default__ = Output(stdout, stderr)

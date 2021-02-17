import subprocess
import copy
from logs import *
import threading
from threading import Lock


# class Report:
#     original_output = None
#     changed_output = None
#     file_path = None
#     workspace = None
#
#     def __init__(self, original, changed, path, workspace):
#         self.original_output = original
#         self.changed_output = changed
#         self.file_path = path
#         self.workspace = workspace
#
# class Reporter:
#     mutex = None
#     reports = []
#
#     def __init__(self):
#         self.mutex = Lock
#
#     def append(self, original, changed, workspace, combination):
#         self.mutex.acquire()
#
#         self.mutex.release()


class Output:
    stdout = None
    stderr = None
    retcode = None

    def __init__(self, stdout, stderr, retcode):
        self.stdout = copy.deepcopy(stdout)
        self.stderr = copy.deepcopy(stderr)
        self.retcode = copy.deepcopy(retcode)

    def __str__(self):
        return str([self.stdout, self.stderr, self.retcode])

    def __eq__(self, other):
        return (self.stderr == other.stderr and self.stdout == other.stdout and self.retcode == other.retcode)

    def __ne__(self, other):
        return not self.__eq__(other)


class Executable:
    path = None
    args = None
    default_output = None
    timeout = None

    def __init__(self, path, timeout=10, args=""):
        self.path = path
        self.args = args
        self.timeout = timeout
        self.storeDefaultOutput()

    def execute(self):
        def target():
            logging.debug('Executable thread started')
            self.process = subprocess.Popen(self.path + " " + self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = self.process.communicate()
            logging.debug('Executable thread finished')
            self.stdout = result[0]
            self.stderr = result[1]
            self.retcode = self.process.returncode

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(self.timeout)
        if thread.is_alive():
            logging.warning('Killing executable thread by timeout')
            self.process.terminate()
            thread.join()

        return Output(self.stdout, self.stderr, self.retcode)

    def storeDefaultOutput(self):
        self.default_output = self.execute()
        logging.debug('Original output: %s', str(self.default_output))

    def getOriginalOutput(self):
        return self.default_output

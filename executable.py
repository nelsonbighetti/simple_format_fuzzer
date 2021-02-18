import subprocess
import copy
from logs import *
import threading
from threading import Lock
import time
import os
from mutator_config import *


class htmlTable:
    @staticmethod
    def getTableStyle():
        code = "<style>" \
               "table { border: solid 1px #DDEEEE; border-collapse: collapse; " \
               "border-spacing: 0; font: normal 13px Arial, sans-serif;}" \
               "th { background-color: #DDEFEF; border: solid 1px #DDEEEE; color: #336B6B; padding: " \
               "10px; text-align: left; text-shadow: 1px 1px 1px #fff; }" \
               "td { border: solid 1px #DDEEEE; color: #333; padding: 10px; text-shadow: 1px 1px 1px #fff;}" \
               "</style>"
        return code

    @staticmethod
    def create(header, rows):
        code = "<html>" + htmlTable.getTableStyle() + "<table><tr>"
        for h in header:
            code += "<th>" + str(h) + "</th>"
        code += "</tr>"

        for row in rows:
            code += "<tr>"
            for column in row:
                code += "<td>" + str(column) + "</td>"
            code += "</tr>"

        code += "</table></html>"
        return code


class Reporter:
    mutex = None
    dir_path = None
    files_path = None
    reports_count = None

    def __init__(self, cfg):
        self.mutex = Lock()
        self.dir_path = cfg.reports + r'\\reports_' + str(int(time.time())) + r"\\"
        self.files_path = self.dir_path + r"modified_files\\"
        self.reports_count = 0

        try:
            os.mkdir(self.dir_path)
            logging.warning('Created reports dir: %s', str(self.dir_path))
        except:
            logging.critical('Cannot create reports dir')
            exit(1)

        try:
            os.mkdir(self.files_path)
            logging.warning('Created modified files dir: %s', str(self.files_path))
        except:
            logging.critical('Cannot create modified files dir')
            exit(1)

    def writeReport(self,
                    original,
                    changed,
                    thread_workspace,
                    mutation_types_set,
                    mutations_set_sequential,
                    mutation_one_shot,
                    cfg,
                    current_sequence
                    ):

        self.mutex.acquire()

        self.reports_count += 1
        modified_file_path = self.files_path + cfg.file_name + "_modified_" + str(self.reports_count)
        header = ["Original output",
                  "Output with modified input file",
                  "Thread workspace",
                  "Mutation types set",
                  "Mutations set sequential",
                  "Mutation one shot",
                  "Modified file path",
                  "Config"]

        rows = [[str(original),
                 str(changed),
                 str(thread_workspace),
                 str(mutation_types_set),
                 str(mutations_set_sequential),
                 str(mutation_one_shot),
                 str(modified_file_path),
                 str(cfg)]]

        try:
            f = open(modified_file_path, 'wb')
            f.write(current_sequence.getBytes())
            f.close()
            logging.warning('Saved modified file to: %s', str(modified_file_path))
        except:
            logging.critical('Cannot save modified file to: %s', str(modified_file_path))

        report_path = self.dir_path + "html_report_" + str(self.reports_count) + "_.html"
        code = htmlTable.create(header, rows)

        try:
            f = open(report_path, 'w')
            f.write(code)
            f.close()
            logging.warning('Saved HTML report No. %s to: %s', str(self.reports_count), str(modified_file_path))
        except:
            logging.debug('Cannot save HTML report No. %s to: %s', str(self.reports_count), str(modified_file_path))

        if self.reports_count == cfg.max_reports:
            logging.critical('Max reports count (%s) exceeded, terminating...', str(cfg.max_reports))
            exit(0)

        self.mutex.release()

class Output:
    stdout = None
    stderr = None
    retcode = None
    comparison_modes = None

    def __init__(self, stdout, stderr, retcode):
        self.stdout = copy.deepcopy(stdout)
        self.stderr = copy.deepcopy(stderr)
        self.retcode = copy.deepcopy(retcode)
        self.comparison_modes = MutatorConfig().output_comparison_modes

    def __str__(self):
        return str([self.stdout, self.stderr, self.retcode])

    def __eq__(self, other):
        if not self.comparison_modes:
            logging.critical('Output comparison modes is not set')
            exit(0)

        flag = True

        if ComparisonMode.STDOUT in self.comparison_modes:
            if self.stdout != other.stdout:
                flag = False

        if ComparisonMode.STDERR in self.comparison_modes:
            if self.stderr != other.stderr:
                flag = False

        if ComparisonMode.RETCODE in self.comparison_modes:
            if self.retcode != other.retcode:
                flag = False

        return flag

    def __ne__(self, other):
        return not self.__eq__(other)


class Executable:
    path = None
    workdir = None
    args = None
    default_output = None
    timeout = None

    def __init__(self, path, workdir, timeout=10, args=""):
        self.path = path
        self.workdir = workdir
        self.args = args
        self.timeout = timeout
        self.storeDefaultOutput()

    def execute(self):
        def target():
            logging.debug('Executable thread started')
            self.process = subprocess.Popen(self.path + " " + self.args,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            cwd=self.workdir)
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

    def isMatchOriginalOutput(self, output_with_modified_input_file):
        return self.default_output == output_with_modified_input_file

    def storeDefaultOutput(self):
        self.default_output = copy.deepcopy(self.execute())
        logging.debug('Original output: %s', str(self.default_output))

    def getOriginalOutput(self):
        return self.default_output

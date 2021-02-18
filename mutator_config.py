from enum import Enum


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class ComparisonMode(Enum):
    STDOUT = 1
    STDERR = 2
    RETCODE = 3

def getComparisonModeStr(mode):
    if mode == ComparisonMode.STDOUT:
        return 'STDOUT'
    if mode == ComparisonMode.STDERR:
        return 'STDERR'
    if mode == ComparisonMode.RETCODE:
        return 'RETCODE'
    return 'UNKNOWN'

@singleton
class MutatorConfig:
    executable_path = None
    executable_name = None
    additional_files = None
    file_path = None
    file_name = None
    regex = None
    timeout = None
    args = None
    threads = None
    workspace = None
    mutation_intensity = None
    stop_on_first_crash = None
    reports = None
    output_comparison_modes = None
    max_reports = None

    def __str__(self):
        comparison_modes_str = str([getComparisonModeStr(m) for m in self.output_comparison_modes])

        return str({"executable_path": self.executable_path,
                    "executable_name": self.executable_name,
                    "file_path": self.file_path,
                    "file_name": self.file_name,
                    "regex": self.regex,
                    "timeout": self.timeout,
                    "args": self.args,
                    "threads": self.threads,
                    "workspace": self.workspace,
                    "mutation_intensity": self.mutation_intensity,
                    "stop_on_first_crash": self.stop_on_first_crash,
                    "reports": self.reports,
                    "output_comparison_modes": comparison_modes_str})

from sequence import *
from logs import *
from colorlog import ColoredFormatter
import re
import os
import time


class ConfigParser:
    __path__ = None
    __name__ = None
    __field_separator = None
    __original_bytes__ = None
    __sequence__ = None

    def __init__(self, path, name, do_backup=True, backup_folder='backup'):
        self.__path__ = path
        self.__name__ = name
        try:
            f = open(self.__path__ + self.__name__, "rb")
            self.__original_bytes__ = f.read()
        except:
            logging.critical('Cannot read config')
            exit(1)

        if do_backup:
            dir_path = self.__path__ + backup_folder + '\\'
            if not os.path.exists(dir_path):
                try:
                    os.mkdir(dir_path)
                    logging.warning('Created config backup dir: %s', str(dir_path))
                except:
                    logging.critical('Cannot create backup directory')
                    exit(1)

            backup_path = dir_path + self.__name__ + str(int(time.time()))
            try:
                f = open(backup_path, 'wb')
                f.write(self.__original_bytes__)
                f.close()
                logging.debug('Config backup: %s', str(backup_path))
            except:
                logging.critical('Cannot write backup file')
                exit(1)

    def splitToChunks(self, field_separator):
        field_separator = b'(' + field_separator + b')'
        logging.warning('Used regex: %s', str(field_separator))

        self.__sequence__ = Sequence()
        splitted = re.split(field_separator, self.__original_bytes__)

        for s in splitted:
            if re.match(field_separator, s):
                logging.debug('Adding chunk %s as SEPARATOR', str(s))
                self.__sequence__.addChunk(s, ChunkType.SEPARATOR)
            else:
                logging.debug('Adding chunk %s as CONTENTS', str(s))
                self.__sequence__.addChunk(s, ChunkType.CONTENTS)

        logging.debug('Restored from chunks: %s', str(self.__sequence__.getBytes()))

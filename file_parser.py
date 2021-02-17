from sequence import *
from logs import *
import re
import os
import time


class FileParser:
    path = None
    name = None
    original_bytes = None
    sequence = None

    def __init__(self, path, name, do_backup=True, backup_folder='backup'):
        self.path = path
        self.name = name
        try:
            f = open(self.path + self.name, "rb")
            self.original_bytes = f.read()
        except:
            logging.critical('Cannot read file')
            exit(1)

        if do_backup:
            dir_path = self.path + backup_folder + '\\'
            if not os.path.exists(dir_path):
                try:
                    os.mkdir(dir_path)
                    logging.warning('Created file backup dir: %s', str(dir_path))
                except:
                    logging.critical('Cannot create backup directory')
                    exit(1)

            backup_path = dir_path + self.name + "_backup_" + str(int(time.time()))
            try:
                f = open(backup_path, 'wb')
                f.write(self.original_bytes)
                f.close()
                logging.debug('File backup: %s', str(backup_path))
            except:
                logging.critical('Cannot write backup file')
                exit(1)

    def splitToChunks(self, field_separator):
        field_separator = b'(' + field_separator + b')'
        logging.warning('Used regex: %s', str(field_separator))

        self.sequence = Sequence()
        splitted = re.split(field_separator, self.original_bytes)

        for s in splitted:
            if re.match(field_separator, s):
                logging.debug('Adding chunk %s as SEPARATOR', str(s))
                self.sequence.addChunk(s, ChunkType.SEPARATOR)
            else:
                logging.debug('Adding chunk %s as CONTENTS', str(s))
                self.sequence.addChunk(s, ChunkType.CONTENTS)

        logging.debug('Restored from chunks: %s', str(self.sequence.getBytes()))

    def getContentsChunksCount(self):
        if not self.sequence:
            return 0
        return self.sequence.getContentsChunksCount()

    def __getitem__(self, key):
        return self.sequence[key]

    def emplaceOriginalFile(self, modified_bytes):
        try:
            f = open(self.path + self.name, 'wb')
            f.write(self.modified_bytes)
            f.close()
        except:
            logging.critical('Cannot emplace original file')

    def getOriginalFileSequence(self):
        return self.sequence

import copy
from enum import Enum


class ChunkType(Enum):
    SEPARATOR = 1
    CONTENTS = 2


class Chunk:
    prev = None
    next = None
    contents = None
    type = None
    size = 0

    def __init__(self, contents, type):
        self.contents = copy.deepcopy(contents)
        self.size = len(self.contents)
        self.type = type


class Sequence:
    __head__ = None

    def addChunk(self, contents, type):
        if not self.__head__:
            self.__head__ = Chunk(contents, type)
        else:
            cur = self.__head__
            while cur.next:
                cur = cur.next
            cur.next = Chunk(contents, type)

    def getBytes(self):
        if not self.__head__:
            return ""

        contents = copy.deepcopy(self.__head__.contents)
        cur = self.__head__
        while cur.next:
            cur = cur.next
            contents += cur.contents
        return contents

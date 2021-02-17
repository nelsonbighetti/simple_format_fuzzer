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
    head = None

    def addChunk(self, contents, type):
        if not self.head:
            self.head = Chunk(contents, type)
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = Chunk(contents, type)

    def getBytes(self):
        if not self.head:
            return ""

        contents = copy.deepcopy(self.head.contents)
        cur = self.head
        while cur.next:
            cur = cur.next
            contents += cur.contents
        return contents

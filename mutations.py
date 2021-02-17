from enum import Enum
import copy
import sequence
import random


def addRandomBytesRight(chunk_in, N):
    right = bytearray(random.getrandbits(8) for _ in range(N))
    chunk_in.size += N
    chunk_in.contents += right
    return chunk_in


def addRandomBytesLeft(chunk_in, N):
    left = bytearray(random.getrandbits(8) for _ in range(N))
    chunk_in.size += N
    chunk_in.contents = left + chunk_in.contents
    return chunk_in


def addFFBytesLeft(chunk_in, N):
    left = bytearray(0xFF for _ in range(N))
    chunk_in.size += N
    chunk_in.contents = left + chunk_in.contents
    return chunk_in


def addFFBytesRight(chunk_in, N):
    right = bytearray(0xFF for _ in range(N))
    chunk_in.size += N
    chunk_in.contents = chunk_in.contents + right
    return chunk_in


def changeBytesToZeros(chunk_in):
    new_bytes = bytearray(0x00 for _ in range(chunk_in.size))
    chunk_in.contents = new_bytes
    return chunk_in


def changeBytesToFF(chunk_in):
    new_bytes = bytearray(0xFF for _ in range(chunk_in.size))
    chunk_in.contents = new_bytes
    return chunk_in


def replaceWithSingleZeroByte(chunk_in):
    chunk_in.size = 1
    chunk_in.contents = b'\x00'


mutationsMapSequential = {
    "addRandomBytesRight": addRandomBytesRight,
    "addRandomBytesLeft": addRandomBytesLeft,
    "addFFBytesLeft": addFFBytesLeft,
    "addFFBytesRight": addFFBytesRight
}

mutationsMapOneShot = {
    "changeBytesToZeros": changeBytesToZeros,
    "changeBytesToFF": changeBytesToFF,
    "replaceWithOneZeroByte": replaceWithSingleZeroByte
}

mutationTypesMap = {
    "sequential": mutationsMapSequential,
    "oneshot": mutationsMapOneShot
}

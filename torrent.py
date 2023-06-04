from pprint import pformat
import bencodepy
import copy
import hashlib

from file import File


class Torrent:
    def __init__(self, data):
        self._data = data

    @staticmethod
    def open(file):
        with open(file, "rb") as f:
            data = bencodepy.bdecode(f.read())
        return Torrent(data)

    @property
    def announce_url(self):
        return self._data[b"announce"].decode()

    @property
    def info_hash(self):
        return hashlib.sha1(bencodepy.encode(self._data[b"info"])).digest()

    @property
    def size(self):
        return sum(f.length for f in self.files)

    @property
    def piece_length(self):
        return self._data[b"info"][b"piece length"]

    @property
    def pieces_count(self):
        return len(self._data[b"info"][b"pieces"]) // 20

    def get_piece_hash(self, index):
        return self._data[b"info"][b"pieces"][index*20:index*20+20]

    @property
    def files(self):
        info = self._data[b"info"]

        # single file
        if b"length" in info:
            path = info[b"name"].decode()
            return [File(path, info[b"length"])]

        # multiple files
        files = []
        for data in info[b"files"]:
            parts = [info[b"name"]] + data[b"path"]
            path = b"/".join(parts).decode()
            files.append(File(path, data[b"length"]))
        return files

    def __str__(self):
        data = copy.deepcopy(self._data)
        data[b"info"][b"pieces"] = b"<OMITTED>"
        return pformat(data)

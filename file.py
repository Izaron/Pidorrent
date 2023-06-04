class File:
    def __init__(self, path, length):
        self._path = path
        self._length = length

    @property
    def path(self):
        return self._path

    @property
    def length(self):
        return self._length

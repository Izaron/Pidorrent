import bitstring
import os


class FileSaver:
    def __init__(self, torrent, file_filter):
        self._piece_len = torrent.piece_length
        self._used_pieces = bitstring.BitArray(bin="1"*torrent.pieces_count)

        self._files = []
        self._file_deltas = {}
        file_delta = 0
        for f in torrent.files:
            file_left = file_delta
            file_right = file_left + f.length
            file_delta = file_right

            if not file_filter(f):
                continue
            self._files.append(f)
            self._file_deltas[f] = file_left

            for i in range(file_left // self._piece_len, file_right // self._piece_len + 1):
                self._used_pieces[i] = True

        self._create_empty_files()

    def _create_empty_files(self):
        for f in self._files:
            pos = f.path.rfind("/")
            if pos != -1:
                dir_path = f.path[:pos]
                os.makedirs(dir_path, exist_ok=True)
            with open(f.path, "wb") as fd:
                fd.seek(f.length - 1)
                fd.write(b"\0")

    @property
    def used_pieces(self):
        return self._used_pieces

    def save_piece(self, piece, piece_id):
        # get piece bounds
        piece_left = piece_id * self._piece_len
        piece_right = piece_left + len(piece)

        # write piece in every file it affects
        for f in self._files:
            file_left = self._file_deltas[f]
            file_right = file_left + f.length
            
            part_left = max(file_left, part_left)
            part_right = min(part_right, part_right)

            if part_left < part_right:
                with open(f.path, "r+w") as fd:
                    fd.seek(part_left - file_left)
                    piece_part = piece[part_left - piece_left : part_right - piece_left]
                    fd.write(piece_part)

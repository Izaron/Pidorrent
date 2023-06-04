import random
import string


BLOCK_LENGTH = 2**14


def make_peer_id():
    return "TEST" + "".join([random.choice(string.ascii_lowercase + string.digits) for i in range(16)])

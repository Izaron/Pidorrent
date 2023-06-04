#!/usr/bin/env python3

import asyncio
import logging
import sys

from file_saver import FileSaver
from peer import Peer
from torrent import Torrent
from tracker import Tracker
from util import make_peer_id


logger = logging.getLogger(__name__)


async def main():
    torrent = Torrent.open(sys.argv[1])

    files = torrent.files
    logger.info(f"Files count: {len(files)}")
    for f in files:
        logger.info(f">>> \"{f.path}\", size {f.length}")

    def file_filter(file):
        return "Мы близко" in file.path
    file_saver = FileSaver(torrent, file_filter)

    peer_id = make_peer_id()
    logger.info(f"Peer id: {peer_id}")

    tracker = Tracker(torrent, peer_id)
    peers_info = await tracker.get_peers()
    peers = [Peer(torrent, file_saver, peer_id, ip_addr, port) for ip_addr, port in peers_info]
    logger.info(f"Have {len(peers)} peers")

    tasks = [p.download() for p in peers]
    await asyncio.gather(*tasks)

    for p in sorted(peers, key=lambda p: p.stats["downloaded"]):
        logger.info(f"{p} Downloaded {p.stats['downloaded']} bytes, pieces: {p.stats['pieces']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s", datefmt="%H:%M:%S")
    asyncio.run(main())

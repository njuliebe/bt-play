# -*- coding: utf-8 -*-

import shutil
import tempfile
import os.path as pt
import sys
import libtorrent as lt
import time
from time import sleep

def magnet2torrent(magnet, output_name=None):
    if output_name and \
            not pt.isdir(output_name) and \
            not pt.isdir(pt.dirname(pt.abspath(output_name))):
        print("Invalid output folder: " + pt.dirname(pt.abspath(output_name)))
        print("")
        sys.exit(0)
    tempdir = tempfile.mkdtemp()
    ses = lt.session()

    ses.add_dht_router('router.bittorrent.com', 6881)
    ses.add_dht_router('router.utorrent.com', 6881)
    ses.add_dht_router('router.bitcomet.com', 6881)
    ses.add_dht_router('dht.transmissionbt.com', 6881)
    ses.start_dht()

    params = {
        'save_path': tempdir,
        'duplicate_is_error': True
        # 'storage_mode': lt.storage_mode_t(2),
        # 'paused': False,
        # 'auto_managed': True
    }
    handle = lt.add_magnet_uri(ses, magnet, params)
    print("Downloading Metadata (this may take a while)")
    while (not handle.has_metadata()):
        try:
            sleep(1)
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            print("Cleanup dir " + tempdir)
            shutil.rmtree(tempdir)
            sys.exit(0)
    ses.pause()
    print("Done")
    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)
    output = pt.abspath(torinfo.name() + ".torrent")
    if output_name:
        if pt.isdir(output_name):
            output = pt.abspath(pt.join(
                output_name, torinfo.name() + ".torrent"))
        elif pt.isdir(pt.dirname(pt.abspath(output_name))):
            output = pt.abspath(output_name)
    print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print("Saved! Cleaning up dir: " + tempdir)
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)
    return output

def download_bt(file_path):

    ses = lt.session()
    ses.listen_on(6881, 6891)

    e = lt.bdecode(open(file_path, 'rb').read())
    info = lt.torrent_info(e)

    params = { 'save_path': '.', \
            'storage_mode': lt.storage_mode_t.storage_mode_sparse, \
            'ti': info }
    h = ses.add_torrent(params)

    s = h.status()
    while (not s.is_seeding):
            s = h.status()

            state_str = ['queued', 'checking', 'downloading metadata', \
                    'downloading', 'finished', 'seeding', 'allocating']

            # print s.state
            print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                    (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                    s.num_peers, s.state)

            time.sleep(1)


if __name__ == "__main__":
    magnet = "magnet:?xt=urn:btih:5d760bcf03cbcaa6c6015f652cc50193e4ecf175"
    output_name = "../resource/torrent"
    magnet2torrent(magnet=magnet, output_name=output_name)
    # bt_name = "./test.torrent"
    # download_bt(bt_name)

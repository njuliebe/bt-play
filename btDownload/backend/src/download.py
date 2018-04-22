# -*- coding: utf-8 -*-

import shutil
import tempfile
import os.path as pt
import sys
import libtorrent as lt
import time
from time import sleep
import datetime
import uuid
from concurrent.futures import ThreadPoolExecutor
import db

download_pool = ThreadPoolExecutor(max_workers=50)
default_movie_path = "../resource/movie/"
default_bt_path = "../resource/torrent"
cache = db.cache

def magnet2torrent(magnet):
    bt_path = default_bt_path
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
    # print("Downloading Metadata (this may take a while)")
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
    if bt_path:
        if pt.isdir(bt_path):
            output = pt.abspath(pt.join(
                bt_path, torinfo.name() + ".torrent"))
        elif pt.isdir(pt.dirname(pt.abspath(bt_path))):
            output = pt.abspath(bt_path)
    # print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print("Saved! Cleaning up dir: " + tempdir)
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)
    return output

def download_bt(magnet, movie_path, task_id):
    print "download"

    try:
        bt_path = magnet2torrent(magnet=magnet)

        ses = lt.session()
        ses.listen_on(6881, 6891)

        e = lt.bdecode(open(bt_path, 'rb').read())
        info = lt.torrent_info(e)

        params = { 'save_path': movie_path, \
                'storage_mode': lt.storage_mode_t.storage_mode_sparse, \
                'ti': info }
        h = ses.add_torrent(params)
        s = h.status()

        movie = db.Movie.query.filter_by(magnet=magnet).first()
        movie.name = info.name()
        db.db.session.commit()

        download = db.Download(taskid=task_id, name=info.name(), progress=0, speed=0, peer_nums=0)

        while (not s.is_seeding):
                s = h.status()

                state_str = ['queued', 'checking', 'downloading metadata', \
                        'downloading', 'finished', 'seeding', 'allocating']

                print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
                        (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                        s.num_peers, s.state)
                download.speed = '%.1f' % (s.download_rate/1000)
                download.progress = '%.2f' % (s.progress * 100)
                download.peer_nums = s.num_peers

                cache.set(task_id, download)
                time.sleep(1)
        movie.status = 1
        db.db.session.commit()
    except Exception as e:
        print e.message
        raise e


def pool_download(magnet):
    movie = db.Movie.query.filter_by(magnet=magnet).first()
    if movie:
        task_id = movie.taskid
        if movie.status is 1:
            return -1

    else:
        task_id = uuid.uuid4()
        movie = db.Movie(name='', magnet=magnet, taskid=task_id, status=0)
        movie.addtime = datetime.datetime.now().date()
        db.db.session.add(movie)
        db.db.session.commit()


    movie_path = default_movie_path
    future = download_pool.submit(download_bt, magnet, movie_path, task_id)

    return task_id, future



if __name__ == "__main__":
    magnet = "magnet:?xt=urn:btih:6823ead20e3b484ccdedff430d5ca839060e9fc5"
    task_id, future = pool_download(magnet)

    for i in range(30):
        download = cache.get(task_id)
        sleep(5)
        if download is not None:
            print download.speed, download.progress

    # print task_id, future.done()


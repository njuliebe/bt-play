1. deps
BeautifulSoup
requests

libtorrent
mac 安装：

brew update
brew install boost --build-from-source --with-python --universal
brew install libtorrent-rasterbar --enable-python-binding --with-python --with-boost-python=mt
sudo ln -s /usr/local/lib/python2.7/site-packages/libtorrent.so /Library/Python/2.7/site-packages/.
sudo ln -s /usr/local/lib/python2.7/site-packages/python_libtorrent-1.0.3-py2.7.egg-info /Library/Python/2.7/site-packages/.
import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import QApplication


class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self.setMinimumSize(1920, 1080)
        self.setMaximumSize(2000, 1080)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(QSize(1200,630))
        # render image
        # image = QImage(self.page().viewportSize(), QImage.Format_ARGB32).scaled(1200, 630)
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        cropped = image.copy(0,0,1200,630)
        painter = QPainter(cropped)
        frame.render(painter)
        painter.end()
        print('saving', output_file)
        cropped.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

s = Screenshot()
s.capture('https://www.96boards.org/blog/i2s-in-dragonboard410c/', 'website.png')
s.capture('http://96boards.org/about/', 'blog.png')
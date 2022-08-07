import os
from .downloader.scrape import Request
from .downloader.save import SaveVTOL
from .downloader.assort import Columns, Section
from .utils.config import HOMEPAGE_PATH, HOMEPAGE_URL

class Download:
    def __init__(self):
        self.html = self.get_home() or self.save_home()
        self.col = Columns(self.html)
        self.sec1 = Section(self.html, self.col.columns[0], 2)
        self.sec2 = Section(self.html, self.col.columns[1], 3)

    def all(self):
        self.save_section(self.sec1)
        self.save_section(self.sec2)

    def save_section(self, sec):
        items = self._get_items(sec)
        self.save_items(sec, items)

    def get_home(self):
        try:
            with open(HOMEPAGE_PATH, "r") as file:
                html = file.read()
                return html
        except FileNotFoundError:
            return None

    def save_home(self):
        req = Request(HOMEPAGE_URL)
        res = req.send_request()
        self.check_html_dirs()
        with open(HOMEPAGE_PATH, "w") as file:
            file.write(res.text)
        return res.text

    @staticmethod
    def save_items(sec, items):
        for item in items:
            topic, detail = getattr(sec, item)
            save_handler = SaveVTOL(topic, detail)
            save_handler.save()

    @staticmethod
    def _get_items(sec):
        return [var for var in dir(sec) if var.startswith('items')]

    @staticmethod
    def check_html_dirs():
        if not os.path.exists("html_samples"):
            os.makedirs("html_samples/main")
            os.makedirs("html_samples/detail")

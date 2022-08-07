import os
from time import sleep
from .scrape import Request
from evtol.utils.config import DETAIL_PATH

class SaveVTOL:
    def __init__(self, title, lis):
        self.title = self.suitable_file_name(title)
        self.lis = lis

    def save(self):
        item_number = 1
        for li in self.lis:
            path = self.check_directory(self.title)
            name = self.suitable_file_name(li.find('a').text)
            file_name = path + str(item_number) + "." + name  + ".html"
            if os.path.isfile(file_name):
                if os.path.getsize(file_name) > 0:
                    item_number += 1
                    continue
            with open(file_name, 'w') as f:
                url = li.find('a').get('href')
                req = Request(url)
                response = req.send_request()
                f.write(response.text)
            item_number += 1
            sleep(1)

    @staticmethod
    def suitable_file_name(name):
        name = name.replace(' ', '')
        name = name.replace('/', '_')
        return name

    @staticmethod
    def check_directory(title):
        path = DETAIL_PATH + title + "/"
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path)
        return path

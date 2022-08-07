import os, sys
from bs4 import BeautifulSoup
from evtol.utils.progress import progressBar
from collections import OrderedDict

class Extract:
    def __init__(self, html, path):
        self.html = html
        self.path = path
        self.soup = self._get_soup()

    def _get_soup(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        return soup

    def get_main(self):
        content = self.soup.find("div", {"class": "content-page"})
        try:
            main = content.find("div", {"class": "row"})
        except:
            try:
                h1 = self.soup.find("h1").text
            except:
                return None
            if h1 is not None:
                if h1.find("Something went wrong")>1:
                    main = None
                else:
                    print("ERROR:", self.path)
                    sys.exit(1)
            else:
                print("ERROR:", self.path)
                sys.exit(1)
        return main

    @staticmethod
    def get_specifications(main):
        if main is not None:
            output_ps = []
            ps = main.find_all("p")
            for p in ps:
                strong = p.find('strong')
                if strong is not None:
                    strong = strong.text.replace(' ', '')
                    if strong.startswith("Specification"):
                        ul = p.next_sibling.next_sibling
                        if ul is None:
                            print("ERROR: EMPTY UL")
                        output_ps.append(ul)
            return output_ps

class Convert:
    converted_data = OrderedDict()

    def __init__(self, path):
        self.path = path

    def execute(self):
        titles = os.listdir(self.path)
        for title in titles:
            files_path = self.path + "/" + title
            file_names = os.listdir(files_path)
            file_names = self.sort_files(file_names)
            self.converted_data[title] = {}
            for file_name in progressBar(file_names, prefix=title , suffix='', fill='=', length=50):
                full_path = files_path + "/" + file_name
                with open(full_path, "r") as file:
                    html = file.read()
                    self.conv_li(title, file_name, html)

    def conv_li(self, title, file_name, html):
        ext = Extract(html, self.path)
        main = ext.get_main()
        res = ext.get_specifications(main)
        vtol = file_name.replace('.html', '')
        if res:
            res = res[0]
            lis = res.find_all('li')
            li_dict = {}
            self.converted_data[title][vtol] = OrderedDict()
            for li in lis:
                try:
                    self.conv_pair(li_dict, li, ':')
                except IndexError:
                    try:
                        self.conv_pair(li_dict, li, ';')
                    except:
                        continue
                self.converted_data[title][vtol] = li_dict

    def conv_pair(self, li_dict, li, item):
        li_pair = li.text.split(':')
        li_topic = li_pair[0]
        li_dict[li_topic] = self.clean(li_pair[1])

    @staticmethod
    def sort_files(files):
        temp_dict = dict()
        sorted_files = list()
        for i, file in enumerate(files):
            temp_dict[i] = int(file.split('.')[0])
        sorted_dict = OrderedDict(sorted(temp_dict.items(), key=lambda item: item[1]))
        for key, value in sorted_dict.items():
            sorted_files.append(files[key])
        return sorted_files

    @staticmethod
    def clean(detail):
        return detail.replace(';', ',')

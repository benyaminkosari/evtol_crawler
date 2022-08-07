from bs4 import BeautifulSoup

class Extract:
    def __init__(self, html):
        self.html = html
        self.soup = self._get_soup()

    def _get_soup(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        return soup

    def get_main(self):
        rows = self.soup.find("div", {"class": "main"})
        return rows

    @staticmethod
    def get_rows(soup):
        rows = soup.find_all("div", {"class": "row"})
        return rows

    @staticmethod
    def get_columns(soup):
        columns = soup.find_all("div", {"class": "col-sm-6"})
        return columns

    @staticmethod
    def get_p(soup):
        p = soup.find("p")
        return p


class Convert:
    def __init__(self, html):
        self.ext = Extract(html)

    def retrieve_first_items(self, col):
        p = self.ext.get_p(col)
        ol = self.find_next(p, 'ol')
        lis = self.get_items(ol)
        return p, ol, lis

    def retrieve_next_items(self, ol):
        col_next_p = self.find_next(ol, 'p')
        next_ol = self.find_next(col_next_p, 'ol')
        lis = self.get_items(next_ol)
        return col_next_p, next_ol, lis

    @staticmethod
    def get_items(soup):
        lis = soup.find_all("li")
        return lis

    @staticmethod
    def find_next(soup, type):
        next = soup.findNext(type)
        return next

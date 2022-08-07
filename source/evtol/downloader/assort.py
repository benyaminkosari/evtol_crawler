from bs4.element import Tag
from .convert import Extract, Convert

class Columns:
    def __init__(self, html):
        self.ext = Extract(html)
        self.columns = self.get_columns()

    def get_columns(self):
        main = self.ext.get_main()
        columns = self.ext.get_columns(main)
        return columns


class SectionBase:
    def __init__(self, html:str, columns:Tag):
        self.conv = Convert(html)

    def __post_init__(self, title_count:int):
        for i in range(title_count-1):
            try:
                self._get_items(i)
            except AttributeError:
                break

    @property
    def items_1(self) -> tuple[str, Tag]:
        pass

    def _get_items(self, columns:Tag):
        pass


class Section(SectionBase):
    def __init__(self, html, columns, title_count):
        super().__init__(html, columns)
        self.p1, self.ol1, self.lis1 = self.conv.retrieve_first_items(columns)
        super().__post_init__(title_count)

    @property
    def items_1(self):
        return self.p1.find('strong').text, self.lis1

    def _get_items(self, count):
        this_ol = getattr(self, 'ol'+str(count+1))
        new_p, new_ol, new_lis = self.conv.retrieve_next_items(this_ol)
        self._set_attrs(new_p, new_ol, new_lis, count)

    def _set_attrs(self, new_p, new_ol, new_lis, count):
        setattr(self, 'p'+str(count+2), new_p)
        setattr(self, 'ol'+str(count+2), new_ol)
        setattr(self, 'lis'+str(count+2), new_lis)
        setattr(self, 'items_'+str(count+2), (new_p.find('strong').text, new_lis))

from typing import List
from bs4 import BeautifulSoup, SoupStrainer, Tag
from ..utils.get_page import get_page, LinkGP


class StaffPageParser:
    def __init__(self, page_url):
        self._url = page_url
        self._page_content = ""
        self._page_soup = ""
        self._current_role = None

        self.actors = []
        self.directors = []
        self.producers = []
        self.voice_directors = []
        self.translators = []
        self.voices = []
        self.writers = []
        self.operators = []
        self.composers = []
        self.designs = []
        self.editors = []

        self.cachedir = None
        self.cachetime = None

    @property
    def full(self):
        return {
            'actors': self.actors,
            'directors': self.directors,
            'producers': self.producers,
            'voice_directors': self.voice_directors,
            'translators': self.translators,
            'voices': self.voices,
            'writers': self.writers,
            'operators': self.operators,
            'composers': self.composers,
            'designs': self.designs,
            'editors': self.editors
        }

    def start(self):
        self.parse()

    def parse(self):
        self.get_page()
        self.create_soup()
        self.walk()

    def get_page(self):
        request = get_page(LinkGP(self._url), cachedir=self.cachedir, cachetime=self.cachetime)
        if request:
            self._page_content = request.content

    def create_soup(self):
        strainer = SoupStrainer("div", class_='block_left')
        if self._page_content:
            self._page_soup = BeautifulSoup(self._page_content, 'lxml', parse_only=strainer)

    def walk(self):
        if self._page_soup:
            block_left = self._page_soup.find("div", class_='block_left')
            for child in block_left.children:
                # Update _current_role
                if isinstance(child, Tag) and child.name == 'a' and child.has_attr("name"):
                    self._current_role = child.attrs['name'] + 's'
                # Save person
                if isinstance(child, Tag) and self._current_role and child.has_attr('class') and 'dub' in child.attrs['class']:
                    role_list = getattr(self, self._current_role)  # type: List
                    div_name = child.find("div", class_="name")
                    div_photo = child.find("div", class_="photo")
                    role_list.append({
                        'id': int(''.join([i for i in div_name.a.attrs['href'] if i.isdigit()])),
                        'nameru': div_name.a.text,
                        'nameen': div_name.span.text,
                        'photo': 'https://st.kp.yandex.net' + div_photo.find("img").attrs['title'],
                        'role': self._current_role[0:-1]
                    })
                    setattr(self, self._current_role, role_list)

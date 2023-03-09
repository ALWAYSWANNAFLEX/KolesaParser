import re

import bs4
import requests
from pirelli_enum import PirelliReplace

class ParseSibirKoleso:
    def __init__(self, mark, size, model):
        self.mark = mark.lower().split(' ')
        self.size = size.replace('x', '/')
        self.width = self.size.split('/')[0] if '/' in self.size else self.size.split('R')[0]
        self.height = self.size.split('/')[1].split('R')[0] if '/' in self.size else ''
        self.diameter = self.size.split('R')[1]
        self.model = model.replace('(*)', '').replace('*', '').replace('+', '').replace('(', '').replace(')', '')
        self.host = 'https://sibirkoleso.ru/tyres/filter'
        self.filter_size_url = '/width-is-' + self.width + ('/height-is-' + self.height if self.height != '' else '') + '/diametr-is-' + self.diameter
        self.filter_brand_url = '/brand-is-'
        self.filter_season_url = '/season-is-letnie-shiny'
        self.filter_type_url = '/type-is-legkovye-avto/apply/'
        self.filter_full_url = self.host + self.filter_size_url + self.filter_brand_url + self.mark[0] + \
                               self.filter_season_url + self.filter_type_url

        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept-language': 'ru',
            'referer': 'https://www.google.com/'
        }

    def filter_spaces(self, str):
        if(str == ''):
            return False
        else:
            return True

    def parse_model(self):
        model_trim_sizes = self.model.replace(self.width + '/', '').replace(self.height, '').replace('R ' + self.diameter, '').replace('ZR ' + self.diameter, '').lower()
        for brand in self.mark:
            model_trim_brand = model_trim_sizes.replace(brand, ' ')
            model_trim_sizes = model_trim_brand
        split_by_spaces = model_trim_brand.split(' ')
        filter_obj = filter(self.filter_spaces, split_by_spaces)
        return list(filter_obj)

    def run(self):
        res = self.session.get(url=self.filter_full_url, headers=self.session.headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        items = soup.find_all('div', {'class': 'catalog__item'})
        if(len(items) == 0):
            return 'Не найдено'
        else:
            parsed_brand = items[0].select_one('div.brand > strong').text.lower()
            if(parsed_brand != self.mark[0]):
                return 'Не найдено'
            else:
                compare_count_array = []
                for item in items:
                    model_tag = item.select('div.catalog__item__info > p > a > span')
                    text = model_tag[0].get_text().lower().replace(' ', '')
                    compare_count = 0
                    for compare_item in self.parse_model():
                        if 'pirelli' in self.mark:
                            compare_item = PirelliReplace(compare_item).run()
                        if(len(re.findall(compare_item, text)) > 0):
                            compare_count = compare_count + 1
                    compare_count_array.append(compare_count)
                max_compare = max(compare_count_array)
                if(len(self.parse_model()) - max_compare > len(self.parse_model()) - 1):
                    return 'Не найдено'
                else:
                    index_of_max = compare_count_array.index(max_compare)
                    finded_element = items[index_of_max]
                    finded_element_price = finded_element.select('div.catalog__item__price-value > strong')[0].text
                    return finded_element_price
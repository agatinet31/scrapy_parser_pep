import re

import scrapy

from pep_parse.exceptions import PEPParseError, PEPStatusNameError
from pep_parse.items import PepParseItem
from pep_parse.settings import PEP_NUMBER_AND_NAME_PATTERN, VALID_STATUS


class PepSpider(scrapy.Spider):
    """Класс паука по документации PEP."""
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """"Парсинг списка документов PEP по ссылкам из таблицы."""
        all_peps_link = response.xpath(
            '//*[@id="numerical-index"]'
            '//*/td[2]/a[@class="pep reference internal"]/@href'
        )
        for pep_link in all_peps_link:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсинг страницы PEP с документами и формирование Items."""
        pep_title = ''.join(
            response.xpath('//*/h1[@class="page-title"]//text()').getall()
        ).strip()
        pep_info = re.search(
            PEP_NUMBER_AND_NAME_PATTERN,
            pep_title
        )
        if pep_info is None:
            raise PEPParseError(
                'Ошибка получения номера и наименования PEP '
                f'со страницы: {response.url}!'
            )
        pep_number, pep_name = pep_info.groups()
        pep_status = response.css(
            '#pep-content > dl > dt:contains("Status") + dd > abbr::text'
        ).get()
        if not pep_status:
            raise PEPParseError(
                f'Ошибка получения статуса PEP {pep_number}!'
            )
        if pep_status not in VALID_STATUS:
            raise PEPStatusNameError(
                f'Невалидный статус PEP {pep_number} '
                f'в карточке: {pep_status}. '
                f'Страница PEP: {response.url}'
            )
        yield PepParseItem(
            number=pep_number,
            name=pep_name,
            status=pep_status
        )

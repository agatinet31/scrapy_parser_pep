import csv
import datetime as dt
from collections import defaultdict

from scrapy.exceptions import DropItem

from pep_parse.settings import (BASE_DIR, DATETIME_FORMAT, RESULTS_DIR,
                                TABLE_FOOTER_STATUS_TOTAL,
                                TABLE_HEADER_STATUS_COUNT)


class PepParsePipeline:
    """Класс Pipeline для сохранения результатов по статусам PEP."""
    def open_spider(self, spider):
        self.peps_status_count = defaultdict(int)

    def process_item(self, item, spider):
        try:
            pep_status = item['status']
            self.peps_status_count[pep_status] += 1
        except KeyError:
            raise DropItem(
                'В Item отсутствует значение статуса(ключ=`status`)!'
            )
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / RESULTS_DIR
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        table_pep_status = [
            TABLE_HEADER_STATUS_COUNT,
            *sorted(self.peps_status_count.items()),
            (TABLE_FOOTER_STATUS_TOTAL, sum(self.peps_status_count.values())),
        ]
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(table_pep_status)
        spider.logger.info(f'Файл с результатами был сохранён: {file_path}')

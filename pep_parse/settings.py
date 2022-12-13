from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PEPS_URL = 'https://peps.python.org/'

BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']

NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

LOG_ENABLED = True

LOG_LEVEL = 'INFO'

HTTP_CACHE = True

HTTPCACHE_ENABLED = True

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

RESULTS_DIR = 'results'

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    f'{RESULTS_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

VALID_STATUS = {
    status for statuses in EXPECTED_STATUS.values() for status in statuses
}

PEP_NUMBER_AND_NAME_PATTERN = r'PEP (?P<number>\d+) – (?P<name>.*)'

TABLE_HEADER_STATUS_COUNT = ('Статус', 'Количество')

TABLE_FOOTER_STATUS_TOTAL = 'Total'

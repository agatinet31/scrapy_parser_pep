import scrapy


class PepParseItem(scrapy.Item):
    """Класс Item информации по документу PEP."""
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()

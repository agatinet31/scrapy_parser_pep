class PEPParseError(Exception):
    """
    Вызывается, когда парсер не может найти номер и наименование документа.
    """
    pass


class PEPStatusNameError(Exception):
    """
    Вызывается, когда парсер возвращает невалидное имя статуса.
    """
    pass

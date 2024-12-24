from django.core.exceptions import ImproperlyConfigured
from kinder.settings import conf


def get_param(section, name, default):
    result = str(conf.get(section, name))
    return result or default


# Директория, предназначенная для хранения xml отчетов
XML_SAVING_DIRECTORY_PATH = get_param(
    'gisdo', 'XML_SAVING_DIRECTORY_PATH', None)


if XML_SAVING_DIRECTORY_PATH is None:
    raise ImproperlyConfigured(
        'Укажите путь до директории, предназначенной для хранения xml отчетов')

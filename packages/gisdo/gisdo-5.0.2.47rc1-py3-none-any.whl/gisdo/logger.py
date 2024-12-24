# coding:utf-8

from __future__ import absolute_import

import logging
import logging.handlers
import os

from django.conf import settings as dj_settings
from future.builtins import object

from . import settings


class Logger(object):
    """
    Для удобства логирования
    """

    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'

    LEVELS = [INFO, ERROR, WARNING]

    _logger = logging.getLogger('suds.client')
    _logger.setLevel(logging.INFO)

    _fh = logging.handlers.TimedRotatingFileHandler(
        os.path.join(dj_settings.LOG_PATH, settings.GISDO_LOG_FILE),
        when='D', encoding='utf-8')
    _fh.setFormatter(logging.Formatter(
        '[%(asctime)s] - %(levelname)s - %(message)s'))

    _logger.addHandler(_fh)

    @classmethod
    def add_record(cls, message, level=INFO):
        """
        Добавляем сообщение в файл с логами + сохраняем в БД
        """

        assert level in Logger.LEVELS

        # Записываем в файл
        level_method = getattr(Logger._logger, level)
        level_method(message)

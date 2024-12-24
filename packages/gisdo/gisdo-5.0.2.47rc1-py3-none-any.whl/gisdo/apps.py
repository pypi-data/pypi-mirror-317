# coding: utf-8

from __future__ import absolute_import

from django.apps import AppConfig


class GisdoConfig(AppConfig):

    name = 'gisdo'
    label = 'gisdo'
    verbose_name = u"фед. отчетность"

    def ready(self):
        from . import signals

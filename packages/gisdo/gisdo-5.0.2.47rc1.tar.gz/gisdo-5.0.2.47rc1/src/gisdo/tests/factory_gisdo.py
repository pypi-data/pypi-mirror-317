# coding: utf-8

from future.builtins import object
import factory

from gisdo.models import GisdoUnit
from kinder.core.unit.tests import factory_unit


class GisdoUnitFactory(factory.DjangoModelFactory):

    class Meta(object):
        model = GisdoUnit

    unit = factory.SubFactory(factory_unit.UnitDouFactory)

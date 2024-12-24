# -*- coding: utf-8 -*-

u"""Модуль содержит определение таблиц SQLA."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table

from gisdo.settings import engine


Base = declarative_base()


class AlchemyDeclaration(Base):
    u"""Заявления."""

    __table__ = Table(
        'declaration', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyDeclarationUnit(Base):
    u"""Желаемые организации."""

    __table__ = Table(
        'declaration_unit',
        Base.metadata, autoload=True, autoload_with=engine)


class AlchemyUnit(Base):
    u"""Учреждения."""

    __table__ = Table(
        'unit', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyChildren(Base):
    u"""Дети."""

    __table__ = Table(
        'children', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyWorkType(Base):
    u"""Режимы работы."""

    __table__ = Table(
        'work_type', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyDeclarationStatus(Base):
    u"""Статус заявления."""

    __table__ = Table(
        'declaration_status',
        Base.metadata, autoload=True, autoload_with=engine)


class AlchemyGroup(Base):
    u"""Группы."""

    __table__ = Table(
        'group', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyPupil(Base):
    u"""Ученики."""

    __table__ = Table(
        'pupil', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyGroupType(Base):
    u"""Типы групп."""

    __table__ = Table(
        'group_type', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyGroupWorkType(Base):
    u"""Режимы работы групп."""

    __table__ = Table(
        'work_type', Base.metadata, autoload=True, autoload_with=engine)

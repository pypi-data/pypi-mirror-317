from __future__ import absolute_import

from m3.plugins import ExtensionHandler
from m3.plugins import ExtensionManager
from m3.plugins import ExtensionPoint

from kinder.controllers import dict_controller

from .actions import GisdoReportFormDictPack
from .actions import GisdoUnitDictPack
from .actions import ReportFormActionPack
from .extensions import get_gisdo_unit_pack_perm_dict


def register_actions():
    dict_controller.packs.extend([
        ReportFormActionPack(),
        GisdoUnitDictPack(),
        GisdoReportFormDictPack()
    ])


def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(ExtensionPoint(
        name='gisdo.extensions.get_gisdo_unit_pack_perm_dict',
        default_listener=ExtensionHandler(
            handler=get_gisdo_unit_pack_perm_dict),
    ))

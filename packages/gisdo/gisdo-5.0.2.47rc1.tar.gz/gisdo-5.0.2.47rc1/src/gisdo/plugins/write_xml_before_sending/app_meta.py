from m3.plugins import ExtensionHandler
from m3.plugins import ExtensionManager
from m3.plugins import ExtensionPoint


from .extensions import write_xml


def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(ExtensionPoint(
        name='write_xml',
        default_listener=ExtensionHandler(handler=write_xml)
    ))

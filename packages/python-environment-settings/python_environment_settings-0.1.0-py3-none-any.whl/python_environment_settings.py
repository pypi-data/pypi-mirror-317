import os
from null_object import Null

SETTING_OBJECTS = []


def add_settings(settings):
    if not settings in SETTING_OBJECTS:
        SETTING_OBJECTS.append(settings)


def clear_settings():
    for i in range(len(SETTING_OBJECTS) - 1, -1, -1):
        del SETTING_OBJECTS[i]


def get(key, default=None, aliases=None):
    """获取配置项。优先从环境变量中获取配置项。后面依次从其它配置源中获取。"""
    aliases = aliases or []
    if isinstance(aliases, str):
        aliases = [aliases]
    if isinstance(key, str):
        keys = [key]
    else:
        keys = key
    keys += aliases
    for key in keys:
        value = os.environ.get(key, Null)
        if value is not Null:
            return value
    for settings in SETTING_OBJECTS:
        for key in keys:
            if isinstance(settings, dict):
                value = settings.get(key, Null)
            else:
                value = getattr(settings, key, Null)
            if value is not Null:
                return value
    return default

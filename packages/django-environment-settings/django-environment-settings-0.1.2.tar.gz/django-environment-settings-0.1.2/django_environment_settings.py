from django.conf import settings
import python_environment_settings

python_environment_settings.add_settings(settings)


def get(key, default, aliases=None):
    """从环境变量或`djang.conf.settings`中获取配置。"""
    return python_environment_settings.get(
        key=key,
        default=default,
        aliases=aliases,
    )

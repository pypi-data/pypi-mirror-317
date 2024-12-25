# django-environment-settings

允许Django应用从settings.py或环境变量中获取配置。

## 安装

```shell
pip install django-environment-settings
```

## 使用

*app/settings.py*

```python
import django_environment_settings

APP_CONFIG1 = django_environment_settings.get(
    "APP_CONFIG_KEY1",
    "DEFAULT_VALUE",
    aliases=[
        "APP_CONFIG_KEY1_ALIAS1",
        "APP_CONFIG_KEY1_ALIAS2"
    ],
)
```

## 版本

### 0.1.1

- 版本首发。

### 0.1.2

- 使用`python_environment_settings`以增强兼容性。

# python-environment-settings

简易的配置项获取方式，支持添加多种配置项获取源。默认从环境变量中获取配置项。

## 安装

```shell
pip install python-environment-settings
```

## 使用

```python
from django.conf import settings
import python_environment_settings

python_environment_settings.add_settings(settings)

CONFIG1 = python_environment_settings.get(
    "CONFIG1",
    default="DEFAULT_VALUE1",
    aliases=[
        "config1",
        "item1",
        "key1",
    ]
)
```

## 版本记录

### v0.1.0

- 版本首发。

# Flywheel-FnCollector

可能是个设想：通过设计一个`FnCollector`，简化现有[Ryanvk Flywheel](https://github.com/GreyElaina/RvFlywheel)中定义`Fn`的流程。

此外添加了一些对后续工作可能有用的东西。

## Project Structure

> 注：标记为`分发包未提供`的文件需要自行从仓库获取，且相关链接失效。

```text
Flywheel-FnCollector
├── demo_*.py ················· 示例代码 (分发包未提供)
├── pdm.lock ·················· PDM 锁定文件 (分发包未提供)
├── pyproject.toml ············ 项目依赖 (PDM)
├── README.md ················· 项目介绍
└── src ······················· 项目源码
    └── flywheel_extras ······· 模块名
        ├── __init__.py ······· 模块入口
        ├── collector.py ······ FnCollector 相关定义
        ├── deprecated.py ····· 已弃用类/函数定义
        ├── instance.py ······· InstanceOf 扩展
        ├── overload.py ······· FnOverload 扩展
        ├── utils.py ·········· 工具函数定义
        ├── protocol.py ······· 内部定义 Protocol 相关
        └── typing.py ········· 类型提示/检查相关
```

## Usage

### FnCollector

```python
from flywheel import SimpleOverload

from flywheel_extras import FnCollector


@FnCollector.set(SimpleOverload('name'), as_default=True)
def greet(name: str) -> str:  # This will become default implementation
    return f'Ordinary, {name}.'


@greet.collect(name='Teague')
def greet_teague(name: str) -> str:
    return 'Stargaztor, but in name only.'


@greet.collect(name='Grey')
def greet_grey(name: str) -> str:
    return 'Symbol, the Founder.'
```

```pycon
>>> greet('Teague')
'Stargaztor, but in name only.'
>>> greet('Grey')
'Symbol, the Founder.'
>>> greet('Hizuki')
'Ordinary, Hizuki.'
```

可以输入多个`FnOverload`，调用时会采取一些数学手段匹配最佳实现；
也可以不输入任何`FnOverload`，此时会自动创建空的`SimpleOverload`。

`FnCollector`支持在类中定义，调用时会自动添加self参数。

```python
from flywheel import SimpleOverload

from flywheel_extras import FnCollector


class Action:
    @FnCollector.set(SimpleOverload('name'))
    def func_n(self, name: str) -> str: ...

    @classmethod
    @FnCollector.set(SimpleOverload('name'))
    def func_c(cls, name: str) -> str: ...

    @property  # 可以定义，但没什么用，也不推荐这么做
    @FnCollector.set(as_default=True)
    def func_p(self) -> str:
        return ''

    @staticmethod
    @FnCollector.set(SimpleOverload('name'))
    def func_s(name: str) -> str: ...


# FnCollector.collect(Ellipsis) will not raise error, see below.
@Action.func_n.collect(...)
def impl_n(self: Action, name: str) -> str: ...


# property.fget here
@Action.func_p.fget.collect(...)  # noqa
def impl_p(self: Action) -> str: ...
```

> [!WARNING]
>
> `FnCollector`改变了存在重复实现时调用顺序：在同一个`CollectContext`下，优先选择**最后定义**的实现；
> 不同`CollectContext`下逻辑与原版一致。
>
> 这么做是为了方便后续在其他项目中实现外挂重载功能。

### Namespace & Context

`FnCollector`采用动态定义`FnCollectEndpoint`的方式，这意味着你可以放心在全局上下文中使用相同命名的`FnOverload`。

此外项目加入了`Namespace`用于模拟Legacy Ryanvk中`Perform`。

```pycon
>>> @greet.collect(123, name='Grey')  # Namespace is 123
... def greet_grey_123(name: str) -> str:
...     return '1111'
... 
>>> greet('Grey')
'Symbol, the Founder.'
>>> greet.call(None, 'Grey')  # Same as greet('Grey'), namespace is None
'Symbol, the Founder.'
>>> greet.call(123, 'Grey')  # Namespace is 123
'1111'
```

默认上下文收集方式与`local_collect`相同。
根据[文档说明](https://github.com/GreyElaina/RvFlywheel/blob/main/README.zh.md#scoped_collect)，
项目将避免使用`scoped_collect`。

对于`CollectContext`与`InstanceContext`，写法与原版一致，具体示例见[`demo_collector.py`](demo_collector.py)。

### FnOverload

`FnOverload`的本质是根据`call_value`在`scope`中查找对应`collect_value`的函数。
`SimpleOverload`中`collect_value`与`call_value`是等价的。

因此，根据`collect_value`与`call_value`之间的关系，
项目参考`SimpleOverload`实现了基于映射关系的`MappingOverload`和基于谓词的`PredicateOverload`。

各`FnOverload`匹配方式如下：

```text
SimpleOverload: call_value == collect_value
TypeOverload: type(call_value) == collect_value
MappingOverload: mapping[call_value] == collect_value
PredicateOverload: predicate(collect_value, call_value) == True
```

具体示例见[`demo_overload.py`](demo_overload.py)。

### InstanceOf

项目添加了`OptionalInstanceOf`描述符，在找不到实例时使用默认值。

具体示例见[`demo_collector.py`](demo_collector.py)。

> [!WARNING]
>
> 据魔女所述，`InstanceOf`可能会在未来被弃用，因此不再推荐使用。
>
> 作为替代，下文实现了一种类似于`Staff`的跨类读取实例的方法。

### Cross Collection

大概是一种`Staff`/`InstanceOf`的替代方案。

你可以在一个类里定义重载函数，在另一个类里定义实现。这两个类要求继承自同一个数据类，且该数据类实现了`__cross__`方法。

```python
class SomePerform:
    ...

    @classmethod
    def __cross__(cls, other: 'SomePerform') -> 'SomePerform':
        ...
```

数据类就是字面意思，不需要`dataclass`。

具体示例见[`demo_cross_class.py`](demo_cross_class.py)。

> 可以不要求同一个数据类，但在需要调用`__cross__`的场合至少不应该报错。

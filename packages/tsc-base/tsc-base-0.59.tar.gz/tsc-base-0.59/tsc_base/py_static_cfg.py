import inspect
from typing import Any, Iterator, Union, TypeVar, Tuple, Callable, List, Optional, get_type_hints, Dict
from itertools import islice
from datetime import datetime
from copy import deepcopy
import random
import string
import re
try:
    from .func import cover_dict
except:
    from func import cover_dict

T = TypeVar('T')


def generate_random_string(length: int):
    """生成长度为 length 的随机字符串, 由大小写字母和数字组成"""
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(characters, k=length))


def create_unduplicated_key(init_key: str, keys: set, max_len: int = 8) -> str:  # isidentifier
    """创建一个不重复的 key

    Args:
        init_key (str): 初始的key, 会在这个key后面加上 _{随机字符串} 直到不重复
        keys (set): 已经存在的key
        max_len (int, optional): 随机字符串的最大长度

    Returns:
        str: 不重复的key
    """
    i = 0
    key = init_key
    while key in keys:
        i += 1
        key = f"{init_key}_{generate_random_string(min(i, max_len))}"
    return key


def unique_list_with_none(lst):
    """使用集合去重，同时保持顺序"""
    seen = set()
    seen_add = seen.add  # 本地函数，提高性能
    # 使用生成器表达式保留 None 值并去除其他重复项
    return [x for x in lst if x is None or not (x in seen or seen_add(x))]


class KeyNotFound:
    """用于标记 key 不存在的返回结果"""
    def __init__(self, use_raise: bool = False):
        self.use_raise = use_raise  # 是否使用抛出异常的方式
    
    def __bool__(self) -> bool:
        if self.use_raise:
            raise KeyError('KEY_NOT_FOUND')
        return False

    def __repr__(self) -> str:
        if self.use_raise:
            raise KeyError('KEY_NOT_FOUND')
        return "KEY_NOT_FOUND"


KEY_NOT_FOUND = KeyNotFound()


class SafeAttributeAccessor(type):
    def __getattr__(cls: 'Cfg', key: str) -> Union[Any, KeyNotFound]:
        """用点访问时，默认允许不存在的属性"""
        return cls._get_(key, default=KEY_NOT_FOUND, allow_default=not KEY_NOT_FOUND.use_raise)
    
    # def __setattr__(cls: 'Cfg', key: str, value: Any):
    #     """用点访问赋值时，更标准的设置属性"""
    #     cls._set_(key, value)  # 这会导致失去全覆盖的能力

    def __getitem__(cls: 'Cfg', key: Union[str, int]) -> Union[Any, KeyNotFound]:
        """可以用 [] 访问静态变量"""
        return cls._get_(key)

    def __setitem__(cls: 'Cfg', key: Union[str, int], value):
        """用 [] 访问赋值时，更标准的设置属性"""
        cls._set_(key, value)


class Cfg(metaclass=SafeAttributeAccessor):
    def __init__(self, recursive: bool = False):
        """配置类的基类, 不可以直接用基类作为配置类, 只能作为父类. Cfg也不能轻易设置其他变量, 否则影响子类设置这些变量
        线程不安全, 多线程注意上锁

        Args:
            recursive (bool, optional): 是否递归初始化
        """
        if recursive:
            for k, v in vars(type(self)).items():
                if self._is_config_class_(v):
                    setattr(self, k, v())

    @classmethod
    def _is_config_class_(cls, v: Any) -> bool:
        """判断是否是合法的配置类"""
        return inspect.isclass(v) and issubclass(v, Cfg) and v.__name__ != Cfg.__name__  # 子类名称是不严格约束

    @classmethod
    def _is_config_key_(cls, key: Any) -> bool:
        """判断是否是合法的配置类的 key"""
        return isinstance(key, str) and key.isidentifier() and key not in vars(Cfg) and key != '__annotations__'

    @classmethod
    def _is_config_value_(cls, value: Any) -> bool:
        """判断是否是合法的配置类的 value"""
        return not callable(value) or cls._is_config_class_(value)

    @classmethod
    def _is_config_key_value_(cls, key: Any, value: Any) -> bool:
        """判断是否是合法的配置类的 key 和 value"""
        return cls._is_config_key_(key) and cls._is_config_value_(value)

    @classmethod
    def _recursive_list_conversion_(cls, obj: Any, list_key: str) -> Any:
        """将字典中的含有 list_key 的 dict 转换为 list

        Args:
            obj (Any): 待转换的对象, 不是 dict 则直接返回
            list_key (str): 含有这个key的dict会被转换为值的list

        Returns:
            Any: 转换后的对象
        """
        if isinstance(obj, dict):
            obj = {k: cls._recursive_list_conversion_(v, list_key) for k, v in obj.items()}
            if list_key in obj:
                return list(obj.values())
        return obj

    @classmethod
    def _get_(cls, 
              key: Union[str, int], 
              return_kv: bool = False,
              default: Any = None,
              allow_default: bool = False,
              ) -> Union[Any, Tuple[str, Any]]:
        """获取静态变量中的内容

        Args:
            key (Union[str, int]): 针对哪个变量进行获取
                注意 key 为 int 则获取的复杂度为O(n)
            return_kv (bool, optional): 是否同时返回 key 和 value
                如果 key 是 int, 则返回的 key 是原始的 str
            default (Any, optional): 默认值v, 如果 key 不存在则返回默认值
            allow_default (bool, optional): 是否允许返回默认值, 否则会抛出异常

        Returns:
            Union[Any, Tuple[str, Any]]: 静态变量中的内容
        """
        if isinstance(key, str):
            assert cls._is_config_key_(key), f'key {key} is not valid'
            # 不用 getattr 为了防止Cfg配置子类的元类的 __getattr__ 被递归调用
            value = vars(cls).get(key, default) if allow_default else vars(cls)[key]
        else:
            assert isinstance(key, int), f'key {key} is not valid'
            try:
                if key < 0:
                    key, value = list(cls._ikv_)[key]
                else:
                    key, value = next(islice(cls._ikv_, key, key + 1))
            except:
                if allow_default:
                    value = default
                else:
                    raise
        assert cls._is_config_value_(value), f'value {value} is not valid'
        if return_kv:
            return key, value
        return value

    @classmethod
    def _set_(cls, 
              key: Union[str, int, None], 
              value: Any,
              create_new: bool = True,
              cover_old: bool = True,
              old_define: Callable[[Any, Any], bool] = lambda old, new: True,
              ancestors_has_cfg: bool = False,
              raise_new: bool = True,
              new_bases: Optional[Tuple[type, ...]] = None,
              ):
        """设置静态变量中的内容

        Args:
            key (Union[str, int, None]): 针对哪个变量进行设置，如果为 None 则直接设置 cls 本身
            value (Any): 设置的值.
                不允许普通变量（如dict/list）内再嵌套cfg类, 否则会导致 model_* 类方法都无法正常工作.
                value 中空的 cfg 类永远不会覆盖, 但普通嵌套类型可能会覆盖.
                新变量会尽量递归转换为配置类, 除非无法转换或者祖先中有配置类可以直接参考, 以及原始配置就不是配置类
            create_new (bool, optional): 是否允许创建新的变量
            cover_old (bool, optional): 是否允许覆盖旧的变量
            old_define (Callable[[Any, Any], bool], optional): 输入 (old, new) 返回old是否是否旧值
                只有 cover_old=True 才会调用
                例如 lambda old, new: not old 可以表示旧值是 None 或 '' 等空值的时候才覆盖
            ancestors_has_cfg (bool, optional): value 递归中的祖先中是否有配置类, 主要用于递归
                设置为 True 则尽量不将一般变量的 value 及其递归转换为配置类
            raise_new (bool, optional): 是否抛出构建了默认参数中没有的参数的异常, 前提是 create_new=False
            new_bases (Optional[Tuple[type, ...]], optional): 新建配置类的基类, 默认为 None 则继承自 (Cfg,)
                也可以是 cls.__bases__ 继承自原来的基类，要求至少有个类是 Cfg 或其子类
        """
        assert cls._is_config_class_(cls), 'model_deepcopy must be called on a config class'
        assert cls._is_config_value_(value), f'value {value} is not valid'
        if key is None:  # 设置 cls 本身
            iter_value = None
            if cls._is_config_class_(value):
                iter_value = value._ikv_
            elif isinstance(value, dict):
                iter_value = value.items()
            elif isinstance(value, list):
                iter_value = enumerate(value)
            assert iter_value is not None, f'value {value} is not valid'
            for k, v in iter_value:
                assert k is not None, f'k is not valid'
                cls._set_(k, v, create_new=create_new, cover_old=cover_old, old_define=old_define,
                          ancestors_has_cfg=ancestors_has_cfg, raise_new=raise_new, new_bases=new_bases)
            return
        try:
            key, this = cls._get_(key, return_kv=True)
        except:
            assert cls._is_config_key_(key) or isinstance(key, int) and key >= 0, f'key {key} is not valid'
            if not create_new:
                assert not raise_new, f'key {key} is not in config'
                return
            # 新变量赋值
            if isinstance(key, int):  # int 转 str
                keys = set(cls._ik_)
                assert key == len(keys), f'key ({key} != {len(keys)}) is not valid in list'
                key = create_unduplicated_key(f'i{key}', keys)
            if cls._is_config_class_(value):  # 配置类直接复制, 都是新变量无需递归
                type.__setattr__(cls, key, value.model_deepcopy(key))
                ancestors_has_cfg = True
            # 以贪心方式尽量将 value 转换为配置类
            elif not ancestors_has_cfg and value and (
                isinstance(value, dict) and all(cls._is_config_key_(k) for k in value) or
                isinstance(value, list) and any(isinstance(v, (dict, list)) for v in value)
            ):
                this = type(key, new_bases or (Cfg,), {})
                type.__setattr__(cls, key, this)
                iter_value = value.items() if isinstance(value, dict) else enumerate(value)
                for k, v in iter_value:
                    assert k is not None, f'k is not valid'
                    this._set_(k, v, create_new=create_new, cover_old=cover_old, old_define=old_define,
                               ancestors_has_cfg=ancestors_has_cfg, raise_new=raise_new, new_bases=new_bases)
            else:  # 无法转换为配置类，直接复制
                type.__setattr__(cls, key, deepcopy(value))
            return
        
        # 拥有正常的 key 和同一级别的 this 和 value
        if cls._is_config_class_(this):
            iter_value = None
            if cls._is_config_class_(value):  # 配置类直接复制
                iter_value = value._ikv_
                ancestors_has_cfg = True
            # 以贪心方式尽量将 value 转换为配置类
            elif not ancestors_has_cfg and value and (
                isinstance(value, dict) and all(cls._is_config_key_(k) for k in value) or
                isinstance(value, list) and any(isinstance(v, (dict, list)) for v in value)
            ):
                iter_value = value.items() if isinstance(value, dict) else enumerate(value)
            elif cover_old or old_define(this, value):  # 无法转换为配置类，直接复制
                type.__setattr__(cls, key, deepcopy(value))
            if iter_value is not None:  # 递归覆盖配置类
                for k, v in iter_value:
                    assert k is not None, f'k is not valid'
                    this._set_(k, v, create_new=create_new, cover_old=cover_old, old_define=old_define,
                               ancestors_has_cfg=ancestors_has_cfg, raise_new=raise_new, new_bases=new_bases)
        else:  # 原始配置不是配置类
            if cls._is_config_class_(value):  # this 不是类则不会再当类处理
                value = value.model_dump(list_conversion=True)
            if isinstance(this, dict) and isinstance(value, dict):  # 递归覆盖普通值
                ret = cover_dict(value, this, 
                                 allow_new=create_new, 
                                 cover_old=cover_old, 
                                 old_define=old_define,
                                 raise_new=raise_new,
                                 new_deepcopy=True)
                type.__setattr__(cls, key, ret)
            elif cover_old or old_define(this, value):  # 无法对齐，则直接覆盖
                type.__setattr__(cls, key, deepcopy(value))
    
    @classmethod
    def _pop_(cls, key: Union[str, int], return_kv: bool = False) -> Union[Any, Tuple[str, Any]]:
        """删除静态变量并取出内容

        Args:
            key (Union[str, int]): 针对哪个变量进行删除
                注意 key 为 int 则删除的复杂度为O(n)
            return_kv (bool, optional): 是否同时返回 key 和 value
                如果 key 是 int, 则返回的 key 是原始的 str

        Returns:
            Union[Any, Tuple[str, Any]]: 删除的内容
        """
        k, v = cls._get_(key, return_kv=True)
        delattr(cls, k)
        if return_kv:
            return k, v
        return v
    
    @classmethod
    def _insert_(cls, 
                 value: Any, 
                 key: int = 0, 
                 key_name: Union[List[str], str, None] = None, 
                 many: bool = False,
                 prevent_value_to_cfg: bool = False,
                 ):
        """在一个位置插入一个或多个静态变量, 复杂度为O(n)

        Args:
            value (Any): 插入的一个或多个值
            key (int, optional): 插入的位置, -1 表示插入到最后
            key_name (Union[List[str], str, None], optional): 插入的名称也可以用标准的str代替, 否则是自动生成, 不能和已有的key重复
            many (bool, optional): 是否插入多个, value 必须是 list 或 tuple 或迭代对象, key_name 也是或者为 None
                key_name 如果是 List[str] 则自动认为 many=True
            prevent_value_to_cfg (bool, optional): 是否阻止 value 的普通变量尽量转换为配置类
        """
        assert isinstance(key, int), f'key {key} is not valid'
        # 构建 many 值
        if isinstance(key_name, list):
            many = True
        if not many:
            value = [value]
            key_name = [key_name]
        value_L = list(value)
        key_name_L = unique_list_with_none(key_name)
        # 检查 key_name
        assert len(key_name_L) == len(key_name), f'key_name {key_name} is duplicated'
        assert len(key_name_L) == len(value_L), f'key_name {key_name_L} and value {value_L} is not match'
        keys = set(cls._ik_)
        assert all(n is None or cls._is_config_key_(n) and n not in keys for n in key_name_L
                   ), f'key_name {key_name_L} is not valid or duplicated'
        # 插入到最后
        if key == -1 or not keys or key >= len(keys):
            for i in range(len(value_L)):
                cls._set_(key_name_L[i] or len(keys) + i, value_L[i], create_new=True, ancestors_has_cfg=prevent_value_to_cfg)
            return
        # 插入在中间
        if key < 0:  # 倒数还原成正数
            key = max(len(keys) + key + 1, 0)
        kv_L: List[Tuple[str, Any]] = []
        try:  # 将后面的元素先取出来
            while True:
                kv_L.append(cls._pop_(key, return_kv=True))
        except:
            ...
        for i in range(len(value_L)):  # 插入
            cls._set_(key_name_L[i] or key + i, value_L[i], create_new=True, ancestors_has_cfg=prevent_value_to_cfg)
        for k, v in kv_L:  # 再放回去
            type.__setattr__(cls, k, v)

    @classmethod
    @property
    def _len_(cls) -> str:
        """获取本层级的所有key的个数，不包括嵌套类的key. 复杂度为O(n)"""
        return len(list(cls._ik_))

    @classmethod
    @property
    def _ikv_(cls) -> Iterator[Tuple[str, Any]]:
        """获取本层级的所有key和值，不包括嵌套类的key和值"""
        for k, v in vars(cls).items():
            if cls._is_config_key_value_(k, v):
                yield k, v

    @classmethod
    @property
    def _ik_(cls) -> Iterator[str]:
        """获取本层级的所有key，不包括嵌套类的key. list也有key"""
        for k, _ in cls._ikv_:
            yield k

    @classmethod
    @property
    def _iv_(cls) -> Iterator[Any]:
        """获取本层级的所有值，不包括嵌套类的值. 可以方便list用"""
        for _, v in cls._ikv_:
            yield v

    @classmethod
    def model_dump(cls,
                   list_conversion: bool = False,
                   list_conversion_key: str = 'i0',
                   **kwargs) -> Union[dict, list]:
        """将配置转换为传统的dict/list

        Args:
            list_conversion (bool, optional): 是否将含有 list_conversion_key 的 dict 转换为 list
            list_conversion_key (str, optional): 含有这个key的dict会被转换为值的list

        Returns:
            Union[dict, list]: 转换后的dict/list
        """
        static_vars = {k: v.model_dump(**kwargs) if cls._is_config_class_(
            v) else v for k, v in vars(cls).items() if cls._is_config_key_value_(k, v)}
        if list_conversion:
            return cls._recursive_list_conversion_(static_vars, list_conversion_key)
        return static_vars

    @classmethod
    def model_dump_code(cls, 
                        indent: int = 0, 
                        tab: str = ' ' * 4, 
                        keep_class_newline: bool = False,
                        ) -> Union[str, list]:
        """导出相关嵌套类和静态变量, 注意使用的时候需要手动加入 import

        Args:
            indent (int, optional): 缩进大小, 单位tab. 一般用于递归
            tab (str, optional): 缩进符号
            keep_class_newline (bool, optional): 是否保留类定义前的空行

        Returns:
            Union[str, list]: 如果 indent > 0 返回列表, 否则返回字符串。为复原的py配置代码
        """
        assert indent >= 0, 'indent must be greater than or equal to 0'
        assert cls._is_config_class_(cls), 'model_deepcopy must be called on a config class'
        base_indent = tab * indent
        if len(cls.__bases__) == 1:
            bases_name = cls.__bases__[0].__name__
        else:
            bases_name = ', '.join([base.__name__ for base in cls.__bases__])
        lines = [''] if keep_class_newline else []
        lines += [f"{base_indent}class {cls.__name__}({bases_name}):"]
        has_body = False  # 是否有定义在类中的内容
        type_hints = get_type_hints(cls)  # 用于补充类型注释
        # 遍历类字典
        for name, value in cls._ikv_:
            has_body = True
            if cls._is_config_class_(value):  # 嵌套类
                nested_class_code = value.model_dump_code(indent=indent+1, tab=tab, keep_class_newline=keep_class_newline)
                lines += nested_class_code
            else:  # 静态变量
                type_annotation = type_hints.get(name)
                if isinstance(type_annotation, type):
                    type_annotation = type_annotation.__name__
                elif type_annotation:
                    type_annotation = re.compile(r'(^|(?<= ))typing\.').sub('', str(type_annotation))
                annotation_str = f": {type_annotation}" if type_annotation else ''
                lines.append(f"{base_indent}{tab}{name}{annotation_str} = {value!r}")
        # 如果类中没有定义内容，添加一个 pass
        if not has_body:
            lines.append(f"{base_indent}{tab}pass")
        if indent > 0:  # 递归中返回列表，否则返回字符串
            return lines
        return '\n'.join(lines)

    @classmethod
    def model_deepcopy(cls: T, new_class_name: str) -> T:
        """递归拷贝静态类，返回新类，新类的静态变量是深拷贝的

        Args:
            cls (T): 静态类
            new_class_name (str): 新类名

        Returns:
            T: 一样类型的新类
        """
        assert cls._is_config_class_(cls), 'model_deepcopy must be called on a config class'
        assert cls._is_config_key_(new_class_name), f'new_class_name {new_class_name} is not valid'
        new_class = type(new_class_name, cls.__bases__, dict(cls._ikv_))
        for k, v in new_class._ikv_:
            if cls._is_config_class_(v):
                # 不用 setattr 为了防止Cfg配置子类的元类的 __setattr__ 被递归调用
                type.__setattr__(new_class, k, v.model_deepcopy(k))
            else:
                type.__setattr__(new_class, k, deepcopy(v))
        return new_class


if __name__ == '__main__':
    Cfg_ = Cfg
    
    class MyClass(Cfg_):
        static_var: bool = False

        class NestedClass(Cfg_, object):
            nested_var: datetime = datetime.now()

            class NestedClass(Cfg_):
                nested_var = 10*2

            class NestedClass2(Cfg_):
                nested_var: Any = '20'

        class Test(Cfg_):
            ...
        static_var1: Dict[str, Any] = {
            'a': {},
            'b': '2',
            'c': (3,),
        }

    print(MyClass.model_dump_code(keep_class_newline=True))
    # print(Cfg_.model_dump_code())
    print(MyClass._len_)
    print()

    MyClass2 = MyClass.model_deepcopy('MyClass2')
    MyClass.static_var1['a'][1] = 100
    MyClass2.static_var1['a'][1] = 101
    print(MyClass.static_var1)
    print(MyClass2.static_var1)
    print()
    
    print(create_unduplicated_key('a', {'a'}))
    
    MyClass2.NestedClass._set_('nested_var2', [{'a': [1, 2]}, 1], create_new=True)
    MyClass2._set_(0, 1)
    MyClass2._insert_(123, 2)
    MyClass2._insert_([2, {'abc': {'test': 123}}, 4], 3, ['test', None, None])
    print(MyClass2.model_dump_code())
    print(MyClass._get_(1))
    print()
    
    MyClass._set_(None, [1, 2, 3])
    print(MyClass.model_dump_code())
    print(MyClass._get_('a1234', allow_default=True))
    
    print('---------meta test---------')
    # KEY_NOT_FOUND.use_raise = True
    print(MyClass.abcdefg, MyClass[-1])
    MyClass.abcdefg = MyClass['abcdefg'] = 1234
    print(MyClass['abcdefg'])

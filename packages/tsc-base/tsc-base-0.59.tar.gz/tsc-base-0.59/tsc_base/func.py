from pprint import pprint
import inspect
import heapq
# 参考 https://docs.python.org/3/library/typing.html#typing.Generator
from typing import Dict, Any, List, Tuple, Generator, Union, Any, Callable, TypeVar
import random
import re
import timeit
from collections.abc import Iterable
import hashlib
import pickle
from collections import OrderedDict
from copy import deepcopy
import os
import time
from itertools import count
import random
import string


T = TypeVar('T')
global_counter = count()
global_random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def get_func_para(func, del_para=None, add_para: dict = None):
    """提取函数的参数和默认值, 没有默认值设为 None
    比如可以用于设定 TaskDB.result 的例子

    Args:
        func (list, function): 单/多个函数组成的列表, 后面函数出现一样的参数会覆盖前面的默认值
        del_para (set, list, optional): 删除不想看到返回的参数
        add_para (dict, optional): 增加想补充的参数和值, 会覆盖原始值, 不会被 del_para 删除

    Returns:
        dict: 所有函数修剪后的参数和默认值
    """
    paras = {}
    func = func if isinstance(func, list) else [func]
    del_para = set(del_para) if del_para else set()
    add_para = add_para if add_para else {}
    for f in func:
        fullargspec = inspect.getfullargspec(f)
        defaults = fullargspec.defaults if fullargspec.defaults else []
        defaults = [None] * (len(fullargspec.args) - len(defaults)) + list(defaults)
        paras.update({k: v for k, v in zip(fullargspec.args, defaults) if k not in del_para})
    paras.update(add_para)
    return paras


def cover_dict(new_para: dict, default_para: dict, allow_new=False, 
               cover_old=True, old_define=lambda old, new: True, raise_new=True,
               new_deepcopy=False):
    """使用 new_para 中的健值对递归覆盖 default_para 中的值, 遇到非 dict 就不再递归而直接覆盖, 出现类型不一样也会直接覆盖
    比如可以用于新参数覆盖旧参数 (注意因为失误导致的参数覆盖)

    Args:
        new_para (dict): 待覆盖的
        default_para (dict): 被覆盖的, 注意还需要原来的值就要 copy.deepcopy(default_para)
        allow_new (bool): 是否能 让 new_para 出现 default_para 中没有的 key, 能的话就直接加入 default_para
        cover_old (bool): 是否覆盖旧值, 否则只会添加新值
        old_define (function): 输入 (old, new) 返回old是否是否旧值, 只有 cover_old=True 才会调用
            例如 lambda old, new: not old 可以表示旧值是 None 或 '' 等空值的时候才覆盖
        raise_new (bool): 是否抛出构建了默认参数中没有的参数的异常, 前提是 allow_new=False
        new_deepcopy (bool): 是否对 new_para 中待使用的值进行深拷贝, 否则出现list等会交叉引用

    Returns:
        dict: default_para
    """
    for k, v in new_para.items():
        if k not in default_para:
            if not allow_new:
                if raise_new:
                    raise f'构建了默认参数中没有的参数: {k} not in {set(default_para)}'
            else:
                default_para[k] = deepcopy(v) if new_deepcopy else v
            continue
        if isinstance(v, dict) and isinstance(default_para[k], dict):
            cover_dict(v, default_para[k], allow_new, cover_old, old_define, raise_new, new_deepcopy)
        elif cover_old and old_define(default_para[k], v):
            default_para[k] = deepcopy(v) if new_deepcopy else v
    return default_para


def get(key, obj, default=None):
    """
    递归从dict/list/tuple中取值, 以list的形式，以避免中括号取值数量不灵活的问题
    :param key: list/tuple/int/str; list表示递归取值
    :param obj: dict/list/tuple
    :param default: 寻找不到后返回的默认值
    :return:
    """
    key = key if isinstance(key, list) else [key]
    if len(key) == 0:
        return default
    for i in key:
        try:
            obj = obj[i]
        except:
            obj = default
            break
    return obj


def put(key, obj, default=None, delete=False):
    """
    递归在dict/list中放值, 以list的形式，以避免中括号放值数量不灵活的问题
    :param key: list/tuple/int/str; list表示递归放值. 空list会返回 ellipsis
    :param obj: dict/list
    :param default: 放的内容, 会覆盖原有值. 如果路径key路径上没有会构建, 仅限于dict类型
    :param delete: bool; 是否删除而不是放置对应的值
    :return: default or ellipsis or 删除的值
    """
    key = key if isinstance(key, list) else [key]
    if len(key) == 0:
        return ...
    for i in key[:-1]:
        try:
            obj = obj[i]
        except:
            obj = obj.setdefault(i, {})
    if delete:
        default = obj[key[-1]]
        del obj[key[-1]]
    else:
        obj[key[-1]] = default
    return default


def merge_dict(dict_L: List[Dict], union=True, ordered=False, new_dict=None):
    """递归求多个字典的并/交集, 多个字典的v类型不一样(除了None)会使用第1个 dict 的值, 如果不存在或为None则优先向后取

    Args:
        dict_L (List[Dict]): list 中的非 dict 元素会被剔除
        union (bool): 是否求并集, 否则交集
        ordered (bool): 融合后是否保持原来顺序, 保持有序速度可能会慢 1~5 倍，尤其是 union=True 的时候
        new_dict (dict, optional): 递归专用, 不能赋值

    Returns:
        dict: new_dict
    """
    new_dict = {} if new_dict is None else new_dict
    dict_L = [i for i in dict_L if isinstance(i, dict)]
    if union:
        if ordered:
            seen = set()
            set_key = [seen.add(key) or key for d in dict_L for key in d if key not in seen]
        else:
            set_key = set().union(*dict_L)
    else:
        set_key = set(dict_L[0]).intersection(*dict_L[1:])
        if ordered:
            set_key = [key for key in dict_L[0] if key in set_key]
    for k in set_key:
        v_L = [d.get(k) for d in dict_L]
        if all(v is None for v in v_L):  # 都是 None
            new_dict[k] = None
        elif set(type(v) for v in v_L) <= {dict, type(None)}:  # 都是 dict 或 None
            merge_dict(v_L, union=union, ordered=ordered, new_dict=new_dict.setdefault(k, {}))
        else:
            new_dict[k] = v_L[0]
            for v in v_L:
                if v is not None:
                    new_dict[k] = v
                    break
    return new_dict


def opt_value_dict(dict1, dict2, opt=lambda v1, v2: v1-v2, in_list=False, new_dict=None):
    """递归求2个字典值的操作值结果, opt操作没有异常才有结果
    如果递归后的 dict1 和 dict2 有一个类型是dict另一个不是, 那么会将是dict的递归然后全部和另一个不是的求opt
    这里的 opt 默认计算的是 dict1 - dict2

    Args:
        dict1 (dict, list, Any): 
        dict2 (dict, list, Any): 
        opt (dict, function): 输入 (v1, v2) 返回 计算结果. 如果是 dict 就和 dict1/dict2 一起递归到 非dict(function)
        in_list (bool): 如果为 True，则dict1和dict2同时为list的时候(或其中一个为None)也会继续递归下去，此时可以使用嵌套的 opt 为 list
            这会导致一个dict不存在键，另一个对应键存在list的话，会保留原始list的值，而不会因为opt异常而不保留，因为list中的None是提前写好的
        new_dict (dict, list, optional): 递归专用, 不能赋值

    Returns:
        dict: new_dict
    """
    use_list = in_list and {type(dict1), type(dict2), type(None)} == {list, type(None)}
    if new_dict is None:
        new_dict = [None] * max(len(dict1) if isinstance(dict1, list) else 0, len(dict2) if isinstance(dict2, list) else 0) if use_list else {}
    if use_list:
        par = range(len(new_dict))
    else:
        par = (set(dict1) if isinstance(dict1, dict) else set()) | (set(dict2) if isinstance(dict2, dict) else set())
    for k in par:
        if use_list:
            v1 = dict1
            if isinstance(dict1, list):
                v1 = dict1[k] if k < len(dict1) else None
            v2 = dict2
            if isinstance(dict2, list):
                v2 = dict2[k] if k < len(dict2) else None
            next_opt = opt[k] if isinstance(opt, list) else opt
        else:
            v1 = dict1.get(k) if isinstance(dict1, dict) else dict1
            v2 = dict2.get(k) if isinstance(dict2, dict) else dict2
            next_opt = opt[k] if isinstance(opt, dict) else opt
        if type(v1) == dict or type(v2) == dict:
            next_dict = new_dict[k] = {}
            opt_value_dict(v1, v2, next_opt, in_list, new_dict=next_dict)
        elif in_list and {type(v1), type(v2), type(None)} == {list, type(None)}:
            next_dict = new_dict[k] = [None] * max(len(v1) if isinstance(v1, list) else 0, len(v2) if isinstance(v2, list) else 0)
            opt_value_dict(v1, v2, next_opt, in_list, new_dict=next_dict)
        else:
            try:
                new_dict[k] = opt(v1, v2)
            except:
                ...
    return new_dict


def any_value_dict(dict1, opt=lambda v1, v2: v1 and v2, start_v=True, raise_error=False):
    """深度遍历递归求1个字典内部相邻值的操作值结果, opt操作没有异常才更新结果
    这里的 opt 默认计算的是 dict1 中的所有值是不是都是 True

    Args:
        dict1 (dict): 
        opt (dict, function): 输入 (start_v, v) 返回 计算结果. 如果是 dict 就和 dict1 一起递归到 非dict(function)
            v 依次是深度遍历递归的值
        start_v (Any): 初始值, 后面每次更新它
        raise_error (bool): opt操作是否有异常就抛出

    Returns:
        Any: start_v
    """
    for k, v in dict1.items():
        if type(v) == dict:
            start_v = any_value_dict(v, opt[k] if isinstance(opt, dict) else opt, start_v=start_v)
        else:
            try:
                start_v = opt(start_v, v)
            except:
                if raise_error:
                    raise
    return start_v


def recur_opt_any(
    any_: T,
    opt: Callable[[list, List[type], Any], Tuple[Any, bool, bool]] = lambda x: (x[-1], False, False),
    root_keys: list = None,
    root_types: List[type] = None,
) -> Union[T, None]:
    """深度遍历dict/list, 以便于修改原值或删除原来的值

    Args:
        any_ (T): 递归对象，如果不是 dict/list 则直接用 opt 处理. 注意如果想保留原来值需要 deepcopy
        opt (Callable, optional): 输入 (root_keys, root_types, value) 返回 (new_value, del_k, stop_recur)
            del_k 表示是否删除原来的值, stop_recur 表示是否停止递归（否的话对 new_value 也会继续递归）
        root_keys (list, optional): 递归专用, 不能赋值，用于存储父路径
        root_types (List[type], optional): 递归专用, 不能赋值，用于存储父类型

    Returns:
        Union[T, None]: new_any
    """
    if not isinstance(any_, (dict, list)):
        v, del_k, _ = opt([], [], any_)
        if del_k:
            del any_
            return None
        return v
    if root_keys is None:
        root_keys = []
    if root_types is None:
        root_types = []
    if isinstance(any_, dict):
        for k in list(any_):
            new_root_keys = root_keys + [k]
            new_root_types = root_types + [type(any_)]
            any_[k], del_k, stop_recur = opt(new_root_keys, new_root_types, any_[k])
            if del_k:
                del any_[k]
            elif not stop_recur:
                recur_opt_any(any_[k], opt, new_root_keys, new_root_types)
    else:
        k = 0
        while k < len(any_):
            new_root_keys = root_keys + [k]
            new_root_types = root_types + [type(any_)]
            any_[k], del_k, stop_recur = opt(new_root_keys, new_root_types, any_[k])
            if del_k:
                del any_[k]
            elif not stop_recur:
                recur_opt_any(any_[k], opt, new_root_keys, new_root_types)
                k += 1
            else:
                k += 1


def arg_extreme_dict(d: Dict[Any, Dict], dv_key=None, dv_reverse=True, allow_type=None, ban_type=None, traverse_d=None,
                     result=None, root=None):
    """给d中的每个v排序, v中递归的每个元素都排序(只取最大值或最小值), 排序结果的极值用d的k表示
    d中的每个v会取并集key计算, 如果一个dv没有相应的key或为None就不参与极值获取

    Args:
        d (Dict[Any, Dict]): 双层字典, 第二层的每个字典构造格式保持一致, 只允许值不一样或者不存在某些key
        dv_key (dict, function, optional): d中v的每个值使用的排序function, 输入是 (d的k,递归后v值) 对, 输出可排序值
            输入 function 类型就是统一针对所有v的方法
        dv_reverse (dict, bool, optional): d中v的每个值取最大值还是最小值, 默认都是True最大值, 使用dict可针对每个v值选择顺序(不在dict中的还是默认值)
        allow_type (set, list, optional): d中v中的值允许排序的类型, 默认见代码
        ban_type (set, list, optional): d中v中的值不允许排序的类型, 使用这个 allow_type 会失效. 使用时建议加入 dict
        traverse_d (dict, optional): 默认是d中所有v的并集, 用于确定排序对象有哪些k
        result (dict, optional): 用于递归存储结果, 不可以赋值
        root (list, optional): 用于递归存储路径, 不可以赋值

    Returns:
        dict: result
    """
    allow_type = {int, float} if allow_type is None else set(allow_type)
    ban_type = {} if ban_type is None else set(ban_type)
    result = {} if result is None else result
    root = [] if root is None else root
    traverse_d = merge_dict(list(d.values())) if traverse_d is None else traverse_d  # 默认排序对象
    for k, v in traverse_d.items():
        result[k] = {}
        type_v = type(v)
        if (len(ban_type) == 0 and type_v not in allow_type) or (len(ban_type) > 0 and type_v in ban_type):  # 不是允许的类型
            if type_v is dict:  # 是dict就递归
                arg_extreme_dict(d, dv_key=dv_key, dv_reverse=dv_reverse, allow_type=allow_type, ban_type=ban_type,
                                 traverse_d=traverse_d[k], result=result[k], root=root + [k])
        else:
            root_ = root + [k]
            key = dv_key if inspect.isfunction(dv_key) else get(root_, dv_key, lambda t: t[1])  # 排序方式
            reverse = dv_reverse if isinstance(dv_reverse, bool) else get(root_, dv_reverse, True)  # 最大还是最小值排序
            sort_ = heapq.nlargest if reverse else heapq.nsmallest
            result[k] = sort_(1, [(k1, get(root_, v1))  # 出现错误 IndexError: list index out of range 可能是因为加入了排序不了的类型, 比如 None
                              for k1, v1 in d.items() if get(root_, v1) is not None], key=key)[0][0]
    return result


def dict_to_pair(dict1: dict, in_list=False, root=None) -> Generator[Tuple[List, Any], None, None]:
    """深度遍历递归返回所有(k_L,v)对, 遇到非空dict就会递归, 否则作为value返回

    Args:
        dict1 (dict, list): 
        in_list (bool): 如果为 True，则dict1或嵌套为list的时候也会继续递归下去
            注意使用这种转换后无法通过 pair_to_dict 还原，因为list的数字编号会被当做key
        root (list, optional): 用于递归存储路径, 不可以赋值

    Yields:
        Generator[Tuple[List, Any], None, None]: ([k,..],value),..
    """
    root = [] if root is None else root
    if isinstance(dict1, list) and in_list:
        par = enumerate(dict1)
    elif isinstance(dict1, dict):
        par = dict1.items()
    else:
        yield root, dict1
        return
    for k, v in par:
        if isinstance(v, (dict, list)) and v:
            yield from dict_to_pair(v, in_list=in_list, root=root + [k])
        else:
            yield (root + [k], v)


def pair_to_dict(traversed_pair: List[Tuple[List, Any]]) -> dict:
    """所有(k_L,v)对依次还原为dict

    Args:
        traversed_pair (List[Tuple[List, Any]]): ([k,..],value),..

    Returns:
        dict: dict1
    """
    dict1 = {}
    for k_L, v in traversed_pair:
        d = dict1
        for k in k_L[:-1]:
            d = d.setdefault(k, {})
        d[k_L[-1]] = v
    return dict1


def recursion_stat(doc: dict, stat: dict, key_stat=None, len_stat=None, content_stat=None, _len_sum=True, _type=True):
    """
    递归统计mongo字典doc中每个属性出现的次数，以及出现属性类型、特殊长度、内容的次数
    如果出现list并其中元素是dict，那么这一条数据list中不同dict的计数会叠加
    list中嵌套list不会再递归，其他情况会一直递归到非dict/list/tuple变量为止
    key_stat中的s也可以针对{list,tuple}类型的v, 会对v中{float,int,str}的值当{值:None}来处理, 就相当于list中元素是dict

    :param doc: dict; 一条mongodb数据，普通json可能出现关键词重合统计错误问题，比如$开头
    :param stat: dict; 统计结果
    :param key_stat: None or {k:{k:{s,..}/[s,..]/None/func,..},..}; 如果k在其中出现则统计v出现的次数或不统计长度或内容，None表示不统计
        list递归dict则当list不存在，dict中k/s首位是$表示路径到这个k为止，路径最后k的v可以是dict/list/tuple变量，但不会统计v出现次数
        s：$^v表示不统计默认内容出现次数，$^l表示不统计默认长度出现次数，$*l表示统计所有长度出现次数，$*v表示统计所有v出现次数
            $l:{i,..} 表示统计某些长度i出现次数, $v:{v,..} 表示统计某些内容v出现次数
            $.l:func(len(v)) 表示统计某些长度出现次数, $.v:func(v) 表示统计某些内容出现次数
                func方法传入长度或内容,返回None或代号,None表示不统计,长度代号会自动加$,内容代号会自动加$_
            优先级: $*l > $l > $.l > 默认统计, 默认统计见代码
            $*key 表示默认匹配任何key, 它的值是dict, 必须要装下级别的key, 递归的时候会带入. 优先级低于一样的key
        例子：
        key_stat = {
            'paperwithcode': {
                'code': {
                    'frame': {'$*v'},
                    'official': {'$*v'},
                    '$l': set(range(10)),
                    '$.l': lambda l: f'{l // 10}0-{l // 10}9' if l < 100 else f'{l // 100}00-{l // 100}99',
                }
            },
            '期刊分区': {
                'JCR分区': {'$*v'}, 
                '$*key': {'综述': {'$*v'}},
            },
        }
    :param len_stat: None or set; 默认统计value长度, 为None则默认见代码, 不想统计可赋值 set()
    :param content_stat: None or set or dict; 默认统计内容value (会针对类型匹配,例如1和1.0不同), 为None则默认见代码, 不想统计可赋值 set()
        因为 {True, 1, False, 0} == {1, 0} 所以当出现这种冲突建议使用 dict {type:{值,..},..}
    :param _len_sum: bool; 是否统计 $len_sum
    :param _type: bool; 是否统计 $type
    :return: stat
        $times: int; 属性出现次数
        $len_sum: int; 如果属性值属于{dict, list, tuple, str}则统计长度总和
        $expand: dict; 如果属性值是dict或list嵌套dict则递归进入内部统计出现情况
        $type: dict; 统计属性值出现各种类型的次数
        $i: int; 如果属性值属于{dict, list, tuple, str}则统计长度i出现的次数
        $_s: int; 如果属性值不属于{dict, list, tuple}则统计内容s出现的次数
        $len: dict; key为 $i 的对象
        $value: dict; key为 $_s 的对象
        $list: dict; 形式类似于 $expand, 但是针对于{list,tuple}类型v中的{float,int,str}, $list中key就是值
        $species: $expand or $list 中key出现的次数, 大于1才记录
    """
    if key_stat is None:
        key_stat = {}
    # 默认需要统计的特殊长度、内容
    if len_stat is None:
        len_stat = {0}  # 默认统计长度
    if content_stat is None:
        content_stat = {  # 默认统计内容
            None, False, True, 0, 1, -1, 'None', 'null', 'false', 'true', 'False', 'True', '0', '1', '-1',
        }
    # content_stat 改造为字典, 用于针对类型匹配
    if type(content_stat) == set:
        content_stat_ = {}
        for i in content_stat:
            content_stat_.setdefault(type(i), set()).add(i)
        content_stat = content_stat_
    # 开始统计
    for k, v in doc.items():
        stat.setdefault(k, {'$times': 0})
        if isinstance(v, dict):
            expand = stat[k].setdefault('$expand', {})
            if k in key_stat and not isinstance(key_stat[k], set):  # 首位不能是$
                ks = key_stat[k]
            else:  # 当 key_stat[k] 为 set 类型时无效, 因为错误认为v不是dict才有v或l的统计
                ks = key_stat['$*key'] if '$*key' in key_stat else {}
            recursion_stat(v, expand, ks, len_stat, content_stat, _len_sum, _type)
            if len(expand) > 1:
                expand['$species'] = len(expand) - 1  # 种数
        elif type(v) in {list, tuple}:
            expand = expand_list = None
            for i in v:
                if isinstance(i, dict):
                    expand = stat[k].setdefault('$expand', {})
                    if k in key_stat and not isinstance(key_stat[k], set):  # 首位不能是$
                        ks = key_stat[k]
                    else:
                        ks = key_stat['$*key'] if '$*key' in key_stat else {}
                    recursion_stat(i, expand, ks, len_stat, content_stat, _len_sum, _type)
                elif type(i) in {float, int, str}:
                    expand_list = stat[k].setdefault('$list', {})
                    ks = key_stat[k] if k in key_stat else (key_stat['$*key'] if '$*key' in key_stat else {})
                    recursion_stat({i: None}, expand_list, ks, set(), set(), _len_sum, _type)
            # 种数
            if expand is not None and len(expand) > 1:
                expand['$species'] = len(expand) - 1
            if expand_list is not None and len(expand_list) > 1:
                expand_list['$species'] = len(expand_list) - 1
        else:
            s = False
            v_ = v
            if k in key_stat:
                if '$*v' in key_stat[k] or ('$v' in key_stat[k] and v in key_stat[k]['$v']):
                    s = True
                elif '$.v' in key_stat[k]:
                    v_ = key_stat[k]['$.v'](v)
                    if v_ is not None:
                        s = True
                    else:
                        v_ = v
                elif '$^v' not in key_stat[k] and type(v) in content_stat and v in content_stat[type(v)]:
                    s = True
            elif type(v) in content_stat and v in content_stat[type(v)]:
                s = True
            if s:
                stat[k].setdefault('$value', {}).setdefault(f'$_{v_}', 0)
                stat[k]['$value'][f'$_{v_}'] += 1
        if type(v) in {dict, list, tuple, str}:
            if _len_sum:
                stat[k].setdefault('$len_sum', 0)
                stat[k]['$len_sum'] += len(v)
            s = False
            v_ = len(v)
            if k in key_stat:
                if '$*l' in key_stat[k] or ('$l' in key_stat[k] and len(v) in key_stat[k]['$l']):
                    s = True
                elif '$.l' in key_stat[k]:
                    v_ = key_stat[k]['$.l'](len(v))
                    if v_ is not None:
                        s = True
                    else:
                        v_ = len(v)
                elif '$^l' not in key_stat[k] and len(v) in len_stat:
                    s = True
            elif len(v) in len_stat:
                s = True
            if s:
                stat[k].setdefault('$len', {}).setdefault(f'${v_}', 0)
                stat[k]['$len'][f'${v_}'] += 1
        stat[k]['$times'] += 1
        if _type:
            stat[k].setdefault('$type', {}).setdefault(f'${type(v)}', 0)
            stat[k]['$type'][f'${type(v)}'] += 1
    return stat


def replace(pattern, repl_f, string, count=0):
    '''
    正则表达式字符串替换, 可以对待替换字符串进行函数操作
    :param pattern: str; 待替换字符的正则匹配
    :param repl_f: function or str; 如果为function则参数是被替换的字符串
    :param string: str; 替换对象
    :param count: int; 替换前几个?
    :return:
    '''
    if isinstance(repl_f, str):
        return re.sub(pattern=pattern, repl=repl_f, string=string, count=count)
    if count <= 0:
        count = len(string) * 2 + 1  # replace('|1', lambda s: '2', '111')
    span_L = [(0, 0)]
    string_split_L = []
    for i in re.finditer(pattern, string):
        if count <= 0:
            break
        else:
            count -= 1
        span = i.span()
        string_split_L.append(string[span_L[-1][1]: span[0]])
        span_L.append(span)
    string_split_L.append(string[span_L[-1][1]:])
    span_L = span_L[1:]
    string_L = [string_split_L[0]]
    for i, (s, e) in enumerate(span_L):
        string_L.append(repl_f(string[s: e]))
        string_L.append(string_split_L[i + 1])
    return ''.join(string_L)


def get_obj_sha512(x, ignore_type=False, out=None):
    """获取一个对象的sha512值, 递归判断不受指针影响, 无序类型改变顺序不影响值
    冲突概率: https://en.wikipedia.org/wiki/Birthday_problem#Probability_table

    Args:
        x (_type_): 由 可str化的有序类型 / 无序类型(set和dict) 构成
        ignore_type (bool, optional): 是否忽略除无序类型以外的类型(类型全变None), 等于只看遍历后的str值是否一致
        out (list, optional): 用于递归,不可修改

    Returns:
        str, list: sha512, x的深度优先遍历结果
    """
    if out is None:
        out = []
        root = True
    else:
        root = False
    type_x = type(x)
    if type_x == set:
        out.append(type_x)
        x = sorted(x, key=lambda t: pickle.dumps(t))
    elif type_x == dict:
        out.append(type_x)
        x = sorted(x.items(), key=lambda t: pickle.dumps(t[0]))
    # 类型忽略处理
    elif ignore_type:
        out.append(None)  # 加入这个使得单一嵌套情况会被区分
    else:
        out.append(type_x)
    # 递归
    if isinstance(x, Iterable) and type_x not in {str, bytes}:
        for i in x:
            get_obj_sha512(i, ignore_type, out)
    else:
        out.append(str(x))
    if root:
        return hashlib.sha512(pickle.dumps(out)).hexdigest(), out
    
    
def fast_uniform_seg(n, array, acc=0.1, low=None, high=None):
    '''
    高效但可能不均衡. 一个分段大于中值的贪心策略可能导致靠后的节点数量较少
    :param n: int, 类别数量
    :param array: [x,..], 待分割数组
    :param acc: float, 分治法的二分精度
    :param low: 递归用参数
    :param high: 递归用参数
    :return: [[x,..],..], 分割结果结果
    '''
    assert 1 < n <= len(array), '划分数和总数不合适!'
    if not high:
        high = sum(array)
    if not low:
        low = max(array)
    if low > high:
        seg = []
        s = 0
        max_v = high + acc
        for no, i in enumerate(array):
            s += i
            if s > max_v or len(array) - no <= n - len(seg):  # 不能让类数减少
                s = i
                seg.append([i])
            else:
                if not seg:
                    seg.append([i])
                else:
                    seg[-1].append(i)
        return seg
    else:
        mid = (low + high) / 2
        seg = s = 0
        juge = True
        for no, i in enumerate(array):
            s += i
            if s > mid or len(array) - no <= n - seg - 1:
                s = i
                seg += 1
        if seg >= n:
            juge = False
        if juge:
            return fast_uniform_seg(n, array, acc=acc, low=low, high=mid - acc)
        else:
            return fast_uniform_seg(n, array, acc=acc, low=mid + acc, high=high)
        
        
def acc_uniform_seg(n, array, *args):
    '''
    穷举速度慢, 但均衡.
    :param n: int, 类别数量
    :param array: [x,..], 待分割数组
    :param args:
    :return: [[x,..],..], 分割结果
    '''
    assert 1 < n <= len(array), '划分数和总数不合适!'
    nums = [i + 1 for i in range(n - 1)]
    nums_opt = nums
    σ_fake = sum(array)
    μ = σ_fake / n
    σ_fake *= n
    count = 0
    while True:
        count += 1
        D_ = 0
        for i in range(n):
            if i == 0:
                D_ += abs(sum(array[:nums[0]]) - μ)
            elif i == n - 1:
                D_ += abs(sum(array[nums[-1]:]) - μ)
            else:
                D_ += abs(sum(array[nums[i - 1]:nums[i]]) - μ)
        if D_ < σ_fake:
            σ_fake = D_
            nums_opt = [i for i in nums]
        add1pos = -1
        for i in range(n - 2, -1, -1):
            pos = nums[i]
            if pos + 1 + n - 2 - i < len(array):
                add1pos = i
                break
        if add1pos < 0:
            break
        nums[add1pos] += 1
        for i in range(add1pos + 1, n - 1):
            nums[i] = nums[i - 1] + 1
    array_L = []
    for i in range(n):
        if i == 0:
            array_L.append(array[:nums_opt[0]])
        elif i == n - 1:
            array_L.append(array[nums_opt[-1]:])
        else:
            array_L.append(array[nums_opt[i - 1]:nums_opt[i]])
    return array_L
        
        
def cumulative_sum(sequence):
    """获得一个序列中每个序列的长度,并进行累加

    Args:
        sequence (list): [[],..]

    Returns:
        list: 子序列长度的累加和
    """
    r, s = [], 0
    for e in sequence:
        l = len(e)
        r.append(l + s)
        s += l
    return r


def obj_to_flat_aux(obj: Any):
    """将一个对象中的 list/tuple/dict/OrderedDict 递归展平成一个list
    可用于解决pytorch中有些forward输入不能嵌套tensor的问题

    Args:
        obj (Any): 展平的对象, 注意存在 OrderedDict 的话后面会还原成Dict

    Returns:
        list: flat, 展平的结果
        Any: aux, 结构类似 obj, obj中的非 list/tuple/dict/OrderedDict 递归对象会为None, 用于辅助flat还原
    """
    flat, aux = [], None
    if isinstance(obj, (list, tuple)):
        aux = []
        for v in obj:
            flat_, aux_ = obj_to_flat_aux(v)
            flat += flat_
            aux.append(aux_)
        aux = tuple(aux) if isinstance(obj, tuple) else aux
    elif isinstance(obj, (dict, OrderedDict)):
        aux = OrderedDict()
        for k, v in obj.items():
            flat_, aux[k] = obj_to_flat_aux(v)
            flat += flat_
    else:
        flat = [obj]
    return flat, aux


def flat_aux_to_obj(flat: list, aux: Any, flat_start=None):
    """递归将 obj_to_flat_aux 生成的 flat,aux 还原成原来的 obj

    Args:
        flat (list): 展平的结果
        aux (Any): 结构类似还原前的 obj, 注意所有 OrderedDict 会还原成Dict
        flat_start (int, optional): 递归用参数, 不可修改

    Returns:
        Any: 还原的 obj
    """
    flat_start, return_flat_start = (0, False) if flat_start is None else (flat_start, True)
    if isinstance(aux, (list, tuple)):
        obj = []
        for v in aux:
            obj_, flat_start = flat_aux_to_obj(flat, v, flat_start)
            obj.append(obj_)
        obj = tuple(obj) if isinstance(aux, tuple) else obj
    elif isinstance(aux, (dict, OrderedDict)):
        obj = {}
        for k, v in aux.items():
            obj[k], flat_start = flat_aux_to_obj(flat, v, flat_start)
    else:
        obj, flat_start = flat[flat_start], flat_start + 1
    if return_flat_start:
        return obj, flat_start
    return obj


def scan_dir(root: str, use_scandir = True) -> List[str]:
    """递归扫描目录下的所有文件

    Args:
        root (str): 要扫描的目录
        use_scandir (bool, optional): 是否使用 os.scandir, 默认为 True。如果为 False 则使用 os.walk
            scandir 速度更快，可能快1/3，但可能递归深度过大会出现错误

    Returns:
        List[str]: 所有文件的绝对路径
    """
    if use_scandir:
        paths = []
        for entry in os.scandir(root):
            if entry.is_file():
                paths.append(entry.path)
            elif entry.is_dir():
                paths.extend(scan_dir(entry.path))
        return paths
    else:
        return [os.path.join(r, f) for r, _, files in os.walk(root) for f in files]


def fast_time_based_id():
    """快速生成一个时间戳id, 保证不会重复"""
    return f"{time.perf_counter_ns():x}-{global_random_part}-{os.getpid():x}-{next(global_counter):x}"


if __name__ == '__main__':
    class c:
        def __init__(self) -> None:
            pass

        @staticmethod
        def f(a, b=2, c=3, **kw):
            pass
    # get_func_para
    print('=' * 10, 'get_func_para')
    print(get_func_para(c), get_func_para(c.f))
    print()

    # cover_dict
    print('=' * 10, 'cover_dict')
    new_para = {'a': [1, 2, {'bb': 2}], 'b': {'c': (1, 2), 'd': 2}}
    default_para = {'a': [4, 2, {'b': 21}], 'b': {'c': (1, 1), 'd': 22, 'e': None}}
    pprint(cover_dict(new_para, default_para))
    new_para['dd'] = {12}
    print('allow_new:', cover_dict(new_para, default_para, allow_new=True))
    print()

    # arg_extreme_dict
    print('=' * 10, 'arg_extreme_dict')
    epoch = {
        str(i): {
            i2: {
                i3: random.randint(1, 100) for i3 in ['P', 'R', 'F1']
            } for i2 in ['train', 'dev', 'test']
        } for i in range(5)
    }
    put(['5', 'train'], epoch, {'P': 30, 'A': 1, 'a': 123})
    print('put-delete:', put(['5', 'train', 'a'], epoch, delete=True))
    # epoch = {
    #     '0': {'dev': {'evaluate': None},
    #           'test': {'evaluate': {'MAP': 0.11008076900138042,
    #                                 'NDCG': 0.23014383925192927,
    #                                 'bpref': 0.5968450000000048,
    #                                 'macro-F1': 0.10884098853570322,
    #                                 'macro-P': 0.20855,
    #                                 'macro-R': 0.07363544070065223}},
    #           'train': {'evaluate': {'MAP': 0,
    #                                  'NDCG': 0,
    #                                  'bpref': 0,
    #                                  'macro-F1': 0,
    #                                  'macro-P': 0,
    #                                  'macro-R': 0},
    #                     'model': {'acc': 0, 'loss': 1e+38}}},
    #     '1': {'train': {'model': {'acc': 0.9903333136013576,
    #                               'loss': 2.2860701941308523}}}
    # }
    print('原始值:')
    pprint(epoch)
    print('极值:')
    pprint(arg_extreme_dict(epoch, dv_reverse=True, ban_type=[dict, type(None)], dv_key=lambda t: -t[1]))
    print()

    # merge_dict / opt_value_dict / any_value_dict
    print('=' * 10, 'merge_dict / opt_value_dict / any_value_dict')
    dict1 = {1: {1: None, 3: 4, 5: 7, 9: 9}, 2: [1, 2], 3: 10, 11: [11, 1]}
    dict2 = {1: {1: 2, 3: None, 5: 6, 6: 6}, 3: {4: 1, 5: 2}, 11: [1, 1]}
    print('union_dict:', merge_dict([dict1, dict2, dict2]))
    print('intersection_dict:', merge_dict([dict1, dict2, dict2], False))
    ret = opt_value_dict(opt_value_dict(dict1, dict2, in_list=True), None, opt=lambda v1, v2: v1 > 4, in_list=True)
    print('opt_value_dict:', ret)
    print('any_value_dict:', any_value_dict(ret))
    print()

    # dict_to_pair / pair_to_dict
    print('=' * 10, 'dict_to_pair / pair_to_dict')
    print('dict_to_pair (in_list):', list(dict_to_pair(dict1, in_list=True)))
    print('dict_to_pair:', list(dict_to_pair(dict1)))
    print('pair_to_dict:', pair_to_dict(dict_to_pair(dict1)))
    print()

    # get_obj_sha512
    print('=' * 10, 'get_obj_sha512')
    a = {2, 3, 1, (1, 2)}, {1: ('123'), 2: 2}
    b = {2, 3, 1, (1, 2)}, {1: ['123'], 2: 2}
    c = {3, 2, 1, (1, 2)}, {2: 2, 1: ['123']}
    print('速度:', timeit.timeit(lambda: get_obj_sha512(a), number=20000))
    a_ = get_obj_sha512(a, True)
    b_ = get_obj_sha512(b, True)
    print('a==b:', a_[0] == b_[0])
    print('a out:', a_[1])
    print('b out:', b_[1])
    b_ = get_obj_sha512(b, False)
    c_ = get_obj_sha512(c, False)
    print('c==b:', c_[0] == b_[0])
    print('c out:', c_[1])
    print('b out:', b_[1])
    print()
    
    # 均匀分割
    print('=' * 10, 'fast_uniform_seg')
    a = fast_uniform_seg(5, [1]*24)
    print(a)
    print(cumulative_sum(a))
    print('=' * 10, 'acc_uniform_seg')
    a = acc_uniform_seg(5, [1]*24)
    print(a)
    print(cumulative_sum(a))
    print()
    
    # obj 和 flat,aux 的转换
    print('=' * 10, 'obj_to_flat_aux')
    obj = {...}, {1: ('123'), 2: dict, 3: []}, [{}, (), [[], 1, None, 3]]
    # obj = 0
    # obj = {}
    flat, aux = obj_to_flat_aux(obj)
    print('obj:', obj)
    print('flat:', flat)
    print('aux:', aux)
    print('=' * 10, 'flat_aux_to_obj')
    obj = flat_aux_to_obj(flat, aux)
    print('obj:', obj)
    print()
    
    # 测试 recur_opt_any
    print('=' * 10, 'recur_opt_any')
    a = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'f': '4'}
    print('原始值:', a)
    recur_opt_any(a, lambda k, t, v: (v, False, False))
    print('不处理:', a)
    recur_opt_any(a, lambda k, t, v: (v - 1, False, True) if isinstance(v, int) else (v, False, False))
    print('int-1:', a)
    recur_opt_any(a, lambda k, t, v: (v, True, False) if isinstance(v, dict) and v.get('d') else (v, False, False))
    print('del d:', a)

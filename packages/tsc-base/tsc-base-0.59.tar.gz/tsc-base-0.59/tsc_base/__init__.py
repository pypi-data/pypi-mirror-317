from .func import get_func_para, cover_dict, get, arg_extreme_dict, merge_dict, opt_value_dict, any_value_dict, pair_to_dict, dict_to_pair, put, recursion_stat, replace, get_obj_sha512, cumulative_sum, acc_uniform_seg, fast_uniform_seg, obj_to_flat_aux, flat_aux_to_obj, recur_opt_any, scan_dir, fast_time_based_id
from .dependency import Excel, range_time, Bib
from .web import bd_translate
from .py_static_cfg import Cfg, create_unduplicated_key, generate_random_string, unique_list_with_none, SafeAttributeAccessor, KeyNotFound, KEY_NOT_FOUND
from .cache import LRUCache
from .async_func import run_find_files_asyncio, run_fd_files_asyncio, handle_background_task_completion
from .myclass import TimerControl

# 常用变量
mark_letter = {  # 单字符tex标记和对应重音符号
    '`': {'a': 'à', 'e': 'è', 'o': 'ò', 'u': 'ù', 'i': 'ì'},
    '\'': {'a': 'á', 'e': 'é', 'o': 'ó', 'u': 'ú', 'n': 'ń', 'i': 'í', 'c': 'ć', 's': 'ś', 'z': 'ź'},
    '"': {'a': 'ä', 'e': 'ë', 'o': 'ö', 'u': 'ü', 'i': 'ï', 'y': 'ÿ'},
    '=': {'a': 'ā', 'e': 'ē', 'o': 'ō', 'u': 'ū', 'i': 'ī'},
    '^': {'a': 'â', 'e': 'ê', 'o': 'ô', 'u': 'û', 'i': 'î'},
    '~': {'a': 'ã', 'o': 'õ', 'n': 'ñ'},
    '.': {'e': 'ė', 'z': 'ż'},
}
fr_en_letter = {}  # {'à':'a',..}; 可用于替换
for _, v in mark_letter.items():
    for k, v2 in v.items():
        fr_en_letter[v2] = k
fr_letter = ''.join(list(fr_en_letter.keys()))  # 所有变音符号


# 其他需要依赖的模块
'''
# pip install watchdog
from tsc_base.file_event_monitor import *
# pip install datrie
from tsc_base.str_trie import *
# pip install pydantic
from tsc_base.mp_basemodel import *
'''

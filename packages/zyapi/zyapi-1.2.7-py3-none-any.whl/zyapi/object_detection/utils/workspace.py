# coding: utf-8
import os
import yaml
import copy
import importlib
import collections

try:
    collectionsAbc = collections.abc
except AttributeError:
    collectionsAbc = collections


class AttrDict(dict):
    def __init__(self, **kwargs):
        super(AttrDict, self).__init__()
        super(AttrDict, self).update(kwargs)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError("没有找到key:'{}'".format(key))


global_config = AttrDict()
BASE_KEY = '_BASE_'


def _load_config_with_base(base_path, file_path):
    """
    将所有_BASE_涉及到的yml数据整合到一个AttrDict中

    Args:
        file_path (str): yml文件地址

    Returns: dict
    """
    with open(file_path) as f:
        file_cfg = yaml.load(f, Loader=yaml.Loader)

    if BASE_KEY in file_cfg:
        all_base_cfg = AttrDict()
        base_ymls = list(file_cfg[BASE_KEY])
        for base_yml in base_ymls:
            if base_yml.startswith("~"):
                base_yml = os.path.expanduser(base_yml)
            if not base_yml.startswith('/'):
                base_yml = os.path.join(base_path, base_yml)

            base_cfg = _load_config_with_base(base_path, base_yml)
            all_base_cfg = merge_config(base_cfg, another_cfg=all_base_cfg)
        del file_cfg[BASE_KEY]
        return merge_config(file_cfg, another_cfg=all_base_cfg)

    return file_cfg


def load_config():
    """
    加载file_path文件.

    Args:
        device: machine platform

    Returns: global config
    """
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
    file_path = os.path.join(base_path, 'alarm_rules.yml')
    _, ext = os.path.splitext(file_path)
    assert ext in ['.yml', '.yaml'], "必须是yaml文件"

    cfg = _load_config_with_base(base_path, file_path)
    cfg['filename'] = os.path.splitext(os.path.split(file_path)[-1])[0]
    merge_config(cfg, base=True)

    global_config_copy = copy.deepcopy(global_config)

    return global_config_copy


def dict_merge(dct, merge_dct):
    """
    将两个dict整合到一个AttrDict中

    Args:
        dct: 将被融合的dict
        merge_dct: 需要整合到其他dict的dict

    Returns: dct
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict) and
                isinstance(merge_dct[k], collectionsAbc.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
    return dct


def dict_merge_base(dct, merge_dct):
    """
    将两个dict整合到一个dict中, 如果字典中套着字典, 则将其包在AttrDict类中

    Args:
        dct: 将被融合的dict
        merge_dct: 需要整合到其他dict的dict

    Returns: dct
    """
    for k, v in merge_dct.items():
        if isinstance(merge_dct[k], dict):
            attr = AttrDict()
            for m, n in merge_dct[k].items():
                if isinstance(merge_dct[k][m], dict):
                    attr2 = AttrDict()
                    for v, f in merge_dct[k][m].items():
                        attr2[v] = f
                    attr[m] = attr2
                else:
                    attr[k] = v
                    break
            dct.update(attr)
        else:
            dct[k] = merge_dct[k]
    return dct


def merge_config(config, another_cfg=None, base=False):
    """
    将config融合到global config.

    Args:
        config (dict): 将要被融合到config文件

    Returns: global config
    """
    global global_config
    if base:
        dct = global_config
        return dict_merge_base(dct, config)
    dct = another_cfg
    return dict_merge(dct, config)


def extract_schema(cls):
    """
    提取待注册类的信息

    Args:
        cls (type): 待注册类

    Returns:
        schema (AttrDict): AttrDict类型字典
    """
    schema = AttrDict()
    schema['name'] = cls.__name__
    schema['pymodule'] = importlib.import_module(cls.__module__)

    return schema


def register(name=None):
    """
    注册表

    Args:
        name (str): 别名

    Returns:
        cls (type): 类本身或函数生成类
    """
    if callable(name):
        cls = name
        return register()(cls)

    def wrapper(cls):
        nonlocal name
        if isinstance(cls, type) and cls.__name__ in global_config:
            raise ValueError(f"该类{cls.__name__}已经被注册过")
        if not isinstance(cls, type) and callable(cls):
            func = cls
            cls = type(
                cls.__name__, (object,), {
                    '__call__': lambda _, *arg, **kws: func(*arg, **kws),
                    '__doc__': func.__doc__,
                })
        if name:
            global_config[name] = cls
        else:
            global_config[cls.__name__] = cls

        return cls

    return wrapper


def create(cls_or_name, args=None, kws=None):
    """
    调用cls_or_name

    Args:
        cls_or_name (str): 类名
        args: 行参
        kws: 关键字参数

    Returns:
        cls_or_name.__call__(*args, **kws)
    """
    assert type(cls_or_name) in [type, str], "必须是类或类的名字"
    name = type(cls_or_name) == str and cls_or_name or cls_or_name.__name__
    cls = global_config[name]
    if args is None:
        args = ()
    return cls()(*args, **kws) if kws is not None else cls()(*args)


if __name__ == '__main__':
    a = load_config('cpu')
    print(a.behavior_1002002.target)

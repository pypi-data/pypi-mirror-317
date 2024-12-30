import datetime
import decimal
import functools
import hashlib
import importlib
import importlib.util
import logging
import os
import random
import re
import socket
import string
import struct
import threading
import time
import traceback
import urllib.parse as urllib2
from pathlib import Path
from typing import Union

import IPy
import dictlib
import yaml
from IPy import IP
from bson.decimal128 import Decimal128
from case_convert import snake_case

from caasm_tool.constants import DATETIME_FORMAT, DATE_FORMAT_1
from caasm_tool.re_table import VARIABLE_RE

logger = logging.getLogger()


def get_now():
    return datetime.datetime.now()


def get_now_format():
    """
    with format '%Y-%m-%d %H:%M:%S'
    """
    return datetime.datetime.now().strftime(DATETIME_FORMAT)


def get_today():
    return datetime.date.today()


def get_today_format():
    """
    with format '%Y-%m-%d'
    :return:
    """
    return datetime.date.today().strftime(DATE_FORMAT_1)


def load_yaml_content(yml_file_path):
    with open(yml_file_path, "r") as f:
        return yaml.safe_load(f)


def load_yaml_content_by_fd(fd):
    return yaml.safe_load(fd.read())


def generate_random_string(name="", number=8):
    """
    生成随机字符串
    """
    return f"{name}-{''.join(random.sample(string.ascii_letters + string.digits, number))}"


def load_module(module_define):
    return importlib.import_module(module_define)


def load_module_by_path(module_path, module_name=None):
    module_name = module_name or module_path
    spec = importlib.util.spec_from_file_location(str(module_name), module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reload_module(module):
    importlib.reload(module)


def load_entry(entry_define, entry_params=None, no_params_execute_flag=False):
    entry_params = entry_params or {}
    module_define, entry = entry_define.split(":")
    module_ = load_module(module_define)
    callback = None

    for entry in entry.split("."):
        if not callback:
            callback = module_
        callback = getattr(callback, entry, None)
        if not callback:
            break
    if callback:
        if entry_params:
            return callback(**entry_params)
        return callback if not no_params_execute_flag else callback()
    return


def load_class(class_define):
    module_define, class_name = class_define.split(":")
    module_ = load_module(module_define)
    return getattr(module_, class_name, None)


class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonInstance(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        unique_key = f"cls:{cls} args:{args}, kwargs:{kwargs}"
        if unique_key not in cls._instances:
            with cls._lock:
                cls._instances[unique_key] = super().__call__(*args, **kwargs)
        return cls._instances[unique_key]


def deduplicate(batch):
    return sorted(set(batch), key=batch.index)


def compute_md5(content: Union[str, bytes]):
    if isinstance(content, str):
        content = content.encode()
    obj = hashlib.md5(content)
    return obj.hexdigest()


def hump2underline(hump_str):
    sub = re.sub(VARIABLE_RE, r"\1_\2", hump_str).lower()
    return sub


def underline2hump(underline_str):
    sub = re.sub(r"(_\w)", lambda x: x.group(1)[1].upper(), underline_str)
    return sub


def number_to_ip(number: int):
    return socket.inet_ntoa(struct.pack("I", socket.htonl(number)))


def compare_version(version1, version2):
    def split_and_2_int(lst):
        """
        将字符串按照“.”分割，并将每部分转成数字
        :param lst:
        :return:
        """
        if not lst:
            return []
        lst = lst.split(".")
        result = []

        for n in lst:
            try:
                result.append(int(n))
            except Exception:
                pass
        return result

    def just_two_lists(lst1, lst2):
        """
        如果两个数字列表长度不一，需要将短一点的列表末尾补零，让它们长度相等
        :param lst1:
        :param lst2:
        :return:
        """
        l1, l2 = len(lst1), len(lst2)
        if l1 > l2:
            lst2 += [0] * (l1 - l2)
        elif l1 < l2:
            lst1 += [0] * (l2 - l1)
        return lst1, lst2

    def compare_version_lists(v1_lst, v2_lst):
        """
        比较版本号列表，从高位到底位逐位比较，根据情况判断大小。
        :param v1_lst:
        :param v2_lst:
        :return:
        """
        for v1, v2 in zip(v1_lst, v2_lst):
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0

    # 预处理版本号
    version1, version2 = just_two_lists(split_and_2_int(version1), split_and_2_int(version2))
    return compare_version_lists(version1, version2)


def extract(record, field):
    if not record:
        return None
    if not isinstance(record, dict):
        return None

    fields = field.split(".")
    if len(fields) == 1:
        return record.get(field)

    first_field = fields[0]
    new_record = record.get(first_field)
    next_field = ".".join(fields[1:])

    return _extract(new_record, next_field)


def restore(field, value, result):
    dictlib.dug(result, field, value)


def _extract(record, field):
    if isinstance(record, list):
        result = []
        for tmp_record in record:
            tmp_result = extract(tmp_record, field)
            if tmp_result is None:
                continue
            if isinstance(tmp_result, list):
                result.extend(tmp_result)
            else:
                result.append(tmp_result)
        return result
    else:
        return extract(record, field)


def get_ignore_exc_decorator(errors=(Exception,), default_value=None):
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                logger.error(f"Error ({e}) detail {traceback.format_exc()} skip")
                return default_value

        return new_func

    return decorator


def to_decimal(data):
    return Decimal128(decimal.Decimal(data))


def get_class_path(clazz):
    return str(clazz).replace("<class '", "").replace("'>", "")


def load_sub_class(path, parent_class, son_define_name):
    result = []
    try:
        path = Path(path)
        if not path.exists():
            return result
        if not path.is_dir():
            return result

        for son in path.iterdir():
            if son.is_dir():
                continue

            son_str = str(son)

            if son_str.endswith("pyc"):
                continue

            if son_str.endswith("__init__.py"):
                continue

            module = load_module_by_path(son)

            if not hasattr(module, son_define_name):
                continue
            son_class = getattr(module, son_define_name)
            if not issubclass(son_class, parent_class):
                continue
            result.append(son_class)
    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.warning(f"load sub_class error({e})")
    return result


def get_max_ip(ip: IP, ori_ip):
    ip_version = ip.version()

    if ip_version == 4:
        return _get_max_ipv4(ip, ori_ip)
    elif ip_version == 6:
        return _get_max_ipv6(ip, ori_ip)
    return None


def get_min_ip(ip: IP):
    ip_version = ip.version()

    if ip_version == 4:
        return _get_min_ipv4(ip)
    elif ip_version == 6:
        return _get_min_ipv6(ip)
    return None


def _get_min_ipv4(ip):
    return _handle_ip_core(ip, ".", "0", 4)


def _get_max_ipv4(ip, ori_ip):
    return _handle_ip_core(ip, ".", "255", 4, ori_ip=ori_ip)


def _get_max_ipv6(ip, ori_ip):
    return _handle_ip_core(ip, ":", "FFFF", 8, ori_ip=ori_ip)


def _get_min_ipv6(ip):
    return _handle_ip_core(ip, ":", "0000", 8)


def _handle_ip_core(ip, sep, value, length, ori_ip=""):
    if not ori_ip:
        ip_str = ip.strFullsize()
    else:
        ip_str = ori_ip
    ip_list = ip_str.split(sep)

    if len(ip_list) == length:
        ip_list[-1] = value
    else:
        while len(ip_list) != length:
            ip_list.append(value)
    return IP(sep.join(ip_list))


def get_random_number(number=8):
    return "".join([str(random.randint(0, 9)) for i in range(number)])


def get_random_string(number=32):
    return "".join(random.sample(string.ascii_letters + string.digits, number))


def right_replace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def left_replace(s, old, new, occurrence):
    li = s.split(old, occurrence)
    return new.join(li)


def build_url(address=None, url=None):
    if not address.endswith("/"):
        address = address + "/"
    if url.startswith("/"):
        url = url[1:]
    return urllib2.urljoin(address, url)


def is_ip(address):
    try:
        IPy.IP(address)
        return True
    except Exception as e:
        return False


def size_convert(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size


def dict_camel_to_snake(src):
    def _convert(attr):
        if isinstance(attr, dict):
            result = dict()
            for k, v in attr.items():
                if isinstance(k, str):
                    key = snake_case(k)
                else:
                    key = k
                result[key] = _convert(v)
        elif isinstance(attr, list):
            result = list()
            for item in attr:
                result.append(_convert(item))
        else:
            result = attr
        return result

    return _convert(src)


def get_mount_path():
    path = os.path.abspath(__file__)
    while not os.path.ismount(path):
        if path == "/":
            break
        path = os.path.dirname(path)
    return path


def sleep(seconds):
    time.sleep(seconds)


def merge_dicts(obj1, obj2):
    if not isinstance(obj1, dict) or not isinstance(obj2, dict):
        return obj1

    merged = obj1.copy()

    for key, value in obj2.items():
        if key in merged:
            if isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value

    return merged


#   将文本中的\t\n\r字符组合转换为相应的转义符号
def escape_text(text: str):
    return text.replace("\\t", "\t").replace("\\r", "\r").replace("\\n", "\n")


def get_mac_hash() -> str:
    MAC_address = "00:00:00:00:00:00"
    try:
        network_info = psutil.net_if_addrs()
        for _, snics in network_info.items():
            for snic in snics:
                if snic.family == psutil.AF_LINK:
                    MAC_address = snic.address
    except Exception:
        logger.warning("get_cpu_info error")
    return hashlib.md5(MAC_address.encode("utf-8")).hexdigest()


def is_english(s: str) -> bool:
    return any(char.isalpha() and (char.isascii()) for char in s)

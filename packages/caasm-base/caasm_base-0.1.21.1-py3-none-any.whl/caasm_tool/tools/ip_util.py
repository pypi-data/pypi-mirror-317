import logging

from IPy import IP

_LOG = logging.getLogger()


class IpType(object):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    UNKNOWN = "unknown"


def check_ip_multi_cidr_relation(value, cidr_values):
    result = False
    try:
        value = IP(value)
        for cidr_value in cidr_values:
            if value in IP(cidr_value):
                result = True
                break
    except Exception as e:
        _LOG.error(f"check_ip_multi_cidr_relation error({e})")
        return result
    else:
        return result


def get_ip_type(value):
    try:
        ip = IP(value)
        if ip.version() != 4:
            return IpType.UNKNOWN
        ip_binary_string = ip.strBin()
        if ip_binary_string.startswith("0"):
            if value.startswith("127") or value.startswith("0"):
                return IpType.UNKNOWN
            return IpType.A
        elif ip_binary_string.startswith("10"):
            return IpType.B
        elif ip_binary_string.startswith("110"):
            return IpType.C
        elif ip_binary_string.startswith("1110"):
            return IpType.D
        else:
            return IpType.E
    except Exception as e:
        _LOG.debug(f"get ip type error({e}), value is {value}")
    return IpType.UNKNOWN

from IPy import IP


def to_full_ip(ip):
    if ip is None:
        return None
    try:
        ip = IP(ip)
        return ip.strFullsize()
    except ValueError:
        return None


def get_full_ip(ip):
    if ip is None:
        return None
    try:
        ip = IP(ip)
        if ip.len() == 1:
            return ip.strFullsize()
        else:
            return None
    except ValueError:
        return None


def get_full_cidr(ip):
    if ip is None:
        return None
    try:
        ip = IP(ip)
        if ip.len() == 1:
            return None
        else:
            return ip.strFullsize()
    except ValueError:
        return None


def get_ip_segment(ip):
    if ip is None:
        return None
    ip_split = ip.split("-")
    if len(ip_split) != 2:
        return None
    try:
        start = get_full_ip(ip_split[0])
        end = get_full_ip(ip_split[1])
        if start > end:
            return None
        return {"start": start, "end": end}
    except ValueError:
        return None


def get_all_ips_in_cidr(ip_cidr, limit=65536):
    if not ip_cidr:
        return []
    try:
        cidr = IP(ip_cidr)
        if cidr.len() > limit:
            return []
    except ValueError:
        return []
    return [ip.strFullsize() for ip in cidr]


def get_all_ips_in_segment(ip_segment, limit=65536):
    start = get_full_ip(ip_segment.get("start"))
    end = get_full_ip(ip_segment.get("end"))
    if not start or not end:
        return []
    start = IP(start)
    end = IP(end)
    if (end.int() - start.int() + 1) > limit:
        return []
    ips = []
    ip = IP(start)
    end_ip = IP(end)
    while ip <= end_ip:
        ips.append(ip.strFullsize())
        ip = IP(ip.int() + 1)
    return ips

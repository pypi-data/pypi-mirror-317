import logging
import pkgutil

log = logging.getLogger()


def parse_module(point_name, path, package_path):
    storage_flag, result = set(), []
    for file_finer, name, is_pkg in pkgutil.iter_modules(package_path.__path__):

        if is_pkg:
            continue
        module_name = path + "." + name
        if module_name in storage_flag:
            continue
        module = file_finer.find_module(module_name).load_module(module_name)
        handler = getattr(module, point_name, "")
        if not handler:
            log.warning(f"Not found module({module}) define({point_name})")
            continue
        storage_flag.add(module_name)
        result.append(handler)
    return result


def parse_instance_callable(instance, flag, filter_flag=True):
    result = {}
    for prop_name in dir(instance):
        if not prop_name.startswith(flag):
            continue
        prop = getattr(instance, prop_name, None)

        if not callable(prop):
            continue

        name = prop_name.replace(flag, "") if filter_flag else prop_name

        result[name] = prop
    return result

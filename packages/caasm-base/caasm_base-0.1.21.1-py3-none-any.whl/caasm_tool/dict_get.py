from typing import Dict, List


def dict_get(path, context):
    paths = path.split(".")
    path_length = len(paths)
    if path_length == 1:
        return context.get(path)

    tmp_context = context.get(paths[0])
    if tmp_context is None:
        return None

    if isinstance(tmp_context, Dict):
        return dict_get(_get_sub_path(paths), tmp_context)
    elif isinstance(tmp_context, List):
        result = []
        for sub_context in tmp_context:
            sub_result = dict_get(_get_sub_path(paths), sub_context)
            if sub_result is None:
                continue
            result.extend(sub_result) if isinstance(sub_result, List) else result.append(sub_result)
        return result

    return None


def _get_sub_path(paths):
    return ".".join(paths[1:])

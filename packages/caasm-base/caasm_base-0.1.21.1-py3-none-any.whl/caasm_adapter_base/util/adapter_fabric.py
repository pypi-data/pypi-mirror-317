import functools
import random
from functools import partial, cmp_to_key

from caasm_tool.util import compare_version, extract


class AdapterFabricUtil:
    _empty_flags = [(), [], {}, "", None]
    _agents_field = "base.agents"
    _last_seen_field = "base.last_seen"

    def choose_record_by_last_seen(self, records):
        if not records:
            return None

        return sorted(records, key=functools.cmp_to_key(self._last_seen_compare))[0]

    def choose_max_property(self, records):
        if not records:
            return None

        current_index, current_score = None, None
        for index, record in enumerate(records):
            tmp_score = 0
            record = record["adapter"]

            for key, val in record.items():
                if val in self._empty_flags:
                    continue
                tmp_score += 1

            if current_index is None:
                current_index = index
                current_score = tmp_score

            if tmp_score > current_score:
                current_index = index
        return records[current_index]

    def choose_record_by_random(self, records):
        if not records:
            return None
        return random.choice(records)

    def choose_record_by_agent_version_status(self, records, clean_func=None, my_check=None):
        if not clean_func:
            clean_func = self._default_clean_agent_version

        compare_func = partial(self._agent_version_compare_status, clean_func=clean_func, my_check=my_check)

        return list(sorted(records, key=cmp_to_key(compare_func)))[0]

    def choose_record_by_agent_version(self, records, clean_func=None, my_check=None):
        if not clean_func:
            clean_func = self._default_clean_agent_version

        compare_func = partial(self._agent_version_compare, clean_func=clean_func, my_check=my_check)

        data = list(sorted(records, key=cmp_to_key(compare_func)))
        if data:
            return data[0]
        return

    @classmethod
    def _last_seen_compare(cls, x, y):
        x_last_seen = extract(x, cls._last_seen_field)
        y_last_seen = extract(y, cls._last_seen_field)

        if not x_last_seen:
            return 1

        if not y_last_seen:
            return 1

        if x_last_seen > y_last_seen:
            return -1
        return 1

    @classmethod
    def _agent_version_compare_status(cls, x, y, clean_func, my_check):
        x_agents = extract(x, cls._agents_field)
        y_agents = extract(y, cls._agents_field)  # y.get("agents")
        if not (x_agents and y_agents):
            return 1
        x_agent = x_agents[0]
        y_agent = y_agents[0]

        x_status = x_agent.get("status")
        y_status = y_agent.get("status")

        if x_status == y_status:
            return cls._agent_version_compare(x, y, clean_func, my_check)

        if x_status == 1:
            return -1
        if y_status == 1:
            return 1
        return cls._agent_version_compare(x, y, clean_func, my_check)

    @classmethod
    def _agent_version_compare(cls, x, y, clean_func, my_check):
        x_agents = extract(x, cls._agents_field)
        y_agents = extract(y, cls._agents_field)  # y.get("agents")

        if not (x_agents and y_agents):
            return 1
        x_agent = x_agents[0]
        y_agent = y_agents[0]

        x_version = x_agent.get("version")
        y_version = y_agent.get("version")

        x_last_online_time = x_agent.get("last_online_time")
        y_last_online_time = y_agent.get("last_online_time")

        if x_version == y_version:
            if x_last_online_time and y_last_online_time:
                if x_last_online_time > y_last_online_time:
                    return -1
                else:
                    return 1

            return 0

        if my_check:
            continue_flag, check_ans = my_check(x_version, y_version)
            if not continue_flag:
                return check_ans

        x_version = clean_func(x_version)
        y_version = clean_func(y_version)

        return compare_version(y_version, x_version)

    @classmethod
    def _default_clean_agent_version(cls, agent_version):
        return agent_version


fabric_util = AdapterFabricUtil()

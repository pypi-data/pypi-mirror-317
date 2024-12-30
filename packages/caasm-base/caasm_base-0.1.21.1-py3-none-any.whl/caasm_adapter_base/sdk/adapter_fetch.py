from functools import lru_cache

from caasm_adapter_base.sdk.base import BaseSDK


class BaseAdapterFetchSdk(BaseSDK):
    def find_fetch_data(self, adapter_instance_id, category, fetch_type, condition=None, fields=None):
        raise NotImplementedError()

    @lru_cache(128)
    def get_fetch_table(self, category, adapter_instance_id, fetch_type):
        raise NotImplementedError()

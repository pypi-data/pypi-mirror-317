class StorageManager:
    def __init__(self):
        self._mapper = {}
        self._build_func_maper = {}

    def build_client(self, storage_type: str, new_instance=False, **kwargs):
        if new_instance:
            return self._build_func_maper[storage_type](**kwargs)

        if storage_type not in self._mapper:
            build_function = self._build_func_maper[storage_type]

            client = build_function(**kwargs)
            self._mapper[storage_type] = client
        return self._mapper[storage_type]

    def register_build_function(self, storage_type, build_func):
        if storage_type in self._build_func_maper:
            return
        self._build_func_maper[storage_type] = build_func


storage_manager = StorageManager()

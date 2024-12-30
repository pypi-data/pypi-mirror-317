import threading


class Cacher:
    def __init__(self):
        self.pool = {}
        self.lock = threading.RLock()

    def get(self, key):
        return self.pool.get(key)

    def get_and_set(self, key, val=None):
        data = self.pool.get(key)
        if data is None:
            data = self.set(key, val)
        return data

    def set(self, key, val):
        with self.lock:
            self.pool[key] = val
        return self.pool[key]

    def clear(self):
        return self.pool.clear()

import traceback

from pymongo import MongoClient
import logging

from caasm_adapter_base.util.connection_method.base import ConnectionBaseMethod

log = logging.getLogger()


class MongodbConnectionHandle(ConnectionBaseMethod):
    DEFAULT_METHOD = "mongo_client"
    METHOD_LIST = ["mongo_client"]

    def __init__(self, address=None, method=None):
        super(MongodbConnectionHandle, self).__init__(address=address, method=method)
        self.method_map = {"mongo_client": self.mongo_client}

    def analysis_address(self):
        pass

    def mongo_client(self):
        try:
            client = MongoClient(self.ip, self.port, serverSelectionTimeoutMS=5000, socketTimeoutMS=5000)
            client.server_info()
            return True
        except Exception as e:
            log.error(
                f"mongo client Error({e}). IP is {self.ip} ,port is {self.port}detail is {traceback.format_exc()}"
            )
            return False


if __name__ == "__main__":
    a = MongodbConnectionHandle(address="")
    print(a.handle())

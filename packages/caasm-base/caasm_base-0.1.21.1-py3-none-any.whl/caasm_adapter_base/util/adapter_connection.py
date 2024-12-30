from caasm_adapter_base.util.connection_method.mongodb import MongodbConnectionHandle
from caasm_adapter_base.util.connection_method.http import WebApiConnectionHandle
from caasm_service_base.constants.connection_method import ConnectionType

AdapterConnectionHandleMap = {
    ConnectionType.Mongodb: MongodbConnectionHandle,
    ConnectionType.Http: WebApiConnectionHandle,
}


class AdapterConnectionUtil(object):
    def __init__(self, connection_type, *args, **kwargs):
        self._connection_type = connection_type
        self.args = args
        self.kwargs = kwargs

    def handle(self):
        adapter_connection = AdapterConnectionHandleMap
        if not self._connection_type in adapter_connection.keys():
            raise ValueError(
                f"connection_type not find ,please input right result,you input {self._connection_type},"
                f"right input is {adapter_connection.keys()}"
            )
        return adapter_connection[self._connection_type](self.args, self.kwargs).handle()


connection_util = AdapterConnectionUtil

class ConnectionBaseMethod(object):
    DEFAULT_METHOD = ""
    METHOD_LIST = []

    def __init__(self, address=None, method=None, data=None):
        self.ip = None
        self.port = None
        self.method = method
        self.address = address
        self.data = data
        self.method_map = {}
        self._method = None

    def check_data(self):
        if not self.ip:
            raise ValueError(f"ip  is must need! you input ip :{self.ip} ")
        if not self.method:
            self._method = self.DEFAULT_METHOD
        if self._method not in self.METHOD_LIST:
            raise ValueError(f"check method fail,please make sure you method in {self.METHOD_LIST}")

    def handle(self):
        self.analysis_address()
        self.check_data()
        return self.method_map[self._method]()

    def analysis_address(self):
        if not self.data:
            raise ValueError("address not input ,please input it")
        self.address = self.data.get("address")
        if not self.address:
            raise ValueError("address not input ,please input it")

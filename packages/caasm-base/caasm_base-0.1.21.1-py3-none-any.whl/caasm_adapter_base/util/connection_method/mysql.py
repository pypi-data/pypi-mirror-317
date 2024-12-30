import logging
import traceback

import pymysql

from caasm_adapter_base.util.connection_method.base import ConnectionBaseMethod

log = logging.getLogger()


class MysqlConnectionHandle(ConnectionBaseMethod):
    DEFAULT_METHOD = "mysql_client"
    METHOD_LIST = ["mysql_client"]

    def __init__(self, address=None, method=None, user=None, passwd=None, db=None):
        super(MysqlConnectionHandle, self).__init__(address=address, method=method)
        self.user = user
        self.passwd = passwd
        self.db = db
        self.method_map = {"mysql_client": self.mysql_client}

    def mysql_client(self):
        try:
            db = pymysql.Connect(
                host=self.ip, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset="utf8"
            )
            cursor = db.cursor()
            db.close()
            return True
        except Exception as e:
            log.error(
                f"mysql client Error({e}). IP is {self.ip} ,port is {self.port}"
                f"User is {self.user} , DB is {self.db}"
                f"detail is {traceback.format_exc()}"
            )
            return False

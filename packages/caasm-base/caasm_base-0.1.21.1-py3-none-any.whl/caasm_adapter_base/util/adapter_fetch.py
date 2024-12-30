from caasm_persistence_base.handler.storage.base import BasePersistenceHandler
from caasm_tool.constants import DATETIME_FORMAT
from caasm_tool.util import get_now


class BaseAdapterFetchUtil:
    def build_asset(self, data, fetch_type="default"):
        result = []
        fetch_time = get_now().strftime(DATETIME_FORMAT)
        data = data or []
        for info in data:
            temp = {"internal": {"fetch_type": fetch_type, "fetch_time": fetch_time}, "adapter": info}
            result.append(temp)
        return result

    def return_success(self, data):
        return data

    def init_driver(self):
        chrome_driver_path = self.get_driver_path()
        from seleniumwire import webdriver

        option = webdriver.ChromeOptions()
        option.add_argument("--ignore-certificate-errors")
        option.add_argument("--headless")
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=option)
        return driver

    def get_driver_path(self):
        raise NotImplementedError()

    def save_file(self, file_content: bytes, filename=None):
        raise NotImplementedError()

    def get_file(self, file_id):
        raise NotImplementedError()

    def check_file_exists(self, file_id):
        raise NotImplementedError()

    def delete_file(self, file_id):
        raise NotImplementedError()

import os

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import datetime

__all__ = [
    'SeleniumParser',
]


class SeleniumParser:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.driver_path = kwargs.get('driver_path')
        self.data_path = kwargs.get('data_path', './data')
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--enable-javascript')
        self.options.add_argument('--window-size=1920x1080')
        self.options.add_argument(
            "--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--ignore-certificate-errors')

        self.driver = webdriver.Chrome(self.driver_path, options=self.options)
        self.driver.set_page_load_timeout(30)
        self.check_data_path()
        self.page_load_timeout = kwargs.get('page_load_timeout', 10)

    def __del__(self):
        try:
            self.driver.close()
        except Exception as e:
            print(e)

    def open_page(self, url):
        self.driver.get(url)

    def screen_shot(self):
        self.open_page(self.url)
        file_path, file_name = self.get_image_name()
        self.driver.get_screenshot_as_file(file_path)
        return file_path, file_name

    def get_image_name(self):
        file_name = f'{datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}.png'
        file_path = '{}/{}'.format(self.data_path, file_name)
        return file_path, file_name

    def check_data_path(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)


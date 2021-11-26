import os

import yadisk

from log import get_logger

logger = get_logger('main')


class InvalidToken(Exception):
    def __init__(self):
        logger.info('Invalid Token')


class YandexApi:
    def __init__(self, **kwargs):
        self.token = kwargs.get('token')
        self.y = yadisk.YaDisk(token=self.token)
        self.is_valid = self.check_token()

        if not self.is_valid:
            raise InvalidToken

    def check_token(self):
        return self.y.check_token()

    def save_file(self, path, file, filename):
        self.y.upload(file, f'{path}{filename}')

    @staticmethod
    def get_token(application_id, application_secret):
        y = yadisk.YaDisk(application_id, application_secret)
        url = y.get_code_url()
        logger.info("Go to the following url: %s " % url)
        code = input("Enter the confirmation code: ")
        try:
            response = y.get_token(code)
            access_token = response.access_token
            logger.info('AccessToken: {}'.format(access_token))
            return access_token
        except yadisk.exceptions.BadRequestError:
            logger.info("Bad code")


if __name__ == '__main__':
    APP_ID = os.environ.get("APP_ID")
    APP_SECRET = os.environ.get("APP_SECRET")
    YandexApi.get_token(APP_ID, APP_SECRET)

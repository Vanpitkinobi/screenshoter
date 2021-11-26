import asyncio
import os

from log import get_logger
from parser import SeleniumParser
from yandex_disk import YandexApi

logger = get_logger('main')


async def run_periodic_heartbeat(link, api, timeout):

    while True:
        p = SeleniumParser(driver_path='./chromedriver', url=link)
        image_path, image_name = p.screen_shot()
        api.save_file('/data/', image_path, image_name)
        logger.info('Created screenshot {} of {}'.format(image_path, link))
        await asyncio.sleep(timeout)


if __name__ == '__main__':

    url = os.environ.get('APP_URL')
    token = os.environ.get('YANDEX_TOKEN')
    timeout = int(os.environ.get('APP_HEARTBEAT', 20))

    logger.info('Starting process')

    loop = asyncio.get_event_loop()

    api = YandexApi(token=token)

    api.check_token()

    loop.run_until_complete(run_periodic_heartbeat(url, api, timeout))
    try:
        loop.run_forever()
    finally:
        loop.close()

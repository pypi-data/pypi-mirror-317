from logging import getLogger

logger = getLogger(__name__)

def info(func):
    async def wrapper(*args):
        res = await func(*args)
        if res['success']:
            logger.info('Success')
        else:
            logger.info(res['msg'])
        return res

    return wrapper
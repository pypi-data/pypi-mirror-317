#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/12/25 18:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

from meutils.caches.redis_cache import cache
from meutils.db.orm import select_first
from meutils.schemas.db.oneapi_types import OneapiTask, OneapiUser, OneapiToken


# engine


@cache()
async def token2user(api_key: str):
    logger.debug(api_key)
    filter_kwargs = {
        "key": api_key[3:],
    }

    return await select_first(OneapiToken, filter_kwargs)


if __name__ == '__main__':
    arun(token2user('sk-q3uMFm0TFWi5lBQVhGwAWKup28j4omr9vThL4V5ynvdWdeZ8'))

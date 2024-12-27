#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/12/20 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from openai import AsyncClient
from meutils.pipe import *


# upstream_base_url: Optional[str] = Header(None),
# upstream_api_key: Optional[str] = Header(None),

async def make_request(
        base_url: str,
        path: str,
        api_key: Optional[str] = None,

        method: str = "GET",
        headers: Optional[dict] = None,
        payload: Optional[dict] = None,
        params: Optional[dict] = None,

):
    client = AsyncClient(base_url=base_url, api_key=api_key, default_headers=headers)

    options = {}
    if params:
        options["params"] = params

    if method == 'GET':
        response = await client.get(path, options=options, cast_to=object)
        return response
    elif method == 'POST':
        response = await client.post(path, body=payload, options=options, cast_to=object)
        return response


if __name__ == '__main__':
    base_url = "https://api.chatfire.cn/tasks/kling-57751135"
    base_url = "https://httpbin.org"

    arun(make_request(base_url=base_url, path='/ip'))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/12/16 17:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from meutils.schemas.jimeng_types import BASE_URL, MODELS_MAP, FEISHU_URL
from meutils.schemas.image_types import ImageRequest
from meutils.schemas.task_types import TaskResponse
from meutils.apis.jimeng.common import create_draft_content, get_headers, check_token
from meutils.config_utils.lark_utils import get_next_token_for_polling

from fake_useragent import UserAgent

ua = UserAgent()


async def create_task(request: ImageRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL, check_token)

    url = "/mweb/v1/aigc_draft/generate"

    headers = get_headers(url, token)

    if "http" in request.prompt:  # 图生
        request.model = "high_aes_general_v20_L:general_v2.0_L"

    draft_content = await create_draft_content(request, token)
    payload = {
        "extend": {
            "root_model": request.model,
            "template_id": ""
        },
        "submit_id": str(uuid.uuid4()),
        "metrics_extra": "{\"templateId\":\"\",\"generateCount\":1,\"promptSource\":\"custom\",\"templateSource\":\"\",\"lastRequestId\":\"\",\"originRequestId\":\"\"}",
        "draft_content": json.dumps(draft_content),
        "http_common_info": {
            "aid": 513695
        }
    }

    logger.debug(bjson(payload))

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))

    task_id = data.get("data", {}).get("aigc_data", {}).get("history_record_id")
    return TaskResponse(task_id=task_id, system_fingerprint=token)


async def get_task(task_id, token):
    url = "/mweb/v1/get_history_by_ids"
    headers = get_headers(url, token)
    payload = {
        "history_ids": [
            task_id
        ]
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.debug(bjson(data))
        # {'ret': '1015', 'errmsg': 'login error', 'systime': '1734524280', 'logid': '20241218201800AC3267447B287E9E6C46', 'data': None}
        item_list = (data.get("data") or {}).get(task_id, {}).get("item_list")
        image_data = map(lambda x: x.get("image", {}).get("large_images"), item_list)

        task_data = sum(image_data, []) | xmap_(lambda x: {"url": x.get("image_url")})

        return TaskResponse(
            task_id=task_id,
            data=task_data,
            message=data.get("errmsg"),
            status="success" if task_data else None,
        )


async def generate(request: ImageRequest):
    task_response = await create_task(request)
    for i in range(1, 10):
        await asyncio.sleep(max(10 / i, 1))
        response = await get_task(task_response.task_id, task_response.system_fingerprint)
        logger.debug(response)
        if data := response.data:
            return {"data": data}


if __name__ == '__main__':
    token = "eb4d120829cfd3ee957943f63d6152ed"

    # request = ImageRequest(prompt="做一个圣诞节的海报", size="1024x1024")
    # request = ImageRequest(prompt="https://oss.ffire.cc/files/kling_watermark.png 让她带上墨镜", size="1024x1024")

    # task = arun(create_task(request))

    # task_id = "10040025470722"

    # task_id = "10053536381698"

    # task_id = "10079694738434"

    # task_id = "10080831230210"  # 图片编辑

    # task_id = "10082971040514"
    #
    # arun(get_task(task_id, token))

    # arun(get_task(task.task_id, task.system_fingerprint))

    arun(generate(ImageRequest(prompt="做一个圣诞节的海报")))

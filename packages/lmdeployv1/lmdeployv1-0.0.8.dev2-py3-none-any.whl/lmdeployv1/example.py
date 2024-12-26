#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : example
# Author  : zhoubohan
# Date    : 2024/12/6
# Time    : 11:37
# Description :
"""
from lmdeployv1.api import BatchChatCompletionRequest
from lmdeployv1.client import (
    LMDeployClient,
    MessageBuilder,
)

endpoint_uri = "http://10.211.18.203:8312/ep-svcdukcq"
client = LMDeployClient(endpoint=endpoint_uri)
image_url = (
    "http://tools.bj.bcebos.com/images/an.jpeg?authorization=bce-auth-v1%2FALTAKTZhksfCVgZJ96g46t21lA%2F2024"
    "-12-06T03%3A41%3A30Z%2F-1%2Fhost%2F524f024252d15ac895f6f41ecf53ff57a53a03cb70d1656a46ace7e39d572041"
)
message = {image_url: "Is there any cat in the image? only answer yes or no."}


def test_chat_completion():
    """
    test_chat_completion
    :return:
    """
    req = MessageBuilder.build_single_message(message)
    resp = client.chat_completion(messages=req)
    choice = [c.message for c in resp.choices]
    assert len(choice[0].content) > 1

    print(f"chat response: {choice[0].content}")


def test_batch_chat_completion():
    """
    test_batch_chat_completion
    :return:
    """
    msg = MessageBuilder.build_batch_messages([message])
    resp = client.batch_chat_completion(BatchChatCompletionRequest(messages=msg))
    choice = [c.message for c in resp.choices]
    assert len(choice[0].content) > 1

    print(f"batch chat response: {choice[0].content}")


if __name__ == "__main__":
    msg_dict = {'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.5.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=e7b137cb982555dbc65b7b53f4b26db1a377f7811acd5869a57357e854dfaada': '图中是否有猫？',
                'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.0.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=f64ca129991def3ce550191a1a8eced90a9b904b43eee5c79896282f67adc0ff': '图中是否有猫？',
                'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.4.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=48c39250b02a79f3fe10002e7d76c7824ba2659f8ba00d42052f9364b74626c2': '图中是否有猫？',
                'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.1.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=a4cfb88a32bd07de5401e43733553154281394bc58732253b95b2897c5c1858c': '图中是否有猫？'}

    message = [{'role': 'user', 'content': [{'type': 'text', 'text': '图中是否有猫？'}, {'type': 'image_url', 'image_url': {'url': 'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.5.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=e7b137cb982555dbc65b7b53f4b26db1a377f7811acd5869a57357e854dfaada'}}, {'type': 'text', 'text': '图中是否有猫？'}, {'type': 'image_url', 'image_url': {'url': 'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.0.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=f64ca129991def3ce550191a1a8eced90a9b904b43eee5c79896282f67adc0ff'}}, {'type': 'text', 'text': '图中是否有猫？'}, {'type': 'image_url', 'image_url': {'url': 'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.4.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=48c39250b02a79f3fe10002e7d76c7824ba2659f8ba00d42052f9364b74626c2'}}, {'type': 'text', 'text': '图中是否有猫？'}, {'type': 'image_url', 'image_url': {'url': 'http://10.92.54.93:8077/windmill/store/01de5ebf9cbb4eaa92c4919624d996dd/workspaces/wsgsdwed/projects/spiproject/annotationsets/as-0B5ZVIgg/IONHEaDx/data/images/cat.1.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20241226%2Fbj%2Fs3%2Faws4_request&X-Amz-Date=20241226T072950Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=a4cfb88a32bd07de5401e43733553154281394bc58732253b95b2897c5c1858c'}}]}]

"""
The response is generated by calling the quianwen api,
You can:
    Use qianwen models with your own api keys.
    Use other models(e.g. openAI) to get generated data
    
!!!!!NOTICE!!!!!
Qualities vary when it comes to different models,
author adopted qwen_max model for it's free to access.
"""

from http import HTTPStatus
import dashscope
import json
from rich.progress import track


def call_with_messages(message_data):
    messages = [
        {
            "role": "system",
            "content": "Conclude preferences of the user ONLY in the format: ([favorite cate1, favorite cate2, ...], preferred game price), rank from the most preferred to the least. Leave the price to 0.0 if there is no purchase info. DO NOT RETURN ANYTHING OTHER THAN THE SPECIFIED FORMAT STRING.",
        },
        {"role": "user", "content": message_data},
    ]
    dashscope.api_key = "sk-xxxxxxxxxxxxxxxxxxxx"  # api token
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_max,
        messages=messages,
        result_format="message",  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return response
    else:
        print(
            "Request id: %s, Status code: %s, error code: %s, error message: %s"
            % (
                response.request_id,
                response.status_code,
                response.code,
                response.message,
            )
        )
        return {}


f_dataset = open("./data/dataset/sft_no_groundtruth.json", "r", encoding="utf-8")

f_dataset_with_gd = open(
    "./data/dataset/sft_ai_groundtruth.json", "w", encoding="utf-8"
)

json_data = json.loads(f_dataset.read())


f_dataset = open("./data/dataset/sft_no_groundtruth.json", "r", encoding="utf-8")
f_dataset_with_gd = open(
    "./data/dataset/sft_ai_groundtruth.json", "w", encoding="utf-8"
)
json_data = json.loads(f_dataset.read())
for item in track(json_data):
    message = item["input"]
    resp = call_with_messages(message)
    item["output"] = (
        resp.get("output", {})
        .get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    print(item["output"])

f_dataset_with_gd.write(json.dumps(json_data, ensure_ascii=False, indent=4))
f_dataset_with_gd.close()
f_dataset.close()

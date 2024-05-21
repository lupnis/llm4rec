import json


def list_str_to_list(in_str: str):
    list_str = in_str[1:-1]
    str_list = list_str.split(", ")
    ret_str_list = []
    for str_item in str_list:
        if str_item.startswith("'") or str_item.startswith('"'):
            str_item = str_item[1:]
        if str_item.endswith("'") or str_item.endswith('"'):
            str_item = str_item[:-1]
        ret_str_list.append(str_item)
    return ret_str_list


def slice_data_tuple(in_str: str):
    text_str = in_str[1:-1]
    split_data = text_str.split(", ")
    price = float(split_data[-1])
    cates = ", ".join(split_data[:-1])
    return list_str_to_list(cates), price


file_ds = open("./data/dataset/sft_ai_groundtruth.json", "r", encoding="utf-8")
json_ds = json.loads(file_ds.read())

final_ds = []
for task in json_ds:
    if task["output"] == "":
        continue
    new_output = [[]]
    try:
        new_output = [*slice_data_tuple(task["output"])]
    except:
        pass
    finally:
        if not len(new_output) or not len(new_output[0]):
            ...
        else:
            task["output"] = str(new_output)
            final_ds.append(task)

with open("./data/dataset/sft_groundtruth.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(final_ds, ensure_ascii=False, indent=4))

print("done.")

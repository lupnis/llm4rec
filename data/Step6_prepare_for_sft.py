import json

json_doc = []

with open('./data/dataset/sft_groundtruth.json', 'r', encoding='utf-8') as f:
    json_doc = json.loads(f.read())
    
json_out = []
for item in json_doc:
    json_out.append({
        "input": f"Instruction: {item['instruction']}.\nInput: {item['input']}",
        "output": item["output"]
    })
    
with open('./data/final_for_sft.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(json_out, ensure_ascii=False, indent=4))
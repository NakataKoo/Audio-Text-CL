import json
import os

def merge_json_files(file_paths, output_file):
    merged_data = []
    current_audio_id = 1

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                item['audio_id'] = current_audio_id
                merged_data.append(item)
                current_audio_id += 1

    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(merged_data, output, ensure_ascii=False, indent=4)

# 使用例
json_files = ['dataset_train.json', 'dataset_val.json', 'dataset_test.json']  # 統合したいJSONファイルのパスをリストで指定
output_file = 'dataset_all.json'  # 統合後の出力ファイル名
merge_json_files(json_files, output_file)
import json

# 元のJSONファイルを読み込む
input_file = '/home/Nakata/muscall/data/datasets/musicbench/MusicBench_train.json'
output_file = '/home/Nakata/muscall/data/datasets/musicbench/dataset_train.json'

# 修正後のJSONデータを格納するリスト
modified_data = []

# 元のJSONデータを読み込む
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 各行のデータを処理
for i, line in enumerate(lines, start=1):
    # 行ごとのJSONオブジェクトをロード
    json_data = json.loads(line)
    
    # 新しいフォーマットに変換
    new_entry = {
        "audio_id": i,
        "caption": json_data.get("main_caption", ""),
        "audio_path": json_data.get("location", "").replace("data_aug2/", "").replace("data/", "").replace(".wav", ".npy")  # .wav を .npy に変換
    }
    
    # 新しいエントリをリストに追加
    modified_data.append(new_entry)

# 修正されたデータをJSONファイルに書き込む
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(modified_data, f, indent=4, ensure_ascii=False)

print("JSONファイルが修正され、出力されました。")

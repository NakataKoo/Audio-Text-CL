# Audio-Text Contrastive Learining for Muisic

## Setup
Create a fresh virtual environment:

```setup
python -m venv venv 
source venv/bin/activate
```

Then, clone the repository and install the dependencies:

```setup
git clone https://www.github.com/ilaria-manco/muscall 
cd muscall 
pip install -r requirements.txt
pip install -e .
```

## Preparing the dataset

### MusicBench Prepare:

```bash
cd /home/Nakata/muscall/data/datasets/
mkdir musicbench_tmp
cd /home/Nakata/muscall/data/datasets/musicbench_tmp
wget https://huggingface.co/datasets/amaai-lab/MusicBench/resolve/main/MusicBench.tar.gz
tar -zxvf MusicBench.tar.gz
rm -rf MusicBench.tar.gz
mv  /home/Nakata/muscall/data/datasets/musicbench_tmp/datashare/data/* /home/Nakata/muscall/data/datasets/musicbench_tmp/datashare/data_aug2
rm -rf /home/Nakata/muscall/data/datasets/musicbench_tmp/datashare/data/
mkdir audio
```

```python
import os
import numpy as np
from scipy.io import wavfile

def convert_wav_to_npy_in_directory(input_dir, output_dir):
    # ディレクトリBが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ディレクトリA内のすべての.wavファイルを取得
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".wav"):
            # WAVファイルのフルパス
            wav_path = os.path.join(input_dir, file_name)

            # 出力するnpyファイルのフルパス (拡張子をnpyに変更)
            npy_filename = os.path.splitext(file_name)[0] + ".npy"
            npy_path = os.path.join(output_dir, npy_filename)

            # WAVファイルの読み込み
            sample_rate, data = wavfile.read(wav_path)

            # NumPy配列として保存
            np.save(npy_path, data)

            print(f"'{wav_path}' を '{npy_path}' に変換しました。")

# ディレクトリAとディレクトリBを指定
input_directory = "/datashare/data_aug2"  # 例: 'A' をWAVファイルがあるディレクトリのパスに変更
output_directory = "/audio"  # 例: 'B' を保存先ディレクトリのパスに変更

# 変換実行
convert_wav_to_npy_in_directory(input_directory, output_directory)
```

```bash
rm -rf /home/Nakata/muscall/data/datasets/musicbench_tmp/datashare/data_aug2
```


### Details

MusCALL is trained on a multimodal dataset of (audio, text) pairs. 

Annotations should be provided in JSON format and must include the following fields:

```audio_id```:     the unique identifier for each audio track in the dataset

```caption``` :     a string with the textual description of the audio track 

```audio_path```:   path to the audio track, relative to the root audio directory

One JSON file per split must be provided and stored in the [`data/datasets`](data/datasets/) directory, following this structure:

```
dataset_name
├── audio            
│   ├── track_1.npy
│   ├── track_2.npy
|   └── ...
├── dataset_train.json    
├── dataset_val.json    
└── dataset_test.json
```

An illustrative example of the dataset is provided in [`data/datasets/audiocaption/`](data/datasets/audiocaption/).

## Training MusCALL
Dataset, model and training configurations are set in the respective `yaml` files in [`configs`](configs). You can also pass some options via the CLI, overwriting the arguments in the config files. For more details on the CLI options, please refer to the [training script](scripts/train.py).

To train the model with the default configs, simply run

```bash
cd scripts/
python train.py 
```

This will generate a `model_id` and create a new folder in [`save/experiments/`](save/experiments/) where the output will be saved.

If you wish to resume training from a saved checkpoint, run this command:

```bash
python train.py --experiment_id <model_id> 
```

## Evaluating MusCALL
Once trained, you can evaluate MusCALL on the cross-modal retrieval task:

```bash
python evaluate.py <model_id> retrieval
```

or, in the zero-shot transfer setting, on an arbitrary music classification task.

In our zero-shot evaluation, we include:

* `mtt`: auto-tagging on the [MagnaTagATune Dataset](https://mirg.city.ac.uk/codeapps/the-magnatagatune-dataset)
* `gtzan`: music genre classification on the [GTZAN dataset](http://marsyas.info/downloads/datasets.html)

```bash
python evaluate.py <model_id> zeroshot <dataset_name>
```

You'll need to download the datasets inside the [`datasets/`](datasets/) folder and preprocess them before running the zeroshot evaluation.

## License
This repository is released under the GNU General Public License v3.0 license. Please see the [LICENSE](LICENSE) file for more details.

Some of the code is adapted from the following repos: 
* [CLIP](https://github.com/openai/CLIP/) by [@openai](https://github.com/openai/)
* [x-clip](https://github.com/lucidrains/x-clip/) by [@lucidrains](https://github.com/lucidrains/)


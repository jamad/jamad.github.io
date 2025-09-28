<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# Q&A 
## pyenv で 一時的に古いバージョンのpython を使いたい
* tensorflow が　古いバージョンだったので。俺のデフォルト環境は　Python 3.9.6
## タイトルだけのメールを送りたい。
* `practicePython\scraping\varaamo_checker_2024.py`　でやったのでそれを確認しよう
## ダウンロード系処理はマルチスレッドで高速化したい　
* `practicePython\XML\rss_checker.py` でやったのでそれを確認しよう
## 質問できるサイト等
* `https://teratail.com/` を使ってみよう（未登録）
* `https://qiita.com/cannorin/items/eb062aae88bfe2ad6fe5`が参考になった　`エラーメッセージの読み方と対処，検索や質問の原則`

## VSCodeで問題が発生した場合
* select iterpreter で recommended を選ぶことが下記のエラーを解決した ![image](https://github.com/jamad/jamad.github.io/assets/949913/c7a99504-911e-47f4-a8ce-a991acb23322) 
  * import cv2 によるエラー `partially initialized module 'cv2' has no attribute 'gapi_wip_gst_GStreamerPipeline' (most likely due to a circular import)`
    

# Pip command list (下記の表)
* tkinter
  * `try:import Tkinter as tk # for Python2 except ImportError:import tkinter as tk # for Python3`

| ライブラリ      | インストールコマンド                 | エラーメッセージ                  |
|----------------|-------------------------------     |---------------------------       |
| cv2            | `pip install opencv-python`        | No module named 'cv2'            |
| pypdf2         | `pip install pypdf2`               | No module named 'PyPDF2'         |
| kivy           | `pip install kivy`                 | No module named 'kivy'           |
| graphillion    | `pip install graphillion`          |                                  |
| networkx       | `pip install networkx`             |                                  |
| bs4            | `Pip install beautifulsoup4`       | No module named 'bs4'            |
| pyperclip      | `Pip install pyperclip`            |                                  |
| PIL            | `pip install pillow`               | No module named 'PIL'            |
| pyinstaller    | `pip install pyinstaller`          | The term 'pyinstaller' is not recognized |
| matplotlib     | `pip install matplotlib`           | No module named 'matplotlib'     |
| pysimplegui    | `pip install pysimplegui`          | No module named 'PySimpleGUI'    |
| pandas         | `pip install pandas`               | No module named 'pandas'         |
| xlrd           | `pip install xlrd`                 | No module named 'xlrd'           |
| pyscreenshot   | `pip install pyscreenshot`         | No module named 'pyscreenshot'   |
| pyautogui      | `pip install pyautogui`            | cannot import name 'drag' from 'pyautogui' |
| Instagram api  | `pip install instagram_private_api`| No module named 'instagram_private_api' |
| pyglet         | `pip install pyglet`               | No module named 'pyglet'         |
| Tkinter        | `tkinter for python3`              | No module named 'Tkinter'        | 
| scipy          | `pip install scipy`                | No module named 'scipy'          |
| instaloader    | `pip install instaloader`          |                                  |
| pyws           | `pip install pyws`                 | No module named 'pyws'           |
| pyaudio        | `pip install "C:\Users\***\Downloads\PyAudio-0.2.11-cp39-cp39-win_amd64.whl` from `https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio` | No module named 'pyaudio' |





# よく使うTips
* ファイルのあるパスを取得する方法 \practicePython\scraping\selenium_basic_test_2024.py を見よ。
```
import os
current_directory = os.path.dirname(os.path.abspath(__file__)) # 現在のスクリプトのディレクトリを取得
imagepath = current_directory+"/img/jam_clock_icon.png"
```

# pipしているものの確認方法
* practicePython> `pip freeze > requirements.txt` と実行すれば
* practicePython のディレクトリ内にその txtが生成されるので、それを確認すれば良い

# VScode で interpreter の選択肢を少なくする方法
* 方法の基本は、パスに対応したものを削除する
* Anaconda関連は anacondaフォルダ内にあった uninstaller exe を実行するだけ。それで２つ消えた
* text gen webui はフォルダをがっつり削除しただけ。それで２つ消えた。

# 問題と解決方法

* pipコマンド
* `pip install bs4` for beautifulsoup 

* problem `invalid character in identifier`  [例](https://github.com/jamad/myPygame/commit/de48df759a5f5d60929908afdcabc22b14cbc6d3)
  * investigation[参考はあるものの未解決](https://stackoverflow.com/questions/14844687/invalid-character-in-identifier)
 
---

* problem `error: (-2:Unspecified error) The function is not implemented.Rebuild the library with Windows, GTK+ 2.x or Cocoa support. `
  * investigation : helpful reference >> https://stackoverflow.com/questions/67120450/error-2unspecified-error-the-function-is-not-implemented-rebuild-the-libra
    * solution
      * `pip uninstall opencv-python`
      * `pip install opencv-python`
 

# 動画を連番静止画に変換する簡単なGUIツール
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/091ebc2c-1368-4cec-b321-2ccb9bbab978)
```python
import tkinter as tk
from tkinter import filedialog
import subprocess

def choose_file():
    input_entry.delete(0, tk.END)
    input_entry.insert(0, filedialog.askopenfilename(title="動画を選んでね"))

def choose_folder():
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filedialog.askdirectory(title="フォルダを選んでね"))

def convert_video():
    if input_entry.get() and output_entry.get():
        subprocess.run(f'ffmpeg -i "{input_entry.get()}" "{output_entry.get()}/%04d.png"', shell=True)
    print('finished!')

# GUIの作成
root = tk.Tk()
root.title("動画を連番静止画に")

# 入力ファイルの選択
tk.Label(root, text="入力用動画:").grid(row=0, column=0)
input_entry = tk.Entry(root, width=80)
input_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=choose_file).grid(row=0, column=2)

# 出力先フォルダの選択
tk.Label(root, text="出力用フォルダ:").grid(row=1, column=0)
output_entry = tk.Entry(root, width=80)
output_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=choose_folder).grid(row=1, column=2)

# コンバートボタン
tk.Button(root, text="生成", command=convert_video).grid(row=2, column=1)

# GUIの実行
root.mainloop()

```

* その逆のツール
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/4b97ca77-34a9-4924-8ddc-86656fad28be)
```python
import tkinter as tk
from tkinter import filedialog
import subprocess

def choose_input_folder():
    input_entry.delete(0, tk.END)
    input_entry.insert(0, filedialog.askdirectory(title="入力用フォルダを選んでね"))

def choose_output_file():
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], title="動画ファイルを保存"))

def convert_images_to_video():
    input_folder, output_file = input_entry.get(), output_entry.get()
    if input_folder and output_file:
        subprocess.run(f'ffmpeg -framerate 25 -i "{input_folder}/%04d.png" -c:v libx264 -pix_fmt yuv420p "{output_file}"', shell=True)
    print('変換完了!')

# GUIの作成
root = tk.Tk()
root.title("連番静止画から動画に変換")

# 入力フォルダの選択
tk.Label(root, text="入力用フォルダ:").grid(row=0, column=0)
input_entry = tk.Entry(root, width=80)
input_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=choose_input_folder).grid(row=0, column=2)

# 出力ファイルの選択
tk.Label(root, text="出力用動画ファイル:").grid(row=1, column=0)
output_entry = tk.Entry(root, width=80)
output_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=choose_output_file).grid(row=1, column=2)

# コンバートボタン
tk.Button(root, text="変換開始", command=convert_images_to_video).grid(row=2, column=1)

# GUIの実行
root.mainloop()

```

  

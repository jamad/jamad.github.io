<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# よく使うTips
* ファイルのあるパスを取得する方法 \practicePython\scraping\selenium_basic_test_2024.py を見よ。
```
import os
current_directory = os.path.dirname(os.path.abspath(__file__)) # 現在のスクリプトのディレクトリを取得
imagepath = current_directory+"/img/jam_clock_icon.png"
```

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
```
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
  

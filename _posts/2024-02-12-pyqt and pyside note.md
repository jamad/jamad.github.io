<link rel="stylesheet" type="text/css" href="/assets/css/styles.css" />

# pyside　（要するに Qt for python のようだ）
* install は　`python -m pip install -U PySide6` 最後に6が必要なので注意
* %localappdata%\Programs\Python\Python310\Lib\site-packages\PySide6 に designer.exe が見つかるが、下記のようにEnvを設定すれば　`pyside6-designer` のコマンドだけで起動できる
* `pyside6-uic untitled.ui > Ui_MainWindow.py` のように認識させるために
   * ENV edit > user veriables > path に
     * `%localappdata%\Programs\Python\Python310\Scripts` と
     * `%localappdata%\Programs\Python\Python310` を追加した
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/e93eaee5-a417-4049-96f1-cacbc6b5f18c)
* できたファイルを保存したら .ui ファイルとなる
* ![image](https://github.com/jamad/jamad.github.io/assets/949913/0b18bbf1-6500-48ae-b0b4-7dec107e0da6)
* .uiファイルはコマンドでpyファイルにコンバートする。そのために、上記のパス通しは必須　`pyside6-uic untitled.ui > Ui_MainWindow.py`
* でも、できたファイルを実行しても何も起きない。今ここ。
* `https://qiita.com/karakuri-t910/items/9d418a4edab081990243` で最初から見直すべきだな。




# pyqt5
## installation (windows)
* `pip install pyqt5`
* `pip install pyqt5-tools`

### NB: base64 for img is via [Simple WYSIWYG editor Summernote](https://summernote.org/)  

![image](https://github.com/jamad/jamad.github.io/assets/949913/fae04ffb-b724-4e8d-bcc2-b3e94ddc185c)

## qt designer
* Pyqt5designer
    * ![image](https://github.com/jamad/jamad.github.io/assets/949913/a4b3b024-5836-469b-aef5-d77511822090)
* Scrollbox (QScrollArea - practicePython/PyQt5/practice_qscrollarea.py )
    * ![image](https://github.com/jamad/jamad.github.io/assets/949913/1aa2e378-1ff7-4b6c-be9c-17326fa42c98)

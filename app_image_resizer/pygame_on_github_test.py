from PIL import Image
from tkinter import filedialog

def open_image():
    # ファイルを選択するダイアログを表示
    file_path = filedialog.askopenfilename()
    
    # ファイルが選択されなかった場合は何もしない
    if not file_path:
        return
    
    # 画像を開く
    img = Image.open(file_path)
    
    # リサイズするサイズを指定します（ここでは幅と高さを半分にします）
    new_width = img.width // 2
    new_height = img.height // 2
    
    # 画像をリサイズします
    resized_img = img.resize((new_width, new_height))
    
    # 画像を表示
    resized_img.show()

open_image()

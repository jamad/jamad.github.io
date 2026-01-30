import sys
import os
import struct
import math
import wave
import random
import tempfile
import re
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QListWidget, 
                             QListWidgetItem, QTextEdit, QLabel, QSplitter, 
                             QComboBox, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QSize, QUrl, QBuffer, QIODevice
from PyQt6.QtGui import QIcon, QPixmap, QAction, QDragEnterEvent, QDropEvent, QImage, QColor
from PyQt6.QtMultimedia import QSoundEffect

from PIL import Image, ImageOps

# --- Sound Generator Utilities ---
# 外部アセットファイルなしで動作させるため、起動時にWAVファイルを動的に生成します。
def generate_tone(frequency, duration, volume=0.5, sample_rate=44100, wave_type='sine'):
    n_samples = int(sample_rate * duration)
    data = bytearray()
    for i in range(n_samples):
        t = float(i) / sample_rate
        if wave_type == 'sine':
            value = math.sin(2.0 * math.pi * frequency * t)
        elif wave_type == 'square':
            value = 1.0 if math.sin(2.0 * math.pi * frequency * t) > 0 else -1.0
        elif wave_type == 'saw':
            value = 2.0 * (t * frequency - math.floor(t * frequency + 0.5))
        else:
            value = 0
        
        # Apply simple envelope (fade out)
        envelope = 1.0 - (i / n_samples)
        packed_value = int(value * volume * envelope * 32767.0)
        data += struct.pack('<h', max(-32768, min(32767, packed_value)))
    return data

def save_wav(filename, data, sample_rate=44100):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(data)

def create_sfx_assets():
    """効果音アセットを一時ディレクトリに生成します"""
    temp_dir = tempfile.gettempdir()
    
    # SFX 1: Select (Selection click)
    select_path = os.path.join(temp_dir, 'pt_select.wav')
    save_wav(select_path, generate_tone(880, 0.05, 0.3, wave_type='square')) # High blip

    # SFX 2: Load (Shaking/Opening)
    load_path = os.path.join(temp_dir, 'pt_load.wav')
    # Create a sweep
    data = bytearray()
    for i in range(int(44100 * 0.3)):
        freq = 440 + (i / (44100 * 0.3)) * 880 # 440Hz to 1320Hz
        val = math.sin(2.0 * math.pi * freq * (i/44100))
        packed = int(val * 0.3 * 32767)
        data += struct.pack('<h', packed)
    save_wav(load_path, data)

    # SFX 3: Copy (Level Up / Success)
    copy_path = os.path.join(temp_dir, 'pt_copy.wav')
    # Major Arpeggio
    data = generate_tone(523.25, 0.1, 0.4, wave_type='square') # C
    data += generate_tone(659.25, 0.1, 0.4, wave_type='square') # E
    data += generate_tone(783.99, 0.1, 0.4, wave_type='square') # G
    data += generate_tone(1046.50, 0.2, 0.4, wave_type='square') # High C
    save_wav(copy_path, data)

    return {'select': select_path, 'load': load_path, 'copy': copy_path}


# --- Image Processing ---
def extract_prompt(image_path):
    """
    画像からプロンプト情報を抽出します。
    Stable Diffusion (PNG info 'parameters') を優先し、Exifなどもフォールバックとして確認します。
    Pillowで取得できない場合、バイナリ直接検索による抽出も試みます（ブックマークレットと同様のロジック）。
    """
    try:
        # 1. Try Pillow Metadata (Standard approach)
        with Image.open(image_path) as img:
            img.load() # データをロード
            info = img.info
            
            # 一般的なキーを順にチェック
            # parameters: Automatic1111等
            # Description, Comment: その他のツールや保存形式
            for key in ['parameters', 'Description', 'Comment']:
                if key in info:
                    return info[key]
            
            # JPEG Exif (UserComment)
            exif = img._getexif()
            if exif:
                # 37510 is UserComment
                if 37510 in exif:
                    return str(exif[37510])

        # 2. Fallback: Binary Regex Search (Bookmarklet logic)
        # ブックマークレットの正規表現: /(?<=Xt(?:parameters|Description|Comment)\0*)([^\0]+)/ug
        # これをPythonのバイト列検索で再現します。
        with open(image_path, 'rb') as f:
            data = f.read()
            # 'Xt' は 'tEXt' や 'iTXt' の末尾2文字に相当します
            # その後にキーワード(parameters等)が続き、Null文字(\x00)を挟んでデータ本体が来ると仮定します
            pattern = re.compile(b'Xt(?:parameters|Description|Comment)\x00+([^\x00]+)')
            match = pattern.search(data)
            if match:
                try:
                    # 見つかったバイト列をUTF-8でデコード
                    return match.group(1).decode('utf-8', errors='ignore')
                except:
                    pass

        return "No metadata found."

    except Exception as e:
        return f"Error reading metadata: {str(e)}"

# --- GUI Class ---
class PromptTileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PromptTile - Metadata Viewer")
        self.resize(1000, 700)
        self.setAcceptDrops(True) # ドラッグ＆ドロップ許可

        # Generate Sounds
        self.sfx_files = create_sfx_assets()
        self.sfx_select = QSoundEffect()
        self.sfx_select.setSource(QUrl.fromLocalFile(self.sfx_files['select']))
        self.sfx_load = QSoundEffect()
        self.sfx_load.setSource(QUrl.fromLocalFile(self.sfx_files['load']))
        self.sfx_copy = QSoundEffect()
        self.sfx_copy.setSource(QUrl.fromLocalFile(self.sfx_files['copy']))

        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1. Header Area
        header_layout = QHBoxLayout()
        
        self.btn_open = QPushButton("📂 Open Folder")
        self.btn_open.clicked.connect(self.open_folder_dialog)
        self.btn_open.setStyleSheet("padding: 5px 15px; font-weight: bold;")
        
        self.combo_size = QComboBox()
        self.combo_size.addItems(["32px", "64px", "128px"])
        self.combo_size.setCurrentIndex(2) # Default 128px
        self.combo_size.currentIndexChanged.connect(self.change_icon_size)
        
        header_layout.addWidget(self.btn_open)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Thumbnail Size:"))
        header_layout.addWidget(self.combo_size)
        
        main_layout.addLayout(header_layout)

        # 2. Main Content (Splitter)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Thumbnail Grid
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSpacing(10)
        self.list_widget.setMovement(QListWidget.Movement.Static) # 移動不可
        self.list_widget.setIconSize(QSize(128, 128))
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        # Style for ListWidget
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
            }
            QListWidget::item {
                border-radius: 5px;
                color: #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                border: 1px solid #6ab0ff;
            }
        """)

        # Right: Details Panel
        details_panel = QWidget()
        details_layout = QVBoxLayout(details_panel)
        
        self.preview_label = QLabel("Select an image")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px dashed #555;")
        
        self.text_prompt = QTextEdit()
        self.text_prompt.setReadOnly(True)
        self.text_prompt.setPlaceholderText("Prompt will appear here...")
        self.text_prompt.setStyleSheet("font-family: Consolas, monospace; font-size: 10pt;")
        
        self.btn_copy = QPushButton("📋 Copy Prompt")
        self.btn_copy.setMinimumHeight(50)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-size: 14px; 
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
        """)
        self.btn_copy.clicked.connect(self.copy_prompt_to_clipboard)

        details_layout.addWidget(QLabel("Preview:"))
        details_layout.addWidget(self.preview_label)
        details_layout.addWidget(QLabel("Prompt:"))
        details_layout.addWidget(self.text_prompt)
        details_layout.addWidget(self.btn_copy)

        splitter.addWidget(self.list_widget)
        splitter.addWidget(details_panel)
        splitter.setStretchFactor(0, 7) # Grid takes 70%
        splitter.setStretchFactor(1, 3) # Details takes 30%

        main_layout.addWidget(splitter)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready. Drag & Drop folder here.")

        # Apply a Dark Theme
        self.setStyleSheet("""
            QMainWindow { background-color: #333; color: #fff; }
            QLabel { color: #ddd; }
        """)

    # --- Logic ---

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # フォルダかファイルか判定してロード
            if os.path.isdir(files[0]):
                self.load_images_from_folder(files[0])
            else:
                # 複数ファイルドロップの簡易対応
                self.load_images_list(files)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.load_images_from_folder(folder)

    def load_images_from_folder(self, folder_path):
        extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        image_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if Path(file).suffix.lower() in extensions:
                    image_files.append(os.path.join(root, file))
        
        self.load_images_list(image_files)

    def load_images_list(self, image_paths):
        self.list_widget.clear()
        self.text_prompt.clear()
        self.preview_label.setText("Select an image")
        self.preview_label.setPixmap(QPixmap())
        
        # Play Load Sound
        self.sfx_load.play()
        self.status_bar.showMessage(f"Loading {len(image_paths)} images...")
        QApplication.processEvents() # UI更新

        count = 0
        for path in image_paths:
            try:
                # Pillowでサムネイル生成（プロポーション維持）
                with Image.open(path) as img:
                    img = ImageOps.contain(img, (256, 256)) # 少し大きめに作ってIconSizeで調整
                    
                    # PIL image to QPixmap
                    if img.mode == "RGB":
                        r, g, b = img.split()
                        img = Image.merge("RGB", (b, g, r))
                        im2 = img.convert("RGBA")
                        data = im2.tobytes("raw", "BGRA")
                        qim = QImage(data, im2.width, im2.height, QImage.Format.Format_ARGB32)
                        pixmap = QPixmap.fromImage(qim)
                    elif img.mode == "RGBA":
                        r, g, b, a = img.split()
                        img = Image.merge("RGBA", (b, g, r, a))
                        data = img.tobytes("raw", "BGRA")
                        qim = QImage(data, img.width, img.height, QImage.Format.Format_ARGB32)
                        pixmap = QPixmap.fromImage(qim)
                    else:
                        # Fallback for Grayscale etc
                        pixmap = QPixmap(path)

                item = QListWidgetItem(QIcon(pixmap), Path(path).name)
                item.setData(Qt.ItemDataRole.UserRole, path) # パスを保持
                item.setToolTip(path)
                self.list_widget.addItem(item)
                count += 1
                
                if count % 10 == 0:
                    QApplication.processEvents() # UIが固まらないように適度に更新
                    
            except Exception as e:
                print(f"Skipped {path}: {e}")

        self.status_bar.showMessage(f"Loaded {count} images.")

    def change_icon_size(self):
        size_str = self.combo_size.currentText()
        size = int(size_str.replace("px", ""))
        self.list_widget.setIconSize(QSize(size, size))

    def on_item_clicked(self, item):
        self.sfx_select.play()
        
        path = item.data(Qt.ItemDataRole.UserRole)
        
        # Extract Prompt
        prompt = extract_prompt(path)
        self.text_prompt.setText(prompt)
        
        # Show larger preview
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.preview_label.size(), 
                                          Qt.AspectRatioMode.KeepAspectRatio, 
                                          Qt.TransformationMode.SmoothTransformation)
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setText("")
        else:
            self.preview_label.setText("Image Error")

    def copy_prompt_to_clipboard(self):
        text = self.text_prompt.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.sfx_copy.play()
            self.status_bar.showMessage("Prompt copied to clipboard!", 3000)
        else:
            self.status_bar.showMessage("Nothing to copy.", 2000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptTileApp()
    window.show()
    sys.exit(app.exec())
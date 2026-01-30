import sys
import os
import struct
import math
import wave
import random
import tempfile
import re
import json
import base64
from io import BytesIO
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
    """
    try:
        if not os.path.exists(image_path):
            return "File not found (Offline Mode)"

        # 1. Try Pillow Metadata (Standard approach)
        with Image.open(image_path) as img:
            img.load() # データをロード
            info = img.info
            
            # 一般的なキーを順にチェック
            for key in ['parameters', 'Description', 'Comment']:
                if key in info:
                    return info[key]
            
            # JPEG Exif (UserComment)
            exif = img._getexif()
            if exif:
                # 37510 is UserComment
                if 37510 in exif:
                    return str(exif[37510])

        # 2. Fallback: Binary Regex Search
        with open(image_path, 'rb') as f:
            data = f.read()
            pattern = re.compile(b'Xt(?:parameters|Description|Comment)\x00+([^\x00]+)')
            match = pattern.search(data)
            if match:
                try:
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
        self.setWindowTitle("PromptTile - Metadata Collector")
        self.resize(1100, 700)
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
        
        self.btn_open = QPushButton("📂 Add Images")
        self.btn_open.clicked.connect(self.open_folder_dialog)
        self.btn_open.setStyleSheet("padding: 5px 10px; font-weight: bold;")

        # Save / Load Buttons
        self.btn_save = QPushButton("💾 Save Book")
        self.btn_save.clicked.connect(self.save_collection)
        self.btn_save.setStyleSheet("padding: 5px 10px; background-color: #0078d7; color: white;")
        
        self.btn_load = QPushButton("📖 Load Book")
        self.btn_load.clicked.connect(self.load_collection)
        self.btn_load.setStyleSheet("padding: 5px 10px; background-color: #d7cd00; color: black;")

        self.btn_clear = QPushButton("🗑️ Clear")
        self.btn_clear.clicked.connect(self.clear_list)
        self.btn_clear.setStyleSheet("padding: 5px 10px;")
        
        self.combo_size = QComboBox()
        self.combo_size.addItems(["32px", "64px", "128px"])
        self.combo_size.setCurrentIndex(2) # Default 128px
        self.combo_size.currentIndexChanged.connect(self.change_icon_size)
        
        header_layout.addWidget(self.btn_open)
        header_layout.addWidget(self.btn_save)
        header_layout.addWidget(self.btn_load)
        header_layout.addWidget(self.btn_clear)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Size:"))
        header_layout.addWidget(self.combo_size)
        
        main_layout.addLayout(header_layout)

        # 2. Main Content (Splitter)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Thumbnail Grid
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSpacing(8)
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
        self.preview_label.setWordWrap(True)
        
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
            if os.path.isdir(files[0]):
                self.load_images_from_folder(files[0])
            else:
                self.load_images_list(files)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.load_images_from_folder(folder)

    def clear_list(self):
        self.list_widget.clear()
        self.text_prompt.clear()
        self.preview_label.clear()
        self.preview_label.setText("List cleared.")
        self.status_bar.showMessage("List cleared.")

    def load_images_from_folder(self, folder_path):
        extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        image_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if Path(file).suffix.lower() in extensions:
                    image_files.append(os.path.join(root, file))
        
        self.load_images_list(image_files)

    def load_images_list(self, image_paths):
        # 注意: 既存リストをクリアせずに追記する仕様に変更
        
        # Play Load Sound
        self.sfx_load.play()
        self.status_bar.showMessage(f"Adding {len(image_paths)} images...")
        QApplication.processEvents()

        # 重複チェック用セット
        existing_paths = set()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            # 既存アイテムに格納されているパス、またはIDを取得
            data = item.data(Qt.ItemDataRole.UserRole)
            if isinstance(data, dict):
                existing_paths.add(data.get('path', ''))
            else:
                existing_paths.add(data)

        count = 0
        for path in image_paths:
            if path in existing_paths:
                continue

            try:
                # Pillowでサムネイル生成
                with Image.open(path) as img:
                    img = ImageOps.contain(img, (128, 128))
                    
                    # QPixmap変換
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
                        pixmap = QPixmap(path)

                item = QListWidgetItem(QIcon(pixmap), Path(path).name)
                
                # アイテムデータとして辞書を持たせる (拡張性のため)
                item_data = {
                    'path': path,
                    'prompt': None, # クリック時に取得
                    'thumbnail_b64': None # 保存時に生成
                }
                item.setData(Qt.ItemDataRole.UserRole, item_data)
                
                item.setToolTip(path)
                self.list_widget.addItem(item)
                count += 1
                
                if count % 10 == 0:
                    QApplication.processEvents()
                    
            except Exception as e:
                print(f"Skipped {path}: {e}")

        self.status_bar.showMessage(f"Added {count} new images.")

    def change_icon_size(self):
        size_str = self.combo_size.currentText()
        size = int(size_str.replace("px", ""))
        self.list_widget.setIconSize(QSize(size, size))

    def on_item_clicked(self, item):
        self.sfx_select.play()
        
        data = item.data(Qt.ItemDataRole.UserRole)
        
        # 互換性維持（古い形式のデータが混ざっている場合）
        if isinstance(data, str): 
            path = data
            prompt = extract_prompt(path)
        else:
            path = data.get('path')
            # プロンプトが既にメモリにあればそれを使う
            if data.get('prompt'):
                prompt = data.get('prompt')
            else:
                # なければ抽出して保存しておく
                prompt = extract_prompt(path)
                data['prompt'] = prompt
                item.setData(Qt.ItemDataRole.UserRole, data)

        self.text_prompt.setText(prompt)
        
        # プレビュー表示
        # 実ファイルが存在すればそれを表示、なければサムネイル（アイコン）を引き伸ばして表示
        if os.path.exists(path):
            pixmap = QPixmap(path)
        else:
            # 埋め込みデータやオフラインの場合、アイコンを拡大表示
            pixmap = item.icon().pixmap(512, 512)
            self.status_bar.showMessage("Original file not found. Showing thumbnail.", 3000)

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

    # --- Save / Load Logic ---

    def save_collection(self):
        """現在のリストをJSONファイルとして保存します。サムネイルは減色して軽量化します。"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Book", "", "JSON Files (*.json)")
        if not file_path:
            return

        self.status_bar.showMessage("Saving collection... This may take a moment.")
        QApplication.processEvents()

        collection_data = []
        
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            data = item.data(Qt.ItemDataRole.UserRole)
            
            path = data['path'] if isinstance(data, dict) else data
            
            # プロンプト取得（まだ取得してなければ抽出）
            prompt = data.get('prompt') if isinstance(data, dict) and data.get('prompt') else extract_prompt(path)
            
            # サムネイル生成（軽量化）
            # アイコンから取得するか、オリジナルから生成するか
            # 綺麗に残すためオリジナルから再生成を試みる
            thumb_b64 = None
            try:
                if os.path.exists(path):
                    with Image.open(path) as img:
                        # 1. リサイズ
                        img.thumbnail((128, 128))
                        # 2. 減色 (Quantize) - GIFのように256色以下に
                        img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=64)
                        # 3. Save to buffer as PNG (P mode PNG is very small)
                        buffered = BytesIO()
                        img.save(buffered, format="PNG", optimize=True)
                        thumb_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                else:
                    # オリジナルがない場合は現在のアイコンデータを使う（画質は落ちるかも）
                    pass 
            except Exception:
                pass

            collection_data.append({
                'filename': Path(path).name,
                'path': path,
                'prompt': prompt,
                'thumbnail': thumb_b64
            })

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(collection_data, f, ensure_ascii=False, indent=2)
            
            self.sfx_copy.play() # Success sound
            QMessageBox.information(self, "Success", f"Saved {len(collection_data)} items to book!")
            self.status_bar.showMessage("Save complete.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")

    def load_collection(self):
        """JSONファイルからコレクションを読み込みます"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Book", "", "JSON Files (*.json)")
        if not file_path:
            return

        self.list_widget.clear()
        self.sfx_load.play()
        self.status_bar.showMessage("Loading book...")
        QApplication.processEvents()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                collection_data = json.load(f)

            for item_data in collection_data:
                # サムネイル復元
                pixmap = None
                if item_data.get('thumbnail'):
                    try:
                        img_data = base64.b64decode(item_data['thumbnail'])
                        qimg = QImage.fromData(img_data)
                        pixmap = QPixmap.fromImage(qimg)
                    except:
                        pass
                
                # サムネイル復元失敗時のフォールバック
                if pixmap is None:
                    pixmap = QPixmap(128, 128)
                    pixmap.fill(QColor("#444"))

                list_item = QListWidgetItem(QIcon(pixmap), item_data.get('filename', 'Unknown'))
                
                # 内部データ構築
                internal_data = {
                    'path': item_data.get('path', ''),
                    'prompt': item_data.get('prompt', ''),
                    'thumbnail_b64': item_data.get('thumbnail')
                }
                list_item.setData(Qt.ItemDataRole.UserRole, internal_data)
                list_item.setToolTip(item_data.get('path', ''))
                
                self.list_widget.addItem(list_item)

            self.status_bar.showMessage(f"Loaded {len(collection_data)} items.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptTileApp()
    window.show()
    sys.exit(app.exec())
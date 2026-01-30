import sys
import os
import struct
import math
import wave
import tempfile
import re
import json
import base64
from io import BytesIO
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QListWidget, 
                             QListWidgetItem, QTextEdit, QLabel, QSplitter, 
                             QFrame, QMessageBox, QLineEdit, QSlider, QStyle,
                             QAbstractItemView, QGroupBox, QMenu)
from PyQt6.QtCore import Qt, QSize, QUrl, QThread, pyqtSignal
from PyQt6.QtGui import (QIcon, QPixmap, QDragEnterEvent, QDropEvent, 
                         QImage, QColor, QUndoStack, QUndoCommand, QKeySequence, QAction)
from PyQt6.QtMultimedia import QSoundEffect

from PIL import Image, ImageOps

# --- Sound Generator Utilities ---
# 起動時に効果音を生成します
def generate_tone(frequency, duration, volume=0.5, sample_rate=44100, wave_type='sine'):
    n_samples = int(sample_rate * duration)
    data = bytearray()
    for i in range(n_samples):
        t = float(i) / sample_rate
        val = math.sin(2.0 * math.pi * frequency * t)
        if wave_type == 'square':
            val = 1.0 if val > 0 else -1.0
        envelope = 1.0 - (i / n_samples)
        packed_value = int(val * volume * envelope * 32767.0)
        data += struct.pack('<h', max(-32768, min(32767, packed_value)))
    return data

def save_wav(filename, data, sample_rate=44100):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1), f.setsampwidth(2), f.setframerate(sample_rate)
        f.writeframes(data)

def create_sfx_assets():
    temp_dir = tempfile.gettempdir()
    sfx = {}
    
    # Define sounds
    defs = [
        ('pt_select.wav', 880, 0.05, 'square'),
        ('pt_load.wav', 440, 0.1, 'sine'),
        ('pt_copy.wav', 1200, 0.1, 'sine'),
        ('pt_trash.wav', 150, 0.2, 'square')
    ]
    
    for name, freq, dur, wtype in defs:
        path = os.path.join(temp_dir, name)
        if not os.path.exists(path):
            save_wav(path, generate_tone(freq, dur, 0.3, wave_type=wtype))
        key = name.replace('pt_', '').replace('.wav', '')
        sfx[key] = path
        
    return sfx

# --- Metadata Extraction ---
def extract_metadata(image_path):
    """画像からメタデータ(プロンプト)を抽出"""
    info_dict = {"prompt": "No metadata found.", "tool": "Unknown"}
    if not os.path.exists(image_path): return info_dict
    
    try:
        with Image.open(image_path) as img:
            img.load()
            metadata = img.info or {}
            
            # A1111
            if 'parameters' in metadata:
                info_dict["prompt"] = metadata['parameters']
                info_dict["tool"] = "A1111"
                return info_dict
            
            # ComfyUI
            for key in ['prompt', 'workflow']:
                if key in metadata:
                    try:
                        # JSON整形して表示
                        json_str = json.dumps(json.loads(metadata[key]), indent=2, ensure_ascii=False)
                        info_dict["prompt"] = f"[{key} (ComfyUI)]\n{json_str}"
                        info_dict["tool"] = "ComfyUI"
                        return info_dict
                    except: pass
            
            # Exif / Civitai
            exif = img._getexif()
            if exif and 37510 in exif:
                info_dict["prompt"] = str(exif[37510])
                info_dict["tool"] = "Exif"
                return info_dict
                
    except Exception as e:
        info_dict["prompt"] = f"Error reading metadata: {e}"
        
    return info_dict

# --- Asynchronous Image Loader ---
class ImageLoaderThread(QThread):
    item_loaded = pyqtSignal(str, QPixmap, dict, int, int, str, float)
    finished_loading = pyqtSignal(int)

    def __init__(self, paths, icon_size=128):
        super().__init__()
        self.paths = paths
        self.icon_size = icon_size
        self.is_running = True

    def run(self):
        count = 0
        for path in self.paths:
            if not self.is_running: break
            try:
                if not os.path.exists(path): continue
                
                # メタデータ取得
                meta = extract_metadata(path)
                
                # 画像処理
                with Image.open(path) as img:
                    w, h = img.size
                    fmt = img.format or "IMG"
                    kb = os.path.getsize(path) / 1024
                    
                    # リサイズ
                    img = ImageOps.contain(img, (self.icon_size, self.icon_size))
                    
                    # RGB/BGR問題の修正: RGBAに変換し、Format_RGBA8888を使用
                    img = img.convert("RGBA")
                    data = img.tobytes("raw", "RGBA")
                    qim = QImage(data, img.width, img.height, QImage.Format.Format_RGBA8888)
                    pixmap = QPixmap.fromImage(qim)

                self.item_loaded.emit(path, pixmap, meta, w, h, fmt, kb)
                count += 1
                self.msleep(5) # UIのレスポンス維持のため少し待機
            except Exception: pass
            
        self.finished_loading.emit(count)

    def stop(self):
        self.is_running = False
        self.wait()

# --- Undo/Redo System ---
class ModifyItemsCommand(QUndoCommand):
    def __init__(self, list_widget, items, new_data_dict, description, app_ref):
        super().__init__(description)
        self.list_widget = list_widget
        self.items = items
        self.new_data_dict = new_data_dict
        # 変更前の状態を保存
        self.old_data_list = [item.data(Qt.ItemDataRole.UserRole).copy() for item in items]
        self.app_ref = app_ref

    def redo(self):
        for item in self.items:
            d = item.data(Qt.ItemDataRole.UserRole)
            for k, v in self.new_data_dict.items():
                d[k] = v
            item.setData(Qt.ItemDataRole.UserRole, d)
            self._update_visuals(item)
        self.app_ref.apply_filters() # フィルタを再適用

    def undo(self):
        for i, item in enumerate(self.items):
            item.setData(Qt.ItemDataRole.UserRole, self.old_data_list[i])
            self._update_visuals(item)
        self.app_ref.apply_filters()

    def _update_visuals(self, item):
        d = item.data(Qt.ItemDataRole.UserRole)
        # ゴミ箱なら赤背景
        if d.get('is_trashed', False):
            item.setBackground(QColor("#550000"))
        else:
            item.setBackground(QColor("#2b2b2b"))

# --- Main Application ---
class PromptTileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PromptTile v4 - Enhanced Loader")
        self.resize(1200, 850)
        self.setAcceptDrops(True)
        
        self.undo_stack = QUndoStack(self)
        self.loader_thread = None
        
        # 音声のロード
        sfx = create_sfx_assets()
        self.sfx_select = QSoundEffect()
        self.sfx_select.setSource(QUrl.fromLocalFile(sfx['select']))
        self.sfx_load = QSoundEffect()
        self.sfx_load.setSource(QUrl.fromLocalFile(sfx['load']))
        self.sfx_copy = QSoundEffect()
        self.sfx_copy.setSource(QUrl.fromLocalFile(sfx['copy']))
        self.sfx_trash = QSoundEffect()
        self.sfx_trash.setSource(QUrl.fromLocalFile(sfx['trash']))

        # === レイアウト構築 ===
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # -- 1. 上部コントロール --
        top_layout = QVBoxLayout()
        
        # 行1: ファイル操作系
        row1 = QHBoxLayout()
        
        # 新しいボタン構成
        self.btn_add_recur = QPushButton("📂 Add (All)")
        self.btn_add_recur.setToolTip("指定フォルダ以下の全ての画像を追加します")
        self.btn_add_recur.clicked.connect(lambda: self.open_folder_dialog(recursive=True))
        
        self.btn_add_flat = QPushButton("📂 Add (Flat)")
        self.btn_add_flat.setToolTip("指定フォルダ直下の画像のみ追加します（サブフォルダ無視）")
        self.btn_add_flat.clicked.connect(lambda: self.open_folder_dialog(recursive=False))

        self.btn_save = QPushButton("💾 Save")
        self.btn_save.clicked.connect(self.save_collection)
        self.btn_save.setStyleSheet("background-color: #0078d7; color: white;")
        
        self.btn_load = QPushButton("📖 Load")
        self.btn_load.clicked.connect(self.load_collection)
        self.btn_load.setStyleSheet("background-color: #d7cd00; color: black;")
        
        self.btn_clear = QPushButton("🗑️ Clear")
        self.btn_clear.clicked.connect(self.clear_list)
        
        # グリッドサイズ変更
        size_layout = QHBoxLayout()
        self.btn_size_s = QPushButton("S")
        self.btn_size_m = QPushButton("M")
        self.btn_size_l = QPushButton("L")
        
        self.size_group = [self.btn_size_s, self.btn_size_m, self.btn_size_l]
        sizes = [64, 128, 256]
        for btn, size in zip(self.size_group, sizes):
            btn.setFixedWidth(30)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, s=size, b=btn: self.change_icon_size(s, b))
        self.btn_size_m.setChecked(True) # デフォルト

        row1.addWidget(self.btn_add_recur)
        row1.addWidget(self.btn_add_flat)
        row1.addSpacing(10)
        row1.addWidget(self.btn_save)
        row1.addWidget(self.btn_load)
        row1.addWidget(self.btn_clear)
        row1.addStretch()
        row1.addWidget(QLabel("Size:"))
        for btn in self.size_group:
            row1.addWidget(btn)

        # 行2: 検索・フィルタリング
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: #252525; border-radius: 5px; padding: 2px;")
        row2 = QHBoxLayout(filter_frame)
        row2.setContentsMargins(5, 2, 5, 2)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search filename or prompt...")
        self.search_bar.textChanged.connect(self.apply_filters)
        self.search_bar.setFixedWidth(200)

        # 評価フィルタボタン群
        rating_layout = QHBoxLayout()
        rating_layout.setSpacing(2)
        
        self.btn_filter_all = QPushButton("ALL")
        self.btn_filter_all.setFixedWidth(40)
        self.btn_filter_all.clicked.connect(lambda: self.set_filter_all(True))
        
        self.btn_filter_none = QPushButton("NONE")
        self.btn_filter_none.setFixedWidth(40)
        self.btn_filter_none.clicked.connect(lambda: self.set_filter_all(False))

        rating_layout.addWidget(QLabel("Filter:"))
        rating_layout.addWidget(self.btn_filter_all)
        rating_layout.addWidget(self.btn_filter_none)
        
        self.rating_btns = {}
        for i in range(11):
            btn = QPushButton(str(i))
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setFixedWidth(25)
            btn.clicked.connect(self.apply_filters)
            btn.setStyleSheet("""
                QPushButton { background-color: #444; color: #aaa; border: 1px solid #555; }
                QPushButton:checked { background-color: #4a90e2; color: white; border: 1px solid #6ab0ff; }
            """)
            self.rating_btns[i] = btn
            rating_layout.addWidget(btn)

        # ゴミ箱フィルタボタン
        self.btn_filter_trash = QPushButton("🗑️")
        self.btn_filter_trash.setCheckable(True)
        self.btn_filter_trash.setFixedWidth(30)
        self.btn_filter_trash.setToolTip("Show/Hide Trash")
        self.btn_filter_trash.clicked.connect(self.apply_filters)
        self.btn_filter_trash.setStyleSheet("""
            QPushButton { background-color: #444; border: 1px solid #555; }
            QPushButton:checked { background-color: #d32f2f; border: 1px solid #ff6666; }
        """)

        row2.addWidget(self.search_bar)
        row2.addLayout(rating_layout)
        row2.addSpacing(10)
        row2.addWidget(self.btn_filter_trash)

        top_layout.addLayout(row1)
        top_layout.addWidget(filter_frame)
        main_layout.addLayout(top_layout)

        # -- 2. メインコンテンツ (左右分割) --
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左: サムネイル一覧
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_widget.setIconSize(QSize(128, 128))
        self.list_widget.setSpacing(6)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.setStyleSheet("QListWidget { background-color: #2b2b2b; border: none; }")

        # 右: 詳細パネル
        details_panel = QFrame()
        details_layout = QVBoxLayout(details_panel)
        
        # Undo / Redo
        ur_layout = QHBoxLayout()
        self.btn_undo = QPushButton("Undo")
        self.btn_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.btn_undo.clicked.connect(self.undo_stack.undo)
        
        self.btn_redo = QPushButton("Redo")
        self.btn_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.btn_redo.clicked.connect(self.undo_stack.redo)
        
        ur_layout.addWidget(self.btn_undo)
        ur_layout.addWidget(self.btn_redo)

        # 操作パネル (Rating, Trash)
        ctl_frame = QFrame()
        ctl_frame.setStyleSheet("background-color: #333; border-radius: 4px; padding: 5px;")
        ctl_layout = QVBoxLayout(ctl_frame)
        
        r_layout = QHBoxLayout()
        self.lbl_rate_val = QLabel("Rate: -")
        self.slider_rate = QSlider(Qt.Orientation.Horizontal)
        self.slider_rate.setRange(0, 10)
        self.slider_rate.valueChanged.connect(lambda v: self.lbl_rate_val.setText(f"Rate: {v}"))
        
        self.btn_set_rate = QPushButton("Set ★")
        self.btn_set_rate.setStyleSheet("background-color: #FFA500; color: black; font-weight: bold;")
        self.btn_set_rate.clicked.connect(self.set_rating)
        
        r_layout.addWidget(self.lbl_rate_val)
        r_layout.addWidget(self.slider_rate)
        r_layout.addWidget(self.btn_set_rate)
        
        self.btn_set_trash = QPushButton("🗑️ Toggle Trash")
        self.btn_set_trash.setCheckable(True)
        self.btn_set_trash.clicked.connect(self.set_trash)
        self.btn_set_trash.setStyleSheet("""
            QPushButton { background-color: #555; padding: 6px; }
            QPushButton:checked { background-color: #d32f2f; }
        """)
        
        ctl_layout.addLayout(r_layout)
        ctl_layout.addWidget(self.btn_set_trash)

        # プレビュー & 情報
        self.preview_label = QLabel("Select Image")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px dashed #555;")
        
        self.text_prompt = QTextEdit()
        self.text_prompt.setReadOnly(True)
        self.text_prompt.setStyleSheet("font-family: Consolas; font-size: 10pt; background: #222;")
        
        btn_copy = QPushButton("📋 Copy Prompt")
        btn_copy.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        btn_copy.clicked.connect(self.copy_prompt)

        details_layout.addLayout(ur_layout)
        details_layout.addWidget(ctl_frame)
        details_layout.addWidget(self.preview_label)
        details_layout.addWidget(QLabel("Prompt:"))
        details_layout.addWidget(self.text_prompt)
        details_layout.addWidget(btn_copy)

        splitter.addWidget(self.list_widget)
        splitter.addWidget(details_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready.")
        self.setStyleSheet("QMainWindow { background-color: #333; color: white; } QLabel { color: #ddd; }")

    # --- Logic Methods ---

    def dragEnterEvent(self, e): e.accept() if e.mimeData().hasUrls() else e.ignore()
    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        if files:
            # ドロップ時は、フォルダなら再帰的に読み込む仕様とする（あるいはダイアログを出す手もあるが今回は簡易化）
            if os.path.isdir(files[0]):
                self.load_images_from_folder_path(files[0], recursive=True)
            else:
                self.load_images_from_list(files)

    def open_folder_dialog(self, recursive=True):
        """フォルダ選択ダイアログ"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.load_images_from_folder_path(folder, recursive)

    def load_images_from_folder_path(self, folder_path, recursive=True):
        """指定パスから画像をリストアップ"""
        extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        image_files = []
        
        if recursive:
            # 再帰的 (os.walk)
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if Path(file).suffix.lower() in extensions:
                        image_files.append(os.path.join(root, file))
        else:
            # 直下のみ (os.listdir)
            try:
                for file in os.listdir(folder_path):
                    full_path = os.path.join(folder_path, file)
                    if os.path.isfile(full_path) and Path(file).suffix.lower() in extensions:
                        image_files.append(full_path)
            except Exception as e:
                print(f"Error reading folder: {e}")

        self.load_images_from_list(image_files)

    def load_images_from_list(self, paths):
        """画像リストを読み込みスレッドに投げる"""
        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.stop()
            
        # 既存チェック
        existing_paths = set()
        for i in range(self.list_widget.count()):
            d = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            existing_paths.add(d['path'])
        
        new_paths = [p for p in paths if p not in existing_paths]
        
        if not new_paths:
            self.status_bar.showMessage("No new images found.")
            return
        
        self.sfx_load.play()
        self.status_bar.showMessage(f"Loading {len(new_paths)} images...")
        
        current_size = self.list_widget.iconSize().width()
        self.loader_thread = ImageLoaderThread(new_paths, current_size)
        self.loader_thread.item_loaded.connect(self.add_item_to_widget)
        self.loader_thread.finished_loading.connect(lambda c: (self.status_bar.showMessage(f"Added {c} items."), self.apply_filters()))
        self.loader_thread.start()

    def add_item_to_widget(self, path, pixmap, meta, w, h, fmt, kb):
        item = QListWidgetItem(QIcon(pixmap), "")
        
        # ツールチップ作成
        tip = (
            f"<b>{Path(path).name}</b><br>"
            f"Size: {w}x{h} ({fmt})<br>"
            f"Disk: {kb:.1f} KB<br>"
            f"Tool: {meta['tool']}<br>"
            f"Prompt: {meta['prompt'][:100]}..."
        )
        item.setToolTip(tip)
        
        # データ格納
        item_data = {
            'path': path,
            'prompt': meta['prompt'],
            'rating': 0,
            'is_trashed': False,
            'thumbnail_b64': None
        }
        item.setData(Qt.ItemDataRole.UserRole, item_data)
        self.list_widget.addItem(item)
        
        # 追加直後にフィルタ適用（検索中などに対応）
        self.apply_filters()

    def on_item_clicked(self, item):
        self.sfx_select.play()
        d = item.data(Qt.ItemDataRole.UserRole)
        
        # UI更新
        self.text_prompt.setText(d['prompt'])
        
        self.slider_rate.blockSignals(True)
        self.slider_rate.setValue(d['rating'])
        self.slider_rate.blockSignals(False)
        self.lbl_rate_val.setText(f"Rate: {d['rating']}")
        
        self.btn_set_trash.blockSignals(True)
        self.btn_set_trash.setChecked(d['is_trashed'])
        self.btn_set_trash.blockSignals(False)
        
        # プレビュー表示
        if os.path.exists(d['path']):
            p = QPixmap(d['path'])
            if not p.isNull():
                self.preview_label.setPixmap(p.scaled(
                    self.preview_label.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                ))
        else:
            self.preview_label.setPixmap(item.icon().pixmap(256))

    # --- Filtering Logic ---
    def set_filter_all(self, state):
        for btn in self.rating_btns.values():
            btn.setChecked(state)
        self.apply_filters()

    def apply_filters(self):
        txt = self.search_bar.text().lower()
        active_ratings = {r for r, b in self.rating_btns.items() if b.isChecked()}
        show_trash = self.btn_filter_trash.isChecked()

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            d = item.data(Qt.ItemDataRole.UserRole)
            
            # 1. テキスト検索
            if txt and (txt not in Path(d['path']).name.lower() and txt not in d['prompt'].lower()):
                item.setHidden(True)
                continue
            
            # 2. ゴミ箱とレーティング
            is_trash = d.get('is_trashed', False)
            
            if is_trash:
                # ゴミ箱ボタンが押されている時のみ表示
                item.setHidden(not show_trash)
            else:
                # 通常アイテムはレーティングフィルタに従う
                rating = d.get('rating', 0)
                item.setHidden(rating not in active_ratings)

    # --- UI Controls ---
    def set_rating(self):
        items = self.list_widget.selectedItems()
        if not items: return
        v = self.slider_rate.value()
        self.undo_stack.push(ModifyItemsCommand(self.list_widget, items, {'rating': v}, f"Rate {v}", self))
        self.status_bar.showMessage(f"Rated {len(items)} items.")

    def set_trash(self):
        items = self.list_widget.selectedItems()
        if not items: return
        v = self.btn_set_trash.isChecked()
        self.undo_stack.push(ModifyItemsCommand(self.list_widget, items, {'is_trashed': v}, "Trash Toggle", self))
        if v: self.sfx_trash.play()
        self.status_bar.showMessage(f"Updated trash status for {len(items)} items.")

    def copy_prompt(self):
        QApplication.clipboard().setText(self.text_prompt.toPlainText())
        self.sfx_copy.play()

    def change_icon_size(self, size, btn):
        for b in self.size_group: b.setChecked(False)
        btn.setChecked(True)
        self.list_widget.setIconSize(QSize(size, size))

    def clear_list(self):
        if self.loader_thread: self.loader_thread.stop()
        self.list_widget.clear()
        self.undo_stack.clear()
        self.status_bar.showMessage("List cleared.")

    # --- Save / Load ---
    def save_collection(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Book", "", "JSON (*.json)")
        if not path: return
        
        arr = []
        for i in range(self.list_widget.count()):
            d = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            
            # 軽量化サムネイル生成(保存時のみ)
            if not d.get('thumbnail_b64') and os.path.exists(d['path']):
                try:
                    with Image.open(d['path']) as img:
                        img.thumbnail((128,128))
                        img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=64)
                        b = BytesIO()
                        img.save(b, "PNG", optimize=True)
                        d['thumbnail_b64'] = base64.b64encode(b.getvalue()).decode()
                except: pass
                
            arr.append({
                'filename': Path(d['path']).name,
                'path': d['path'],
                'prompt': d['prompt'], 
                'rating': d.get('rating',0), 
                'is_trashed': d.get('is_trashed',False), 
                'thumbnail': d.get('thumbnail_b64')
            })
            
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(arr, f, indent=2, ensure_ascii=False)
        self.sfx_copy.play()
        QMessageBox.information(self, "Saved", f"{len(arr)} items saved.")

    def load_collection(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Book", "", "JSON (*.json)")
        if not path: return
        
        self.clear_list()
        self.sfx_load.play()
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                arr = json.load(f)
                
            for d in arr:
                # サムネイル復元
                pix = QPixmap(128, 128)
                pix.fill(QColor("#444"))
                if d.get('thumbnail'):
                    try: pix.loadFromData(base64.b64decode(d['thumbnail']))
                    except: pass
                
                item = QListWidgetItem(QIcon(pix), "")
                
                # ツールチップ
                tip = (f"<b>{d.get('filename')}</b><br>"
                       f"Rate: {d.get('rating')}<br>"
                       f"Prompt: {d.get('prompt')[:50]}...")
                item.setToolTip(tip)
                
                # データ復元
                d.setdefault('thumbnail_b64', d.get('thumbnail'))
                item.setData(Qt.ItemDataRole.UserRole, d)
                
                if d.get('is_trashed'):
                    item.setBackground(QColor("#550000"))
                    
                self.list_widget.addItem(item)
                
            self.apply_filters()
            self.status_bar.showMessage(f"Loaded {len(arr)} items.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PromptTileApp()
    win.show()
    sys.exit(app.exec())
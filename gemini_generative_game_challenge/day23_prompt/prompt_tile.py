"""
[DEVELOPMENT NOTES FOR AI ASSISTANTS]
CURRENT VERSION: v20260130.01-GZIP

MANDATORY RULES FOR CODE MODIFICATION:
1. NO UNSOLICITED REFACTORING: Do not reorder, clean up, re-indent, or delete code unless explicitly requested.
   Maintain the exact indentation (4 spaces) and spacing found in this file.
2. PINPOINT MODIFICATIONS: Change only the specific lines or functions related to the user's request.
3. MAINTAIN STABLE LOGICS (PROMPT-TILE-SPECIFIC):
   - [COLOR CORRECTION]: QImage MUST use QImage.Format.Format_RGBA8888 with Pillow's RGBA mode to prevent blue-tint (BGR) issues.
   - [SQUARE THUMBNAILS]: Images must be pasted onto a transparent square background (padding to center).
   - [BATCH LOADING]: ImageLoaderThread MUST emit items in batches (e.g., 10 items) to prevent UI freeze.
   - [METADATA PRIORITY]: Try A1111 parameters -> ComfyUI JSON (stringified) -> Exif -> None.
   - [AUTO-TRASH]: If prompt length < 10 chars, set is_trashed=True automatically on load.
   - [SELECTION SYNC]: Right panel must clear/disable when selection is empty. Use currentItemChanged signal.
   - [COMPRESSION]: Save/Load must use GZIP + UTF-8 for the JSON structure to reduce file size.
   - [COMPATIBILITY]: Load function MUST attempt GZIP read first, falling back to plain text for legacy files.
4. AI PROTOCOL: If token limit is reached, instruct user to start a new chat with the current file.
5. VERSIONING: Always increment CURRENT VERSION using YYYYMMDD.XX format.
6. PRE-FLIGHT VERIFICATION (Internal Monologue):
   Before outputting code, verify these specific cases:
   [ ] Regression Test A: Does load_book handle both .json (plain) and .json.gz (compressed)?
   [ ] Regression Test B: Is QImage format explicitly RGBA8888?
   [ ] Logic Check: Is the < 10 char auto-trash logic present in the loader thread?

"""

import sys
import os
import struct
import math
import wave
import tempfile
import re
import json
import base64
import gzip  # Added for compression
from io import BytesIO
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QListWidget, 
                             QListWidgetItem, QTextEdit, QLabel, QSplitter, 
                             QFrame, QMessageBox, QLineEdit, QSlider, QStyle,
                             QAbstractItemView, QGroupBox, QMenu)
from PyQt6.QtCore import Qt, QSize, QUrl, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import (QIcon, QPixmap, QDragEnterEvent, QDropEvent, 
                         QImage, QColor, QUndoStack, QUndoCommand, QKeySequence, QAction)
from PyQt6.QtMultimedia import QSoundEffect

from PIL import Image, ImageOps

# --- Sound Generator Utilities ---
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
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(data)

def create_sfx_assets():
    temp_dir = tempfile.gettempdir()
    sfx = {}
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
    info = {"prompt": "", "tool": "Unknown"}
    if not os.path.exists(image_path):
        return info
    
    try:
        with Image.open(image_path) as img:
            img.load()
            meta = img.info or {}
            
            # 1. A1111
            if 'parameters' in meta:
                info["prompt"] = meta['parameters']
                info["tool"] = "A1111"
            else:
                # 2. ComfyUI
                found_comfy = False
                for k in ['prompt', 'workflow']:
                    if k in meta:
                        try:
                            json_str = json.dumps(json.loads(meta[k]), indent=2, ensure_ascii=False)
                            info["prompt"] = f"[{k}]\n{json_str}"
                            info["tool"] = "ComfyUI"
                            found_comfy = True
                            break
                        except:
                            pass
                
                # 3. Exif / Other
                if not found_comfy:
                    exif = img._getexif()
                    if exif and 37510 in exif:
                        info["prompt"] = str(exif[37510])
                        info["tool"] = "Exif"
                        
    except Exception as e:
        info["prompt"] = f"Error: {e}"
    
    return info

# --- Loader Thread (Batched for Speed) ---
class ImageLoaderThread(QThread):
    # Sends a list of items at once to reduce GUI overhead
    batch_loaded = pyqtSignal(list)
    finished_loading = pyqtSignal(int)

    def __init__(self, paths, icon_size=64):
        super().__init__()
        self.paths = paths
        self.icon_size = icon_size
        self.is_running = True

    def run(self):
        batch = []
        total = 0
        
        for path in self.paths:
            if not self.is_running:
                break
            try:
                if not os.path.exists(path):
                    continue
                
                meta = extract_metadata(path)
                
                with Image.open(path) as img:
                    w, h = img.size
                    fmt = img.format or "IMG"
                    kb = os.path.getsize(path) / 1024
                    
                    # --- 正方形サムネイル生成 ---
                    # 画像を縮小
                    img.thumbnail((self.icon_size, self.icon_size), Image.Resampling.LANCZOS)
                    
                    # 透明な台紙を作成
                    thumb = Image.new('RGBA', (self.icon_size, self.icon_size), (0, 0, 0, 0))
                    
                    # 中央に配置
                    offset_x = (self.icon_size - img.width) // 2
                    offset_y = (self.icon_size - img.height) // 2
                    thumb.paste(img, (offset_x, offset_y))
                    
                    # QPixmap作成 (RGBA8888で色化け防止)
                    data = thumb.tobytes("raw", "RGBA")
                    qim = QImage(data, thumb.width, thumb.height, QImage.Format.Format_RGBA8888)
                    pixmap = QPixmap.fromImage(qim)

                batch.append((path, pixmap, meta, w, h, fmt, kb))
                total += 1
                
                # 10枚ごとにGUIへ送信
                if len(batch) >= 10:
                    self.batch_loaded.emit(batch)
                    batch = []
                    self.msleep(10)

            except Exception:
                pass
            
        if batch:
            self.batch_loaded.emit(batch)
        self.finished_loading.emit(total)

    def stop(self):
        self.is_running = False
        self.wait()

# --- Undo Command ---
class ModifyItemsCommand(QUndoCommand):
    def __init__(self, items, new_data, desc, app):
        super().__init__(desc)
        self.items = items
        self.new_data = new_data
        self.app = app
        self.old_data = [i.data(Qt.ItemDataRole.UserRole).copy() for i in items]

    def redo(self):
        for i in self.items:
            d = i.data(Qt.ItemDataRole.UserRole)
            d.update(self.new_data)
            i.setData(Qt.ItemDataRole.UserRole, d)
            self._visuals(i)
        self.app.apply_filters()
        # 選択中のアイテムが変更された場合、右パネルも更新
        if self.items and self.items[0].isSelected():
            self.app.on_selection_change(self.items[0], None)

    def undo(self):
        for idx, i in enumerate(self.items):
            i.setData(Qt.ItemDataRole.UserRole, self.old_data[idx])
            self._visuals(i)
        self.app.apply_filters()
        if self.items and self.items[0].isSelected():
            self.app.on_selection_change(self.items[0], None)

    def _visuals(self, i):
        d = i.data(Qt.ItemDataRole.UserRole)
        if d.get('is_trashed'):
            i.setBackground(QColor("#550000"))
        else:
            i.setBackground(QColor("#2b2b2b"))

# --- Main Application ---
class PromptTileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PromptTile v7 - Compressed Save")
        self.resize(1200, 850)
        self.setAcceptDrops(True)
        self.undo_stack = QUndoStack(self)
        self.loader_thread = None
        
        # Audio
        sfx = create_sfx_assets()
        self.sfx_select = QSoundEffect()
        self.sfx_select.setSource(QUrl.fromLocalFile(sfx['select']))
        self.sfx_load = QSoundEffect()
        self.sfx_load.setSource(QUrl.fromLocalFile(sfx['load']))
        self.sfx_copy = QSoundEffect()
        self.sfx_copy.setSource(QUrl.fromLocalFile(sfx['copy']))
        self.sfx_trash = QSoundEffect()
        self.sfx_trash.setSource(QUrl.fromLocalFile(sfx['trash']))

        # --- Layout Construction ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1. Top Bar
        top_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        
        self.btn_add_recur = QPushButton("📂 Add (All)")
        self.btn_add_recur.clicked.connect(lambda: self.open_folder(True))
        
        self.btn_add_flat = QPushButton("📂 Add (Flat)")
        self.btn_add_flat.clicked.connect(lambda: self.open_folder(False))
        
        self.btn_save = QPushButton("💾 Save")
        self.btn_save.clicked.connect(self.save_book)
        self.btn_save.setStyleSheet("background-color: #0078d7; color: white;")
        
        self.btn_load = QPushButton("📖 Load")
        self.btn_load.clicked.connect(self.load_book)
        self.btn_load.setStyleSheet("background-color: #d7cd00; color: black;")
        
        self.btn_clear = QPushButton("🗑️ Clear List")
        self.btn_clear.clicked.connect(self.clear_list)
        
        row1.addWidget(self.btn_add_recur)
        row1.addWidget(self.btn_add_flat)
        row1.addSpacing(10)
        row1.addWidget(self.btn_save)
        row1.addWidget(self.btn_load)
        row1.addWidget(self.btn_clear)
        row1.addStretch()
        
        # Grid Size
        row1.addWidget(QLabel("Grid:"))
        self.btn_size_32 = QPushButton("32px")
        self.btn_size_64 = QPushButton("64px")
        self.size_group = [self.btn_size_32, self.btn_size_64]
        
        for btn, size in zip(self.size_group, [32, 64]):
            btn.setCheckable(True)
            btn.setFixedWidth(50)
            btn.clicked.connect(lambda c, s=size, b=btn: self.set_grid_size(s, b))
        
        row1.addWidget(self.btn_size_32)
        row1.addWidget(self.btn_size_64)

        # Filter Bar
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: #252525; border-radius: 4px; padding: 2px;")
        row2 = QHBoxLayout(filter_frame)
        row2.setContentsMargins(5, 2, 5, 2)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search...")
        self.search_bar.textChanged.connect(self.apply_filters)
        self.search_bar.setFixedWidth(200)
        
        self.btn_all = QPushButton("ALL")
        self.btn_all.setFixedWidth(40)
        self.btn_all.clicked.connect(lambda: self.toggle_rates(True))
        
        self.btn_none = QPushButton("NONE")
        self.btn_none.setFixedWidth(40)
        self.btn_none.clicked.connect(lambda: self.toggle_rates(False))
        
        row2.addWidget(self.search_bar)
        row2.addWidget(QLabel("Filter:"))
        row2.addWidget(self.btn_all)
        row2.addWidget(self.btn_none)
        
        self.rate_btns = {}
        for i in range(11):
            btn = QPushButton(str(i))
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setFixedWidth(25)
            btn.clicked.connect(self.apply_filters)
            btn.setStyleSheet("""
                QPushButton { background-color: #444; color: #aaa; border: none; }
                QPushButton:checked { background-color: #4a90e2; color: white; }
            """)
            self.rate_btns[i] = btn
            row2.addWidget(btn)
            
        self.btn_trash_view = QPushButton("🗑️")
        self.btn_trash_view.setCheckable(True)
        self.btn_trash_view.setFixedWidth(30)
        self.btn_trash_view.clicked.connect(self.apply_filters)
        self.btn_trash_view.setStyleSheet("""
            QPushButton { background-color: #444; border: 1px solid #555; }
            QPushButton:checked { background-color: #d32f2f; border: 1px solid #ff6666; }
        """)
        row2.addSpacing(10)
        row2.addWidget(self.btn_trash_view)

        top_layout.addLayout(row1)
        top_layout.addWidget(filter_frame)
        main_layout.addLayout(top_layout)

        # 2. Main Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: List
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_widget.setSpacing(1)
        # Selection Changed Signal
        self.list_widget.currentItemChanged.connect(self.on_selection_change)
        self.list_widget.setStyleSheet("""
            QListWidget { background-color: #2b2b2b; border: none; }
            QListWidget::item:selected { background-color: #4a90e2; border: 1px solid #6ab0ff; }
        """)
        
        # Right: Details
        details_panel = QFrame()
        details_layout = QVBoxLayout(details_panel)
        
        # Undo Controls
        undo_layout = QHBoxLayout()
        self.btn_undo = QPushButton("Undo")
        self.btn_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.btn_undo.clicked.connect(self.undo_stack.undo)
        
        self.btn_redo = QPushButton("Redo")
        self.btn_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.btn_redo.clicked.connect(self.undo_stack.redo)
        
        undo_layout.addWidget(self.btn_undo)
        undo_layout.addWidget(self.btn_redo)

        # Rating Controls
        ctl_frame = QFrame()
        ctl_frame.setStyleSheet("background-color: #333; border-radius: 4px; padding: 5px;")
        ctl_layout = QVBoxLayout(ctl_frame)
        
        r_row = QHBoxLayout()
        self.lbl_rate_val = QLabel("-")
        self.slider_rate = QSlider(Qt.Orientation.Horizontal)
        self.slider_rate.setRange(0, 10)
        self.slider_rate.valueChanged.connect(lambda v: self.lbl_rate_val.setText(str(v)))
        
        self.btn_set_rate = QPushButton("Set ★")
        self.btn_set_rate.setStyleSheet("background-color: #FFA500; color: black; font-weight: bold;")
        self.btn_set_rate.clicked.connect(self.set_rating)
        
        r_row.addWidget(QLabel("Rate:"))
        r_row.addWidget(self.lbl_rate_val)
        r_row.addWidget(self.slider_rate)
        r_row.addWidget(self.btn_set_rate)
        
        self.btn_toggle_trash = QPushButton("🗑️ Toggle Trash")
        self.btn_toggle_trash.setCheckable(True)
        self.btn_toggle_trash.clicked.connect(self.toggle_trash_state)
        self.btn_toggle_trash.setStyleSheet("""
            QPushButton { background-color: #555; padding: 6px; }
            QPushButton:checked { background-color: #d32f2f; }
        """)
        
        ctl_layout.addLayout(r_row)
        ctl_layout.addWidget(self.btn_toggle_trash)

        # Preview
        self.preview_label = QLabel("No Selection")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px dashed #555;")
        
        self.text_prompt = QTextEdit()
        self.text_prompt.setReadOnly(True)
        self.text_prompt.setStyleSheet("background-color: #222; font-family: Consolas; font-size: 10pt;")
        
        self.btn_copy = QPushButton("📋 Copy Prompt")
        self.btn_copy.clicked.connect(self.copy_prompt)
        self.btn_copy.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")

        details_layout.addLayout(undo_layout)
        details_layout.addWidget(ctl_frame)
        details_layout.addWidget(self.preview_label)
        details_layout.addWidget(QLabel("Prompt:"))
        details_layout.addWidget(self.text_prompt)
        details_layout.addWidget(self.btn_copy)

        splitter.addWidget(self.list_widget)
        splitter.addWidget(details_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready.")
        self.setStyleSheet("QMainWindow { background-color: #333; color: white; } QLabel { color: #ddd; }")
        
        # Init State
        self.set_grid_size(64, self.btn_size_64)
        self.reset_right_panel() # 初期状態は空にする

    # --- Logic ---

    def reset_right_panel(self):
        """右パネルの情報をクリアし、操作を無効化する"""
        self.preview_label.setText("No Selection")
        self.preview_label.setPixmap(QPixmap()) # Clear image
        self.text_prompt.clear()
        
        self.lbl_rate_val.setText("-")
        self.slider_rate.blockSignals(True)
        self.slider_rate.setValue(0)
        self.slider_rate.blockSignals(False)
        self.slider_rate.setEnabled(False)
        
        self.btn_set_rate.setEnabled(False)
        
        self.btn_toggle_trash.blockSignals(True)
        self.btn_toggle_trash.setChecked(False)
        self.btn_toggle_trash.blockSignals(False)
        self.btn_toggle_trash.setEnabled(False)
        
        self.btn_copy.setEnabled(False)

    def on_selection_change(self, current, previous):
        """アイテム選択変更時の処理"""
        if not current:
            # 選択解除された場合
            self.reset_right_panel()
            return
        
        # 選択された場合、GUI有効化
        self.slider_rate.setEnabled(True)
        self.btn_set_rate.setEnabled(True)
        self.btn_toggle_trash.setEnabled(True)
        self.btn_copy.setEnabled(True)
        
        self.sfx_select.play()
        d = current.data(Qt.ItemDataRole.UserRole)
        
        # プロンプト表示
        self.text_prompt.setText(d['prompt'])
        
        # レーティング表示
        self.slider_rate.blockSignals(True)
        self.slider_rate.setValue(d['rating'])
        self.slider_rate.blockSignals(False)
        self.lbl_rate_val.setText(str(d['rating']))
        
        # ゴミ箱状態表示
        self.btn_toggle_trash.blockSignals(True)
        self.btn_toggle_trash.setChecked(d['is_trashed'])
        self.btn_toggle_trash.blockSignals(False)
        
        # プレビュー画像表示
        if os.path.exists(d['path']):
            p = QPixmap(d['path'])
            if not p.isNull():
                scaled = p.scaled(self.preview_label.size(), 
                                  Qt.AspectRatioMode.KeepAspectRatio, 
                                  Qt.TransformationMode.SmoothTransformation)
                self.preview_label.setPixmap(scaled)
                self.preview_label.setText("")
        else:
            # ファイルが見つからない場合はアイコンを拡大
            self.preview_label.setPixmap(current.icon().pixmap(256))

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        if files:
            if os.path.isdir(files[0]):
                self.open_folder(True, files[0])
            else:
                self.load_files(files)

    def open_folder(self, recursive, path=None):
        target_dir = path or QFileDialog.getExistingDirectory(self, "Select Folder")
        if not target_dir:
            return
            
        file_list = []
        extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        
        if recursive:
            for root, _, fs in os.walk(target_dir):
                for x in fs:
                    if Path(x).suffix.lower() in extensions:
                        file_list.append(os.path.join(root, x))
        else:
            try:
                for x in os.listdir(target_dir):
                    full = os.path.join(target_dir, x)
                    if os.path.isfile(full) and Path(x).suffix.lower() in extensions:
                        file_list.append(full)
            except Exception:
                pass
                
        self.load_files(file_list)

    def load_files(self, paths):
        if self.loader_thread:
            self.loader_thread.stop()
            
        # 重複チェック
        current_paths = set()
        for i in range(self.list_widget.count()):
            d = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            current_paths.add(d['path'])
            
        new_paths = [p for p in paths if p not in current_paths]
        if not new_paths:
            return
            
        self.sfx_load.play()
        self.status_bar.showMessage(f"Loading {len(new_paths)} items...")
        
        # スレッド起動
        icon_size = self.list_widget.iconSize().width()
        self.loader_thread = ImageLoaderThread(new_paths, icon_size)
        self.loader_thread.batch_loaded.connect(self.add_batch)
        self.loader_thread.finished_loading.connect(lambda c: (self.status_bar.showMessage(f"Loaded {c} images."), self.apply_filters()))
        self.loader_thread.start()

    def add_batch(self, batch):
        for path, pix, meta, w, h, fmt, kb in batch:
            item = QListWidgetItem(QIcon(pix), "")
            
            # 自動ゴミ箱判定 (プロンプトが空または10文字未満)
            p_text = meta['prompt'] or ""
            is_auto_trashed = len(p_text.strip()) < 10
            
            tooltip = (f"<b>{Path(path).name}</b><br>"
                       f"{w}x{h} ({fmt})<br>"
                       f"{kb:.1f} KB<br>"
                       f"{'TRASHED (Auto)' if is_auto_trashed else ''}<br>"
                       f"Prompt: {p_text[:100]}...")
            item.setToolTip(tooltip)
            
            data = {
                'path': path, 
                'prompt': p_text, 
                'rating': 0, 
                'is_trashed': is_auto_trashed, 
                'thumb': None
            }
            item.setData(Qt.ItemDataRole.UserRole, data)
            
            if is_auto_trashed:
                item.setBackground(QColor("#550000"))
                
            self.list_widget.addItem(item)
            
        self.apply_filters()

    def set_grid_size(self, size, btn):
        for b in self.size_group:
            b.setChecked(False)
        btn.setChecked(True)
        # グリッドサイズをアイコンより少し大きくして余白確保
        self.list_widget.setIconSize(QSize(size, size))
        self.list_widget.setGridSize(QSize(size + 4, size + 4))

    def apply_filters(self):
        txt = self.search_bar.text().lower()
        active_rates = {r for r, b in self.rate_btns.items() if b.isChecked()}
        show_trash = self.btn_trash_view.isChecked()
        
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            d = item.data(Qt.ItemDataRole.UserRole)
            
            should_hide = False
            
            # 1. 検索フィルタ
            if txt and (txt not in Path(d['path']).name.lower() and txt not in d['prompt'].lower()):
                should_hide = True
            
            if not should_hide:
                is_trashed = d.get('is_trashed')
                if is_trashed:
                    # ゴミ箱アイテムは、ゴミ箱表示ボタンがONの時だけ表示
                    if not show_trash:
                        should_hide = True
                else:
                    # 通常アイテムはレーティングフィルタに従う
                    if d.get('rating') not in active_rates:
                        should_hide = True
            
            item.setHidden(should_hide)

    def toggle_rates(self, state):
        for b in self.rate_btns.values():
            b.setChecked(state)
        self.apply_filters()

    def set_rating(self):
        items = self.list_widget.selectedItems()
        if not items:
            return
        val = self.slider_rate.value()
        self.undo_stack.push(ModifyItemsCommand(items, {'rating': val}, f"Rate {val}", self))

    def toggle_trash_state(self):
        items = self.list_widget.selectedItems()
        if not items:
            return
        val = self.btn_toggle_trash.isChecked()
        self.undo_stack.push(ModifyItemsCommand(items, {'is_trashed': val}, "Trash Toggle", self))
        if val:
            self.sfx_trash.play()

    def copy_prompt(self):
        QApplication.clipboard().setText(self.text_prompt.toPlainText())
        self.sfx_copy.play()

    def save_book(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Book", "", "JSON (*.json)")
        if not path:
            return
            
        arr = []
        for i in range(self.list_widget.count()):
            d = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            
            # サムネイル軽量化 (64px PNG)
            if not d.get('thumb') and os.path.exists(d['path']):
                try:
                    with Image.open(d['path']) as img:
                        img.thumbnail((64, 64))
                        # 減色してPNG化
                        img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=64)
                        b = BytesIO()
                        img.save(b, "PNG", optimize=True)
                        d['thumb'] = base64.b64encode(b.getvalue()).decode()
                except:
                    pass
            
            arr.append({
                'path': d['path'], 
                'prompt': d['prompt'], 
                'rating': d['rating'], 
                'is_trashed': d['is_trashed'], 
                'thumb': d['thumb']
            })
            
        # GZIP圧縮して保存
        try:
            with gzip.open(path, 'wt', encoding='utf-8') as f:
                json.dump(arr, f, ensure_ascii=False)
            self.sfx_copy.play()
            self.status_bar.showMessage(f"Saved {len(arr)} items (Compressed).")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def load_book(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Book", "", "JSON (*.json)")
        if not path:
            return
            
        self.clear_list()
        
        try:
            # まずGZIPとして読み込みを試みる
            try:
                with gzip.open(path, 'rt', encoding='utf-8') as f:
                    arr = json.load(f)
            except (OSError, gzip.BadGzipFile):
                # 失敗したら通常のJSONとして読み込む（後方互換性）
                with open(path, 'r', encoding='utf-8') as f:
                    arr = json.load(f)
                
            for d in arr:
                # サムネイル復元 (透明背景)
                pix = QPixmap(64, 64)
                pix.fill(Qt.GlobalColor.transparent)
                
                if d.get('thumb'):
                    try:
                        pix.loadFromData(base64.b64decode(d['thumb']))
                    except:
                        pass
                
                item = QListWidgetItem(QIcon(pix), "")
                
                # 古いデータ形式対策
                d.setdefault('thumb', d.get('thumb'))
                d.setdefault('is_trashed', False)
                d.setdefault('rating', 0)
                
                item.setData(Qt.ItemDataRole.UserRole, d)
                
                if d.get('is_trashed'):
                    item.setBackground(QColor("#550000"))
                    
                self.list_widget.addItem(item)
                
            self.apply_filters()
            self.sfx_load.play()
            self.status_bar.showMessage(f"Loaded {len(arr)} items.")
            
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    def clear_list(self):
        if self.loader_thread:
            self.loader_thread.stop()
        self.list_widget.clear()
        self.undo_stack.clear()
        self.reset_right_panel() # 表示クリア
        self.status_bar.showMessage("List cleared.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PromptTileApp()
    win.show()
    sys.exit(app.exec())
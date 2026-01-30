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
                             QAbstractItemView)
from PyQt6.QtCore import Qt, QSize, QUrl, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import (QIcon, QPixmap, QDragEnterEvent, QDropEvent, 
                         QImage, QColor, QUndoStack, QUndoCommand, QAction, QKeySequence)
from PyQt6.QtMultimedia import QSoundEffect

from PIL import Image, ImageOps

# --- Sound Generator (変更なし) ---
def generate_tone(frequency, duration, volume=0.5, sample_rate=44100, wave_type='sine'):
    n_samples = int(sample_rate * duration)
    data = bytearray()
    for i in range(n_samples):
        t = float(i) / sample_rate
        if wave_type == 'sine':
            value = math.sin(2.0 * math.pi * frequency * t)
        elif wave_type == 'square':
            value = 1.0 if math.sin(2.0 * math.pi * frequency * t) > 0 else -1.0
        else:
            value = 0
        envelope = 1.0 - (i / n_samples)
        packed_value = int(value * volume * envelope * 32767.0)
        data += struct.pack('<h', max(-32768, min(32767, packed_value)))
    return data

def save_wav(filename, data, sample_rate=44100):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1), f.setsampwidth(2), f.setframerate(sample_rate)
        f.writeframes(data)

def create_sfx_assets():
    temp_dir = tempfile.gettempdir()
    select_path = os.path.join(temp_dir, 'pt_select.wav')
    if not os.path.exists(select_path): save_wav(select_path, generate_tone(880, 0.05, 0.3, wave_type='square'))
    
    load_path = os.path.join(temp_dir, 'pt_load.wav')
    if not os.path.exists(load_path):
        data = bytearray()
        for i in range(int(44100 * 0.2)):
            freq = 440 + (i / (44100 * 0.2)) * 880
            val = math.sin(2.0 * math.pi * freq * (i/44100))
            data += struct.pack('<h', int(val * 0.3 * 32767))
        save_wav(load_path, data)
        
    copy_path = os.path.join(temp_dir, 'pt_copy.wav')
    if not os.path.exists(copy_path): save_wav(copy_path, generate_tone(1046.5, 0.15, 0.3, wave_type='square'))
    
    trash_path = os.path.join(temp_dir, 'pt_trash.wav')
    if not os.path.exists(trash_path): save_wav(trash_path, generate_tone(110, 0.2, 0.5, wave_type='sine'))

    return {'select': select_path, 'load': load_path, 'copy': copy_path, 'trash': trash_path}

# --- Metadata Extraction Logic (強化版) ---
def extract_metadata(image_path):
    """
    画像からプロンプト情報を抽出します (A1111, ComfyUI, Civitai対応)
    """
    info_dict = {"prompt": "No metadata found.", "tool": "Unknown"}
    
    if not os.path.exists(image_path):
        return info_dict

    try:
        with Image.open(image_path) as img:
            img.load()
            metadata = img.info or {}
            
            # 1. A1111 / Standard
            if 'parameters' in metadata:
                info_dict["prompt"] = metadata['parameters']
                info_dict["tool"] = "A1111/WebUI"
                return info_dict

            # 2. ComfyUI (workflow or prompt JSON)
            # ComfyUI often stores the workflow in 'prompt' or 'workflow' keys
            for key in ['prompt', 'workflow']:
                if key in metadata:
                    try:
                        # JSONとしてパースを試みる
                        json_data = json.loads(metadata[key])
                        # 単純にJSON全体を整形して返す（Comfyは構造が複雑なため）
                        formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                        info_dict["prompt"] = f"[{key} (ComfyUI)]\n{formatted_json}"
                        info_dict["tool"] = "ComfyUI"
                        return info_dict
                    except:
                        pass

            # 3. UserComment (JPEG Exif or others)
            exif = img._getexif()
            if exif and 37510 in exif: # UserComment
                comment = str(exif[37510])
                # Civitai often puts JSON in UserComment with "u0000" encoding stuff
                # Try to clean it up or detect JSON
                if "{" in comment and "}" in comment:
                    info_dict["tool"] = "Civitai/Exif"
                info_dict["prompt"] = comment
                return info_dict

    except Exception as e:
        info_dict["prompt"] = f"Error reading: {str(e)}"
    
    return info_dict

# --- Asynchronous Loader Thread ---
class ImageLoaderThread(QThread):
    # Signal emits: (path, pixmap, info_dict, width, height, format, filesize)
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
                
                # Metadata extraction (Heavy I/O)
                meta = extract_metadata(path)
                
                # Thumbnail generation (Heavy CPU)
                with Image.open(path) as img:
                    width, height = img.size
                    fmt = img.format or "IMG"
                    file_size_kb = os.path.getsize(path) / 1024
                    
                    img = ImageOps.contain(img, (self.icon_size, self.icon_size))
                    
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
                        pixmap = QPixmap(path).scaled(self.icon_size, self.icon_size, 
                                                      Qt.AspectRatioMode.KeepAspectRatio)

                self.item_loaded.emit(path, pixmap, meta, width, height, fmt, file_size_kb)
                count += 1
                
                # Small sleep to keep UI responsive
                self.msleep(5) 
                
            except Exception as e:
                print(f"Error loading {path}: {e}")
        
        self.finished_loading.emit(count)

    def stop(self):
        self.is_running = False
        self.wait()

# --- Undo/Redo Commands ---
class ModifyItemsCommand(QUndoCommand):
    def __init__(self, list_widget, items, new_data_dict, description):
        super().__init__(description)
        self.list_widget = list_widget
        self.items = items # List of QListWidgetItem
        self.new_data_dict = new_data_dict # Key-Value pairs to update
        self.old_data_list = [] # Store old data for each item

        # Capture old state
        for item in self.items:
            current_data = item.data(Qt.ItemDataRole.UserRole).copy()
            self.old_data_list.append(current_data)

    def redo(self):
        for item in self.items:
            data = item.data(Qt.ItemDataRole.UserRole)
            # Update specific keys
            for key, val in self.new_data_dict.items():
                data[key] = val
            
            item.setData(Qt.ItemDataRole.UserRole, data)
            self._update_visuals(item)
        
        # Trigger UI refresh if needed (handled by logic outside mostly, but visual refresh here)

    def undo(self):
        for i, item in enumerate(self.items):
            # Restore full old dictionary
            item.setData(Qt.ItemDataRole.UserRole, self.old_data_list[i])
            self._update_visuals(item)

    def _update_visuals(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        # Trash visual (Red background)
        if data.get('is_trashed', False):
            item.setBackground(QColor("#550000")) # Dark Red
        else:
            item.setBackground(QColor("#2b2b2b")) # Default Dark

# --- Main Application ---
class PromptTileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PromptTile v2 - Smart Collector")
        self.resize(1200, 800)
        self.setAcceptDrops(True)
        
        # Data & Undo
        self.undo_stack = QUndoStack(self)
        self.loader_thread = None

        # Sounds
        self.sfx_files = create_sfx_assets()
        self.sfx_select = QSoundEffect()
        self.sfx_select.setSource(QUrl.fromLocalFile(self.sfx_files['select']))
        self.sfx_load = QSoundEffect()
        self.sfx_load.setSource(QUrl.fromLocalFile(self.sfx_files['load']))
        self.sfx_copy = QSoundEffect()
        self.sfx_copy.setSource(QUrl.fromLocalFile(self.sfx_files['copy']))
        self.sfx_trash = QSoundEffect()
        self.sfx_trash.setSource(QUrl.fromLocalFile(self.sfx_files['trash']))

        # --- UI Setup ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1. Header (File Ops & Search)
        header_layout = QHBoxLayout()
        
        self.btn_open = QPushButton("📂 Add Images")
        self.btn_open.clicked.connect(self.open_folder_dialog)
        
        self.btn_save = QPushButton("💾 Save Book")
        self.btn_save.clicked.connect(self.save_collection)
        self.btn_save.setStyleSheet("background-color: #0078d7; color: white;")
        
        self.btn_load = QPushButton("📖 Load Book")
        self.btn_load.clicked.connect(self.load_collection)
        self.btn_load.setStyleSheet("background-color: #d7cd00; color: black;")
        
        self.btn_clear = QPushButton("🗑️ Clear All")
        self.btn_clear.clicked.connect(self.clear_list)

        # Size Buttons
        size_layout = QHBoxLayout()
        size_layout.setSpacing(0)
        self.btn_size_s = QPushButton("S")
        self.btn_size_m = QPushButton("M")
        self.btn_size_l = QPushButton("L")
        for b in [self.btn_size_s, self.btn_size_m, self.btn_size_l]:
            b.setFixedWidth(30)
            b.setCheckable(True)
        self.btn_size_m.setChecked(True) # Default
        self.size_group = [self.btn_size_s, self.btn_size_m, self.btn_size_l]
        self.btn_size_s.clicked.connect(lambda: self.change_icon_size(64, self.btn_size_s))
        self.btn_size_m.clicked.connect(lambda: self.change_icon_size(128, self.btn_size_m))
        self.btn_size_l.clicked.connect(lambda: self.change_icon_size(256, self.btn_size_l))

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Filter by filename or prompt...")
        self.search_bar.textChanged.connect(self.filter_items)
        self.search_bar.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #555;")

        header_layout.addWidget(self.btn_open)
        header_layout.addWidget(self.btn_save)
        header_layout.addWidget(self.btn_load)
        header_layout.addWidget(self.btn_clear)
        header_layout.addSpacing(20)
        header_layout.addWidget(QLabel("Size:"))
        header_layout.addWidget(self.btn_size_s)
        header_layout.addWidget(self.btn_size_m)
        header_layout.addWidget(self.btn_size_l)
        header_layout.addSpacing(20)
        header_layout.addWidget(self.search_bar)
        
        main_layout.addLayout(header_layout)

        # 2. Main Content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Grid
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSpacing(6)
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # Multi-select
        self.list_widget.setIconSize(QSize(128, 128))
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.setStyleSheet("""
            QListWidget { background-color: #2b2b2b; border: none; }
            QListWidget::item { border-radius: 4px; border: 1px solid transparent; }
            QListWidget::item:selected { background-color: #4a90e2; border: 1px solid #6ab0ff; }
            QListWidget::item:hover { background-color: #3d3d3d; }
        """)
        
        # Right: Details & Controls
        details_panel = QFrame()
        details_layout = QVBoxLayout(details_panel)
        details_layout.setContentsMargins(10, 0, 0, 0)
        
        # Undo/Redo Buttons
        undo_layout = QHBoxLayout()
        self.btn_undo = QPushButton("Undo")
        self.btn_undo.clicked.connect(self.undo_stack.undo)
        self.btn_undo.setShortcut(QKeySequence.StandardKey.Undo)
        
        self.btn_redo = QPushButton("Redo")
        self.btn_redo.clicked.connect(self.undo_stack.redo)
        self.btn_redo.setShortcut(QKeySequence.StandardKey.Redo)
        
        undo_layout.addWidget(self.btn_undo)
        undo_layout.addWidget(self.btn_redo)

        # Rating & Trash Controls
        control_group = QFrame()
        control_group.setStyleSheet("background-color: #333; border-radius: 5px; padding: 5px;")
        cg_layout = QVBoxLayout(control_group)

        # Rating Slider
        r_layout = QHBoxLayout()
        self.lbl_rating_val = QLabel("Rate: -")
        self.lbl_rating_val.setFixedWidth(50)
        self.slider_rating = QSlider(Qt.Orientation.Horizontal)
        self.slider_rating.setRange(0, 10)
        self.slider_rating.setValue(0)
        self.slider_rating.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_rating.setTickInterval(1)
        self.slider_rating.valueChanged.connect(self.update_rating_label)
        
        self.btn_apply_rating = QPushButton("Set ★")
        self.btn_apply_rating.clicked.connect(self.apply_rating)
        self.btn_apply_rating.setStyleSheet("background-color: #FFA500; color: black; font-weight: bold;")
        
        r_layout.addWidget(self.lbl_rating_val)
        r_layout.addWidget(self.slider_rating)
        r_layout.addWidget(self.btn_apply_rating)
        
        # Trash Button
        self.btn_trash = QPushButton("🗑️ Mark Trash")
        self.btn_trash.setCheckable(True)
        self.btn_trash.clicked.connect(self.toggle_trash)
        self.btn_trash.setStyleSheet("""
            QPushButton { background-color: #555; color: white; padding: 5px; }
            QPushButton:checked { background-color: #d32f2f; color: white; border: 2px solid #ff6666; }
        """)

        cg_layout.addLayout(r_layout)
        cg_layout.addWidget(self.btn_trash)

        # Preview Image
        self.preview_label = QLabel("Select an image")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px dashed #555;")
        
        # Info Text
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("color: #aaa; font-size: 11px;")

        # Prompt Text
        self.text_prompt = QTextEdit()
        self.text_prompt.setReadOnly(True)
        self.text_prompt.setPlaceholderText("Prompt info...")
        self.text_prompt.setStyleSheet("font-family: Consolas; font-size: 10pt; background-color: #222; color: #ddd;")

        self.btn_copy = QPushButton("📋 Copy Prompt")
        self.btn_copy.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.btn_copy.clicked.connect(self.copy_prompt_to_clipboard)

        # Assemble Right Panel
        details_layout.addLayout(undo_layout)
        details_layout.addWidget(control_group)
        details_layout.addSpacing(10)
        details_layout.addWidget(self.preview_label)
        details_layout.addWidget(self.lbl_info)
        details_layout.addWidget(QLabel("Prompt:"))
        details_layout.addWidget(self.text_prompt)
        details_layout.addWidget(self.btn_copy)

        splitter.addWidget(self.list_widget)
        splitter.addWidget(details_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready.")
        
        # Style
        self.setStyleSheet("QMainWindow { background-color: #333; color: #fff; } QLabel { color: #eee; }")

    # --- Logic ---

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            if os.path.isdir(files[0]): self.load_folder(files[0])
            else: self.load_files(files)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder: self.load_folder(folder)

    def clear_list(self):
        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.stop()
        self.list_widget.clear()
        self.undo_stack.clear()
        self.status_bar.showMessage("List cleared.")

    def change_icon_size(self, size, btn):
        for b in self.size_group: b.setChecked(False)
        btn.setChecked(True)
        self.list_widget.setIconSize(QSize(size, size))

    # --- Loading Logic (Async) ---

    def load_folder(self, folder_path):
        extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        image_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if Path(file).suffix.lower() in extensions:
                    image_files.append(os.path.join(root, file))
        self.load_files(image_files)

    def load_files(self, paths):
        # Stop existing thread if running
        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.stop()

        existing_paths = set()
        for i in range(self.list_widget.count()):
            d = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            existing_paths.add(d['path'])
        
        new_paths = [p for p in paths if p not in existing_paths]
        
        if not new_paths:
            self.status_bar.showMessage("No new images to add.")
            return

        self.sfx_load.play()
        self.status_bar.showMessage(f"Loading {len(new_paths)} images in background...")
        
        # Start Thread
        icon_size = self.list_widget.iconSize().width()
        self.loader_thread = ImageLoaderThread(new_paths, icon_size)
        self.loader_thread.item_loaded.connect(self.add_single_item)
        self.loader_thread.finished_loading.connect(lambda c: self.status_bar.showMessage(f"Loaded {c} images."))
        self.loader_thread.start()

    def add_single_item(self, path, pixmap, meta, w, h, fmt, size_kb):
        # Tooltip HTML
        prompt_snippet = (meta['prompt'][:100] + "...") if len(meta['prompt']) > 100 else meta['prompt']
        tooltip = (
            f"<b>File:</b> {Path(path).name}<br>"
            f"<b>Size:</b> {w}x{h} ({fmt})<br>"
            f"<b>Disk:</b> {size_kb:.1f} KB<br>"
            f"<b>Tool:</b> {meta.get('tool', '?')}<br>"
            f"<b>Prompt:</b> {prompt_snippet}"
        )

        item = QListWidgetItem(QIcon(pixmap), "") # Name is empty
        item.setToolTip(tooltip)
        
        item_data = {
            'path': path,
            'prompt': meta['prompt'],
            'rating': 0,
            'is_trashed': False,
            'thumbnail_b64': None # Fill on save
        }
        item.setData(Qt.ItemDataRole.UserRole, item_data)
        
        self.list_widget.addItem(item)

        # Apply search filter immediately if active
        if self.search_bar.text():
            self.check_filter_match(item, self.search_bar.text().lower())

    # --- Interaction Logic ---

    def on_item_clicked(self, item):
        self.sfx_select.play()
        data = item.data(Qt.ItemDataRole.UserRole)
        
        # Update Preview
        path = data['path']
        if os.path.exists(path):
            full_pix = QPixmap(path)
            if not full_pix.isNull():
                self.preview_label.setPixmap(full_pix.scaled(
                    self.preview_label.size(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation))
        else:
            self.preview_label.setPixmap(item.icon().pixmap(256, 256))
        
        # Update Text
        self.text_prompt.setText(data.get('prompt', ''))
        
        # Update Controls
        self.slider_rating.blockSignals(True)
        self.slider_rating.setValue(data.get('rating', 0))
        self.lbl_rating_val.setText(f"Rate: {data.get('rating', 0)}")
        self.slider_rating.blockSignals(False)

        self.btn_trash.blockSignals(True)
        self.btn_trash.setChecked(data.get('is_trashed', False))
        self.btn_trash.blockSignals(False)
        
        # Update Info Label
        stars = "★" * data.get('rating', 0)
        status = " [TRASHED]" if data.get('is_trashed') else ""
        self.lbl_info.setText(f"{Path(path).name} {stars}{status}")

    def update_rating_label(self, val):
        self.lbl_rating_val.setText(f"Rate: {val}")

    def apply_rating(self):
        items = self.list_widget.selectedItems()
        if not items: return
        
        val = self.slider_rating.value()
        cmd = ModifyItemsCommand(self.list_widget, items, {'rating': val}, f"Set Rating {val}")
        self.undo_stack.push(cmd)
        
        self.status_bar.showMessage(f"Set rating {val} for {len(items)} items.")
        self.on_item_clicked(items[0]) # Refresh UI

    def toggle_trash(self):
        items = self.list_widget.selectedItems()
        if not items: return
        
        new_state = self.btn_trash.isChecked()
        cmd = ModifyItemsCommand(self.list_widget, items, {'is_trashed': new_state}, "Toggle Trash")
        self.undo_stack.push(cmd)
        
        if new_state: self.sfx_trash.play()
        self.status_bar.showMessage(f"{'Trashed' if new_state else 'Restored'} {len(items)} items.")
        self.on_item_clicked(items[0]) # Refresh UI

    # --- Search / Filter ---

    def filter_items(self, text):
        search_text = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            self.check_filter_match(item, search_text)

    def check_filter_match(self, item, search_text):
        if not search_text:
            item.setHidden(False)
            return

        data = item.data(Qt.ItemDataRole.UserRole)
        filename = Path(data['path']).name.lower()
        prompt = data.get('prompt', '').lower()
        
        if search_text in filename or search_text in prompt:
            item.setHidden(False)
        else:
            item.setHidden(True)

    def copy_prompt_to_clipboard(self):
        text = self.text_prompt.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.sfx_copy.play()
            self.status_bar.showMessage("Prompt copied!")

    # --- Save / Load ---

    def save_collection(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Book", "", "JSON Files (*.json)")
        if not file_path: return

        self.status_bar.showMessage("Saving...")
        QApplication.processEvents()

        collection = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            data = item.data(Qt.ItemDataRole.UserRole)
            
            # Generate thumbnail only if missing (simple cache logic)
            if not data.get('thumbnail_b64'):
                try:
                    if os.path.exists(data['path']):
                        with Image.open(data['path']) as img:
                            img.thumbnail((128, 128))
                            img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=64)
                            buffered = BytesIO()
                            img.save(buffered, format="PNG", optimize=True)
                            data['thumbnail_b64'] = base64.b64encode(buffered.getvalue()).decode('utf-8')
                except: pass
            
            entry = {
                'filename': Path(data['path']).name,
                'path': data['path'],
                'prompt': data['prompt'],
                'rating': data.get('rating', 0),
                'is_trashed': data.get('is_trashed', False),
                'thumbnail': data.get('thumbnail_b64')
            }
            collection.append(entry)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(collection, f, ensure_ascii=False, indent=2)
            self.sfx_copy.play()
            QMessageBox.information(self, "Success", f"Saved {len(collection)} items.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        self.status_bar.showMessage("Saved.")

    def load_collection(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Book", "", "JSON Files (*.json)")
        if not file_path: return

        self.clear_list()
        self.sfx_load.play()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)

            for d in data_list:
                pixmap = None
                if d.get('thumbnail'):
                    try:
                        b = base64.b64decode(d['thumbnail'])
                        pixmap = QPixmap.fromImage(QImage.fromData(b))
                    except: pass
                
                if not pixmap:
                    pixmap = QPixmap(128, 128)
                    pixmap.fill(QColor("#444"))
                
                item = QListWidgetItem(QIcon(pixmap), "")
                
                # Tooltip for loaded items
                short_p = (d['prompt'][:100] + "...") if len(d['prompt']) > 100 else d['prompt']
                tooltip = (
                    f"<b>File:</b> {d['filename']}<br>"
                    f"<b>Prompt:</b> {short_p}<br>"
                    f"<b>Rating:</b> {d.get('rating', 0)}/10<br>"
                    f"{'[TRASHED]' if d.get('is_trashed') else ''}"
                )
                item.setToolTip(tooltip)

                # Internal Data
                internal = {
                    'path': d.get('path', ''),
                    'prompt': d.get('prompt', ''),
                    'rating': d.get('rating', 0),
                    'is_trashed': d.get('is_trashed', False),
                    'thumbnail_b64': d.get('thumbnail')
                }
                item.setData(Qt.ItemDataRole.UserRole, internal)
                
                # Visuals
                if internal['is_trashed']:
                    item.setBackground(QColor("#550000"))

                self.list_widget.addItem(item)

            self.status_bar.showMessage(f"Loaded {len(data_list)} items.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptTileApp()
    window.show()
    sys.exit(app.exec())
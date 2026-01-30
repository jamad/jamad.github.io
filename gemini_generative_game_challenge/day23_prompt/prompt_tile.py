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
from PyQt6.QtCore import Qt, QSize, QUrl, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import (QIcon, QPixmap, QDragEnterEvent, QDropEvent, 
                         QImage, QColor, QUndoStack, QUndoCommand, QKeySequence, QAction)
from PyQt6.QtMultimedia import QSoundEffect

from PIL import Image, ImageOps

# --- Sound Generator ---
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
    defs = [('pt_select.wav', 880, 0.05, 'square'), ('pt_load.wav', 440, 0.1, 'sine'), 
            ('pt_copy.wav', 1200, 0.1, 'sine'), ('pt_trash.wav', 150, 0.2, 'square')]
    for name, freq, dur, wtype in defs:
        path = os.path.join(temp_dir, name)
        if not os.path.exists(path): save_wav(path, generate_tone(freq, dur, 0.3, wave_type=wtype))
        sfx[name.replace('pt_', '').replace('.wav', '')] = path
    return sfx

# --- Metadata Extraction ---
def extract_metadata(image_path):
    info = {"prompt": "", "tool": "Unknown"}
    if not os.path.exists(image_path): return info
    try:
        with Image.open(image_path) as img:
            img.load()
            meta = img.info or {}
            if 'parameters' in meta:
                info["prompt"], info["tool"] = meta['parameters'], "A1111"
            else:
                for k in ['prompt', 'workflow']:
                    if k in meta:
                        try:
                            info["prompt"] = f"[{k}]\n" + json.dumps(json.loads(meta[k]), indent=2, ensure_ascii=False)
                            info["tool"] = "ComfyUI"
                            break
                        except: pass
                if not info["prompt"]:
                    exif = img._getexif()
                    if exif and 37510 in exif:
                        info["prompt"], info["tool"] = str(exif[37510]), "Exif"
    except Exception as e:
        info["prompt"] = f"Error: {e}"
    
    # Clean up
    if info["prompt"] == "No metadata found.": info["prompt"] = ""
    return info

# --- Loader Thread (Batched) ---
class ImageLoaderThread(QThread):
    # バッチで送る: [(path, pixmap, meta, w, h, fmt, kb), ...]
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
            if not self.is_running: break
            try:
                if not os.path.exists(path): continue
                
                meta = extract_metadata(path)
                
                with Image.open(path) as img:
                    w, h = img.size
                    fmt = img.format or "IMG"
                    kb = os.path.getsize(path) / 1024
                    
                    # --- 正方形サムネイル生成 ---
                    # 1. アスペクト比を維持してリサイズ
                    img.thumbnail((self.icon_size, self.icon_size), Image.Resampling.LANCZOS)
                    
                    # 2. 透明な正方形の背景を作成
                    thumb = Image.new('RGBA', (self.icon_size, self.icon_size), (0, 0, 0, 0))
                    
                    # 3. 中央に貼り付け
                    offset_x = (self.icon_size - img.width) // 2
                    offset_y = (self.icon_size - img.height) // 2
                    thumb.paste(img, (offset_x, offset_y))
                    
                    # 4. QPixmap変換
                    data = thumb.tobytes("raw", "RGBA")
                    qim = QImage(data, thumb.width, thumb.height, QImage.Format.Format_RGBA8888)
                    pixmap = QPixmap.fromImage(qim)

                batch.append((path, pixmap, meta, w, h, fmt, kb))
                total += 1
                
                # 10個たまったらGUIに送る（描画負荷軽減）
                if len(batch) >= 10:
                    self.batch_loaded.emit(batch)
                    batch = []
                    self.msleep(10) # 少し休んでGUIスレッドに処理させる

            except Exception: pass
            
        if batch: self.batch_loaded.emit(batch)
        self.finished_loading.emit(total)

    def stop(self):
        self.is_running = False
        self.wait()

# --- Undo Command ---
class ModifyItemsCommand(QUndoCommand):
    def __init__(self, items, new_data, desc, app):
        super().__init__(desc)
        self.items, self.new_data, self.app = items, new_data, app
        self.old_data = [i.data(Qt.ItemDataRole.UserRole).copy() for i in items]
    def redo(self):
        for i in self.items:
            d = i.data(Qt.ItemDataRole.UserRole)
            d.update(self.new_data)
            i.setData(Qt.ItemDataRole.UserRole, d)
            self._visuals(i)
        self.app.apply_filters()
    def undo(self):
        for idx, i in enumerate(self.items):
            i.setData(Qt.ItemDataRole.UserRole, self.old_data[idx])
            self._visuals(i)
        self.app.apply_filters()
    def _visuals(self, i):
        d = i.data(Qt.ItemDataRole.UserRole)
        i.setBackground(QColor("#550000") if d.get('is_trashed') else QColor("#2b2b2b"))

# --- Main App ---
class PromptTileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PromptTile v5 - Square Grid & Auto Trash")
        self.resize(1200, 850)
        self.setAcceptDrops(True)
        self.undo_stack = QUndoStack(self)
        self.loader_thread = None
        sfx = create_sfx_assets()
        self.sfx_select = QSoundEffect(); self.sfx_select.setSource(QUrl.fromLocalFile(sfx['select']))
        self.sfx_load = QSoundEffect(); self.sfx_load.setSource(QUrl.fromLocalFile(sfx['load']))
        self.sfx_copy = QSoundEffect(); self.sfx_copy.setSource(QUrl.fromLocalFile(sfx['copy']))
        self.sfx_trash = QSoundEffect(); self.sfx_trash.setSource(QUrl.fromLocalFile(sfx['trash']))

        # UI Layout
        main = QWidget(); self.setCentralWidget(main)
        layout = QVBoxLayout(main)

        # Top Control
        top = QVBoxLayout()
        row1 = QHBoxLayout()
        
        self.btn_add_r = QPushButton("📂 Add (All)"); self.btn_add_r.clicked.connect(lambda: self.open_folder(True))
        self.btn_add_f = QPushButton("📂 Add (Flat)"); self.btn_add_f.clicked.connect(lambda: self.open_folder(False))
        self.btn_save = QPushButton("💾 Save"); self.btn_save.clicked.connect(self.save_book)
        self.btn_save.setStyleSheet("background:#0078d7; color:white")
        self.btn_load = QPushButton("📖 Load"); self.btn_load.clicked.connect(self.load_book)
        self.btn_load.setStyleSheet("background:#d7cd00; color:black")
        self.btn_clear = QPushButton("🗑️ Clear"); self.btn_clear.clicked.connect(self.clear_list)
        
        # Grid Size Buttons (32 / 64)
        row1.addWidget(self.btn_add_r); row1.addWidget(self.btn_add_f); row1.addSpacing(10)
        row1.addWidget(self.btn_save); row1.addWidget(self.btn_load); row1.addWidget(self.btn_clear)
        row1.addStretch()
        row1.addWidget(QLabel("Grid:"))
        
        self.btn_size_32 = QPushButton("32px")
        self.btn_size_64 = QPushButton("64px")
        self.size_group = [self.btn_size_32, self.btn_size_64]
        for b, s in zip(self.size_group, [32, 64]):
            b.setCheckable(True); b.setFixedWidth(50)
            b.clicked.connect(lambda c, size=s, btn=b: self.set_grid_size(size, btn))
        
        row1.addWidget(self.btn_size_32); row1.addWidget(self.btn_size_64)

        # Filter
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background:#252525; border-radius:4px; padding:2px")
        row2 = QHBoxLayout(filter_frame); row2.setContentsMargins(5,2,5,2)
        
        self.search = QLineEdit(); self.search.setPlaceholderText("🔍 Search...")
        self.search.textChanged.connect(self.apply_filters); self.search.setFixedWidth(200)
        
        self.btn_all = QPushButton("ALL"); self.btn_all.setFixedWidth(40); self.btn_all.clicked.connect(lambda: self.toggle_rates(True))
        self.btn_none = QPushButton("NONE"); self.btn_none.setFixedWidth(40); self.btn_none.clicked.connect(lambda: self.toggle_rates(False))
        
        row2.addWidget(self.search); row2.addWidget(QLabel("Filter:")); row2.addWidget(self.btn_all); row2.addWidget(self.btn_none)
        
        self.rate_btns = {}
        for i in range(11):
            b = QPushButton(str(i)); b.setCheckable(True); b.setChecked(True); b.setFixedWidth(25)
            b.clicked.connect(self.apply_filters)
            b.setStyleSheet("QPushButton{background:#444;color:#aaa}QPushButton:checked{background:#4a90e2;color:white}")
            self.rate_btns[i] = b; row2.addWidget(b)
            
        self.btn_trash_view = QPushButton("🗑️"); self.btn_trash_view.setCheckable(True); self.btn_trash_view.setFixedWidth(30)
        self.btn_trash_view.clicked.connect(self.apply_filters)
        self.btn_trash_view.setStyleSheet("QPushButton{background:#444}QPushButton:checked{background:#d32f2f}")
        row2.addSpacing(10); row2.addWidget(self.btn_trash_view)

        top.addLayout(row1); top.addWidget(filter_frame); layout.addLayout(top)

        # Content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # List Widget
        self.list = QListWidget()
        self.list.setViewMode(QListWidget.ViewMode.IconMode)
        self.list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list.setSpacing(1) # padding 1px equivalent together with grid size
        # 重要: Selection Changed で更新
        self.list.currentItemChanged.connect(self.on_selection_change)
        self.list.setStyleSheet("QListWidget{background:#2b2b2b; border:none} QListWidget::item:selected{background:#4a90e2}")
        
        # Details
        details = QFrame(); d_layout = QVBoxLayout(details)
        
        ur_layout = QHBoxLayout()
        b_undo = QPushButton("Undo"); b_undo.clicked.connect(self.undo_stack.undo); b_undo.setShortcut(QKeySequence.StandardKey.Undo)
        b_redo = QPushButton("Redo"); b_redo.clicked.connect(self.undo_stack.redo); b_redo.setShortcut(QKeySequence.StandardKey.Redo)
        ur_layout.addWidget(b_undo); ur_layout.addWidget(b_redo)

        ctl = QFrame(); ctl.setStyleSheet("background:#333; border-radius:4px")
        c_layout = QVBoxLayout(ctl)
        r_row = QHBoxLayout()
        self.lbl_rate = QLabel("-"); self.slider = QSlider(Qt.Orientation.Horizontal); self.slider.setRange(0,10)
        self.slider.valueChanged.connect(lambda v: self.lbl_rate.setText(str(v)))
        b_set_rate = QPushButton("Set ★"); b_set_rate.setStyleSheet("background:#FFA500;color:black;font-weight:bold")
        b_set_rate.clicked.connect(self.set_rating)
        r_row.addWidget(QLabel("Rate:")); r_row.addWidget(self.lbl_rate); r_row.addWidget(self.slider); r_row.addWidget(b_set_rate)
        
        self.b_toggle_trash = QPushButton("🗑️ Toggle Trash"); self.b_toggle_trash.setCheckable(True)
        self.b_toggle_trash.clicked.connect(self.toggle_trash_state)
        self.b_toggle_trash.setStyleSheet("QPushButton{background:#555}QPushButton:checked{background:#d32f2f}")
        c_layout.addLayout(r_row); c_layout.addWidget(self.b_toggle_trash)

        self.preview = QLabel("Select Image"); self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumHeight(200); self.preview.setStyleSheet("background:#1e1e1e; border:1px dashed #555")
        
        self.prompt_txt = QTextEdit(); self.prompt_txt.setReadOnly(True); self.prompt_txt.setStyleSheet("background:#222; font-family:Consolas")
        b_copy = QPushButton("📋 Copy"); b_copy.clicked.connect(self.copy_prompt)
        b_copy.setStyleSheet("background:#4CAF50;color:white")

        d_layout.addLayout(ur_layout); d_layout.addWidget(ctl); d_layout.addWidget(self.preview)
        d_layout.addWidget(QLabel("Prompt:")); d_layout.addWidget(self.prompt_txt); d_layout.addWidget(b_copy)

        splitter.addWidget(self.list); splitter.addWidget(details)
        splitter.setStretchFactor(0, 3); splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)
        
        self.status = self.statusBar(); self.status.showMessage("Ready.")
        self.setStyleSheet("QMainWindow{background:#333;color:white} QLabel{color:#ddd}")
        
        # Init Default Size
        self.set_grid_size(64, self.btn_size_64)

    # --- Logic ---
    def dragEnterEvent(self, e): e.accept() if e.mimeData().hasUrls() else e.ignore()
    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        if files: self.open_folder(True, files[0]) if os.path.isdir(files[0]) else self.load_files(files)

    def open_folder(self, recursive, path=None):
        d = path or QFileDialog.getExistingDirectory(self, "Select Folder")
        if not d: return
        f = []
        if recursive:
            for r, _, fs in os.walk(d):
                for x in fs:
                    if Path(x).suffix.lower() in {'.png','.jpg','.jpeg','.webp'}: f.append(os.path.join(r, x))
        else:
            try: f = [os.path.join(d,x) for x in os.listdir(d) if Path(x).suffix.lower() in {'.png','.jpg','.jpeg','.webp'}]
            except: pass
        self.load_files(f)

    def load_files(self, paths):
        if self.loader_thread: self.loader_thread.stop()
        exist = {self.list.item(i).data(Qt.ItemDataRole.UserRole)['path'] for i in range(self.list.count())}
        new_p = [p for p in paths if p not in exist]
        if not new_p: return
        
        self.sfx_load.play(); self.status.showMessage(f"Loading {len(new_p)} items...")
        
        # 現在のグリッドサイズに合わせてロード
        sz = self.list.iconSize().width()
        self.loader_thread = ImageLoaderThread(new_p, sz)
        self.loader_thread.batch_loaded.connect(self.add_batch) # バッチ受信
        self.loader_thread.finished_loading.connect(lambda c: (self.status.showMessage(f"Loaded {c}."), self.apply_filters()))
        self.loader_thread.start()

    def add_batch(self, batch):
        # batch = list of (path, pix, meta, w, h, fmt, kb)
        for path, pix, meta, w, h, fmt, kb in batch:
            item = QListWidgetItem(QIcon(pix), "")
            
            # Auto Trash Logic: Prompt < 10 chars
            p_text = meta['prompt'] or ""
            is_trashed = len(p_text.strip()) < 10
            
            tooltip = f"<b>{Path(path).name}</b><br>{w}x{h}<br>{kb:.1f}KB<br>{'TRASHED (Auto)' if is_trashed else ''}<br>{p_text[:100]}..."
            item.setToolTip(tooltip)
            
            data = {'path': path, 'prompt': p_text, 'rating': 0, 'is_trashed': is_trashed, 'thumb': None}
            item.setData(Qt.ItemDataRole.UserRole, data)
            
            if is_trashed: item.setBackground(QColor("#550000"))
            self.list.addItem(item)
            
        self.apply_filters()

    def on_selection_change(self, current, previous):
        # 矢印キー移動などでここが呼ばれる
        if not current: return
        self.sfx_select.play()
        d = current.data(Qt.ItemDataRole.UserRole)
        
        self.prompt_txt.setText(d['prompt'])
        self.slider.blockSignals(True); self.slider.setValue(d['rating']); self.slider.blockSignals(False)
        self.lbl_rate.setText(str(d['rating']))
        self.b_toggle_trash.blockSignals(True); self.b_toggle_trash.setChecked(d['is_trashed']); self.b_toggle_trash.blockSignals(False)
        
        if os.path.exists(d['path']):
            p = QPixmap(d['path'])
            if not p.isNull(): 
                self.preview.setPixmap(p.scaled(self.preview.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.preview.setPixmap(current.icon().pixmap(256))

    def set_grid_size(self, size, btn):
        for b in self.size_group: b.setChecked(False)
        btn.setChecked(True)
        # padding 1px + border/spacing consideration. 
        # Making grid slightly larger than icon ensures fit.
        self.list.setIconSize(QSize(size, size))
        self.list.setGridSize(QSize(size + 4, size + 4))

    def apply_filters(self):
        txt = self.search.text().lower()
        rates = {r for r,b in self.rate_btns.items() if b.isChecked()}
        show_trash = self.btn_trash_view.isChecked()
        
        for i in range(self.list.count()):
            item = self.list.item(i)
            d = item.data(Qt.ItemDataRole.UserRole)
            
            hide = False
            if txt and (txt not in Path(d['path']).name.lower() and txt not in d['prompt'].lower()): hide = True
            
            if not hide:
                is_trash = d.get('is_trashed')
                if is_trash:
                    if not show_trash: hide = True
                else:
                    if d.get('rating') not in rates: hide = True
            
            item.setHidden(hide)

    def toggle_rates(self, state):
        for b in self.rate_btns.values(): b.setChecked(state)
        self.apply_filters()

    def set_rating(self):
        items = self.list.selectedItems()
        if not items: return
        self.undo_stack.push(ModifyItemsCommand(items, {'rating': self.slider.value()}, "Rate", self))

    def toggle_trash_state(self):
        items = self.list.selectedItems()
        if not items: return
        v = self.b_toggle_trash.isChecked()
        self.undo_stack.push(ModifyItemsCommand(items, {'is_trashed': v}, "Trash", self))
        if v: self.sfx_trash.play()

    def copy_prompt(self):
        QApplication.clipboard().setText(self.prompt_txt.toPlainText())
        self.sfx_copy.play()

    def save_book(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save", "", "JSON (*.json)")
        if not path: return
        arr = []
        for i in range(self.list.count()):
            d = self.list.item(i).data(Qt.ItemDataRole.UserRole)
            if not d.get('thumb') and os.path.exists(d['path']):
                try:
                    with Image.open(d['path']) as img:
                        img.thumbnail((64,64)); img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=64)
                        b = BytesIO(); img.save(b, "PNG", optimize=True)
                        d['thumb'] = base64.b64encode(b.getvalue()).decode()
                except: pass
            arr.append({'path':d['path'], 'prompt':d['prompt'], 'rating':d['rating'], 'is_trashed':d['is_trashed'], 'thumb':d['thumb']})
        with open(path,'w',encoding='utf-8') as f: json.dump(arr,f,ensure_ascii=False)
        self.sfx_copy.play()

    def load_book(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load", "", "JSON (*.json)")
        if not path: return
        self.list.clear(); self.undo_stack.clear()
        with open(path,'r',encoding='utf-8') as f: arr = json.load(f)
        for d in arr:
            pix = QPixmap(64,64); pix.fill(Qt.GlobalColor.transparent)
            if d.get('thumb'): 
                try: pix.loadFromData(base64.b64decode(d['thumb']))
                except: pass
            item = QListWidgetItem(QIcon(pix), "")
            d.setdefault('thumb', d.get('thumb'))
            item.setData(Qt.ItemDataRole.UserRole, d)
            if d.get('is_trashed'): item.setBackground(QColor("#550000"))
            self.list.addItem(item)
        self.apply_filters()
        self.sfx_load.play()

    def clear_list(self):
        if self.loader_thread: self.loader_thread.stop()
        self.list.clear(); self.undo_stack.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PromptTileApp()
    win.show()
    sys.exit(app.exec())
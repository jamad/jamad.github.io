import customtkinter as ctk
import os
import datetime
import re
import concurrent.futures
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags  # ExifTagsを復活させました

# --- 定数設定 ---
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.tiff'}
SCREENSHOT_KEYWORDS = ["screenshot", "screen shot", "スクリーンショット", "s_", "capture"]
CLEAN_PREFIXES = ["Exif_", "exif0_", "File_", "IMG_ymd_", "scrn_ymd_"]
UUID_PATTERN = r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
APPLE_ID_PATTERN = r"^\d{11}__"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ImageLogic:
    """リネームルールの判定ロジックを専門に扱うクラス"""

    @staticmethod
    def get_date_info(file_path: Path):
        """Exifから撮影日時を取得。不完全な場合はステータスを返す。"""
        dt_obj = None
        source = "FileTime"
        try:
            with Image.open(file_path) as image:
                exif = image.getexif()
                if exif:
                    # ExifTagsを使用してマジックナンバーを回避
                    # 36867: DateTimeOriginal, 306: DateTime
                    date_str = exif.get(36867) or exif.get(306)
                    
                    if date_str:
                        dt_obj = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                        source = "Exif"
                    else:
                        # Exifコンテナはあるが日付が空の状態
                        source = "ExifMissingDate"
        except Exception:
            pass

        if dt_obj is None:
            # Exifが取れなかった場合、ファイルの最終更新日時を使用
            mtime = os.path.getmtime(file_path)
            dt_obj = datetime.datetime.fromtimestamp(mtime)
            if source != "ExifMissingDate":
                source = "FileTime"
        return dt_obj, source

    @staticmethod
    def is_junk_name(stem: str) -> bool:
        """UUIDやシステム識別用IDなどの『ジャンク名』かどうかを判定"""
        return bool(re.search(UUID_PATTERN, stem)) or bool(re.match(APPLE_ID_PATTERN, stem))

    @classmethod
    def generate_candidate_name(cls, original_path: Path, dt_obj: datetime.datetime, source: str) -> str:
        """仕様に基づくリネーム候補名の生成ロジック"""
        stem = original_path.stem
        suffix = original_path.suffix
        date_str = dt_obj.strftime("%Y%m%d_%H%M%S")
        
        # 1. スクリーンショット検知 (PNGかつExifなし、またはキーワード一致)
        is_screenshot = any(kw in stem.lower() for kw in SCREENSHOT_KEYWORDS) or \
                        (suffix.lower() == ".png" and source == "FileTime")
        prefix = "scrn_ymd_" if is_screenshot else ""

        # 2. 二重処理防止：既に整理済みPrefixが付いており日付も正しい場合は維持
        if any(stem.startswith(tag) and date_str in stem for tag in CLEAN_PREFIXES):
            return original_path.name

        # 3. プレフィックスのクレンジング (既存のscrn_やIMG_を除去)
        if is_screenshot:
            stem = re.sub(r"^(scrn_ymd_|scrn_|IMG_(\d+|ymd)_?)", "", stem)
        elif re.match(r"^IMG_\d+", stem):
            stem = re.sub(r"^IMG_\d+", "IMG_ymd", stem)

        # 4. メインのリネーム優先順位ルール
        if source == "Exif":
            return f"{prefix}Exif_{date_str}{suffix}"
        if source == "ExifMissingDate":
            return f"{prefix}exif0_{date_str}{suffix}"
        if cls.is_junk_name(stem):
            return f"{prefix}File_{date_str}{suffix}"

        # 既存の日時が含まれている場合の二重付与防止
        if re.search(r"\d{8}_\d{6}", stem):
            final = f"{prefix}{stem}{suffix}"
            return original_path.name if final == original_path.name else final

        # 特殊ケース：Prefixのみで名前が空になった場合
        if is_screenshot and not stem:
            return f"{prefix}{date_str}{suffix}"
        
        # 通常のファイルリネーム
        if stem.endswith(f"_{date_str}"):
            return original_path.name

        return f"{prefix}{stem}_{date_str}{suffix}"


class RenameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Suffix Renamer (Stable Edition)")
        self.geometry("1000x850")
        
        self.file_data = []
        self.skip_count = 0
        self.setup_ui()

    def setup_ui(self):
        """UIコンポーネントの初期化"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. ヘッダーエリア
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        ctk.CTkButton(self.header_frame, text="ファイルを追加", command=self.add_files).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.header_frame, text="フォルダを追加", command=self.add_folder).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.header_frame, text="リストをクリア", command=self.clear_list, fg_color="gray").pack(side="left", padx=10, pady=10)
        
        self.lbl_info = ctk.CTkLabel(self.header_frame, text="画像を選択してください。")
        self.lbl_info.pack(side="left", padx=20)
        self.lbl_skip_info = ctk.CTkLabel(self.header_frame, text="", text_color="#FF3B30", font=("Arial", 14, "bold"))
        self.lbl_skip_info.pack(side="left", padx=10)

        # 2. プログレスエリア
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=5)
        self.progress_bar.set(0)

        # 3. プレビューエリア (1024件制限を回避するTextbox方式)
        self.preview_box = ctk.CTkTextbox(self, font=("Consolas", 12), state="disabled")
        self.preview_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # 4. フッター・ログエリア
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.btn_run = ctk.CTkButton(self.footer_frame, text="リネーム実行", command=self.run_rename, 
                                     font=("Arial", 16, "bold"), height=40, fg_color="#2CC985")
        self.btn_run.pack(fill="x", padx=20, pady=10)
        
        self.log_box = ctk.CTkTextbox(self.footer_frame, height=150, font=("Consolas", 12))
        self.log_box.pack(fill="x", padx=20, pady=(0, 10))

        # スクロール用キーバインド
        self.bind_all("<Down>", lambda e: self.preview_box.yview_scroll(1, "units"))
        self.bind_all("<Up>", lambda e: self.preview_box.yview_scroll(-1, "units"))
        self.bind_all("<Next>", lambda e: self.preview_box.yview_scroll(1, "pages"))
        self.bind_all("<Prior>", lambda e: self.preview_box.yview_scroll(-1, "pages"))

    def log(self, message):
        """ログ追記"""
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")

    def add_files(self):
        fps = filedialog.askopenfilenames(title="ファイルを選択", filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.heic;*.tiff"), ("All", "*.*")])
        if fps: self.add_paths_to_list([Path(f) for f in fps])

    def add_folder(self):
        path = filedialog.askdirectory(title="フォルダを選択")
        if not path: return
        path_objs = [f for f in Path(path).iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]
        if not path_objs:
            messagebox.showinfo("info", "画像が見つかりませんでした。")
            return
        self.add_paths_to_list(path_objs)

    def _process_single_path(self, path_obj):
        """並列処理用ワーカー"""
        dt_obj, source = ImageLogic.get_date_info(path_obj)
        candidate = ImageLogic.generate_candidate_name(path_obj, dt_obj, source)
        return path_obj, candidate, source

    def add_paths_to_list(self, path_objects):
        """解析、重複解決、UI描画の3段階で処理を実行"""
        new_paths = [p for p in path_objects if not any(d['original_path'] == p for d in self.file_data)]
        if not new_paths: return

        total = len(new_paths)
        self.lbl_info.configure(text="分析中...")
        self.progress_bar.set(0.1)
        self.update()

        # Phase 1: 並列解析 (I/O高速化)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            raw_results = list(executor.map(self._process_single_path, new_paths))

        # Phase 2: 名前衝突解決 (メモリ上での一括処理)
        used_names = {d['new_name'] for d in self.file_data}
        final_entries = []
        for path_obj, candidate, source in raw_results:
            new_name = candidate
            if new_name in used_names or ((path_obj.parent / new_name).exists() and new_name != path_obj.name):
                stem, suffix = Path(candidate).stem, Path(candidate).suffix
                idx = 1
                while f"{stem}_{idx}{suffix}" in used_names or (path_obj.parent / f"{stem}_{idx}{suffix}").exists():
                    idx += 1
                new_name = f"{stem}_{idx}{suffix}"
            used_names.add(new_name)
            final_entries.append({'original_path': path_obj, 'new_name': new_name, 'date_source': source})

        # Phase 3: UIへの描画 (バッチ描画でフリーズを防止)
        self.preview_box.configure(state="normal")
        if not self.file_data and self.skip_count == 0:
            self.preview_box.insert("end", f"{'No.':<6} {'元のファイル名':<40}  →  {'変更後のファイル名':<40}\n{'-'*100}\n")

        for i, entry in enumerate(final_entries):
            if entry['original_path'].name == entry['new_name']:
                self.skip_count += 1
                self.lbl_skip_info.configure(text=f"変更なし: {self.skip_count} 件")
            else:
                self.file_data.append(entry)
                line = f"{len(self.file_data):<5} {entry['original_path'].name:<40}  >>>  {entry['new_name']:<40}\n"
                self.preview_box.insert("end", line)

            if i % 20 == 0 or i == total - 1:
                self.progress_bar.set(0.1 + (0.9 * ((i+1)/total)))
                self.lbl_info.configure(text=f"描画中... ({i+1}/{total})")
                self.update()

        self.preview_box.configure(state="disabled")
        self.lbl_info.configure(text=f"{total} 件のファイル解析完了。")

    def clear_list(self):
        """完全なリセット"""
        self.file_data, self.skip_count = [], 0
        self.lbl_skip_info.configure(text=""), self.progress_bar.set(0)
        self.lbl_info.configure(text="リストをクリアしました。")
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.configure(state="disabled")
        self.log_box.delete("1.0", "end")

    def run_rename(self):
        """リネーム実行。物理的な衝突回避を最終確認しつつ進める。"""
        if not self.file_data: return
        self.log(f"--- 実行開始: {datetime.datetime.now().strftime('%H:%M:%S')} ---")
        total = len(self.file_data)
        count, error_count = 0, 0

        for i, entry in enumerate(self.file_data):
            src = entry['original_path']
            dst = src.parent / entry['new_name']
            
            # 書き込み直前の物理衝突チェック
            if dst.exists() and src != dst:
                base, ext = dst.stem, dst.suffix
                idx = 1
                while (src.parent / f"{base}_{idx}{ext}").exists(): idx += 1
                dst = src.parent / f"{base}_{idx}{ext}"

            try:
                os.rename(src, dst)
                self.log(f"[成功] {src.name} -> {dst.name}")
                count += 1
            except Exception as e:
                self.log(f"[エラー] {src.name}: {e}")
                error_count += 1
            
            if i % 10 == 0:
                self.progress_bar.set((i + 1) / total)
                self.update()

        messagebox.showinfo("完了", f"{count} 件リネーム完了。")
        self.clear_list()

if __name__ == "__main__":
    RenameApp().mainloop()
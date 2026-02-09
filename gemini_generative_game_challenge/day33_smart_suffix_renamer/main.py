import customtkinter as ctk
import os
import datetime
import re  # 正規表現用に追加
import concurrent.futures  # 【高速化】マルチスレッド用に追加
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags

# --- 設定 ---
ctk.set_appearance_mode("System")  # Light/Darkモード自動追従
ctk.set_default_color_theme("blue")

class RenameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("Smart Suffix Renamer (Prototype)")
        self.geometry("1000x850")

        # データ保持用リスト
        self.file_data = [] # {'original_path': Path, 'new_name': str, 'date_source': str}
        self.skip_count = 0 # 変更不要ファイルの集計用

        # --- UIレイアウト ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # プレビューエリアを伸縮させる

        # 1. ヘッダーエリア
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.btn_add_files = ctk.CTkButton(self.header_frame, text="ファイルを追加", command=self.add_files, width=140)
        self.btn_add_files.pack(side="left", padx=10, pady=10)

        self.btn_add_folder = ctk.CTkButton(self.header_frame, text="フォルダを追加", command=self.add_folder, width=140)
        self.btn_add_folder.pack(side="left", padx=10, pady=10)

        self.btn_clear = ctk.CTkButton(self.header_frame, text="リストをクリア", command=self.clear_list, fg_color="gray", width=120)
        self.btn_clear.pack(side="left", padx=10, pady=10)

        self.lbl_info = ctk.CTkLabel(self.header_frame, text="画像を選択してください。Exif優先でリネームします。")
        self.lbl_info.pack(side="left", padx=20)

        # 変更不要なファイル数を赤い太字で表示するラベル
        self.lbl_skip_info = ctk.CTkLabel(self.header_frame, text="", text_color="#FF3B30", font=("Arial", 14, "bold"))
        self.lbl_skip_info.pack(side="left", padx=10)

        # プログレスエリア（プレビューの上に配置）
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=5)
        self.progress_bar.set(0)

        # 2. 【変更】プレビュー表示エリア（Textbox方式に変更：1024件制限を突破）
        # ScrollableFrameからTextboxに変えることで大量のファイルでもクラッシュせず高速に表示できます
        self.preview_box = ctk.CTkTextbox(self, font=("Consolas", 12), state="disabled")
        self.preview_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # 3. フッターエリア（実行ボタン ＆ ログエリア）
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.btn_run = ctk.CTkButton(self.footer_frame, text="リネーム実行", command=self.run_rename, font=("Arial", 16, "bold"), height=40, fg_color="#2CC985", hover_color="#26A66F")
        self.btn_run.pack(fill="x", padx=20, pady=10)

        # エラーログ表示用のテキストボックス
        self.log_box = ctk.CTkTextbox(self.footer_frame, height=150, font=("Consolas", 12))
        self.log_box.pack(fill="x", padx=20, pady=(0, 10))
        self.log_box.insert("0.0", "--- 実行ログ ---\n")

    def append_log(self, message):
        """ログエリアにテキストを追記する"""
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")

    def add_files(self):
        """ファイル選択ダイアログを開き、リストに追加する"""
        filetypes = [("Images", "*.jpg;*.jpeg;*.png;*.heic;*.tiff"), ("All Files", "*.*")]
        filepaths = filedialog.askopenfilenames(title="ファイルを選択", filetypes=filetypes)
        if not filepaths: return
        self.add_paths_to_list([Path(fp) for fp in filepaths])

    def add_folder(self):
        """フォルダ選択ダイアログを開き、中の画像をリストに追加する"""
        folder_path = filedialog.askdirectory(title="フォルダを選択")
        if not folder_path: return
        target_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.tiff'}
        path_objects = []
        try:
            folder = Path(folder_path)
            for item in folder.iterdir():
                if item.is_file() and item.suffix.lower() in target_extensions:
                    path_objects.append(item)
            if not path_objects:
                messagebox.showinfo("info", "画像ファイルが見つかりませんでした。")
                return
            self.add_paths_to_list(path_objects)
        except Exception as e:
            messagebox.showerror("エラー", f"フォルダの読み込み中にエラーが発生しました:\n{e}")

    def process_file_parallel(self, path_obj):
        """【並列処理用】個別のファイルを解析して新しい名前を計算する"""
        dt_obj, source = self.get_date_info(path_obj)
        candidate_name = self.generate_new_name(path_obj, dt_obj, source)
        return path_obj, candidate_name, source

    def add_paths_to_list(self, path_objects):
        """計算と表示を完全に分離。表示はTextboxへ1つのテキストとして流し込む（1024件制限対策）"""
        new_paths = [p for p in path_objects if not any(d['original_path'] == p for d in self.file_data)]
        if not new_paths: return

        total_count = len(new_paths)
        self.lbl_info.configure(text=f"分析中...")
        self.progress_bar.set(0.1)
        self.update()

        # STEP 1: 並列処理でデータ収集
        with concurrent.futures.ThreadPoolExecutor() as executor:
            raw_results = list(executor.map(self.process_file_parallel, new_paths))

        # STEP 2: メモリ上での一括名前衝突解決（超高速）
        self.lbl_info.configure(text=f"重複をチェック中...")
        self.update()
        used_names = {d['new_name'] for d in self.file_data}
        entries_to_add = []

        for path_obj, candidate_name, source in raw_results:
            new_name = candidate_name
            if new_name in used_names or ((path_obj.parent / new_name).exists() and new_name != path_obj.name):
                stem = Path(candidate_name).stem
                suffix = Path(candidate_name).suffix
                counter = 1
                while f"{stem}_{counter}{suffix}" in used_names or \
                      ((path_obj.parent / f"{stem}_{counter}{suffix}").exists() and f"{stem}_{counter}{suffix}" != path_obj.name):
                    counter += 1
                new_name = f"{stem}_{counter}{suffix}"

            used_names.add(new_name)
            entries_to_add.append({
                'original_path': path_obj,
                'new_name': new_name,
                'date_source': source
            })

        # STEP 3: テキストボックスへの出力（高速・安定）
        self.preview_box.configure(state="normal")
        if not self.file_data and self.skip_count == 0:
            # 初回追加時のみヘッダーを入れる
            header = f"{'No.':<6} {'元のファイル名':<40}  →  {'変更後のファイル名':<40}\n"
            header += "-" * 100 + "\n"
            self.preview_box.insert("end", header)

        self.append_log(f"--- プレビュー作成中 ---")
        for i, entry in enumerate(entries_to_add):
            if entry['original_path'].name == entry['new_name']:
                self.skip_count += 1
                self.lbl_skip_info.configure(text=f"変更なし: {self.skip_count} 件")
            else:
                self.file_data.append(entry)
                row_no = len(self.file_data)
                # 表示用テキスト行の生成
                line = f"{row_no:<5} {entry['original_path'].name:<40}  >>>  {entry['new_name']:<40}\n"
                self.preview_box.insert("end", line)

            # 進行状況の更新（Textboxなら50件ごとでも十分スムーズ）
            if i % 50 == 0 or i == total_count - 1:
                self.progress_bar.set(0.1 + (0.9 * ((i + 1) / total_count)))
                self.lbl_info.configure(text=f"表示を更新中... ({i+1}/{total_count})")
                self.update()

        self.preview_box.configure(state="disabled")
        self.lbl_info.configure(text=f"{total_count} 件のファイル解析完了。")
        self.update()

    def get_date_info(self, file_path: Path):
        """Exifから撮影日時を取得する。失敗した場合はファイルの最終更新日時を返す。"""
        dt_obj = None
        source = "FileTime"
        try:
            image = Image.open(file_path)
            exif = image.getexif()
            if exif:
                date_str = exif.get(36867) or exif.get(306)
                if date_str:
                    dt_obj = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    source = "Exif"
                else:
                    source = "ExifMissingDate"
        except Exception: pass
        if dt_obj is None:
            dt_obj = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if source != "ExifMissingDate": source = "FileTime"
        return dt_obj, source

    def generate_new_name(self, original_path: Path, dt_obj: datetime.datetime, source: str):
        """詳細な仕様に基づき新しい名前を生成する"""
        stem = original_path.stem
        suffix = original_path.suffix
        date_str = dt_obj.strftime("%Y%m%d_%H%M%S")
        date_suffix = f"_{date_str}"

        screenshot_keywords = ["screenshot", "screen shot", "スクリーンショット", "s_", "capture"]
        is_screenshot = any(kw in stem.lower() for kw in screenshot_keywords) or (suffix.lower() == ".png" and source == "FileTime")
        prefix = "scrn_ymd_" if is_screenshot else ""

        clean_tags = ["Exif_", "exif0_", "File_", "IMG_ymd_", "scrn_ymd_"]
        if any(original_path.stem.startswith(tag) and date_str in original_path.stem for tag in clean_tags):
            return original_path.name

        if is_screenshot:
            stem = re.sub(r"^(scrn_ymd_|scrn_|IMG_(\d+|ymd)_?)", "", stem)
        elif re.match(r"^IMG_\d+", stem):
            stem = re.sub(r"^IMG_\d+", "IMG_ymd", stem)

        is_uuid = bool(re.search(r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}", stem))
        is_apple_id = bool(re.match(r"^\d{11}__", stem))

        if source == "Exif": return f"{prefix}Exif_{date_str}{suffix}"
        if source == "ExifMissingDate": return f"{prefix}exif0_{date_str}{suffix}"
        if is_uuid or is_apple_id: return f"{prefix}File_{date_str}{suffix}"
        if re.search(r"\d{8}_\d{6}", stem):
            final_name = f"{prefix}{stem}{suffix}"
            return original_path.name if final_name == original_path.name else final_name
        if is_screenshot and not stem: return f"{prefix}{date_str}{suffix}"
        if stem.endswith(date_suffix): return original_path.name

        return f"{prefix}{stem}{date_suffix}{suffix}"

    def clear_list(self):
        """リストと表示エリアをクリアする"""
        self.file_data = []
        self.skip_count = 0
        self.lbl_skip_info.configure(text="")
        self.lbl_info.configure(text="リストをクリアしました。")
        self.progress_bar.set(0)
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.configure(state="disabled")

    def run_rename(self):
        """実際にファイル名を変更する"""
        if not self.file_data:
            messagebox.showinfo("info", "リネーム対象のファイルがありません。")
            return

        self.append_log(f"--- 実行開始: {datetime.datetime.now().strftime('%H:%M:%S')} ---")
        self.progress_bar.set(0)
        total = len(self.file_data)
        count = 0
        error_count = 0

        for i, entry in enumerate(self.file_data):
            src = entry['original_path']
            dst = src.parent / entry['new_name']
            
            if dst.exists() and src != dst:
                base, ext = dst.stem, dst.suffix
                idx = 1
                while dst.exists():
                    dst = src.parent / f"{base}_{idx}{ext}"
                    idx += 1
            
            try:
                os.rename(src, dst)
                self.append_log(f"[成功] {src.name} -> {dst.name}")
                count += 1
            except Exception as e:
                self.append_log(f"[エラー] {src.name}: {e}")
                error_count += 1
            
            if i % 10 == 0 or i == total - 1:
                self.progress_bar.set((i + 1) / total)
                self.update()

        self.append_log(f"完了: {count}個リネーム成功 / {error_count}個失敗\n")
        messagebox.showinfo("完了", f"{count} 個のファイルをリネームしました。")
        self.clear_list()

if __name__ == "__main__":
    app = RenameApp()
    app.mainloop()
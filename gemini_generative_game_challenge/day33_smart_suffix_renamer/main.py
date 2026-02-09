import customtkinter as ctk
import os
import datetime
import re  # 正規表現用に追加
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
        self.geometry("1000x800") # ログエリア確保のため少し縦を伸ばしました

        # データ保持用リスト
        self.file_data = [] # {'original_path': Path, 'new_name': str, 'status': str}
        self.skip_count = 0 # 変更不要ファイルの集計用

        # --- UIレイアウト ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. ヘッダーエリア
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.btn_add_files = ctk.CTkButton(self.header_frame, text="ファイルを追加", command=self.add_files, width=140)
        self.btn_add_files.pack(side="left", padx=10, pady=10)

        self.btn_add_folder = ctk.CTkButton(self.header_frame, text="フォルダを追加", command=self.add_folder, width=140)
        self.btn_add_folder.pack(side="left", padx=10, pady=10)

        self.btn_clear = ctk.CTkButton(self.header_frame, text="リストをクリア", command=self.clear_list, fg_color="gray", width=120)
        self.btn_clear.pack(side="left", padx=10, pady=10)

        self.lbl_info = ctk.CTkLabel(self.header_frame, text="画像を選択してください。Exif優先で「Exif_日時」にリネームします。")
        self.lbl_info.pack(side="left", padx=20)

        # 変更不要なファイル数を赤い太字で表示するラベル
        self.lbl_skip_info = ctk.CTkLabel(self.header_frame, text="", text_color="#FF3B30", font=("Arial", 14, "bold"))
        self.lbl_skip_info.pack(side="left", padx=10)

        # 2. リスト表示エリア (スクロール可能)
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="変更プレビュー")
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # リストのヘッダーラベル
        self.header_label = ctk.CTkLabel(self.scroll_frame, text=f"{'元のファイル名':<40}  →  {'変更後のファイル名':<40}", font=("Consolas", 14, "bold"), anchor="w")
        self.header_label.pack(fill="x", padx=5, pady=5)

        # 3. フッターエリア（実行ボタン ＆ ログエリア）
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.btn_run = ctk.CTkButton(self.footer_frame, text="リネーム実行", command=self.run_rename, font=("Arial", 16, "bold"), height=40, fg_color="#2CC985", hover_color="#26A66F")
        self.btn_run.pack(fill="x", padx=20, pady=10)

        # エラーログ表示用のテキストボックス
        self.log_box = ctk.CTkTextbox(self.footer_frame, height=150, font=("Consolas", 12))
        self.log_box.pack(fill="x", padx=20, pady=(0, 10))
        self.log_box.insert("0.0", "--- 実行ログ ---\n")

    def append_log(self, message):
        """ログエリアにテキストを追記する共通メソッド"""
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")

    def add_files(self):
        """ファイル選択ダイアログを開き、リストに追加する"""
        filetypes = [("Images", "*.jpg;*.jpeg;*.png;*.heic;*.tiff"), ("All Files", "*.*")]
        filepaths = filedialog.askopenfilenames(title="ファイルを選択", filetypes=filetypes)

        if not filepaths:
            return
        
        # パスオブジェクトのリストに変換して共通処理へ
        path_objects = [Path(fp) for fp in filepaths]
        self.add_paths_to_list(path_objects)

    def add_folder(self):
        """フォルダ選択ダイアログを開き、中の画像をリストに追加する"""
        folder_path = filedialog.askdirectory(title="フォルダを選択")
        
        if not folder_path:
            return

        target_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.tiff'}
        path_objects = []
        
        try:
            folder = Path(folder_path)
            for item in folder.iterdir():
                if item.is_file() and item.suffix.lower() in target_extensions:
                    path_objects.append(item)
            
            if not path_objects:
                messagebox.showinfo("info", "選択したフォルダに画像ファイルが見つかりませんでした。")
                return

            self.add_paths_to_list(path_objects)
            
        except Exception as e:
            messagebox.showerror("エラー", f"フォルダの読み込み中にエラーが発生しました:\n{e}")

    def add_paths_to_list(self, path_objects):
        """パスのリストを受け取り、UIに追加する共通処理"""
        for path_obj in path_objects:
            # 既にリストにあるファイルはスキップ
            if any(d['original_path'] == path_obj for d in self.file_data):
                continue

            dt_obj, source = self.get_date_info(path_obj)
            new_name = self.generate_new_name(path_obj, dt_obj, source)
            
            # 名前が変わらない場合はリストに表示せず、赤いラベルでカウント
            if path_obj.name == new_name:
                self.skip_count += 1
                self.lbl_skip_info.configure(text=f"変更なし: {self.skip_count} 件")
                continue

            entry = {
                'original_path': path_obj,
                'new_name': new_name,
                'date_source': source
            }
            self.file_data.append(entry)
            self.add_row_to_ui(entry)

    def get_date_info(self, file_path: Path):
        """
        Exifから撮影日時を取得する。
        失敗した場合はファイルの最終更新日時を返す。
        戻り値: (datetimeオブジェクト, ソース文字列 'Exif' or 'FileTime')
        """
        dt_obj = None
        source = "FileTime"

        # 1. Exif情報の取得を試みる
        try:
            image = Image.open(file_path)
            exif = image.getexif()
            if exif:
                # DateTimeOriginal (タグID 36867) を探す
                date_str = exif.get(36867)
                # なければ DateTime (タグID 306)
                if not date_str:
                    date_str = exif.get(306)
                
                if date_str:
                    # Exifの日付形式は通常 "YYYY:MM:DD HH:MM:SS"
                    dt_obj = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    source = "Exif"
        except Exception:
            pass # Exifがない、または画像でない場合はスルー

        # 2. Exifが取れなかった場合、ファイルの更新日時を使用
        if dt_obj is None:
            mtime = os.path.getmtime(file_path)
            dt_obj = datetime.datetime.fromtimestamp(mtime)
            source = "FileTime"

        return dt_obj, source

    def generate_new_name(self, original_path: Path, dt_obj: datetime.datetime, source: str):
        """仕様に基づき新しい名前を生成する"""
        stem = original_path.stem # 拡張子なしのファイル名
        suffix = original_path.suffix # 拡張子 (.jpgなど)
        
        # フォーマット: YYYYMMDD_HHmmSS
        date_str = dt_obj.strftime("%Y%m%d_%H%M%S")
        date_suffix = f"_{date_str}"

        # --- 1. スクリーンショットの検知 ---
        # ファイル名に特定のキーワードが含まれる場合はプレフィックスを付与
        screenshot_keywords = ["screenshot", "screen shot", "スクリーンショット", "s_", "capture"]
        # 名前判定に加え、PNG形式でExifがない場合(FileTime)もスクリーンショットとみなす
        is_screenshot = any(kw in stem.lower() for kw in screenshot_keywords) or (suffix.lower() == ".png" and source == "FileTime")
        prefix = "scrn_ymd_" if is_screenshot else ""

        # --- 2. プレフィックスのクレンジング ---
        # 重複を防ぐため、既存のプレフィックスを一旦取り除く
        if is_screenshot:
            # scrn_ymd_, scrn_, IMG_... などを除去して純粋な本体(日付等)だけにする
            stem = re.sub(r"^(scrn_ymd_|scrn_|IMG_(\d+|ymd)_?)", "", stem)
        elif re.match(r"^IMG_\d+", stem):
            # IMG_8153 のような数字部分を IMG_ymd に置き換える
            stem = re.sub(r"^IMG_\d+", "IMG_ymd", stem)

        # --- 3. 二重処理防止ロジック ---
        # 既にファイル名に YYYYMMDD_HHMMSS 形式の日時が含まれているかチェック
        if re.search(r"\d{8}_\d{6}", stem):
            # すでに日時はあるので、プレフィックス(scrn_ymd_)やクレンジング(IMG_ymd)のみ適用
            final_name = f"{prefix}{stem}{suffix}"
            # 元の名前と完全に一致するならスキップ対象になる
            if final_name == original_path.name:
                return original_path.name
            return final_name

        # --- 4. 通常のリネームロジック ---
        # スクリーンショットでかつstemが空になった（元がプレフィックスのみだった）場合の処理
        if is_screenshot and not stem:
            return f"{prefix}{date_str}{suffix}"

        # Exif情報がある場合: [prefix]Exif_YYYYMMDD_HHmmSS.ext
        if source == "Exif":
            return f"{prefix}Exif_{date_str}{suffix}"
        
        # Exifがない場合（従来通り）: 元のファイル名_YYYYMMDD_HHmmSS.ext
        # 既に同じ日時サフィックスがついているかチェック
        if stem.endswith(date_suffix):
            return original_path.name

        return f"{prefix}{stem}{date_suffix}{suffix}"

    def add_row_to_ui(self, entry):
        """UIのスクロールフレームに行を追加する"""
        original = entry['original_path'].name
        new = entry['new_name']
        
        # 行用のフレーム
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=5, pady=2)
        
        # 表示テキスト
        label_text = f"{original:<30}  >>>  {new:<30}"
        
        label = ctk.CTkLabel(row_frame, text=label_text, font=("Consolas", 12), anchor="w")
        label.pack(side="left", padx=10)

        # 変更がない場合はここに来ない想定ですが、念のため
        if original == new:
            label.configure(text_color="gray")

    def clear_list(self):
        """リストをクリアし、スキップ件数もリセットする"""
        self.file_data = []
        self.skip_count = 0
        self.lbl_skip_info.configure(text="")
        for widget in self.scroll_frame.winfo_children():
            # ヘッダー以外を削除
            if widget != self.header_label:
                widget.destroy()

    def run_rename(self):
        """実際にファイル名を変更する"""
        if not self.file_data:
            messagebox.showinfo("info", "リネーム対象のファイルがありません。")
            return

        # 実行ログの開始
        self.append_log(f"--- 実行開始: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        count = 0
        error_count = 0

        for entry in self.file_data:
            src = entry['original_path']
            dst_name = entry['new_name']
            
            # 名前が変わらない場合は念のためスキップ
            if src.name == dst_name:
                continue

            dst = src.parent / dst_name

            # 重複チェック（簡易版）
            if dst.exists():
                # 重複する場合、(1), (2)などを付与して回避
                base_stem = dst.stem
                i = 1
                while dst.exists():
                    dst = src.parent / f"{base_stem}_{i}{src.suffix}"
                    i += 1
            
            try:
                os.rename(src, dst)
                self.append_log(f"[成功] {src.name} -> {dst.name}")
                count += 1
            except Exception as e:
                # エラーをログエリアに表示
                self.append_log(f"[エラー] {src.name}: {e}")
                error_count += 1

        self.append_log(f"完了: {count}個リネーム成功 / {error_count}個失敗\n")
        messagebox.showinfo("完了", f"{count} 個のファイルをリネームしました。\n詳細はログを確認してください。")
        self.clear_list()

if __name__ == "__main__":
    app = RenameApp()
    app.mainloop()
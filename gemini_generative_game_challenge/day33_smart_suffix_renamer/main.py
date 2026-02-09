import customtkinter as ctk
import os
import datetime
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
        self.geometry("900x600")

        # データ保持用リスト
        self.file_data = [] # {'original_path': Path, 'new_name': str, 'status': str}

        # --- UIレイアウト ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. ヘッダーエリア
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.btn_add_files = ctk.CTkButton(self.header_frame, text="ファイルを追加", command=self.add_files, width=150)
        self.btn_add_files.pack(side="left", padx=10, pady=10)

        self.btn_clear = ctk.CTkButton(self.header_frame, text="リストをクリア", command=self.clear_list, fg_color="gray", width=120)
        self.btn_clear.pack(side="left", padx=10, pady=10)

        self.lbl_info = ctk.CTkLabel(self.header_frame, text="画像ファイルを選択してください。撮影日時を末尾に付与します。")
        self.lbl_info.pack(side="left", padx=20)

        # 2. リスト表示エリア (スクロール可能)
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="変更プレビュー")
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # リストのヘッダーラベル（簡易的）
        self.header_label = ctk.CTkLabel(self.scroll_frame, text=f"{'元のファイル名':<40}  →  {'変更後のファイル名':<40}", font=("Consolas", 14, "bold"), anchor="w")
        self.header_label.pack(fill="x", padx=5, pady=5)

        # 3. フッターエリア（実行ボタン）
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.btn_run = ctk.CTkButton(self.footer_frame, text="リネーム実行", command=self.run_rename, font=("Arial", 16, "bold"), height=40, fg_color="#2CC985", hover_color="#26A66F")
        self.btn_run.pack(fill="x", padx=20, pady=10)

    def add_files(self):
        """ファイル選択ダイアログを開き、リストに追加する"""
        filetypes = [("Images", "*.jpg;*.jpeg;*.png;*.heic;*.tiff"), ("All Files", "*.*")]
        filepaths = filedialog.askopenfilenames(title="ファイルを選択", filetypes=filetypes)

        if not filepaths:
            return

        for fp in filepaths:
            path_obj = Path(fp)
            # 既にリストにあるファイルはスキップ
            if any(d['original_path'] == path_obj for d in self.file_data):
                continue

            date_str = self.get_date_info(path_obj)
            new_name = self.generate_new_name(path_obj, date_str)
            
            entry = {
                'original_path': path_obj,
                'new_name': new_name,
                'date_source': 'Exif' if date_str else 'FileTime'
            }
            self.file_data.append(entry)
            self.add_row_to_ui(entry)

    def get_date_info(self, file_path: Path):
        """
        Exifから撮影日時を取得する。
        失敗した場合はファイルの最終更新日時を返す。
        戻り値: datetimeオブジェクト
        """
        dt_obj = None

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
        except Exception:
            pass # Exifがない、または画像でない場合はスルー

        # 2. Exifが取れなかった場合、ファイルの更新日時を使用
        if dt_obj is None:
            mtime = os.path.getmtime(file_path)
            dt_obj = datetime.datetime.fromtimestamp(mtime)

        return dt_obj

    def generate_new_name(self, original_path: Path, dt_obj: datetime.datetime):
        """仕様に基づき新しい名前を生成する"""
        stem = original_path.stem # 拡張子なしのファイル名
        suffix = original_path.suffix # 拡張子 (.jpgなど)
        
        # フォーマット: _YYYYMMDDHHmmSS
        date_suffix = dt_obj.strftime("_%Y%m%d%H%M%S")
        
        # 既に同じ日時サフィックスがついているかチェック（多重付与防止）
        if stem.endswith(date_suffix):
            return original_path.name

        return f"{stem}{date_suffix}{suffix}"

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

        # 変更がない場合（既にリネーム済みなど）は色を変える
        if original == new:
            label.configure(text_color="gray")

    def clear_list(self):
        """リストをクリアする"""
        self.file_data = []
        for widget in self.scroll_frame.winfo_children():
            # ヘッダー以外を削除
            if widget != self.header_label:
                widget.destroy()

    def run_rename(self):
        """実際にファイル名を変更する"""
        if not self.file_data:
            messagebox.showinfo("info", "ファイルが選択されていません。")
            return

        count = 0
        error_count = 0

        for entry in self.file_data:
            src = entry['original_path']
            dst_name = entry['new_name']
            
            # 名前が変わらない場合はスキップ
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
                count += 1
            except Exception as e:
                print(f"Error renaming {src}: {e}")
                error_count += 1

        messagebox.showinfo("完了", f"{count} 個のファイルをリネームしました。\n(エラー/スキップ: {error_count})")
        self.clear_list()

if __name__ == "__main__":
    app = RenameApp()
    app.mainloop()
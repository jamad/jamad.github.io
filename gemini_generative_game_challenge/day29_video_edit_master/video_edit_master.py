import customtkinter as ctk # pip install customtkinter
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
import sys
from pathlib import Path
import time

# --- 設定 ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class SoundManager:
    """
    効果音を管理するクラス。
    実際のWAVファイルがあればそれを再生し、なければOS標準音やログ出力で代用します。
    """
    def play(self, event_type):
        # ここに実際のファイルパスを指定するとリッチな音になります
        # 例: self.play_wav("assets/success.wav")
        
        print(f"♪ Sound Effect: {event_type}")
        
        if sys.platform == "win32":
            import winsound
            if event_type == "click":
                winsound.Beep(1000, 100) # ピッ
            elif event_type == "start":
                winsound.Beep(600, 100)  # シュン
                time.sleep(0.05)
                winsound.Beep(800, 200)
            elif event_type == "success":
                winsound.Beep(1000, 150) # チャリーン
                time.sleep(0.1)
                winsound.Beep(1500, 300)
            elif event_type == "error":
                winsound.Beep(200, 400)  # ブブー
        else:
            # Mac/Linux用の簡易実装 (printのみ)
            pass

class VideoProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("SmartCut Pro (Prototype)")
        self.geometry("900x700")
        
        # 音響マネージャー
        self.sound = SoundManager()

        # グリッド構成 (2列構成)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # === 1. ファイル選択エリア (上部) ===
        self.file_frame = ctk.CTkFrame(self, corner_radius=10)
        self.file_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        self.btn_file = ctk.CTkButton(self.file_frame, text="動画ファイルを選択 (複数可)", command=self.select_file, height=40, font=("Arial", 14, "bold"))
        self.btn_file.pack(side="left", padx=20, pady=20)
        
        self.lbl_filepath = ctk.CTkLabel(self.file_frame, text="ファイルが選択されていません", text_color="gray")
        self.lbl_filepath.pack(side="left", padx=10, pady=20, fill="x", expand=True)

        self.input_paths = [] # 修正：単数から複数保持へ

        # === 2. 機能タブエリア (メイン) ===
        self.tabview = ctk.CTkTabview(self, width=800)
        self.tabview.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")

        # タブの追加
        self.tab_crop = self.tabview.add("画面トリミング")
        self.tab_trim = self.tabview.add("時間カット")
        self.tab_resize = self.tabview.add("リサイズ")
        self.tab_speed = self.tabview.add("再生速度")
        self.tab_rotate = self.tabview.add("回転")

        # 各タブの中身を構築
        self.setup_crop_tab()
        self.setup_trim_tab()
        self.setup_resize_tab()
        self.setup_speed_tab()
        self.setup_rotate_tab()

        # === 3. 実行エリア (下部) ===
        self.action_frame = ctk.CTkFrame(self, height=100, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.btn_process = ctk.CTkButton(self.action_frame, text="加工を実行する", command=self.run_process, 
                                         height=50, fg_color="#2CC985", hover_color="#229A65",
                                         font=("Arial", 16, "bold"))
        self.btn_process.pack(fill="x")

        # ログ表示エリア
        self.textbox_log = ctk.CTkTextbox(self, height=100)
        self.textbox_log.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.log("アプリを起動しました。動画を選択してください。")

    # --- UI構築ヘルパー ---
    def create_input_row(self, parent, label_text, default_val=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=10, fill="x", padx=50)
        lbl = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w", font=("Arial", 14))
        lbl.pack(side="left")
        
        # 修正: placeholderではなく初期値として入力済みにする (空文字エラー防止)
        entry = ctk.CTkEntry(frame)
        if default_val:
            entry.insert(0, default_val)
            
        entry.pack(side="left", fill="x", expand=True)
        return entry

    # === 各機能タブのUI実装 ===

    def setup_crop_tab(self):
        """1. 画面の一部をトリミング"""
        lbl = ctk.CTkLabel(self.tab_crop, text="画面上の指定した範囲を切り抜きます (例: 4Kから特定部分のみ)", font=("Arial", 16))
        lbl.pack(pady=20)
        
        self.entry_crop_w = self.create_input_row(self.tab_crop, "幅 (Width):", "1920")
        self.entry_crop_h = self.create_input_row(self.tab_crop, "高さ (Height):", "1080")
        self.entry_crop_x = self.create_input_row(self.tab_crop, "X座標 (左から):", "0")
        self.entry_crop_y = self.create_input_row(self.tab_crop, "Y座標 (上から):", "0")

    def setup_trim_tab(self):
        """2. タイムラインの一部をトリミング"""
        lbl = ctk.CTkLabel(self.tab_trim, text="指定した時間範囲を切り出します", font=("Arial", 16))
        lbl.pack(pady=20)

        self.entry_trim_start = self.create_input_row(self.tab_trim, "開始時間 (例 00:01:10):", "00:00:00")
        self.entry_trim_duration = self.create_input_row(self.tab_trim, "切り出す長さ (秒):", "20")

    def setup_resize_tab(self):
        """3. 動画のリサイズ"""
        lbl = ctk.CTkLabel(self.tab_resize, text="アスペクト比を維持してサイズを変更します", font=("Arial", 16))
        lbl.pack(pady=20)

        self.entry_resize_w = self.create_input_row(self.tab_resize, "新しい幅 (Width):", "320")
        lbl_hint = ctk.CTkLabel(self.tab_resize, text="※高さは自動計算されます", text_color="gray")
        lbl_hint.pack()

    def setup_speed_tab(self):
        """4. 再生速度の変更"""
        lbl = ctk.CTkLabel(self.tab_speed, text="再生速度を選択してください (音声も調整されます)", font=("Arial", 16))
        lbl.pack(pady=20)

        self.speed_var = tk.StringVar(value="1.0")
        
        speeds = ["1.2", "1.5", "1.75", "2.0"]
        frame = ctk.CTkFrame(self.tab_speed, fg_color="transparent")
        frame.pack(pady=20)

        for sp in speeds:
            rb = ctk.CTkRadioButton(frame, text=f"x {sp}", variable=self.speed_var, value=sp, font=("Arial", 14))
            rb.pack(side="left", padx=20)

    def setup_rotate_tab(self):
        """5. 動画を90度回転"""
        lbl = ctk.CTkLabel(self.tab_rotate, text="動画を時計回りに90度回転させます (縦⇔横)", font=("Arial", 16))
        lbl.pack(pady=20)
        
        self.rotate_icon = ctk.CTkLabel(self.tab_rotate, text="⟳", font=("Arial", 80))
        self.rotate_icon.pack(pady=20)

    # === イベントハンドラ ===

    def select_file(self):
        self.sound.play("click")
        # 修正：複数選択を許可する askopenfilenames に変更
        file_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv")])
        if file_paths:
            self.input_paths = list(file_paths)
            self.lbl_filepath.configure(text=f"{len(self.input_paths)} 個のファイルを選択中", text_color="white")
            self.log(f"{len(self.input_paths)} 個のファイルを選択しました。")

    def log(self, message):
        self.textbox_log.insert("end", f"> {message}\n")
        self.textbox_log.see("end")

    def run_process(self):
        self.sound.play("click")
        if not self.input_paths:
            self.sound.play("error")
            messagebox.showerror("エラー", "動画ファイルを選択してください")
            return

        # 現在選択されているタブを取得
        current_tab = self.tabview.get()
        
        # GPU設定
        v_encoder = "h264_nvenc" 

        # 複数ファイル分、コマンドのリストを作成する
        commands = []
        
        suffix_dict = {
            "画面トリミング": "_crop",
            "時間カット": "_trim",
            "リサイズ": "_resize",
            "再生速度": "_speed",
            "回転": "_rotate"
        }
        suffix = suffix_dict.get(current_tab, "_edit")

        try:
            for input_path in self.input_paths:
                p = Path(input_path)
                # 自動的に A_trim.mp4 のような名前を生成
                output_path = str(p.parent / f"{p.stem}{suffix}{p.suffix}")
                
                command = ["ffmpeg", "-y", "-i", input_path]

                if current_tab == "画面トリミング":
                    w = self.entry_crop_w.get() or "1920"
                    h = self.entry_crop_h.get() or "1080"
                    x = self.entry_crop_x.get() or "0"
                    y = self.entry_crop_y.get() or "0"
                    command += ["-vf", f"crop={w}:{h}:{x}:{y}", "-c:v", v_encoder, "-c:a", "copy", output_path]

                elif current_tab == "時間カット":
                    start = self.entry_trim_start.get() or "00:00:00"
                    duration = self.entry_trim_duration.get() or "20"
                    command = ["ffmpeg", "-y", "-ss", start, "-i", input_path, "-t", duration, "-c", "copy", output_path]

                elif current_tab == "リサイズ":
                    w = self.entry_resize_w.get() or "320"
                    command += ["-vf", f"scale={w}:-2", "-c:v", v_encoder, output_path]

                elif current_tab == "再生速度":
                    speed = float(self.speed_var.get())
                    filter_complex = f"[0:v]setpts=PTS/{speed}[v];[0:a]atempo={speed}[a]"
                    command += ["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]", "-c:v", v_encoder, output_path]

                elif current_tab == "回転":
                    command += ["-vf", "transpose=1", "-c:v", v_encoder, "-c:a", "copy", output_path]

                commands.append(command)

            # 別スレッドで順次実行を開始
            threading.Thread(target=self.execute_ffmpeg, args=(commands,)).start()

        except Exception as e:
            self.sound.play("error")
            self.log(f"コマンド生成エラー: {str(e)}")

    def execute_ffmpeg(self, commands):
        """FFmpegコマンドのリストを順次実行（リアルタイムログ表示付き）"""
        self.sound.play("start")
        self.after(0, lambda: self.btn_process.configure(state="disabled", text="処理中..."))

        try:
            for i, command in enumerate(commands):
                self.after(0, lambda idx=i+1: self.log(f"--- ファイル [{idx}/{len(commands)}] の処理を開始 ---"))
                
                # Windows用設定
                startupinfo = None
                if sys.platform == "win32":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                # Popenを使用してリアルタイムでstderrを読み取る
                process = subprocess.Popen(
                    command, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    text=True,
                    encoding='utf-8', 
                    errors='replace'
                )
                
                # ログ表示ループ
                while True:
                    line = process.stderr.readline()
                    if not line and process.poll() is not None:
                        break
                    
                    if line:
                        clean_line = line.strip()
                        if clean_line:
                            self.after(0, lambda msg=clean_line: self.log(msg))

                process.wait()

                if process.returncode != 0:
                    self.after(0, lambda: self.log(f"エラーが発生したため中断しました (コード: {process.returncode})"))
                    self.sound.play("error")
                    break

            if process.returncode == 0:
                self.sound.play("success")
                self.after(0, lambda: self.log("すべての処理が完了しました！"))
                self.after(0, lambda: messagebox.showinfo("成功", "全動画の加工が完了しました"))
        
        except Exception as e:
            self.sound.play("error")
            self.after(0, lambda: self.log(f"予期せぬエラー: {str(e)}"))
        
        finally:
            self.after(0, lambda: self.btn_process.configure(state="normal", text="加工を実行する"))

if __name__ == "__main__":
    app = VideoProcessorApp()
    app.mainloop()
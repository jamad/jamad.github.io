import customtkinter as ctk
import requests
import threading
import json
import base64
from datetime import datetime

# --- 設定 ---
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class GitLabAPI:
    """GitLab APIとの通信を担当するクラス"""
    def __init__(self, base_url, token, logger_func):
        self.base_url = base_url.rstrip('/')
        self.headers = {"PRIVATE-TOKEN": token}
        self.log = logger_func

    def check_connection(self):
        try:
            r = requests.get(f"{self.base_url}/api/v4/user", headers=self.headers, timeout=5)
            if r.status_code == 200:
                user = r.json()
                self.log(f"接続成功: ユーザー {user['username']} として認証しました。")
                return True
            else:
                self.log(f"接続失敗: ステータスコード {r.status_code}")
                return False
        except Exception as e:
            self.log(f"接続エラー: {e}")
            return False

    def get_namespaces(self):
        """ユーザーがアクセス可能なグループ/ユーザー名前空間を取得"""
        try:
            # 簡略化のため最初の20件のみ取得
            r = requests.get(f"{self.base_url}/api/v4/namespaces", headers=self.headers, params={'per_page': 50})
            if r.status_code == 200:
                return r.json()
            return []
        except:
            return []

    def create_project(self, name, path, namespace_id, visibility):
        url = f"{self.base_url}/api/v4/projects"
        data = {
            "name": name,
            "path": path,
            "namespace_id": namespace_id,
            "visibility": visibility,
            "initialize_with_readme": False # 手動で制御するためFalse
        }
        r = requests.post(url, headers=self.headers, json=data)
        if r.status_code == 201:
            project = r.json()
            self.log(f"✅ プロジェクト作成完了: ID {project['id']}")
            return project
        else:
            self.log(f"❌ プロジェクト作成失敗: {r.text}")
            return None

    def create_file(self, project_id, file_path, content, branch="main"):
        url = f"{self.base_url}/api/v4/projects/{project_id}/repository/files/{requests.utils.quote(file_path)}"
        data = {
            "branch": branch,
            "content": content,
            "commit_message": f"Add {file_path} via Helper Tool"
        }
        r = requests.post(url, headers=self.headers, json=data)
        if r.status_code == 201:
            self.log(f"📄 ファイル作成: {file_path}")
            return True
        else:
            self.log(f"⚠️ ファイル作成失敗 ({file_path}): {r.text}")
            return False

    def protect_branch(self, project_id, branch="main"):
        url = f"{self.base_url}/api/v4/projects/{project_id}/protected_branches"
        data = {
            "name": branch,
            "push_access_level": 0,   # No one
            "merge_access_level": 40  # Maintainers
        }
        r = requests.post(url, headers=self.headers, json=data)
        if r.status_code in [201, 409]: # 409は既に存在する場合
            self.log(f"🛡️ ブランチ保護設定: {branch}")
        else:
            self.log(f"⚠️ ブランチ保護失敗: {r.text}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("GitLab Project Helper")
        self.geometry("900x600")

        # グリッド構成 (2列構成: 左サイドバー、右メイン)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        
        # APIインスタンス保持用
        self.api = None
        self.namespaces = []

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="GitLab Helper", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # API設定
        ctk.CTkLabel(self.sidebar_frame, text="GitLab URL:").grid(row=1, column=0, padx=20, sticky="w")
        self.url_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="https://gitlab.com")
        self.url_entry.insert(0, "https://gitlab.com")
        self.url_entry.grid(row=2, column=0, padx=20, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Access Token:").grid(row=3, column=0, padx=20, sticky="w")
        self.token_entry = ctk.CTkEntry(self.sidebar_frame, show="*")
        self.token_entry.grid(row=4, column=0, padx=20, pady=5, sticky="n")

        self.connect_btn = ctk.CTkButton(self.sidebar_frame, text="接続テスト & グループ取得", command=self.connect_gitlab)
        self.connect_btn.grid(row=5, column=0, padx=20, pady=20)

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # --- プロジェクト情報セクション ---
        ctk.CTkLabel(self.main_frame, text="新規プロジェクト作成", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=10, padx=10)

        # Namespace (Group) 選択
        self.ns_label = ctk.CTkLabel(self.main_frame, text="Namespace (Group/User):")
        self.ns_label.pack(anchor="w", padx=20)
        self.ns_option = ctk.CTkOptionMenu(self.main_frame, values=["先に接続してください"])
        self.ns_option.pack(fill="x", padx=20, pady=5)

        # プロジェクト名
        ctk.CTkLabel(self.main_frame, text="Project Name:").pack(anchor="w", padx=20)
        self.name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="My New Project")
        self.name_entry.pack(fill="x", padx=20, pady=5)

        # パス (Slug)
        ctk.CTkLabel(self.main_frame, text="Project Slug (Path):").pack(anchor="w", padx=20)
        self.path_entry = ctk.CTkEntry(self.main_frame, placeholder_text="my-new-project")
        self.path_entry.pack(fill="x", padx=20, pady=5)

        # 公開設定
        ctk.CTkLabel(self.main_frame, text="Visibility:").pack(anchor="w", padx=20)
        self.visibility_var = ctk.StringVar(value="private")
        self.vis_seg = ctk.CTkSegmentedButton(self.main_frame, values=["private", "internal", "public"], variable=self.visibility_var)
        self.vis_seg.pack(fill="x", padx=20, pady=5)

        # --- オプション (チェックボックス) ---
        ctk.CTkLabel(self.main_frame, text="自動化オプション", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(20, 5), padx=10)
        
        self.chk_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.chk_frame.pack(fill="x", padx=10)

        self.chk_readme = ctk.CTkCheckBox(self.chk_frame, text="README.md を作成")
        self.chk_readme.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.chk_readme.select()

        self.chk_ci = ctk.CTkCheckBox(self.chk_frame, text=".gitlab-ci.yml (テンプレート) を作成")
        self.chk_ci.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.chk_ci.select()

        self.chk_protect = ctk.CTkCheckBox(self.chk_frame, text="Mainブランチを保護 (Push禁止)")
        self.chk_protect.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.chk_protect.select()

        # --- 実行ボタンとログ ---
        self.create_btn = ctk.CTkButton(self.main_frame, text="プロジェクトを作成する", command=self.start_creation, fg_color="green", height=40)
        self.create_btn.pack(fill="x", padx=20, pady=20)

        self.log_box = ctk.CTkTextbox(self.main_frame, height=150)
        self.log_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.log_box.configure(state="disabled")

    def log(self, message):
        """ログボックスにメッセージを追加（スレッドセーフ）"""
        def _update():
            self.log_box.configure(state="normal")
            timestamp = datetime.now().strftime("[%H:%M:%S] ")
            self.log_box.insert("end", timestamp + message + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.after(0, _update)

    def connect_gitlab(self):
        url = self.url_entry.get()
        token = self.token_entry.get()
        
        if not url or not token:
            self.log("エラー: URLとトークンを入力してください")
            return

        self.api = GitLabAPI(url, token, self.log)
        
        # UIフリーズ回避のため別スレッドで実行
        threading.Thread(target=self._fetch_groups_thread).start()

    def _fetch_groups_thread(self):
        self.log("GitLabに接続中...")
        if self.api.check_connection():
            namespaces = self.api.get_namespaces()
            self.namespaces = namespaces
            names = [f"{ns['name']} ({ns['path']})" for ns in namespaces]
            
            if names:
                self.ns_option.configure(values=names)
                self.ns_option.set(names[0])
                self.log(f"グループ情報を取得しました: {len(names)}件")
            else:
                self.log("グループが見つかりませんでした。")
        else:
            self.log("認証に失敗しました。")

    def start_creation(self):
        if not self.api:
            self.log("エラー: まずGitLabに接続してください。")
            return
        
        name = self.name_entry.get()
        path = self.path_entry.get()
        
        # 選択されたnamespaceからIDを特定
        selected_text = self.ns_option.get()
        ns_id = None
        for ns in self.namespaces:
            if f"{ns['name']} ({ns['path']})" == selected_text:
                ns_id = ns['id']
                break
        
        if not name or not path or not ns_id:
            self.log("エラー: プロジェクト名、パス、Namespaceは必須です。")
            return

        # ボタンを無効化
        self.create_btn.configure(state="disabled")
        
        # 別スレッドで実行
        threading.Thread(target=self._creation_process, args=(name, path, ns_id)).start()

    def _creation_process(self, name, path, ns_id):
        self.log("=== プロジェクト作成プロセス開始 ===")
        
        # 1. プロジェクト作成
        project = self.api.create_project(name, path, ns_id, self.visibility_var.get())
        
        if project:
            pid = project['id']
            
            # 2. README作成
            if self.chk_readme.get():
                content = f"# {name}\n\nGenerated by GitLab Helper Tool."
                self.api.create_file(pid, "README.md", content)

            # 3. CI/CD作成 (サンプルテンプレート)
            if self.chk_ci.get():
                ci_content = """stages:
  - build
  - test

build_job:
  stage: build
  script:
    - echo "Building the project..."

test_job:
  stage: test
  script:
    - echo "Running tests..."
"""
                self.api.create_file(pid, ".gitlab-ci.yml", ci_content)

            # 4. ブランチ保護
            if self.chk_protect.get():
                # 注意: ファイル作成直後だとブランチが存在しない場合があるため、
                # READMEを作成していない場合はブランチがない可能性がある
                if self.chk_readme.get() or self.chk_ci.get():
                    self.api.protect_branch(pid)
                else:
                    self.log("⚠️ ファイルが作成されていないため、ブランチ保護をスキップしました。")

            self.log(f"✨ 全工程完了! URL: {project['web_url']}")
        
        self.log("==================================")
        # ボタンを戻す
        self.after(0, lambda: self.create_btn.configure(state="normal"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
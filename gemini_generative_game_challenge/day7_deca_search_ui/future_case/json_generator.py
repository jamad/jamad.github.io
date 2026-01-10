# https://aistudio.google.com/prompts/10FQ5JcrTLYQj0h7DhTfHjWFpAR9D5twS



import json
import os

# ==========================================
# 設定: 1ファイルあたりの単語数
# ==========================================
WORDS_PER_FILE = 10000  # 1ファイル1万語
FILE_COUNT = 10         # 0~9 の10ファイル作成 (合計10万語)

def main():
    print(f"--- Split Data Generator ---")
    print(f"1ファイル {WORDS_PER_FILE} 語 x {FILE_COUNT} ファイル = 合計 {WORDS_PER_FILE * FILE_COUNT} 語")

    for file_index in range(FILE_COUNT):
        data = {"items": {}}
        start_index = file_index * WORDS_PER_FILE
        
        print(f"Creating data_{file_index}.json (Index {start_index} ~ )...")

        for i in range(WORDS_PER_FILE):
            # 全体通しのインデックス
            global_id = start_index + i
            
            # ダミーデータ生成
            # 本番ではここをCSV読み込みなどに変えればOK
            data["items"][str(global_id)] = {
                "en": f"Word-{global_id:06d}",
                "fi": f"Sana-{global_id:06d}",
                "ja": f"単語-{global_id:06d}"
            }

        # ファイル書き出し: data_0.json, data_1.json ...
        filename = f"data_{file_index}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            
    print("\n[完了] 10個のjsonファイルを作成しました。")
    print("python -m http.server 8000 を実行してHTMLを開いてください。")

if __name__ == "__main__":
    main()
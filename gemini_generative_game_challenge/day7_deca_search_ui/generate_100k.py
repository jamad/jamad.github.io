# https://aistudio.google.com/prompts/10FQ5JcrTLYQj0h7DhTfHjWFpAR9D5twS

import json
import urllib.request

# ==========================================
# 設定: 全件取得モード
# ==========================================
OUTPUT_FILE = 'data.json'
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

def main():
    print(f"--- Deca-Search Data Generator (UNLIMITED) ---")
    
    # 1. ダウンロード
    print("1. 英単語リストをダウンロード中...")
    try:
        with urllib.request.urlopen(WORD_LIST_URL) as response:
            content = response.read().decode('utf-8')
            words = content.splitlines()
            total_words = len(words)
            print(f"   ダウンロード完了: 合計 {total_words} 語を取得しました。")
    except Exception as e:
        print(f"   [エラー] ダウンロード失敗: {e}")
        return

    # 2. JSON生成
    print("2. データベース構築中（全件処理）...")
    dataset = {"items": {}}
    
    for i, word in enumerate(words):
        # 先頭大文字
        word = word.capitalize()
        
        # 37万件すべてにインデックスを振る
        dataset["items"][str(i)] = {
            "en": word,
            "fi": f"(fi) {word}", 
            "ja": f"{word} の意味"
        }
        
        if i % 50000 == 0:
            print(f"   処理中... {i}/{total_words}")

    # 3. 書き出し
    print(f"3. {OUTPUT_FILE} に書き出し中...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False)
        
    print(f"\n[成功] {OUTPUT_FILE} を作成しました。")
    print(f"最終データ件数: {len(dataset['items'])}")
    print("ブラウザをリロードしてください。")

if __name__ == "__main__":
    main()
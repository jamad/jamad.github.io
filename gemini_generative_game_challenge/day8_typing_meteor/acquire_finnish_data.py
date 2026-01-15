import json
import re
import time
import urllib.request
from deep_translator import GoogleTranslator
from uralicNLP import uralicApi

# --- 設定 ---
# 取得したい単語数（テスト用に小さくしていますが、増やせます）
WORD_LIMIT = 50 

# 生成したい格（前回と同じ）
CASES = [
    {"morph": "+N+Sg+Gen", "suffix_en": "'s"},
    {"morph": "+N+Sg+Par", "suffix_en": ""}, # 分格は英語訳を変えないことが多い
    {"morph": "+N+Sg+Ine", "prefix_en": "in "},
]

def fetch_common_words(limit):
    """
    Wiktionaryの頻出語リスト（などのソース）から単語をスクレイピングする関数。
    今回は安定性のために、ネット上のテキストファイルから取得する例を示します。
    """
    print("Fetching word list...")
    # GitHub上のオープンなフィンランド語頻出単語リスト（10000語）を使用
    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/fi/fi_50k.txt"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            lines = data.split('\n')
            
            words = []
            # format: "word count" -> "koti 12345"
            for line in lines:
                parts = line.split(' ')
                if len(parts) >= 1:
                    word = parts[0].strip()
                    # 2文字以下や記号を含むものは除外
                    if len(word) > 2 and word.isalpha():
                        words.append(word)
                        if len(words) >= limit:
                            break
            return words
    except Exception as e:
        print(f"Error fetching list: {e}")
        return ["koti", "koira", "kissa"] # 失敗時のバックアップ

def main():
    # 1. モデルの準備
    if not uralicApi.is_language_installed("fin"):
        uralicApi.download("fin")
    
    translator = GoogleTranslator(source='fi', target='en')
    
    # 2. 単語リストの取得
    base_words = fetch_common_words(WORD_LIMIT)
    print(f"Acquired {len(base_words)} base words. Starting processing...")
    
    final_dataset = []
    
    for i, fi_word in enumerate(base_words):
        try:
            # 3. 翻訳 (API制限を避けるため少し待機)
            en_word = translator.translate(fi_word)
            time.sleep(0.5) 
            
            print(f"[{i+1}/{len(base_words)}] Base: {fi_word} -> {en_word}")
            
            # 基本形を追加
            final_dataset.append({"fi": fi_word, "en": en_word})
            
            # 4. 格変化の生成
            for case in CASES:
                generated = uralicApi.generate(fi_word + case["morph"], "fin")
                if generated:
                    inflected_fi = generated[0][0]
                    
                    # 英語訳の加工
                    inflected_en = en_word
                    if "prefix_en" in case: inflected_en = case["prefix_en"] + inflected_en
                    if "suffix_en" in case: inflected_en = inflected_en + case["suffix_en"]
                    
                    final_dataset.append({"fi": inflected_fi, "en": inflected_en})
                    
        except Exception as e:
            print(f"Skipping {fi_word}: {e}")

    # 5. 保存
    output_file = "finnish_auto_collection.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_dataset, f, indent=4, ensure_ascii=False)
        
    print(f"\nDone! Saved {len(final_dataset)} words to {output_file}")

if __name__ == "__main__":
    main()
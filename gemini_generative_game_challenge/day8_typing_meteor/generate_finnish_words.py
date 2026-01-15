import json
from uralicNLP import uralicApi

# uralicNLPのモデルをダウンロード（初回のみ時間がかかります）
if not uralicApi.is_language_installed("fin"):
    uralicApi.download("fin")

# 基本単語リスト (ここに追加していけば無限に増やせます)
base_words = [
    {"fi": "koti", "en": "home"},
    {"fi": "vesi", "en": "water"},
    {"fi": "yö", "en": "night"},
    {"fi": "kirja", "en": "book"},
    {"fi": "kissa", "en": "cat"},
    {"fi": "kauppa", "en": "shop"},
    {"fi": "järvi", "en": "lake"},
    {"fi": "tuli", "en": "fire"},
]

# 生成したい格（Case）の定義
# Sg = 単数形 (Singular)
# Gen = 属格 (〜の / 's)
# Par = 分格 (部分的な対象 / part of)
# Ine = 内格 (〜の中で / in)
# Ade = 接格 (〜の上で、〜で / on/at)
cases_to_generate = [
    {"morph": "+N+Sg+Gen", "suffix_en": "'s"},        # Genitive
    {"morph": "+N+Sg+Par", "suffix_en": " (part)"},   # Partitive
    {"morph": "+N+Sg+Ine", "prefix_en": "in "},       # Inessive
    {"morph": "+N+Sg+Ade", "prefix_en": "at "},       # Adessive
]

final_list = []

print("Generating inflected forms...")

for word in base_words:
    # 1. 基本形を追加
    final_list.append(word)
    
    # 2. 格変化形を生成して追加
    for case in cases_to_generate:
        try:
            # uralicApiを使って変化形を生成
            # generate関数は候補をリストで返すので、最初の1つを使うのが一般的
            generated = uralicApi.generate(word["fi"] + case["morph"], "fin")
            
            if generated:
                inflected_fi = generated[0][0] # (form, morphine_info) のタプルが返る
                
                # 英語訳の生成
                base_en = word["en"]
                inflected_en = base_en
                
                if "prefix_en" in case:
                    inflected_en = case["prefix_en"] + inflected_en
                if "suffix_en" in case:
                    inflected_en = inflected_en + case["suffix_en"]
                
                # リストに追加
                final_list.append({
                    "fi": inflected_fi,
                    "en": inflected_en
                })
                print(f"Generated: {word['fi']} -> {inflected_fi} ({inflected_en})")
                
        except Exception as e:
            print(f"Error generating {word['fi']}: {e}")

# JSONファイルとして保存
with open("finnish_game_data.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4, ensure_ascii=False)

print(f"\nDone! Total words generated: {len(final_list)}")
print("Copy the content of 'finnish_game_data.json' into your WORD_LIST variable.")
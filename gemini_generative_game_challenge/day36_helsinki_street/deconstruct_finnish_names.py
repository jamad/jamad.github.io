import json
import time
import re

def translate_with_perfect_nuance():
    # ファイル読み込み
    with open('streets_metadata_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. フィンランド語の自然・地形パーツ辞書（和名・意味を重視）
    # 属格のnで終わるものも考慮
    fin_dict = {
        # 植物・自然
        'kataja': '杜松', 'katajan': '杜松',
        'kuusi': 'モミ', 'kuusen': 'モミ',
        'mänty': '松', 'männyn': '松',
        'koivu': '白樺', 'koivun': '白樺',
        'pihlaja': 'ななかまど', 'pihlajan': 'ななかまど',
        'tammi': '樫', 'tammen': '樫',
        'pähkinä': 'くるみ', 'pähkinän': 'くるみ',
        'mustikka': 'ブルーベリー',
        # 地形
        'harju': '尾根', 'harjun': '尾根',
        'saari': '島', 'saaren': '島',
        'järvi': '湖', 'järven': '湖',
        'lahti': '湾', 'lahden': '湾',
        'niemi': '岬', 'niemen': '岬',
        'puro': '小川', 'puron': '小川',
        'mäki': '丘', 'mäen': '丘',
        'joki': '川', 'joen': '川',
        'ranta': '海岸', 'rannan': '海岸',
        'suo': '沼', 'suon': '沼',
        'kallio': '岩山', 'kallion': '岩山',
        'laakso': '谷', 'laakson': '谷',
        'pohja': '底', 'pohjan': '底',
        # 施設・概念
        'asema': '駅', 'aseman': '駅',
        'kirkko': '教会', 'kirkon': '教会',
        'linna': '城', 'linnan': '城',
        'tori': '広場', 'torin': '広場',
        'kylä': '村', 'kylän': '村',
        'kartano': '邸宅', 'kartanon': '邸宅',
        'pelto': '畑', 'pellon': '畑',
        'puisto': '公園', 'puiston': '公園',
        'vanha': '旧', 'uusi': '新',
        'etelä': '南', 'pohjois': '北', 'länsi': '西', 'itä': '東'
    }

    # 2. ユーザー指定の接尾辞ルール
    suffixes = {
        'katu': '街',
        'tie': '通り',
        'kuja': '路地',
        'polku': '小道',
        'väylä': '街道',
        'kaari': 'カーブ',
        'silta': '橋'
    }

    # 3. AIが暴走した地名の個別修正（追加分）
    manual_fixes = {
        "Ulvilantie": "ウルヴィラ通り", # Ulvilaは町の名前
        "Perkkaantie": "ペルッカー通り", # Perkkaaは地名
        "Lansantie": "ランサ通り",
        "Hiiralantie": "ヒーララ通り",
        "Kaivokatu": "井戸街"
    }

    print("高精度翻訳を開始します...")

    for item in data:
        fi = item['fi']
        fi_lower = fi.lower()
        
        # 個別修正リストにある場合は即適用
        if fi in manual_fixes:
            item['ja'] = manual_fixes[fi]
            continue

        root = fi_lower
        ja_suffix = ""

        # 語尾の切り離し
        for s, ja_s in suffixes.items():
            if fi_lower.endswith(s):
                root = fi_lower[:-len(s)]
                ja_suffix = ja_s
                break
        
        # ルート単語の翻訳（辞書引き）
        ja_root = ""
        # 複数のパーツで構成されている場合（kataja + harjuなど）を考慮
        temp_root = root
        while temp_root:
            found_part = False
            # 長い単語から順にマッチさせる
            sorted_keys = sorted(fin_dict.keys(), key=len, reverse=True)
            for key in sorted_keys:
                if temp_root.startswith(key):
                    ja_root += fin_dict[key]
                    temp_root = temp_root[len(key):]
                    found_part = True
                    break
            
            if not found_part:
                # 辞書にない場合は、残りをそのままカタカナ推測（簡易処理）
                # 複雑なものはAIに頼らずカタカナ化
                ja_root += temp_root.capitalize()
                break
        
        item['ja'] = f"{ja_root}{ja_suffix}"

    # 保存
    with open('streets_metadata_refined.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n完了！ 'streets_metadata_refined.json' を作成しました。")

if __name__ == "__main__":
    translate_with_perfect_nuance()
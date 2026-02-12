import json
import re

def clean_streets():
    with open('streets_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 致命的な誤訳・不適切な訳の個別修正リスト
    # (名前: 修正後の日本語)
    manual_fixes = {
        "Lippajärventie": "リッパ湖通り", # または「ひさし湖通り」
        "Lansantie": "ランサ通り",
        "Lansanpurontie": "ランサンプロン通り",
        "Perkkaantie": "ペルッカー通り",
        "Henttaankaari": "ヘンッタ・カーブ",
        "Toppelundintie": "トッペルンド通り",
        "Vääksyntie": "ヴァークシュ通り",
        "Koskelontie": "コスケロ通り",
        "Koskelonsilta": "コスケロ橋",
        "Kustaankatu": "クスター街",
        "Hämeentie": "ハメ通り",
        "Bembölentie": "ベンボレ通り",
        "Maarintie": "マーリ通り",
        "Vihdintie": "ヴィヒティ通り",
        "Haartmaninkatu": "ハールトマン街",
        "Untamalantie": "ウンタマ通り",
        "Toivonkatu": "トイボ街",
        "Kutsuntatie": "クツンタ通り",
        "Ollaksentie": "オッラス通り",
        "Porkkalankatu": "ポルッカラ街",
        "Kaivokatu": "井戸街",
        "Hiiralantie": "ヒーララ通り",
        "Henttaanaukio": "ヘンッタ広場",
        "Ylästöntie": "ユラスト通り",
        "Kontulantie": "コントゥラ通り",
        "Lansan": "ランサ",
        "Parrulaituri": "パッル桟橋", # 理髪店ではない
        "Ahmatie": "クズリ通り"      # 大食いではない
    }

    # 2. 接尾辞の統一ルール (ユーザー様の希望を反映)
    suffix_rules = [
        ('katu', '街', 'Street'),
        ('tie', '通り', 'Road'),
        ('kuja', '路地', 'Alley'),
        ('polku', '小道', 'Path'),
        ('ranta', '海岸通り', 'Shore'),
        ('puisto', '公園', 'Park'),
        ('väylä', '街道', 'Way'),
        ('silta', '橋', 'Bridge'),
        ('kaari', 'カーブ', 'Arc'),
        ('aukio', '広場', 'Square'),
        ('tori', '広場', 'Market Square'),
        ('laituri', '桟橋', 'Pier'),
        ('rinne', '坂', 'Slope')
    ]

    fixed_count = 0

    for item in data:
        fi = item['fi']
        
        # 個別修正リストにあるかチェック
        found_manual = False
        for key, fixed_ja in manual_fixes.items():
            if key in fi:
                item['ja'] = fixed_ja
                found_manual = True
                break
        
        # ルールに基づいた一括置換
        for suffix, ja_suffix, en_suffix in suffix_rules:
            if fi.lower().endswith(suffix):
                # 日本語の語尾を強制書き換え
                # 既に「〜通り」などになっている場合も考慮して、一旦語尾をカットしてから付ける
                if not found_manual:
                    # 日本語のクリーニング（AIが作った変な言葉を消す）
                    # 「おかしくなった」「ヤリまくる」等が含まれていたらカタカナ推測（簡易的）
                    bad_words = ["ヤリ", "セックス", "狂った", "死ぬ", "おかしく", "ごめんなさい", "冗談です"]
                    if any(bad in item['ja'] for bad in bad_words):
                        # 変な言葉が入っていたら、フィンランド語の頭文字をそのまま使う
                        root = fi[:-len(suffix)]
                        item['ja'] = root + ja_suffix
                
                # 語尾の統一
                # 現在の語尾（通り、街、道など）を削除
                item['ja'] = re.sub(r'(通り|街|道|路地|公園|街道|橋|カーブ|広場|海岸通り)$', '', item['ja'])
                item['ja'] += ja_suffix

                # 英語の語尾も統一
                item['en'] = re.sub(r'(Road|Street|Alley|Path|Way|Bridge|Arc|Square|Shore)$', '', item['en']).strip()
                item['en'] += " " + en_suffix
                break

        # 微調整
        item['ja'] = item['ja'].replace(" Road", "").replace(" Street", "")
        item['en'] = item['en'].replace("  ", " ").strip()

    # 保存
    with open('streets_metadata_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("クリーニング完了！ 'streets_metadata_fixed.json' を作成しました。")

if __name__ == "__main__":
    clean_streets()
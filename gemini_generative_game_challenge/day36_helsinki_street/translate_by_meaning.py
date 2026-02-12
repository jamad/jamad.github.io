import json
import time
from deep_translator import GoogleTranslator

def translate_final_nuance():
    # ユーザー様のこだわり設定
    # katu = 街 (Street/Urban feel)
    # tie = 通り (Road/Path feel)
    suffix_map = {
        'katu': {'en': 'Street', 'ja': '街'},   # 例: 井戸街 (Kaivokatu)
        'tie': {'en': 'Road', 'ja': '通り'},    # 例: マンネルヘイム通り (Mannerheimintie)
        'kuja': {'en': 'Alley', 'ja': '路地'},
        'polku': {'en': 'Path', 'ja': '小道'},
        'ranta': {'en': 'Shore', 'ja': '海岸通り'},
        'puisto': {'en': 'Park', 'ja': '公園'},
        'aukio': {'en': 'Square', 'ja': '広場'},
        'väylä': {'en': 'Way', 'ja': '街道'},
        'rinne': {'en': 'Slope', 'ja': '坂'},
        'silta': {'en': 'Bridge', 'ja': '橋'},
    }

    # ファイル読み込み
    with open('streets.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    translator_ja = GoogleTranslator(source='fi', target='ja')
    translator_en = GoogleTranslator(source='fi', target='en')

    print(f"katu=街 / tie=通り 設定で翻訳を開始します...")

    for i, item in enumerate(data):
        fi_name = item['fi']
        root_name = fi_name
        en_suffix = ""
        ja_suffix = ""

        # 接尾辞の判定
        for suffix, trans in suffix_map.items():
            if fi_name.lower().endswith(suffix):
                root_name = fi_name[:-len(suffix)]
                en_suffix = " " + trans['en']
                ja_suffix = trans['ja']
                break
        
        try:
            if root_name:
                # 属格の '-n' を取り除く (Mannerheimin -> Mannerheim)
                if root_name.endswith('in'):
                    root_name = root_name[:-1]
                
                # 翻訳実行
                meaning_ja = translator_ja.translate(root_name)
                meaning_en = translator_en.translate(root_name)
                
                # 日本語の組み立て
                item['ja'] = f"{meaning_ja}{ja_suffix}"
                item['en'] = f"{meaning_en}{en_suffix}"
            else:
                item['ja'] = ja_suffix
                item['en'] = en_suffix

            #if i % 20 == 0:
            print(f"[{i}/{len(data)}] {fi_name} -> {item['en']} {item['ja']}")
            
            time.sleep(0.2) # API負荷軽減

        except Exception as e:
            print(f"Error at {fi_name}: {e}")
            time.sleep(1)

    # 上書き保存
    with open('streets.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n完了！ 理想のマッピングに更新されました。")

if __name__ == "__main__":
    translate_final_nuance()
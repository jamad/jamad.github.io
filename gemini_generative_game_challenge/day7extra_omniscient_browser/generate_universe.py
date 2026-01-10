import json
import urllib.request
import csv
import io

# ==========================================
# 設定: データ・ユニバース定義
# ==========================================
OUTPUT_FILE = 'data.json'

# 各セクターのIDオフセット (10億単位 = COSMICスライダーが1動くごとの単位)
# BASE=10, L0(COSMIC)=10^9
OFFSET_UNIT = 10**9 

SECTORS = [
    {
        "id": 0,
        "name": "GENERAL (English)",
        "url": "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
        "type": "txt"
    },
    {
        "id": 1,
        "name": "MEDICAL (Diseases)",
        # Open Disease Data (簡易リスト)
        "url": "https://raw.githubusercontent.com/glutanimate/wordlist-medicalterms-en/master/wordlist.txt",
        "type": "txt"
    },
    {
        "id": 2,
        "name": "BIOLOGY (Taxonomy)",
        # 動物名のリスト (簡易)
        "url": "https://raw.githubusercontent.com/imsky/wordlists/master/nouns/animals.txt",
        "type": "txt"
    },
    {
        "id": 3,
        "name": "CHEMICAL (Elements/Drugs)",
        # 元素と化合物のリスト
        "url": "https://raw.githubusercontent.com/imsky/wordlists/master/nouns/science.txt",
        "type": "txt"
    }
]

def download_text_list(url):
    print(f"   Downloading from {url}...")
    try:
        # User-Agentを設定しないと拒否される場合があるため設定
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
            # 空行を除去してリスト化
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            return lines
    except Exception as e:
        print(f"   [ERROR] Failed to download: {e}")
        return []

def main():
    print(f"--- Deca-Search UNIVERSE Generator ---")
    dataset = {"items": {}, "sectors": {}}

    total_records = 0

    for sector in SECTORS:
        sector_id = sector["id"]
        sector_name = sector["name"]
        base_index = sector_id * OFFSET_UNIT
        
        print(f"\nProcessing Sector {sector_id}: {sector_name}")
        
        # データの取得
        words = download_text_list(sector["url"])
        count = len(words)
        print(f"   -> Retrieved {count} records.")

        if count == 0:
            continue

        # データ生成
        print(f"   -> Mapping to IDs starting from {base_index}...")
        
        for i, word in enumerate(words):
            # 先頭大文字
            word = word.capitalize()
            
            # ID計算: セクターのベース + 連番
            # 例: 医学(Sector 1)の5番目の単語 -> ID: 1,000,000,005
            current_id = base_index + i
            
            # 分野ごとの翻訳プレースホルダー
            fi_text = ""
            ja_text = ""
            
            if sector_id == 0: # General
                fi_text = f"(fi) {word}"
                ja_text = "一般用語"
            elif sector_id == 1: # Medical
                fi_text = f"(fi-med) {word}"
                ja_text = "医学用語 / 病名"
            elif sector_id == 2: # Biology
                fi_text = f"(fi-bio) {word}"
                ja_text = "生物名 / 学名"
            elif sector_id == 3: # Chemical
                fi_text = f"(fi-chem) {word}"
                ja_text = "化学物質 / 科学用語"

            dataset["items"][str(current_id)] = {
                "en": word,
                "fi": fi_text,
                "ja": ja_text,
                "sector": sector_name # メタデータとしてセクター名を保持
            }
        
        total_records += count
        # セクター情報の保存（アプリ側で表示するため）
        dataset["sectors"][str(sector_id)] = {
            "name": sector_name,
            "count": count,
            "start": base_index,
            "end": base_index + count - 1
        }

    # ファイル書き出し
    print(f"\nWriting to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False)
        
    print(f"\n[SUCCESS] Generated {total_records} records across {len(SECTORS)} sectors.")
    print("Please reload the Deca-Search application.")

if __name__ == "__main__":
    main()
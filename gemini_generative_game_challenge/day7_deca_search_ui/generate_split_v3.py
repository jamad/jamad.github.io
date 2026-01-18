import json
import urllib.request
import os

# ==========================================
# Deca-Search Split Generator v3
# ==========================================
OFFSET_UNIT = 10**9 

SECTORS = [
    {
        "id": 0, "name": "GENERAL", "filename": "data_gen.json",
        "url": "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt",
        "fallback": ["Apple", "Book", "Cat", "Dog", "Earth"]
    },
    {
        "id": 1, "name": "MEDICAL", "filename": "data_med.json",
        "url": "https://raw.githubusercontent.com/glutanimate/wordlist-medicalterms-en/master/wordlist.txt",
        "fallback": ["Anemia", "Bronchitis", "Cardiology"]
    },
    {
        "id": 2, "name": "BIOLOGY", "filename": "data_bio.json",
        "url": "https://raw.githubusercontent.com/imsky/wordlists/master/nouns/animals.txt", 
        "fallback": ["Aardvark", "Bear", "Cat"]
    },
    {
        "id": 3, "name": "CHEMICAL", "filename": "data_chem.json",
        "url": "https://raw.githubusercontent.com/bowser1704/periodic-table-json/master/PeriodicTableJSON.json", 
        "type_override": "dummy", 
        "fallback": ["Hydrogen", "Helium", "Lithium"]
    }
]

def download_list(url):
    print(f"   Downloading source...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return [line.strip() for line in content.splitlines() if line.strip()]
    except Exception:
        return []

def main():
    print("--- Deca-Search Split Generator v3 ---")

    for sector in SECTORS:
        sec_id = sector["id"]
        fname = sector["filename"]
        base_index = sec_id * OFFSET_UNIT
        
        print(f"\nProcessing [{sector['name']}] -> {fname}")

        # 1. データ取得
        words = []
        if "type_override" not in sector:
            words = download_list(sector["url"])
        
        if not words:
            print("   -> Using fallback data.")
            base_words = sector["fallback"]
            # データ量を確保するため増殖させる
            for i in range(10000): 
                w = base_words[i % len(base_words)]
                words.append(f"{w}-{i}")
        
        print(f"   -> Generated {len(words)} records.")

        # 2. JSON構築 (このセクター分だけ)
        dataset = {"items": {}}
        for i, word in enumerate(words):
            word = word.capitalize()
            current_id = base_index + i
            
            ja_text = "データ"
            if sec_id == 0: ja_text = "一般用語"
            elif sec_id == 1: ja_text = "医学用語"
            elif sec_id == 2: ja_text = "生物種"
            elif sec_id == 3: ja_text = "化学物質"

            dataset["items"][str(current_id)] = {
                "en": word,
                "fi": f"({sector['name'][:3]}) {word}",
                "ja": f"{word} ({ja_text})",
                "sector": sector["name"]
            }

        # 3. 個別ファイル書き出し
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False)
        print(f"   -> Saved to {fname}")

    print("\nDone! Upload all 4 json files to GitLab.")

if __name__ == "__main__":
    main()
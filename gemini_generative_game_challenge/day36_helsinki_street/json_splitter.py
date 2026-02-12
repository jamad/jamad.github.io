import json

def split_streets():
    with open('streets.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = []
    geometry = {}

    for item in data:
        # メタデータ（軽い情報）
        metadata.append({
            "id": item["id"],
            "fi": item["fi"],
            "en": item["en"],
            "ja": item["ja"],
            "desc": item.get("desc", "")
        })
        # ジオメトリ（重い座標情報）
        geometry[item["id"]] = item["path"]

    # 分けて保存
    with open('streets_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    with open('streets_geometry.json', 'w', encoding='utf-8') as f:
        json.dump(geometry, f, ensure_ascii=False, indent=None) # 容量削減のため改行なし

    print(f"分割完了！")
    print(f"- streets_metadata.json (名前のみ)")
    print(f"- streets_geometry.json (座標のみ)")

if __name__ == "__main__":
    split_streets()
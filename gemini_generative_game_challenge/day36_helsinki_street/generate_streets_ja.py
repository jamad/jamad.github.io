import requests
import json
import time
from deep_translator import GoogleTranslator

def fetch_and_translate_streets():
    # 1. 翻訳機の準備 (フィンランド語 -> 日本語)
    translator = GoogleTranslator(source='fi', target='ja')

    # 2. Overpass API クエリ (ヘルシンキとエスポーの主要道路)
    query = """
    [out:json][timeout:90];
    (
      area["name"="Helsinki"]->.a;
      area["name"="Espoo"]->.b;
    );
    (
      way["highway"~"^(primary|secondary|tertiary)$"]["name"](area.a);
      way["highway"~"^(primary|secondary|tertiary)$"]["name"](area.b);
    );
    out geom;
    """

    print("Overpass APIから道路データを取得中...")
    url = "https://overpass-api.de/api/interpreter"
    try:
        response = requests.get(url, params={'data': query})
        response.raise_for_status()
        elements = response.json().get('elements', [])
    except Exception as e:
        print(f"API取得エラー: {e}")
        return

    # 3. 名前ごとにグループ化（同じ名前のセグメントをまとめる）
    grouped = {}
    for el in elements:
        name_fi = el['tags'].get('name')
        if not name_fi: continue
        
        geom = [[pt['lat'], pt['lon']] for pt in el['geometry']]
        
        if name_fi not in grouped:
            grouped[name_fi] = {
                "fi": name_fi,
                "sv": el['tags'].get('name:sv', ''),
                "paths": []
            }
        grouped[name_fi]["paths"].append(geom)

    print(f"合計 {len(grouped)} 件のユニークな通りが見つかりました。")
    print("日本語への翻訳を開始します（時間がかかります）...")

    # 4. 翻訳とデータ整形
    final_list = []
    unique_id = 1
    count = 0
    total = len(grouped)

    for name_fi, data in grouped.items():
        count += 1
        try:
            # 翻訳実行
            # ※ Mikonkatu -> ミコンカトゥ のようにカタカナ転写を目指しますが
            # Google翻訳なので「ミコン通り」のような意訳になる場合もあります
            name_ja = translator.translate(name_fi)
            
            # 英語名もついでに生成（フィンランド語のままでも良いですが翻訳を通すと Alexander Street 等になります）
            # ここではシンプルにフィンランド語名のままか、英語への翻訳を入れることも可能です
            name_en = name_fi 

            street_obj = {
                "id": unique_id,
                "fi": name_fi,
                "en": name_en,
                "ja": name_ja,
                "desc": f"フィンランド名: {name_fi} / スウェーデン名: {data['sv']}",
                "path": data["paths"]
            }
            final_list.append(street_obj)
            unique_id += 1

            if count % 10 == 0:
                print(f"進捗: {count}/{total} - {name_fi} -> {name_ja}")
                # サーバーに負荷をかけないよう少し待機
                time.sleep(0.5)

        except Exception as e:
            print(f"翻訳エラー ({name_fi}): {e}")
            # エラー時はそのままの名前を入れる
            data["ja"] = name_fi
            time.sleep(2) # エラー時は長めに待機

    # 5. 保存
    with open("streets.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"\n完了！ 'streets.json' に {len(final_list)} 件のデータを保存しました。")

if __name__ == "__main__":
    fetch_and_translate_streets()
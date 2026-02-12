import requests
import json
import time
from deep_translator import GoogleTranslator

def fetch_osm_data(area_id):
    """指定したエリアIDから道路データを取得する"""
    query = f"""
    [out:json][timeout:180];
    area({area_id})->.searchArea;
    (
      way["highway"~"^(primary|secondary|tertiary)$"]["name"](area.searchArea);
    );
    out geom;
    """
    url = "https://overpass-api.de/api/interpreter"
    print(f"エリア {area_id} のデータを取得中...")
    
    try:
        response = requests.get(url, params={'data': query})
        if response.status_code == 200:
            return response.json().get('elements', [])
        else:
            print(f"エラー: APIがステータスコード {response.status_code} を返しました。")
            return []
    except Exception as e:
        print(f"通信エラー: {e}")
        return []

def main():
    # エリアIDの設定 (3600000000 + OSM Relation ID)
    # Helsinki: 34914 -> 3600034914
    # Espoo: 34913 -> 3600034913
    areas = [3600034914, 3600034913]
    
    all_elements = []
    for aid in areas:
        elements = fetch_osm_data(aid)
        all_elements.extend(elements)
        print(f"エリア {aid} から {len(elements)} 件取得しました。")
        time.sleep(2) # 連続リクエストを避けるための休憩

    if not all_elements:
        print("データが取得できませんでした。終了します。")
        return

    # 名前ごとにグループ化
    grouped = {}
    for el in all_elements:
        tags = el.get('tags', {})
        name_fi = tags.get('name')
        if not name_fi: continue
        
        geom = [[pt['lat'], pt['lon']] for pt in el.get('geometry', [])]
        if not geom: continue
        
        if name_fi not in grouped:
            grouped[name_fi] = {
                "fi": name_fi,
                "sv": tags.get('name:sv', ''),
                "paths": []
            }
        grouped[name_fi]["paths"].append(geom)

    print(f"合計 {len(grouped)} 件のユニークな通りを処理します。")

    # 翻訳の準備
    translator = GoogleTranslator(source='fi', target='ja')
    final_list = []
    unique_id = 1
    
    # 翻訳には時間がかかるため、上位300件程度に制限してテストするのもアリです
    # 全件やる場合はそのまま実行してください
    count = 0
    total = len(grouped)

    for name_fi, data in grouped.items():
        count += 1
        try:
            # 翻訳実行
            name_ja = translator.translate(name_fi)
            
            street_obj = {
                "id": unique_id,
                "fi": name_fi,
                "en": name_fi,
                "ja": name_ja,
                "desc": f"フィンランド語: {name_fi} / スウェーデン語: {data['sv']}",
                "path": data["paths"]
            }
            final_list.append(street_obj)
            unique_id += 1

            if count % 10 == 0:
                print(f"進捗: {count}/{total} - {name_fi} -> {name_ja}")
                time.sleep(0.3) # 翻訳APIへの負荷軽減

        except Exception as e:
            print(f"翻訳エラー ({name_fi}): {e}")
            time.sleep(2)

    # 保存
    with open("streets.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"\n完了！ 'streets.json' に {len(final_list)} 件のデータを保存しました。")

if __name__ == "__main__":
    main()
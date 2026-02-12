import requests
import json
import time
from deep_translator import GoogleTranslator

def fetch_osm_with_fallback(bbox):
    """
    複数のOverpassサーバーを試行し、バウンディングボックスでデータを取得する
    bbox: (min_lat, min_lon, max_lat, max_lon)
    """
    # 接続先サーバーのリスト
    endpoints = [
        "https://lz4.overpass-api.de/api/interpreter",
        "https://z.overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass-api.de/api/interpreter"
    ]
    
    # 検索条件：主要道路(primary)と二次道路(secondary)に絞る（軽量化のため）
    # tertiary（三次道路）まで含めたい場合は "^(primary|secondary|tertiary)$" に戻してください
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"^(primary|secondary|tertiary)$"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out geom;
    """

    for url in endpoints:
        print(f"サーバー {url} に接続を試みています...")
        try:
            response = requests.get(url, params={'data': query}, timeout=90)
            if response.status_code == 200:
                print("データの取得に成功しました！")
                return response.json().get('elements', [])
            else:
                print(f"サーバー {url} がエラー {response.status_code} を返しました。次を試します。")
        except Exception as e:
            print(f"サーバー {url} でエラーが発生しました: {e}")
        
        time.sleep(1) # 少し待ってから次のサーバーへ
    
    return []

def main():
    # ヘルシンキとエスポーをカバーするバウンディングボックス
    # (南緯, 西経, 北緯, 東経)
    # これにより広大なエリア計算を避けます
    helsinki_espoo_bbox = (60.10, 24.60, 60.30, 25.15)
    
    elements = fetch_osm_with_fallback(helsinki_espoo_bbox)
    
    if not elements:
        print("全てのサーバーからデータを取得できませんでした。時間をおいて再試行してください。")
        return

    # 名前ごとにグループ化
    grouped = {}
    for el in elements:
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

    print(f"合計 {len(grouped)} 件のユニークな通りが見つかりました。")

    # 日本語翻訳の実行
    translator = GoogleTranslator(source='fi', target='ja')
    final_list = []
    unique_id = 1
    
    count = 0
    total = len(grouped)

    print("日本語へ翻訳中...")
    for name_fi, data in grouped.items():
        count += 1
        try:
            name_ja = translator.translate(name_fi)
            
            street_obj = {
                "id": unique_id,
                "fi": name_fi,
                "en": name_fi,
                "ja": name_ja,
                "desc": f"🇫🇮 {name_fi} / 🇸🇪 {data['sv']}",
                "path": data["paths"]
            }
            final_list.append(street_obj)
            unique_id += 1

            if count % 20 == 0:
                print(f"進捗: {count}/{total} - {name_fi} -> {name_ja}")
                time.sleep(0.3)

        except Exception as e:
            print(f"翻訳エラー: {e}")
            time.sleep(1)

    with open("streets.json", "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"\n完了！ 'streets.json' が正常に作成されました。({len(final_list)}件)")

if __name__ == "__main__":
    main()
import requests
import json
import time

def fetch_streets():
    # 1. Overpass QL クエリ
    # ヘルシンキ(Helsinki)とエスポー(Espoo)の
    # primary, secondary, tertiary (主要道路) を取得
    # ※住宅街も含めたい場合は "residential" を追加しますが、データ量が激増します
    query = """
    [out:json][timeout:60];
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

    print("Overpass APIからデータを取得中... (数秒〜数十秒かかります)")
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    
    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        return []

    data = response.json()
    elements = data.get('elements', [])
    print(f"取得したセグメント数: {len(elements)}")

    # 2. データの加工（名前ごとのグループ化）
    # OSMでは1つの通りが複数の線に分かれているため、名前で辞書にまとめる
    grouped_streets = {}

    for el in elements:
        tags = el.get('tags', {})
        name_fi = tags.get('name')  # フィンランド語名
        name_sv = tags.get('name:sv', '') # スウェーデン語名（あれば）
        
        if not name_fi:
            continue

        # 形状データの変換
        # Leaflet用に [lat, lon] の配列にする
        geometry = [[pt['lat'], pt['lon']] for pt in el['geometry']]

        if name_fi not in grouped_streets:
            grouped_streets[name_fi] = {
                "fi": name_fi,
                "sv": name_sv,
                "paths": [] # 複数のセグメントを格納するリスト
            }
        
        grouped_streets[name_fi]["paths"].append(geometry)

    # 3. アプリ用フォーマットへの変換
    final_list = []
    unique_id = 1

    print("データを整形中...")
    for name, data in grouped_streets.items():
        # 日本語と英語は自動では取れないため、プレースホルダーを入れる
        # Descriptionにはスウェーデン語名を入れておく
        
        street_obj = {
            "id": unique_id,
            "fi": data["fi"],
            "en": data["fi"], # 英語名がなければ一旦フィンランド語と同じに
            "ja": "（翻訳待ち）", # 後で手動または翻訳APIで埋める
            "desc": f"スウェーデン語名: {data['sv']}" if data['sv'] else "ヘルシンキ/エスポーの通り",
            "path": data["paths"] # Leafletは配列の配列（MultiPolyline）も描画可能
        }
        final_list.append(street_obj)
        unique_id += 1

    # 名前順にソート
    final_list.sort(key=lambda x: x['fi'])

    return final_list

if __name__ == "__main__":
    streets = fetch_streets()
    
    if streets:
        filename = "streets_all.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(streets, f, ensure_ascii=False, indent=2)
        print(f"\n完了！ {len(streets)} 件の通りデータを '{filename}' に保存しました。")
        print("注意: アプリ側で path の読み込み処理を少し修正する必要があります（MultiPolyline対応）")
    else:
        print("データが見つかりませんでした。")
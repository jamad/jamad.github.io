title = "TITLE TO DISPLAY";// ブラウザのタブにも表示されるし、初期画面にも表示される

description = `DESCRIPTIN\nTO DISPLAY`;// 初期画面に表示される　改行可能

characters = [];// 現時点では何に使うか不明

options = {};// 現時点では何に使うか不明

/** @type {Vector[]} */ //必須でないが、このsyntaxで型宣言すると、デバッグ等に役立つらしい
let box_list;

/** @type {{angle: number, length: number, pivot:Vector}}*/
let player_cord;

const scroll_y = 0.1234;
const boxsize = 2.0;
const cord_default_length = 5;
const line_thickness = 1.2;

function update() { //1 秒に 60 回呼び出される
    if (!ticks) { //開始フレームのみ実行という意味　つまり初期化処理 
        box_list = [vec(50, 5)]; // x=50, y=5　の2Dベクトルを１つ保持
        nextPinDist = -10; // 次のbox生成トリガーに利用　画面に表示されそうになった時点で次の新規生成を行う

        player_cord = { angle: 0, length: cord_default_length, pivot: box_list[0] }// プレイヤーのデータ構造

    }

    if (input.isPressed) {//input 変数には、マウスやタッチパネル、キーボードからの入力状態が格納
        player_cord.length += 1.5;//入力で長さが１伸びる
    } else {
        player_cord.length -= (player_cord.length - cord_default_length) * 0.5; //入力無ければ増分の半分だけ短くなるように
    }

    player_cord.angle += 0.05;//自動回転
    let edge0 = player_cord.pivot;//回転軸側の端点
    let edge1 = vec(edge0).addWithAngle(player_cord.angle, player_cord.length);// edge0自身が変更されてしまわないようにvec(edge0)によってVectorのコピーを作成している
    line(edge0, edge1, line_thickness);// playerのlineを描画　細くできた。着色は可能？あとラインが鎖線にならないようにできる？


    //box_list.forEach((pos) => {
    remove(box_list, (pos) => {//これはライブラリの独自メソッドっぽい？
        pos.y += scroll_y; // 画面下方向にｙが増加するため。　右下座標が(99,99)
        box(pos, boxsize);// box の描画
        return 100 + boxsize < pos.y // 条件にマッチした要素は自動的に box_list からremove される
    });

    nextPinDist += scroll_y; //他のbox同様にスクロールさせる 

    while (-boxsize * 2 < nextPinDist) { //boxが画面に表示されそうになったので実体化
        let pos_x = rnd(10, 90);// ｘ座標はランダムな値 range(10,90)　画面がrange(0,100)なので。
        let pos_y = nextPinDist; // 条件から、必ず画面外に新規boxは描画されるはず
        box_list.push(vec(pos_x, pos_y));// box_list にドットを追加

        nextPinDist = rnd(-10, -20);// 次の生成距離ｙをランダムに決定しつつ更新
    }

}


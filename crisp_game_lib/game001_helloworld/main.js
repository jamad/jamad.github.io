title = "TITLE TO DISPLAY";// ブラウザのタブにも表示されるし、初期画面にも表示される

description = `DESCRIPTIN\nTO DISPLAY`;// 初期画面に表示される　改行可能

characters = [];// 現時点では何に使うか不明

options = {};// 現時点では何に使うか不明

/** @type {Vector[]} */ //必須でないが、このsyntaxで型宣言すると、デバッグ等に役立つ

let box_list;
let scroll_y = 1.234;
let boxsize = 2.0;

function update() { //1 秒に 60 回呼び出される
    if (!ticks) { //開始フレームのみ実行という意味　つまり初期化処理 
        box_list = [vec(50, -5)]; // x=50, y=-5　の2Dベクトルを１つ保持
        nextPinDist = -5; // 次のbox生成トリガーに利用　画面に表示されそうになった時点で次の新規生成を行う
    }

    box_list.forEach((pos) => {
        pos.y += scroll_y; // 画面下方向にｙが増加するため。　右下座標が(99,99)
        box(pos, boxsize);// box の描画
    });

    nextPinDist += scroll_y; //他のbox同様にスクロールさせる 

    while (-boxsize * 2 < nextPinDist) { //boxが画面に表示されそうになったので実体化
        let pos_x = rnd(10, 90);// ｘ座標はランダムな値 range(10,90)　画面がrange(0,100)なので。
        let pos_y = nextPinDist; // 条件から、必ず画面外に新規boxは描画されるはず
        box_list.push(vec(pos_x, pos_y));// box_list にドットを追加

        nextPinDist = -rnd(5, 15);// 次の生成距離ｙをランダムに決定しつつ更新
    }

}


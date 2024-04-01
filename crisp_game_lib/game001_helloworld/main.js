title = "TITLE TO DISPLAY";// ブラウザのタブにも表示されるし、初期画面にも表示される

description = `DESCRIPTIN\nTO DISPLAY`;// 初期画面に表示される　改行可能

characters = [];// 現時点では何に使うか不明

options = {};// 現時点では何に使うか不明

/** @type {Vector[]} */ //必須でないが、このsyntaxで型宣言すると、デバッグ等に役立つ

let pins;
let scroll_y = 0.1234;
let boxsize = 2.0;

function update() { //1 秒に 60 回呼び出される
    if (!ticks) { //開始フレームのみ実行という意味　つまり初期化処理 
        pins = [vec(50, 5)]; // x=50, y=5
        nextPinDist = 5; // 次に生成するboxのトリガーに利用する変数　負になったら新規生成
    }

    pins.forEach((pos) => {
        pos.y += scroll_y; // 画面下方向にｙが増加する　右下座標が(99,99)
        box(pos, boxsize);// draw box objects
    });

    nextPinDist -= scroll_y;

    while (nextPinDist < 0) { //負になったのでboxを新規生成
        let pos_x = rnd(10, 90);// random value range(10,90)
        let pos_y = nextPinDist - boxsize; // 必ず画面外に新規boxは描画されるはず

        pins.push(vec(pos_x, pos_y));

        nextPinDist += rnd(5, 15);
    }

}


title = "表示されるタイトル";

description = `表示されるデスクリプション`;

characters = [];

options = {};

/** @type {Vector[]} */
let pins;

function update() { //1 秒に 60 回呼び出される
    if (!ticks) { //開始フレームのみ実行という意味　つまり初期化処理 
        pins = [vec(50, 5)];
        nextPinDist = 5;
    }
    let scr = 0.02;
    pins.forEach((p) => {
        p.y += scr;
        box(p, 3);
    });
    nextPinDist -= scr;
    while (nextPinDist < 0) {
        pins.push(vec(rnd(10, 90), -2 - nextPinDist));
        nextPinDist += rnd(5, 15);
    }
}
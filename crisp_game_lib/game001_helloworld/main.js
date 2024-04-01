title = "TITLE TO DISPLAY";// ブラウザのタブにも表示されるし、初期画面にも表示される

description = `DESCRIPTIN\nTO DISPLAY`;// 初期画面に表示される　改行可能

characters = [];// 現時点では何に使うか不明

options = {};// 現時点では何に使うか不明

/** @type {Vector[]} */
let pins;

function update() { //1 秒に 60 回呼び出される
    if (!ticks) { //開始フレームのみ実行という意味　つまり初期化処理 
        pins = [vec(50, 5)]; // x=50, y=5
        nextPinDist = 5; // 現時点では何に使うか不明
    }

    let scroll_y = 1.234;
    let boxsize = 1.5;
    pins.forEach((pos) => {
        pos.y += scroll_y;
        box(pos, boxsize);// draw box objects
    });

    nextPinDist -= scroll_y;
    while (nextPinDist < 0) {
        pins.push(vec(rnd(10, 90), -2 - nextPinDist));
        nextPinDist += rnd(5, 15);
    }
}


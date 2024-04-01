title = "表示されるタイトル";

description = `表示されるデスクリプション`;

characters = [];

options = {};

/** @type {Vector[]} */
let pins;

function update() {
    if (!ticks) {
        pins = [vec(50, 5)];
    }
    pins.forEach((p) => {
        box(p, 3);
    });
}

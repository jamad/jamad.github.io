title = "ABC";

description = `
THIS IS
MULTI LINE
MULTI LINE
MULTI LINE
MULTI LINE
MULTI LINE
`;

characters = [];

options = {
    viewSize: { x: 512, y: 256 },
    theme: "pixel",
    isPlayingBgm: true,
    isReplayEnabled: true,
    seed: 3000,
};


/** @type {Vector[]} */
let player = vec(256, 128);

let length = 32;

function update() {
    if (!ticks) {
        // init
        angle = 0.0;
        direction = 1.0;
        angle_speed = 0.01;
    }

    box(player, 5);

    if (input.isJustPressed) {
        direction *= -1;
        angle_speed = 0.01;
    }

    angle_speed *= 1.001;
    angle += angle_speed * direction;


    let dest = vec(player).addWithAngle(angle, length);
    line(player, dest, 1);
}
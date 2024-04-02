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

// https://github.com/JunoNgx/crisp-game-lib-tutorial?tab=readme-ov-file#step-013-container-variable-and-jsdoc

/**
* @typedef {{
* pos: Vector,
* speed: number
* }} Star
*/

/**
* @type  { Star [] }
*/
let stars;
<link rel="stylesheet" type="text/css" href="../assets/css/styles.css" />

* testbed : https://codepen.io/jamad/pen/ZEPQrrQ


<br>
<canvas></canvas>
<style>
body{  background: #222a33;}
</style>

<script>
const CELL_SIZE = 12;
const DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 40*CELL_SIZE;
canvas.height = 60*CELL_SIZE;
ctx.lineWidth = 8;
ctx.fillStyle = '#499';
ctx.strokeStyle = '#000';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.beginPath();
ctx.moveTo(CELL_SIZE, CELL_SIZE); // Set initial position to (0, 0)
const map = Array.from({ length: canvas.height / CELL_SIZE-1 }, () => Array.from({ length: canvas.width / CELL_SIZE-1}, () => false));
map[0][0] = true; // Initial visited pos (1, 1)
const route = [[0,0]]; // Initial route starting at (1, 1)
const getCurrentPos = () => route[route.length-1];// last element is the current pos
const loop = () => {
  const [x, y] = getCurrentPos();
  const ops = DIRECTIONS.filter(([u, v]) => (map[y + v]?.[x + u] === false && map[y + v] !== undefined));
  if (ops.length) {
    const [DX, DY] = ops[Math.random() * ops.length | 0]; // Random choice
    const newX = DX + x;
    const newY = DY + y;
    route.push([newX, newY]); // Stack new position
    ctx.lineTo(newX * CELL_SIZE + CELL_SIZE, newY * CELL_SIZE + CELL_SIZE); // Create line to new pos
    map[newY][newX] = true; // Mark visited cell
  } else {
    route.pop(); // Go 1 step back
    if (route.length < 1) return; // Finish if route is empty
    const [prevX, prevY] = getCurrentPos();
    ctx.moveTo(prevX * CELL_SIZE + CELL_SIZE, prevY * CELL_SIZE + CELL_SIZE); // Go back
  }
  ctx.stroke(); // Draw line
  requestAnimationFrame(loop); // Use requestAnimationFrame for recursion
};
loop();
console.log('done');
</script>

const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

let width = window.innerWidth;
let height = window.innerHeight;
canvas.width = width;
canvas.height = height;

const spacing = 30;
const squares = [];

for (let y = 0; y < height; y += spacing) {
  for (let x = 0; x < width; x += spacing) {
    squares.push({ x, y, phase: Math.random() * 2 * Math.PI });
  }
}

let time = 0;

function draw() {
  ctx.clearRect(0, 0, width, height);
  time += 0.05;

  for (const square of squares) {
    const pulse = (Math.sin(time + square.phase) + 1) / 2; // 0 to 1

    const r = Math.floor(255 * pulse);
    const g = 0;
    const b = Math.floor(255 * (1 - pulse));
    ctx.fillStyle = `rgb(${r},${g},${b})`;

    ctx.fillRect(square.x, square.y, 5, 5);
  }

  requestAnimationFrame(draw);
}

window.addEventListener("resize", () => {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
  squares.length = 0;
  for (let y = 0; y < height; y += spacing) {
    for (let x = 0; x < width; x += spacing) {
      squares.push({ x, y, phase: Math.random() * 2 * Math.PI });
    }
  }
});

draw();

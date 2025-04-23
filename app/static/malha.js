// Obtém o elemento canvas da página
const canvas = document.getElementById("bg");
// Obtém o contexto 2D para desenhar no canvas
const ctx = canvas.getContext("2d");

// Define a largura e altura do canvas com base no tamanho da janela
let width = window.innerWidth;
let height = window.innerHeight;
canvas.width = width;
canvas.height = height;

// Define o espaçamento entre os quadrados na malha
const spacing = 30;
// Armazena todos os quadrados da malha
const squares = [];

// Preenche a tela com quadrados distribuídos em grade
for (let y = 0; y < height; y += spacing) {
  for (let x = 0; x < width; x += spacing) {
    // Cada quadrado tem uma fase aleatória para criar variações no brilho
    squares.push({ x, y, phase: Math.random() * 2 * Math.PI });
  }
}

// Variável usada para controlar o tempo no efeito de animação
let time = 0;

// Função que desenha os quadrados animados no canvas
function draw() {
  // Limpa a tela a cada frame
  ctx.clearRect(0, 0, width, height);

  // Avança o tempo para movimentar a animação
  time += 0.05;

  // Para cada quadrado, calcula um brilho pulsante com base no tempo
  for (const square of squares) {
    // Calcula um valor entre 0 e 1 usando seno com fase
    const pulse = (Math.sin(time + square.phase) + 1) / 2;

    // Define a cor RGB baseada no pulso (efeito azul/roxo)
    const r = Math.floor(255 * pulse);
    const g = 0;
    const b = Math.floor(255 * (1 - pulse));
    ctx.fillStyle = `rgb(${r},${g},${b})`;

    // Desenha o quadrado com 5x5 pixels
    ctx.fillRect(square.x, square.y, 5, 5);
  }

  // Solicita o próximo frame para continuar a animação
  requestAnimationFrame(draw);
}

// Evento para redimensionar o canvas dinamicamente com a janela
window.addEventListener("resize", () => {
  // Atualiza tamanho do canvas
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;

  // Limpa o array de quadrados e o repopula
  squares.length = 0;
  for (let y = 0; y < height; y += spacing) {
    for (let x = 0; x < width; x += spacing) {
      squares.push({ x, y, phase: Math.random() * 2 * Math.PI });
    }
  }
});

// Inicia a animação
draw();

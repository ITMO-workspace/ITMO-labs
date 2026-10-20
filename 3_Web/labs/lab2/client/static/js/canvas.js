const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = 600;
canvas.height = 600;

const width = canvas.width;
const height = canvas.height;
const centerX = width / 2;
const centerY = height / 2;
const padding = 60;
const maxR = (Math.min(width, height) - 2 * padding) / 2;
const R = maxR * 0.85;

ctx.clearRect(0, 0, width, height);

ctx.strokeStyle = '#eee';
ctx.lineWidth = 1;

for (let i = -5; i <= 5; i++) {
    const x = centerX + i * (R / 3);
    if (x > 0 && x < width) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
    }
    const y = centerY - i * (R / 3);
    if (y > 0 && y < height) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }
}

ctx.fillStyle = 'rgba(49, 152, 254, 0.75)';
ctx.strokeStyle = '#4A90D9';
ctx.lineWidth = 2;

ctx.fillRect(centerX, centerY, R, R/2);
ctx.strokeRect(centerX, centerY, R, R/2);

ctx.beginPath();
ctx.moveTo(centerX, centerY);
ctx.arc(centerX, centerY, R, 0, -Math.PI/2, true);
ctx.closePath();
ctx.fill();
ctx.stroke();

ctx.beginPath();
ctx.moveTo(centerX, centerY);
ctx.lineTo(centerX - R/2, centerY);
ctx.lineTo(centerX, centerY - R/2);
ctx.closePath();
ctx.fill();
ctx.stroke();

ctx.strokeStyle = 'white';
ctx.lineWidth = 2;

ctx.beginPath();
ctx.moveTo(0, centerY);
ctx.lineTo(width, centerY);
ctx.stroke();

ctx.beginPath();
ctx.moveTo(centerX, 0);
ctx.lineTo(centerX, height);
ctx.stroke();

ctx.fillStyle = 'white';

ctx.beginPath();
ctx.moveTo(width - 10, centerY - 5);
ctx.lineTo(width, centerY);
ctx.lineTo(width - 10, centerY + 5);
ctx.fill();

ctx.beginPath();
ctx.moveTo(centerX - 5, 10);
ctx.lineTo(centerX, 0);
ctx.lineTo(centerX + 5, 10);
ctx.fill();

ctx.font = "26px monospace";
ctx.fillStyle = 'white';
ctx.textAlign = 'center';
ctx.textBaseline = 'top';

ctx.fillText('X', width - 20, centerY + 10);
ctx.fillText('Y', centerX + 10, 5);

const labels = [
    { v: -R, l: '-R' },
    { v: -R/2, l: '-R/2' },
    { v: R/2, l: 'R/2' },
    { v: R, l: 'R' }
];

labels.forEach(item => {
    const x = centerX + item.v;
    if (x > 0 && x < width) {
        ctx.textBaseline = 'top';
        ctx.fillStyle = 'white';
        ctx.fillText(item.l, x, centerY + 6);
        ctx.strokeStyle = 'white';
        ctx.beginPath();
        ctx.moveTo(x, centerY - 4);
        ctx.lineTo(x, centerY + 4);
        ctx.stroke();
    }
    const y = centerY - item.v;
    if (y > 0 && y < height) {
        ctx.textBaseline = 'middle';
        ctx.textAlign = 'right';
        ctx.fillStyle = 'white';
        ctx.fillText(item.l, centerX - 8, y);
        ctx.strokeStyle = 'white';
        ctx.beginPath();
        ctx.moveTo(centerX - 4, y);
        ctx.lineTo(centerX + 4, y);
        ctx.stroke();
    }
});

ctx.textBaseline = 'top';
ctx.fillStyle = 'white';
ctx.textAlign = 'center';
ctx.fillText('0', centerX, centerY + 6);
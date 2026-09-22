import { Point2D } from './cartesian/Point2D.js';
import { saveResult } from './resultTable.js';

let currentPoint = new Point2D({x: 0, y: 0, r: 0}, isPointInArea);

export function bindEventListeners() {
    document.getElementById("main-form").addEventListener("submit", function(e)  {
        e.preventDefault();
        if (!currentPoint.validate()) {
            showError("некорректные данные");
            return;
        };
        saveResult(currentPoint);
    })

    document.querySelectorAll('input[name="xInput"]').forEach(input => {
        input.addEventListener("change", function (ev) {
            currentPoint.x = ev.target.value;
        });
    });

    document.querySelectorAll('input[name="R-input"]').forEach(input => {
        input.addEventListener("click", function (ev) {
            document.getElementById("R-value-display").textContent = ev.target.value;
            currentPoint.r = ev.target.value;
        });
    });

    document.getElementById('Y-input').addEventListener("input", function() {
        currentPoint.y = this.value.replace(",", ".")
    })
}



function isPointInArea(x, y, R) {
    const halfR = R / 2;
    
    if ((0 <= x && x <= R) && (-halfR <= y && y <= 0)) {
        return true;
    }

    if ((0 <= x && x <= R) && (0 <= y && y <= R) && (x * x + y * y <= R * R)) {
        return true;
    }

    if ((-halfR <= x && x <= 0) && (0 <= y && y <= halfR) && (y <= x + halfR)) {
        return true;
    }

    return false;
}
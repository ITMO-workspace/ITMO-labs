const table = document.getElementById("result-table");

export function saveResult(data) {
    const newRow = table.insertRow(-1);

    const rowX = newRow.insertCell(0);
    const rowY = newRow.insertCell(1);
    const rowR = newRow.insertCell(2);
    const rowTime = newRow.insertCell(3);
    const rowResult = newRow.insertCell(4);
    const rowScriptTime = newRow.insertCell(5);

    const prevResults = JSON.parse(localStorage.getItem("results") || "[]");
    
    data.clientTime = new Date().toISOString();
    
    const updatedResults = [...prevResults, data];
    localStorage.setItem("results", JSON.stringify(updatedResults));

    rowX.innerText = data.x.toString();
    rowY.innerText = data.y.toString();
    rowR.innerText = data.r.toString();
    
    rowTime.innerText = new Date(data.clientTime).toLocaleString('ru-RU');
    rowResult.innerText = data.inside ? 'Внутри' : 'Снаружи';
    rowScriptTime.innerText = data.scriptTime + " ms";

    const warningBlock = document.querySelector(".warning");
    if (warningBlock) {
        warningBlock.classList.remove("show");
    }
}

export function loadResults() {
    const saved = localStorage.getItem("results");
    if (!saved) return;
    
    const results = JSON.parse(saved);
    
    while(table.rows.length > 1) {
        table.deleteRow(1);
    }
    
    results.forEach(item => {
        if (item.x === undefined) return;

        const newRow = table.insertRow(-1);
        
        newRow.insertCell(0).innerText = item.x.toString();
        newRow.insertCell(1).innerText = item.y.toString();
        newRow.insertCell(2).innerText = item.r.toString();
        newRow.insertCell(3).innerText = new Date(item.clientTime).toLocaleString('ru-RU');
        newRow.insertCell(4).innerText = item.inside ? 'Попадание' : 'Промах';
        newRow.insertCell(5).innerText = item.scriptTime ? item.scriptTime + " ms" : "—";
    });
}
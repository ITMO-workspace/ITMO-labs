const $table = $("#result-table");

export function saveResult(data) {
    const $newRow = $("<tr>");

    const localTime = new Date().toLocaleString('ru-RU');

    $("<td>").text(data.x).appendTo($newRow);
    $("<td>").text(data.y).appendTo($newRow);
    $("<td>").text(data.r).appendTo($newRow);
    $("<td>").text(localTime).appendTo($newRow);
    $("<td>").text(data.inside ? 'Попадание' : 'Промах').appendTo($newRow);
    $("<td>").text(data.serverTime || "—").appendTo($newRow);
    $("<td>").text(data.scriptTime ? data.scriptTime + " ms" : "—").appendTo($newRow);

    $table.find("tbody").append($newRow);

    const prevResults = JSON.parse(localStorage.getItem("results") || "[]");
    data.clientTime = new Date().toISOString();
    
    const updatedResults = [...prevResults, data];
    localStorage.setItem("results", JSON.stringify(updatedResults));

    $(".warning").removeClass("show");
}

export function loadResults() {
    const saved = localStorage.getItem("results");
    if (!saved) return;
    
    const results = JSON.parse(saved);
    
    $table.find("tbody").empty();
    
    results.forEach(item => {
        if (item.x === undefined) return;

        const $newRow = $("<tr>");
        
        $("<td>").text(item.x).appendTo($newRow);
        $("<td>").text(item.y).appendTo($newRow);
        $("<td>").text(item.r).appendTo($newRow);
        $("<td>").text(new Date(item.clientTime).toLocaleString('ru-RU')).appendTo($newRow);
        $("<td>").text(item.inside ? 'Попадание' : 'Промах').appendTo($newRow);
        $("<td>").text(item.serverTime || "—").appendTo($newRow);
        $("<td>").text(item.scriptTime ? item.scriptTime + " ms" : "—").appendTo($newRow);

        $table.find("tbody").append($newRow);
    });
}
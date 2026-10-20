const $warningBlock = $(".warning");
const $warningTitle = $warningBlock.find(".warning-title");
const $warningText = $warningBlock.find(".warning-text");
const $warningCloseBtn = $warningBlock.find(".warning-close");

$warningCloseBtn.on("click", closeWarning);

export function closeWarning() {
    $warningBlock.removeClass("show");
}

export function showInfo(message, title) {
    showWarning("info", title, message);
}

export function showError(message) {
    showWarning("error", "Ошибка при вводе!", message);
}

function showWarning(type, title, message) {
    if (type === "error") {
        $warningTitle.text(title);
        $warningBlock.css("background-color", "var(--red-bg-color)"); 
    } else if (type === "info") {
        $warningTitle.text(title || "Информация");
        $warningBlock.css("background-color", "var(--blue-bg-color)"); 
    } else {
        return;
    }
    
    $warningBlock.addClass("show");
    $warningText.text(message);
}
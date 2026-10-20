const warningBlock = document.querySelector(".warning");
const warningTitle = warningBlock.querySelector(".warning-title");
const warningText = warningBlock.querySelector(".warning-text");
const warningCloseBtn = warningBlock.querySelector(".warning-close");

warningCloseBtn.addEventListener("click", closeWarning)

function closeWarning() {
    warningBlock.classList.remove("show")
}

function showInfo(message, title) {
    showWarning("info", title, message)
}

function showError(message) {
    showWarning("error", "Ошибка при вводе!", message)
}

function showWarning(type, title, message) {
    if (type === "error") {
        warningTitle.textContent = title
        warningBlock.style.backgroundColor = "var(--red-bg-color)"; 
    } else if (type === "info") {
        warningTitle.textContent
        warningBlock.style.backgroundColor = "var(--blue-bg-color)"; 
    } else {
        return;
    }
    warningBlock.classList.add("show");
    warningText.textContent = message
}

import { saveResult } from './storage.js';

export function bindEventListeners() {
    const form = document.getElementById("main-form");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        const x = formData.get('X');
        const y = formData.get('yInput');
        const r = formData.get('rInput');

        if (!x || !y || !r) {
            console.error("Missing values", { x, y, r });
            return;
        }

        try {
            const response = await fetch(`/fcgi-bin/server.jar?x=${x}&y=${y}&r=${r}`);
            const data = await response.json();

            if (!response.ok) {
                console.error("Server error:", data.error);
                showError(data.error);
                return;
            }

            saveResult(data);

        } catch (err) {
            console.error("Network error:", err);
        }
    });
}
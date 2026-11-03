import { saveResult } from './storage.js';
import { showError } from './warning.js';

export function bindEventListeners() {
    const $form = $("#main-form");

    $form.on("submit", (e) => {
        e.preventDefault();
        
        const x = $("input[name='X']").val();
        const y = $("input[name='yInput']:checked").val();
        const r = $("input[name='rInput']:checked").val();

        if (!x || !y || !r) {
            showError("Пожалуйста, заполните все поля (X, Y, R).");
            return;
        }

        $.ajax({
            url: `/fcgi-bin/server.jar`,
            method: "GET",
            dataType: "json",
            data: {x, y, r},
            success: (data) => {
                saveResult(data);
            },
            error: (jqXHR) => {
                const errorData = jqXHR.responseJSON;
                const errorMsg = errorData && errorData.error ? errorData.error : "Ошибка сервера";
                showError(errorMsg);
            }
        });
    });
}
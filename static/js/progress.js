"use strict";

function updateProgress(percent, text) {

    const bar = document.getElementById("progressBar");
    const label = document.getElementById("progressText");

    if (!bar || !label)
        return;

    bar.style.width = percent + "%";

    bar.textContent = percent + "%";

    label.textContent = text;

}
"use strict";

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("myDropzone");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const submitBtn = document.getElementById("submitBtn");
        const loading = document.getElementById("loading");

        submitBtn.disabled = true;
        loading.style.display = "block";

        const formData = new FormData(form);

        const recId = formData.get("uuid");

        startProgressPolling(recId);

        try {

            const response = await fetch("/create", {

                method: "POST",

                body: formData

            });

            const data = await response.json();

            let finished = false;

            while (!finished) {

                const progressResponse = await fetch("/progress/" + recId);

                const progress = await progressResponse.json();

                updateProgress(
                    progress.percent,
                    progress.message
                );

                if (progress.percent >= 100) {

                    finished = true;

                }

                else {

                    await new Promise(resolve => setTimeout(resolve, 300));

                }

            }

            stopProgressPolling();

            window.location.href = data.redirect;

        }

        catch (err) {

            stopProgressPolling();

            console.log(err);

            alert("Reel generation failed.");

            submitBtn.disabled = false;

        }

    });

    let progressInterval = null;

    function startProgressPolling(recId) {

    progressInterval = setInterval(async function () {

        try {

            const response = await fetch("/progress/" + recId);

            const data = await response.json();

            updateProgress(
                data.percent,
                data.message
            );

        }

        catch (err) {

            console.log(err);

        }

    }, 1000);

}

    function stopProgressPolling() {

        clearInterval(progressInterval);

    }

    const ttsRadio = document.getElementById("ttsRadio");
    const uploadRadio = document.getElementById("uploadRadio");
    const ttsSection = document.getElementById("ttsSection");
    const uploadSection = document.getElementById("uploadSection");
    uploadRadio.addEventListener("change", function () {
        ttsSection.style.display = "none";
        uploadSection.style.display = "block";
    });


    ttsRadio.addEventListener("change", function () {
        ttsSection.style.display = "block";
        uploadSection.style.display = "none";
    });
    const manualMusicRadio = document.getElementById("manualMusicRadio");

    const manualMusicSection = document.getElementById("manualMusicSection");

    manualMusicRadio.addEventListener("change", function () {

        manualMusicSection.style.display = "block";

    });

    document.querySelector('input[value="none"]').addEventListener("change", function () {

        manualMusicSection.style.display = "none";

    });

    document.querySelector('input[value="ai"]').addEventListener("change", function () {

        manualMusicSection.style.display = "none";

    });

    const volumeSlider = document.getElementById("musicVolume");

    const volumeValue = document.getElementById("volumeValue");

    volumeSlider.addEventListener("input", function () {

        volumeValue.innerText = this.value + "%";

    });



});

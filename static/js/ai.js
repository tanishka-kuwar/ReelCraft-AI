"use strict";

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("generateAiBtn").addEventListener("click", async function () {

        this.disabled = true;
        this.innerText = "Generating...";

        try {
            const formData = new FormData();

            const inputs = document.querySelectorAll(".file-input");

            let hasImage = false;

            inputs.forEach((input) => {
                if (input.files.length > 0) {
                    hasImage = true;
                }
            });

            if (!hasImage) {
                alert("Please upload at least one image.");
                return;
            }

            inputs.forEach((input) => {

                if (input.files.length > 0) {

                    formData.append("images", input.files[0]);

                }

            });

            const response = await fetch("/generate-script", {

                method: "POST",

                body: formData

            });

            const textBox = document.getElementById("textInput");
            const data = await response.json();
            textBox.value = data.script;
        }

        catch (err) {
            alert("AI generatin failed.")
            console.log(err);
        }
        this.disabled = false;
        this.innerText = "✨ Generate AI Script";

    });

    document.getElementById("generateHashtagsBtn").addEventListener("click", async function () {

        const hashtagsBox = document.getElementById("hashtagsBox");

        this.disabled = true;
        this.innerText = "Generating...";

        try {

            const formData = new FormData();

            const inputs = document.querySelectorAll(".file-input");

            let hasImage = false;

            inputs.forEach((input) => {

                if (input.files.length > 0) {

                    hasImage = true;
                    formData.append("images", input.files[0]);

                }

            });

            if (!hasImage) {

                alert("Please upload at least one image.");

                return;

            }

            const response = await fetch("/generate-hashtags", {

                method: "POST",

                body: formData

            });

            const data = await response.json();

            hashtagsBox.value = data.hashtags;

        }

        catch (err) {

            alert("Hashtag generation failed.");

            console.log(err);

        }

        this.disabled = false;
        this.innerText = "✨ Generate AI Hashtags";

    });


});

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const generateAiBtn = document.getElementById("generateAiBtn");

    generateAiBtn.addEventListener("click", async function () {

        generateAiBtn.classList.add("loading");

        generateAiBtn.innerHTML =
            `<i class="fas fa-spinner fa-spin"></i> Generating...`;
        generateAiBtn.disabled = true;
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
            if (!response.ok) {
                throw new Error("Failed to generate script.");
            }

            if (!response.ok) {
                throw new Error("Failed to generate script.");
            }

            const data = await response.json();
            textBox.value = data.script;
        }
        catch (error) {

            console.error(error);

            alert("Unable to generate AI script. Please try again.");

        }

        finally {
            generateAiBtn.disabled = false;
            generateAiBtn.classList.remove("loading");

            generateAiBtn.innerHTML =
                `<i class="fas fa-wand-magic-sparkles"></i> Generate AI Script`;

        }
    });

    const generateHashtagsBtn =
        document.getElementById("generateHashtagsBtn");

    generateHashtagsBtn.addEventListener("click", async function () {

        generateHashtagsBtn.classList.add("loading");

        generateHashtagsBtn.innerHTML =
            `<i class="fas fa-spinner fa-spin"></i> Generating...`;
        generateHashtagsBtn.disabled = true;
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
        catch (error) {

            console.error(error);

            alert("Unable to generate AI hashtags.");

        }
        finally {
            generateHashtagsBtn.disabled = false;

            generateHashtagsBtn.classList.remove("loading");

            generateHashtagsBtn.innerHTML =
                `<i class="fas fa-hashtag"></i> Generate AI Hashtags`;

        }
    });


});

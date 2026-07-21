"use strict";

document.addEventListener("DOMContentLoaded", function () {

    let fileCounter = 2; // start from 2 since we already have file1

    function addFileInput() {

        const fileInputs = document.getElementById("fileInputs");

        const div = document.createElement("div");

        div.className = "file-input-group";

        div.innerHTML = `
        <input
            name="file${fileCounter}"
            type="file"
            class="file-input"
            accept="image/*,video/*"
            onchange="previewImages()"
        >

        <label>Duration</label>

        <select
            name="duration${fileCounter}"
            class="duration-select">

            <option value="1">1 sec</option>
            <option value="2">2 sec</option>
            <option value="3">3 sec</option>
            <option value="4">4 sec</option>
            <option value="5">5 sec</option>

        </select>

        <button
            type="button"
            class="remove-file-btn"
            onclick="removeFileInput(this)">
        </button>
    `;

        fileInputs.appendChild(div);

        fileCounter++;

    }

    function removeFileInput(button) {
        const fileInputGroup = button.parentElement;
        fileInputGroup.remove();

        previewImages();
    }

    function previewImages() {
        const previewContainer = document.getElementById("imagePreviewContainer")

        previewContainer.innerHTML = "";

        const inputs = document.querySelectorAll(".file-input");

        inputs.forEach(input => {
            if (input.files.length === 0)
                return;
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const file = input.files[0];
                    const durationSelect = input.parentElement.querySelector(".duration-select");

                    if (file.type.startsWith("video/")) {

                        durationSelect.style.pointerEvents = "none";
                        durationSelect.style.opacity = "0.6";
                        durationSelect.options[0].text = "Original";

                    } else {

                        durationSelect.style.pointerEvents = "auto";
                        durationSelect.style.opacity = "1";
                        durationSelect.options[0].text = "1 sec";

                    }

                    if (file.type.startsWith("image/")) {

                        const img = document.createElement("img");

                        img.src = e.target.result;

                        img.style.width = "120px";
                        img.style.height = "120px";
                        img.style.objectFit = "cover";
                        img.style.margin = "10px";

                        previewContainer.appendChild(img);

                    }

                    else if (file.type.startsWith("video/")) {

                        const video = document.createElement("video");

                        video.src = e.target.result;

                        video.controls = true;
                        video.muted = true;

                        video.style.width = "120px";
                        video.style.height = "120px";
                        video.style.objectFit = "cover";
                        video.style.margin = "10px";

                        previewContainer.appendChild(video);

                    }

                }

                reader.readAsDataURL(input.files[0]);
            }
        });
    }

    function processMedia(files) {

        const fileInputs = document.getElementById("fileInputs");

        for (const file of files) {

            if (
                !file.type.startsWith("image/") &&
                !file.type.startsWith("video/")
            )
                continue;

            const dt = new DataTransfer();

            dt.items.add(file);

            const div = document.createElement("div");

            div.className = "file-input-group";

            div.innerHTML = `
            <input
                name="file${fileCounter}"
                type="file"
                class="file-input"
                accept="image/*,video/*"
            >

            <label>Duration</label>

            <select
                name="duration${fileCounter}"
                class="duration-select">

                <option value="1">1 sec</option>
                <option value="2">2 sec</option>
                <option value="3" selected>3 sec</option>
                <option value="4">4 sec</option>
                <option value="5">5 sec</option>

            </select>

            <button
                type="button"
                class="remove-file-btn"
                onclick="removeFileInput(this)">
            </button>
        `;

            fileInputs.appendChild(div);

            const input = div.querySelector(".file-input");

            input.files = dt.files;

            const durationSelect = div.querySelector(".duration-select");

            if (file.type.startsWith("video/")) {

                durationSelect.disabled = true;
                durationSelect.options[0].text = "Original";

            } else {

                durationSelect.disabled = false;
                durationSelect.options[0].text = "1 sec";

            }

            fileCounter++;

        }

        previewImages();

    }
    const dropZone = document.getElementById("dropZone");

    const hiddenInput = document.getElementById("hiddenImageInput");

    dropZone.addEventListener("click", () => {

        hiddenInput.click();

    });

    hiddenInput.addEventListener("change", function () {

        processMedia(this.files);

    });

    dropZone.addEventListener("dragover", function (e) {

        e.preventDefault();

        dropZone.classList.add("dragover");

    });

    dropZone.addEventListener("dragleave", function () {

        dropZone.classList.remove("dragover");

    });

    dropZone.addEventListener("drop", function (e) {

        e.preventDefault();

        dropZone.classList.remove("dragover");

        processMedia(e.dataTransfer.files);

    });

    window.addFileInput = addFileInput;
    window.removeFileInput = removeFileInput;
    window.previewImages = previewImages;

});

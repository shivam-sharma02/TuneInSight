document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const video = document.querySelector("video");

    form.addEventListener("submit", function () {
    video.pause();
    });
});

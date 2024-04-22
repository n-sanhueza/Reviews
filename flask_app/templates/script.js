document.addEventListener("DOMContentLoaded", function () {
    var likeButtons = document.querySelectorAll(".like-btn");

    likeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            var reviewId = button.getAttribute("data-review-id");
            var likeCountSpan = button.parentElement.querySelector(".like-count");
            var currentLikes = parseInt(likeCountSpan.innerText);
            likeCountSpan.innerText = currentLikes + 1;
        });
    });
});


 window.onload = function () {
    const msg = document.getElementById("message");
    if (msg) {
        setTimeout(() => {
            msg.style.transition = "opacity 1s ease";
            msg.style.opacity = "0";

            // remove after fade
            setTimeout(() => msg.remove(), 1000);
        }, 2000); // fade after 2 seconds
    }
}
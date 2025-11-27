//  window.onload = function () {
//     const msg = document.getElementById("message");
//     if (msg) {
//         setTimeout(() => {
//             msg.style.transition = "opacity 1s ease";
//             msg.style.opacity = "0";

//             // remove after fade
//             setTimeout(() => msg.remove(), 1000);
//         }, 2000); // fade after 2 seconds
//     }
// }


// Automatically FadOut Alert message after success or error
setTimeout(function () {
    let alert = document.querySelector(".alert");
    if (alert) {
        alert.style.transition = "opacity 1s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 1000);
    }
}, 4000); // disappear after 3 seconds
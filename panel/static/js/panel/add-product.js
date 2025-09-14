// Generate Captcha
function generateCaptcha() {
  let randomNum = Math.floor(1000 + Math.random() * 9000);
  document.getElementById("captchaCode").innerText = randomNum;
}

// View Admit Card (Dummy function)
function viewAdmitCard() {
  alert("Viewing Admit Card... (Demo)");
}

// Form Validation
document.getElementById("admitForm").addEventListener("submit", function (e) {
  e.preventDefault();
  let captchaCode = document.getElementById("captchaCode").innerText;
  let captchaInput = document.getElementById("captchaInput").value;

  if (captchaCode !== captchaInput) {
    alert("Invalid Captcha. Please try again.");
    generateCaptcha();
    return;
  }

  alert("Downloading Admit Card... (Demo)");
});

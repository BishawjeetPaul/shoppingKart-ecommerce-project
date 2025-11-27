console.log("This is category page...!");

// when "Upload" button is clicked, trigger hidden file input
document.querySelector(".file-upload-browse").addEventListener("click", function () {
    document.querySelector("#fileUpload").click();
});

// when file is selected, show file name in text field
document.querySelector("#fileUpload").addEventListener("change", function () {
    let fileName = this.files[0] ? this.files[0].name : "Upload Image";
    document.querySelector(".file-upload-info").value = fileName;
});
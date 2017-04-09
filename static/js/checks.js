function check_story() {
    var toret = true;
    var number = document.getElementById("temperature");
    var error = document.getElementById("dvError");
    error.style.display = "none";

    if (number.value.trim == "") {
        error.style.display = "block";
        error.innerHTML = "Type a number value";
        toret = false;
    }
    return toret;
}

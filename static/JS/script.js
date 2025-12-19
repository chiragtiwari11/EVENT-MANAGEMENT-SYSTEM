// ================= FORM VALIDATION =================
function validateForm() {
    let inputs = document.querySelectorAll("input[required]");
    
    for (let input of inputs) {
        if (input.value.trim() === "") {
            alert("Please fill all required fields");
            input.focus();
            return false;
        }
    }
    return true;
}

// ================= EVENT REGISTRATION CONFIRM =================
function confirmRegistration() {
    return confirm("Are you sure you want to register for this event?");
}

// ================= SIMPLE PAGE LOAD EFFECT =================
window.onload = function () {
    document.body.style.opacity = "0";
    setTimeout(() => {
        document.body.style.transition = "opacity 0.6s ease";
        document.body.style.opacity = "1";
    }, 100);
};

// ================= LOGOUT CONFIRM =================
function confirmLogout() {
    return confirm("Do you really want to logout?");
}


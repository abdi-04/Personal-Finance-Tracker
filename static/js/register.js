// DOM ELEMENT REFERENCES
const registerform = document.getElementById("form");
const firstnameInput = document.getElementById("firstname");
const lastnameInput = document.getElementById("lastname");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmInput = document.getElementById("confirm_password");

// Error message elements
const firstnameError = document.getElementById("firstname-error");
const lastnameError = document.getElementById("lastname-error");
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");
const confirmError = document.getElementById("confirm-error");

// VALIDATION FUNCTIONS
// Validate name - must not be empty
function validateName(name) {
    return name.trim().length > 0;
}

// Validate email - must match email pattern
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Validate password - must be at least 8 characters
function validatePassword(password) {
    return password.trim().length >= 8;
}

// Validate confirm password - must match password
function validateConfirm(confirm, password) {
    return confirm === password;
}

// UI FEEDBACK FUNCTIONS
// Show error state for input field
function showError(input, errorElement, message) {
    input.classList.add("invalid");
    errorElement.textContent = message;
}

// Hide error state for input field
function hideError(input, errorElement) {
    input.classList.remove("invalid");
    errorElement.textContent = "";
}

// FORM VALIDATION HANDLER
function validateForm() {
    let isValid = true;

    // Validate Firstname
    if (!validateName(firstnameInput.value)) {
        showError(firstnameInput, firstnameError, "Firstname is required.");
        isValid = false;
    } else {
        hideError(firstnameInput, firstnameError);
    }

    // Validate Lastname
    if (!validateName(lastnameInput.value)) {
        showError(lastnameInput, lastnameError, "Lastname is required.");
        isValid = false;
    } else {
        hideError(lastnameInput, lastnameError);
    }

    // Validate Email
    if (!validateEmail(emailInput.value.trim())) {
        showError(emailInput, emailError, "Enter a valid email address.");
        isValid = false;
    } else {
        hideError(emailInput, emailError);
    }

    // Validate Password
    if (!validatePassword(passwordInput.value)) {
        showError(passwordInput, passwordError, "Password must be at least 8 characters.");
        isValid = false;
    } else {
        hideError(passwordInput, passwordError);
    }

    // Validate Confirm Password
    if (!validateConfirm(confirmInput.value, passwordInput.value)) {
        showError(confirmInput, confirmError, "Passwords do not match.");
        isValid = false;
    } else {
        hideError(confirmInput, confirmError);
    }

    return isValid;
}

// FORM SUBMISSION HANDLER
function handleFormSubmit(event) {
    // Validate all fields before allowing the form to submit to the server
    const isValid = validateForm();

    // If validation fails, stop the form from submitting
    if (!isValid) {
        event.preventDefault();
    }
}

// EVENT LISTENERS 
if (registerform) {
    registerform.addEventListener("submit", handleFormSubmit);
}
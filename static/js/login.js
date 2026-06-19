// DOM ELEMENT REFERENCES
const loginform = document.getElementById("form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

// Error message elements
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");

// VALIDATION FUNCTIONS
// Validate email - must match email pattern
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Validate password - must not be empty
function validatePassword(password) {
    return password.trim().length > 0;
}

// UI FEEDBACK FUNCTIONS
// Show error state for input field
function showError(input, errorElement, message) {
    input.classList.add("invalid"); // Add red border
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

    // Validate Email
    if (!validateEmail(emailInput.value.trim())) {
        showError(emailInput, emailError, "Enter a valid email address.");
        isValid = false;
    } else {
        hideError(emailInput, emailError);
    }

    // Validate Password
    if (!validatePassword(passwordInput.value.trim())) {
        showError(passwordInput, passwordError, "Password is required.");
        isValid = false;
    } else {
        hideError(passwordInput, passwordError);
    }

    return isValid;
}

// FORM SUBMISSION HANDLER
function handleFormSubmit(event) {
    // Validate all fields before allowing the form to submit to the server
    const isValid = validateForm();

    // If validation fails, stop the form from submitting
    if (!isValid) {
        event.preventDefault(); // Prevent form submission to the server
    }
}

// EVENT LISTENERS
if (loginform) {
    loginform.addEventListener("submit", handleFormSubmit);
}
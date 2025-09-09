// registration validation elements.
const form = document.getElementById('form');
const firstName = document.getElementById('first_name');
const lastName = document.getElementById('last_name');
const phone = document.getElementById('phone_number');
const email = document.getElementById('email');
const password = document.getElementById('password');
const passwordConfirm = document.getElementById('password_confirm');
const errorDisplay = document.getElementsByClassName('.error');


form.addEventListener('submit', e => {
    e.preventDefault();
    if (validateInputs()) {
        form.submit(); // manually submit if valid
    }
});

// setting function for error message
const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    errorDisplay.style.fontSize = '12px'; // Set font size here
    errorDisplay.style.color = 'red';     // optional: text color

    inputControl.classList.add('error');
    inputControl.classList.remove('success');
};

// setting function for success message
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

// regex for email
const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
};

// regex for name
const isValidName = name => {
    const re = /^[A-Za-z]{2,30}$/; // Only letters, 2–30 chars
    return re.test(name);
};

// regex for name
const isValidPhone = phone => {
    const re = /^\d{10}$/; // Only 10 digits
    return re.test(phone);
};

const validateInputs = () => {
    let isValid = true;
    const firstNameValue = firstName.value.trim();
    const lastNameValue = lastName.value.trim();
    const phoneValue = phone.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const passwordConfirmValue = passwordConfirm.value.trim();

    // first name validation check
    if (firstNameValue === '') {
        setError(firstName, 'First name is required');
    } else if (!isValidName(firstNameValue)) {
        setError(firstName, 'First name must be letters only (2-30 characters)')
    } else {
        setSuccess(firstName);
    }

    // last name validation check
    if (lastNameValue === '') {
        setError(lastName, 'Last name is required');
    } else if (!isValidName(lastNameValue)) {
        setError(lastName, 'Last name must be letters only (2-30 characters)')
    } else {
        setSuccess(lastName);
    }

    // phone number validation check
    if (phoneValue === '') {
        setError(phone, 'Phone number is required');
        isValid = false;
    } else if (!isValidPhone(phoneValue)) {
        setError(phone, 'Enter a valid phone number');
        isValid = false;
    } else {
        setSuccess(phone);
    }

    // email validation check
    if (emailValue === '') {
        setError(email, 'Email is required');
        isValid = false;
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Provide a valid email address');
        isValid = false;
    } else {
        setSuccess(email);
    }

    // password validation check
    if (passwordValue === '') {
        setError(password, 'Password is required');
        isValid = false;
    } else if (passwordValue.length < 8) {
        setError(password, 'Password must be at least 8 characters.');
        isValid = false;
    } else {
        setSuccess(password);
    }

    // confirm password validation check
    if (passwordConfirmValue === '') {
        setError(passwordConfirm, 'Confirm password is required');
        isValid = false;
    } else if (passwordConfirmValue.length < 8) {
        setError(passwordConfirm, 'Confirm password must be at least 8 characters.');
        isValid = false;
    } else {
        setSuccess(passwordConfirm);
    }

    return isValid;
};
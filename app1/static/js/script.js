//Date Picker
  
// Initialize flatpickr on all desired fields
document.addEventListener('DOMContentLoaded', function () {
    const selectors = ['#id_employee_date', '#id_project_start_date', '#id_project_end_date'];
  
    selectors.forEach(selector => {
      flatpickr(selector, {
        dateFormat: "m/d/Y",  
        allowInput: true,
        minDate: new Date(2000, 0, 1)
      });
  
      const input = document.querySelector(selector);
      if (input) {
        input.addEventListener('input', function () {
          const parts = input.value.split('/');
          if (parts[2] && parts[2].length > 4) {
            parts[2] = parts[2].slice(0, 4);
            input.value = parts.join('/');
          }
        });
      }
    });
  });
  

//Password View Icon

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function () {
            const input = this.previousElementSibling.querySelector('input') || this.previousElementSibling;
            const type = input.getAttribute('type');
            if (type === 'password') {
                input.setAttribute('type', 'text');
                this.innerHTML = '<i class="fa fa-eye-slash" aria-hidden="true"></i>';
            } else {
                input.setAttribute('type', 'password');
                this.innerHTML = '<i class="fa fa-eye" aria-hidden="true"></i>';
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('employeeForm');

    const usernameInput = document.querySelector('#id_username');
    const emailInput = document.querySelector('#id_email');
    const passwordInput = document.querySelector('#id_password');
    const confirmPasswordInput = document.querySelector('#id_confirm_password');

    const togglePasswordButton = document.getElementById('toggle-password');
    const toggleConfirmPasswordButton = document.getElementById('toggle-confirm-password');

    // --------------------------------------------------------------------
    // General: Remove errors on typing
    // --------------------------------------------------------------------
    form.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('input', function () {
            const parent = input.closest('.form-group');
            const error = parent?.querySelector('.invalid-feedback');
            if (error) error.remove();
            input.classList.remove('is-invalid');
        });
    });

    // --------------------------------------------------------------------
    // USERNAME: Real-time uniqueness check
    // --------------------------------------------------------------------
    if (usernameInput) {
        const usernameFeedback = document.createElement('div');
        usernameFeedback.style.color = 'red';
        usernameInput.parentNode.appendChild(usernameFeedback);

        usernameInput.addEventListener('input', function () {
            const username = usernameInput.value;
            if (username.length > 0) {
                fetch(`/check-username/?username=${encodeURIComponent(username)}`)
                    .then(response => response.json())
                    .then(data => {
                        usernameFeedback.textContent = data.exists ? 'This username is already taken.' : '';
                    });
            } else {
                usernameFeedback.textContent = '';
            }
        });
    }

    // --------------------------------------------------------------------
    // PASSWORD: Strength validation
    // --------------------------------------------------------------------
    if (passwordInput) {
        const passwordFeedback = document.createElement('ul');
        passwordFeedback.style.color = 'red';
        passwordInput.parentNode.appendChild(passwordFeedback);

        passwordInput.addEventListener('input', function () {
            const value = passwordInput.value;
            const errors = [];

            if (value.length < 8) errors.push('At least 8 characters');
            if (!/[A-Z]/.test(value)) errors.push('At least one uppercase letter');
            if (!/\d/.test(value)) errors.push('At least one digit');
            if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) errors.push('At least one special character');

            passwordFeedback.innerHTML = '';
            errors.forEach(error => {
                const li = document.createElement('li');
                li.textContent = error;
                passwordFeedback.appendChild(li);
            });
        });
    }

    // --------------------------------------------------------------------
    // CONFIRM PASSWORD: Match validation
    // --------------------------------------------------------------------
    if (passwordInput && confirmPasswordInput) {
        function validatePasswordsMatch() {
            const errorClass = 'invalid-feedback';

            const existingError = confirmPasswordInput.parentNode.querySelector(`.${errorClass}`);
            if (existingError) {
                existingError.remove();
                confirmPasswordInput.classList.remove('is-invalid');
            }

            if (passwordInput.value && confirmPasswordInput.value && passwordInput.value !== confirmPasswordInput.value) {
                const error = document.createElement('div');
                error.classList.add(errorClass);
                error.innerText = "Passwords do not match.";
                confirmPasswordInput.classList.add('is-invalid');
                confirmPasswordInput.parentNode.appendChild(error);
            }
        }

        passwordInput.addEventListener('input', validatePasswordsMatch);
        confirmPasswordInput.addEventListener('input', validatePasswordsMatch);
    }

    // --------------------------------------------------------------------
    // PASSWORD + CONFIRM PASSWORD: Show/Hide toggle
    // --------------------------------------------------------------------
    function setupToggle(inputElement, toggleButtonElement) {
        if (toggleButtonElement && inputElement) {
            toggleButtonElement.addEventListener('click', function () {
                const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
                inputElement.setAttribute('type', type);
                this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
            });
        }
    }

    setupToggle(passwordInput, togglePasswordButton);
    setupToggle(confirmPasswordInput, toggleConfirmPasswordButton);

    // --------------------------------------------------------------------
    // FORM: Final validation before submission
    // --------------------------------------------------------------------
    form.addEventListener('submit', function (e) {
        let isValid = true;

        form.querySelectorAll('input, select, textarea').forEach(input => {
            if (input.type !== 'hidden' && !input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert("Please fill in all required fields.");
        }
    });
});


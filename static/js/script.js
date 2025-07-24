// Basic client-side validation for forms
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener("submit", function (e) {
            let valid = true;
            const inputs = form.querySelectorAll("input[required], select[required]");

            inputs.forEach((input) => {
                if (!input.value.trim()) {
                    input.classList.add("is-invalid");
                    valid = false;
                } else {
                    input.classList.remove("is-invalid");
                }
            });

            if (!valid) {
                e.preventDefault();
                alert("Please fill out all required fields.");
            }
        });
    });
});

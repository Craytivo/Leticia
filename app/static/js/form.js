document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#question-form");
  if (!form) return;
  const contactFields = document.querySelector("#contact-fields");
  const preferenceInputs = form.querySelectorAll('input[name="response_preference"]');
  const question = document.querySelector("#question");
  const count = document.querySelector("#question-count");
  const message = document.querySelector("#form-message");

  function syncContactFields() {
    const contact = form.querySelector('input[name="response_preference"]:checked')?.value === "contact";
    contactFields.hidden = !contact;
    document.querySelector("#name").required = contact;
    document.querySelector("#email").required = contact;
  }
  preferenceInputs.forEach(input => input.addEventListener("change", syncContactFields));
  question.addEventListener("input", () => { count.textContent = question.value.length + " / 3000"; });
  syncContactFields();

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    message.textContent = "The form is ready for the submission backend. Your question has not been sent yet.";
    message.className = "form-message info";
  });
});

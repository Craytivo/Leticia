document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#question-form");
  if (!form) return;

  const contactFields = document.querySelector("#contact-fields");
  const preferenceInputs = form.querySelectorAll('input[name="response_preference"]');
  const question = document.querySelector("#question");
  const count = document.querySelector("#question-count");
  const message = document.querySelector("#form-message");
  const submitButton = form.querySelector(".submit-button");

  function syncContactFields() {
    const contact = form.querySelector('input[name="response_preference"]:checked')?.value === "contact";
    contactFields.hidden = !contact;
    document.querySelector("#name").required = contact;
    document.querySelector("#email").required = contact;
  }

  function clearErrors() {
    form.querySelectorAll(".field-error").forEach((el) => { el.textContent = ""; });
    form.querySelectorAll("[aria-invalid='true']").forEach((el) => el.removeAttribute("aria-invalid"));
  }

  function showErrors(errors) {
    Object.entries(errors).forEach(([field, text]) => {
      const error = form.querySelector(`[data-error-for="${field}"]`);
      const input = form.querySelector(`[name="${field}"]`) || document.querySelector(`#${field}`);
      if (error) error.textContent = text;
      if (input) input.setAttribute("aria-invalid", "true");
    });
  }

  preferenceInputs.forEach((input) => input.addEventListener("change", syncContactFields));
  question.addEventListener("input", () => { count.textContent = question.value.length + " / 3000"; });
  syncContactFields();

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearErrors();
    message.textContent = "";

    const data = Object.fromEntries(new FormData(form).entries());
    data.privacy = document.querySelector("#privacy").checked;
    data.website = "";

    submitButton.disabled = true;
    submitButton.textContent = "Sending…";

    try {
      const response = await fetch("/api/questions", {
        method: "POST",
        headers: {"Content-Type": "application/json", "Accept": "application/json"},
        body: JSON.stringify(data)
      });
      const result = await response.json();

      if (!response.ok) {
        showErrors(result.errors || {form: "Please check your answers and try again."});
        message.textContent = "Please check the highlighted fields.";
        message.className = "form-message error";
        return;
      }

      window.location.href = `/thank-you?id=${encodeURIComponent(result.question_id)}&response=${encodeURIComponent(data.response_preference)}`;
    } catch {
      message.textContent = "We couldn't send your question right now. Please try again.";
      message.className = "form-message error";
    } finally {
      submitButton.disabled = false;
      if (submitButton.textContent === "Sending…") {
        submitButton.innerHTML = 'Send My Question <span aria-hidden="true">→</span>';
      }
    }
  });
});

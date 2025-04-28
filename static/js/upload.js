const form = document.getElementById("upload-form");
const submitButton = document.getElementById("submit-button");
const loadingIndicator = document.getElementById("loading-indicator");
const fileInput = document.getElementById("file_upload");
const docTypeSelect = document.getElementById("document_type");

form.addEventListener("submit", (event) => {
  // Basic Client-side validation
  let isValid = true;
  if (!docTypeSelect.value) {
    alert("Please select a document type.");
    isValid = false;
  } else if (fileInput.files.length === 0) {
    alert("Please select a PDF file to upload.");
    isValid = false;
  } else if (fileInput.files[0].type !== "application/pdf") {
    alert("Invalid file type. Only PDF files are allowed.");
    isValid = false;
  }

  if (!isValid) {
    event.preventDefault(); // Prevent form submission if validation fails
  } else {
    // Show loading indicator and disable button if validation passes
    loadingIndicator.classList.remove("hidden");
    submitButton.disabled = true;
    // Optionally change button text
    submitButton.innerHTML = `
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...`;
    // The form will now submit naturally
  }
});

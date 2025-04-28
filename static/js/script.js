document.addEventListener("DOMContentLoaded", function () {
  const toggleButtons = document.querySelectorAll(".toggle-button");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const targetElement = document.querySelector(targetId);
      const icon = this.querySelector("i");

      if (targetElement) {
        // Toggle visibility
        targetElement.classList.toggle("hidden");

        // Toggle icon
        if (targetElement.classList.contains("hidden")) {
          icon.classList.remove("fa-chevron-up");
          icon.classList.add("fa-chevron-down");
        } else {
          icon.classList.remove("fa-chevron-down");
          icon.classList.add("fa-chevron-up");
        }
      }
    });

    // Optional: Set initial state based on 'hidden' class
    // (The HTML already sets the initial state, but this ensures consistency if needed)
    const targetId = button.getAttribute("data-target");
    const targetElement = document.querySelector(targetId);
    const icon = button.querySelector("i");
    if (targetElement && targetElement.classList.contains("hidden")) {
      icon.classList.remove("fa-chevron-up");
      icon.classList.add("fa-chevron-down");
    } else if (targetElement) {
      icon.classList.remove("fa-chevron-down");
      icon.classList.add("fa-chevron-up");
    }
  });
});

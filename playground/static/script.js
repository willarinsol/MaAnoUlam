function findrecipe() {
  alert("the user clicked on find recipe!");
}

// Remove the function wrapper. Let the event listener sit at the top level.
document.addEventListener("DOMContentLoaded", () => {
  const tagsContainer = document.querySelector(".ingredient-tags");

  // If tagsContainer doesn't exist on the page, exit early to prevent errors
  if (!tagsContainer) return;

  tagsContainer.addEventListener("click", (event) => {
    // Check if the clicked element is the remove button
    if (event.target.tagName === "BUTTON") {
      const tagToRemove = event.target.closest(".ingredient-tag");

      // 1. Trigger the CSS transition
      tagToRemove.classList.add("fade-out");

      // 2. Wait for the CSS transition to finish (0.2s = 200ms) before removing from DOM
      setTimeout(() => {
        tagToRemove.remove();
      }, 200);
    }
  });
});

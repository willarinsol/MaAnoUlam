function findrecipe(event) {
  // Prevent the form from submitting normally (stops the blank reload)
  if (event) event.preventDefault();

  // Find all current ingredient tags on the page
  const tagElements = document.querySelectorAll(".ingredient-tag");
  const ingredients = [];

  tagElements.forEach((tag) => {
    // Grab the raw text node before the <button> element
    const ingredientText = tag.childNodes[0].textContent.trim();
    if (ingredientText) {
      ingredients.push(ingredientText);
    }
  });

  // NEW: Grab whatever the user typed into the input box too!
  const searchInput = document.querySelector(".search-box input");
  if (searchInput && searchInput.value.trim()) {
    ingredients.push(searchInput.value.trim());
  }

  // Construct the URL and redirect
  const queryString = encodeURIComponent(ingredients.join(","));
  window.location.href = `/playground/discover/?ingredients=${queryString}`;
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

  // THIS PART IS FOR DISCOVER DO NOT MOVE SHIT
  const discoverSearchInput = document.getElementById("discover-search-input");
  const ingredientsBar = document.querySelector(".ingredients-bar");

  function updateUrlIngredients(ingredient, action) {
    const urlParams = new URLSearchParams(window.location.search);
    let currentIngredients = urlParams.get("ingredients")
      ? urlParams.get("ingredients").split(",")
      : [];

    if (action === "add" && !currentIngredients.includes(ingredient)) {
      currentIngredients.push(ingredient);
    } else if (action === "remove") {
      currentIngredients = currentIngredients.filter(
        (item) => item !== ingredient,
      );
    }

    if (currentIngredients.length > 0) {
      urlParams.set("ingredients", currentIngredients.join(","));
    } else {
      urlParams.delete("ingredients");
    }

    // Reload the page with the new URL parameters
    window.location.search = urlParams.toString();
  }

  // 1. Add ingredient when pressing "Enter" in the search box
  if (discoverSearchInput) {
    discoverSearchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const newIngredient = discoverSearchInput.value.trim();
        if (newIngredient) {
          updateUrlIngredients(newIngredient, "add");
        }
      }
    });
  }

  // 2. Remove ingredient when clicking the "X" button on a tag
  if (ingredientsBar) {
    ingredientsBar.addEventListener("click", (e) => {
      const removeBtn = e.target.closest(".remove-ingredient-btn");
      if (removeBtn) {
        const tag = removeBtn.closest(".ingredient-tag");
        const ingredientToRemove = tag.getAttribute("data-ingredient");
        if (ingredientToRemove) {
          updateUrlIngredients(ingredientToRemove, "remove");
        }
      }
    });
  }
});
function showUserPanel() {
  alert("This part is not yet finished");
}

// ---------------------------------------------------------
// 1. Homepage Search & Redirection
// ---------------------------------------------------------
function findrecipe(event) {
  if (event) event.preventDefault();

  const tagElements = document.querySelectorAll(".ingredient-tag");
  const ingredients = [];

  tagElements.forEach((tag) => {
    const ingredientText = tag.childNodes[0].textContent.trim();
    if (ingredientText) {
      ingredients.push(ingredientText);
    }
  });

  const searchInput = document.querySelector(".search-box input");
  if (searchInput && searchInput.value.trim()) {
    ingredients.push(searchInput.value.trim());
  }

  const queryString = encodeURIComponent(ingredients.join(","));
  window.location.href = `/playground/discover/?ingredients=${queryString}`;
}

// ---------------------------------------------------------
// 2. User Panel Alert
// ---------------------------------------------------------
function showUserPanel() {
  alert("This part is not yet finished");
}

// ---------------------------------------------------------
// 3. Make removeTag globally accessible
// ---------------------------------------------------------
const selectedIngredients = []; // Track homepage ingredients

window.removeTag = function (btnElement, tagToRemove) {
  const index = selectedIngredients.indexOf(tagToRemove);
  if (index > -1) {
    selectedIngredients.splice(index, 1);
  }
  const tagContainer = btnElement.closest(".ingredient-tag");
  tagContainer.classList.add("fade-out");
  setTimeout(() => {
    tagContainer.remove();
  }, 200);
};

// ---------------------------------------------------------
// 4. Main Event Listeners (Runs when page loads)
// ---------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  // --- A. Homepage Tags Deletion (existing static tags) ---
  const tagsContainer = document.querySelector(".ingredient-tags");
  if (tagsContainer) {
    tagsContainer.addEventListener("click", (event) => {
      if (event.target.tagName === "BUTTON" || event.target.closest("button")) {
        const tagToRemove = event.target.closest(".ingredient-tag");
        tagToRemove.classList.add("fade-out");
        setTimeout(() => {
          tagToRemove.remove();
        }, 200);
      }
    });
  }

  // --- B. Discovery Page: URL updating & Tag removal ---
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
    window.location.search = urlParams.toString();
  }

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

  // --- C. Homepage Auto-Suggestions ---
  const homeSearchInput = document.getElementById("ingredient-search");
  const homeSuggestionList = document.getElementById("suggestion-list");
  const selectedTagsContainer = document.getElementById(
    "selected-tags-container",
  );

  function addTag(tag) {
    if (!selectedIngredients.includes(tag)) {
      selectedIngredients.push(tag);
      const tagSpan = document.createElement("span");
      tagSpan.className = "ingredient-tag";
      tagSpan.innerHTML = `
        ${tag}
        <button type="button" onclick="removeTag(this, '${tag}')">
           <span class="material-symbols-outlined" style="font-size: 16px;">close</span>
        </button>
      `;
      selectedTagsContainer.appendChild(tagSpan);
    }
    homeSearchInput.value = "";
    homeSuggestionList.style.display = "none";
    homeSearchInput.focus();
  }

  if (
    homeSearchInput &&
    homeSuggestionList &&
    typeof recipeTags !== "undefined"
  ) {
    homeSearchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase().trim();
      homeSuggestionList.innerHTML = "";

      if (query) {
        const filteredTags = recipeTags.filter(
          (tag) => tag.includes(query) && !selectedIngredients.includes(tag),
        );
        if (filteredTags.length > 0) {
          homeSuggestionList.style.display = "block";
          filteredTags.forEach((tag) => {
            const li = document.createElement("li");
            li.textContent = tag;
            li.onclick = () => addTag(tag);
            homeSuggestionList.appendChild(li);
          });
        } else {
          homeSuggestionList.style.display = "none";
        }
      } else {
        homeSuggestionList.style.display = "none";
      }
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".search-box")) {
        homeSuggestionList.style.display = "none";
      }
    });
  }

  // --- D. Discovery Page Auto-Suggestions ---
  const discoverSuggestionList = document.getElementById(
    "discover-suggestion-list",
  );

  if (
    discoverSearchInput &&
    discoverSuggestionList &&
    typeof recipeTags !== "undefined"
  ) {
    discoverSearchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase().trim();
      discoverSuggestionList.innerHTML = "";

      if (query) {
        const filteredTags = recipeTags.filter((tag) => tag.includes(query));

        if (filteredTags.length > 0) {
          discoverSuggestionList.style.display = "block";
          filteredTags.forEach((tag) => {
            const li = document.createElement("li");
            li.textContent = tag;
            li.onclick = () => {
              updateUrlIngredients(tag, "add");
            };
            discoverSuggestionList.appendChild(li);
          });
        } else {
          discoverSuggestionList.style.display = "none";
        }
      } else {
        discoverSuggestionList.style.display = "none";
      }
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".search-container")) {
        discoverSuggestionList.style.display = "none";
      }
    });
  }
});

function updateFilter(paramKey, paramValue) {
    const urlParams = new URLSearchParams(window.location.search);
    
    // Toggle logic: If clicking the same filter, remove it. Otherwise, set it.
    if (urlParams.get(paramKey) === paramValue) {
        urlParams.delete(paramKey);
    } else {
        urlParams.set(paramKey, paramValue);
    }
    
    // Reload the page with the new query string
    window.location.search = urlParams.toString();
}
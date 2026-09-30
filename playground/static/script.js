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
  document
    .querySelectorAll(".profile-dropdown-container")
    .forEach((container) => {
      const button = container.querySelector(".profile-btn");
      if (!button) return;

      button.addEventListener("click", (event) => {
        event.stopPropagation();
        const isOpen = container.classList.toggle("is-open");
        button.setAttribute("aria-expanded", String(isOpen));
      });

      container.addEventListener("click", (event) => event.stopPropagation());
    });

  document.addEventListener("click", () => {
    document
      .querySelectorAll(".profile-dropdown-container.is-open")
      .forEach((container) => {
        container.classList.remove("is-open");
        container
          .querySelector(".profile-btn")
          ?.setAttribute("aria-expanded", "false");
      });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    document
      .querySelectorAll(".profile-dropdown-container.is-open")
      .forEach((container) => {
        container.classList.remove("is-open");
        container
          .querySelector(".profile-btn")
          ?.setAttribute("aria-expanded", "false");
      });
  });

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

// --- E. Interactive Collection Picker Modal for Bookmarks ---
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("save-modal");
  const closeModalBtn = document.getElementById("close-save-modal");
  const collectionsListContainer = document.getElementById(
    "modal-collections-list",
  );
  const createCollectionForm = document.getElementById(
    "modal-create-collection-form",
  );
  const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");

  let activeRecipeCardBtn = null;
  let activeRecipeId = null;

  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

  // Close modal when clicking outside content area
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });

  document.addEventListener("click", (e) => {
    const bookmarkBtn = e.target.closest(".bookmark-btn");
    if (bookmarkBtn) {
      e.preventDefault();
      activeRecipeCardBtn = bookmarkBtn;
      activeRecipeId = bookmarkBtn.getAttribute("data-recipe-id");
      if (!activeRecipeId) return;

      if (!csrfInput) {
        alert("Please log in to save recipes.");
        window.location.href = "/playground/login/";
        return;
      }

      // Fetch collections data via AJAX request
      fetchCollectionsAndOpenModal();
    }
  });

  function fetchCollectionsAndOpenModal() {
    fetch(`/playground/recipe/${activeRecipeId}/toggle-save/`, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfInput.value,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        renderModalContent(data);
        modal.style.display = "flex";
        updateCardIconState(data);
      })
      .catch((err) => console.error("Error loading collections:", err));
  }

  function renderModalContent(data) {
    collectionsListContainer.innerHTML = "";
    data.user_collections.forEach((col) => {
      const isChecked = data.recipe_collection_ids.includes(col.id);
      const item = document.createElement("div");
      item.style.cssText =
        "display:flex; align-items:center; justify-content:space-between; padding:10px 12px; background:var(--surface-container-low); border-radius:10px; cursor:pointer;";
      item.innerHTML = `
                <span style="font-weight:600; font-size:14px;">${col.name}</span>
                <input type="checkbox" data-collection-id="${col.id}" ${isChecked ? "checked" : ""} style="width:18px; height:18px; accent-color:var(--primary); cursor:pointer;" />
            `;

      // Toggle item on click
      item.addEventListener("click", (e) => {
        if (e.target.tagName !== "INPUT") {
          const checkbox = item.querySelector("input");
          checkbox.checked = !checkbox.checked;
          triggerToggle(col.id, checkbox.checked);
        }
      });

      item.querySelector("input").addEventListener("change", (e) => {
        triggerToggle(col.id, e.target.checked);
      });

      collectionsListContainer.appendChild(item);
    });
  }

  function triggerToggle(collectionId, isChecked) {
    const formData = new FormData();
    formData.append("collection_id", collectionId);

    fetch(`/playground/recipe/${activeRecipeId}/toggle-save/`, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfInput.value,
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        updateCardIconState(data);
      })
      .catch((err) => console.error("Error toggling collection:", err));
  }

  function updateCardIconState(data) {
    if (!activeRecipeCardBtn) return;
    const icon = activeRecipeCardBtn.querySelector(
      ".material-symbols-outlined",
    );
    if (data.recipe_collection_ids && data.recipe_collection_ids.length > 0) {
      icon.style.fontVariationSettings = "'FILL' 1";
      icon.style.color = "var(--primary)";
    } else {
      icon.style.fontVariationSettings = "'FILL' 0";
      icon.style.color = "";
    }
  }

  // Handle quick-creation of a collection right from the modal
  if (createCollectionForm) {
    createCollectionForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const inputField =
        createCollectionForm.querySelector("input[name='name']");
      const formData = new FormData(createCollectionForm);

      fetch(`/playground/saved/create/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrfInput.value,
        },
        body: formData,
      })
        .then(() => {
          inputField.value = "";
          // Refresh modal collections list
          fetchCollectionsAndOpenModal();
        })
        .catch((err) => console.error("Error creating collection:", err));
    });
  }
});

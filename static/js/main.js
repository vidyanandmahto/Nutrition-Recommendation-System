// ─────────────────────────────────────────
// Quick-fill example buttons (Predict page)
// ─────────────────────────────────────────
document.querySelectorAll(".example-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const [calories, protein, carbs, fat, iron, vitamin_c] = btn.dataset.vals.split(",");
    document.getElementById("calories")  && (document.getElementById("calories").value  = calories);
    document.getElementById("protein")   && (document.getElementById("protein").value   = protein);
    document.getElementById("carbs")     && (document.getElementById("carbs").value     = carbs);
    document.getElementById("fat")       && (document.getElementById("fat").value       = fat);
    document.getElementById("iron")      && (document.getElementById("iron").value      = iron);
    document.getElementById("vitamin_c") && (document.getElementById("vitamin_c").value = vitamin_c);
  });
});

// ─────────────────────────────────────────
// Auto-submit recommend form on goal change
// ─────────────────────────────────────────
document.querySelectorAll(".goal-pills input[type=radio]").forEach(radio => {
  radio.addEventListener("change", () => {
    const form = document.getElementById("filterForm");
    if (form) form.submit();
  });
});

// ─────────────────────────────────────────
// Animate nutrient bars on load
// ─────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".bar-fill").forEach(bar => {
    const target = bar.style.width;
    bar.style.width = "0";
    setTimeout(() => { bar.style.width = target; }, 100);
  });
});

// ─────────────────────────────────────────
// Explore: live search filter (client-side)
// ─────────────────────────────────────────
const exploreSearch = document.querySelector(".explore-search");
if (exploreSearch) {
  exploreSearch.addEventListener("input", () => {
    const q = exploreSearch.value.toLowerCase();
    document.querySelectorAll(".food-table tbody tr").forEach(row => {
      const name = row.querySelector(".food-name-cell");
      if (name) {
        row.style.display = name.textContent.toLowerCase().includes(q) ? "" : "none";
      }
    });
  });
}

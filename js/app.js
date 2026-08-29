(function () {
  var root = document.documentElement;
  var stored = null;

  try {
    stored = window.localStorage.getItem("teamulate-theme");
  } catch (err) {
    stored = null;
  }

  function applyTheme(theme) {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
    }
    document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-theme-set") === theme ? "true" : "false");
    });
  }

  if (stored === "dark" || stored === "light") {
    applyTheme(stored);
  } else {
    applyTheme("light");
  }

  document.querySelectorAll("[data-theme-set]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = btn.getAttribute("data-theme-set");
      applyTheme(next);
      try {
        window.localStorage.setItem("teamulate-theme", next);
      } catch (err) {
        /* ignore */
      }
    });
  });

  var toggle = document.querySelector("[data-side-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", document.body.classList.contains("nav-open") ? "true" : "false");
    });
  }

  var profile = document.querySelector("[data-profile]");
  if (profile) {
    var button = profile.querySelector("button");
    if (button) {
      button.addEventListener("click", function (event) {
        event.stopPropagation();
        profile.classList.toggle("is-open");
        button.setAttribute("aria-expanded", profile.classList.contains("is-open") ? "true" : "false");
      });
    }
    document.addEventListener("click", function () {
      profile.classList.remove("is-open");
      if (button) button.setAttribute("aria-expanded", "false");
    });
  }

  var search = document.querySelector("[data-app-search]");
  if (search) {
    var empty = document.querySelector("[data-empty-search]");
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var rows = document.querySelectorAll("[data-row]");
      var shown = 0;
      rows.forEach(function (row) {
        var hit = !q || (row.getAttribute("data-row") || "").toLowerCase().indexOf(q) !== -1 || row.textContent.toLowerCase().indexOf(q) !== -1;
        row.classList.toggle("hidden-row", !hit);
        if (hit) shown += 1;
      });
      if (empty) {
        empty.style.display = q && rows.length && !shown ? "block" : "none";
      }
    });
  }

  document.querySelectorAll("[data-filter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var key = btn.getAttribute("data-filter");
      var group = btn.parentElement;
      group.querySelectorAll("[data-filter]").forEach(function (other) {
        other.setAttribute("aria-pressed", other === btn ? "true" : "false");
      });
      document.querySelectorAll("[data-row]").forEach(function (row) {
        var status = row.getAttribute("data-status") || "";
        row.classList.toggle("hidden-row", key !== "all" && status !== key);
      });
    });
  });
})();

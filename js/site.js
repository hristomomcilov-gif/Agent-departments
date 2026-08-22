(function () {
  var root = document.documentElement;
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var themeBtn = document.querySelector(".theme-toggle");
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
    if (themeBtn) {
      themeBtn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
      themeBtn.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
    }
  }

  if (stored === "dark" || stored === "light") {
    applyTheme(stored);
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    applyTheme("dark");
  } else {
    applyTheme("light");
  }

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        window.localStorage.setItem("teamulate-theme", next);
      } catch (err) {
        /* ignore */
      }
    });
  }

  if (header && toggle) {
    var nav = header.querySelector("#site-nav");
    var tools = header.querySelector(".header-tools");
    function setOpen(open) {
      header.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (nav) nav.hidden = !open && window.matchMedia("(max-width: 1179px)").matches;
      if (tools) tools.hidden = !open && window.matchMedia("(max-width: 1179px)").matches;
    }
    setOpen(false);
    toggle.addEventListener("click", function () {
      setOpen(!header.classList.contains("is-open"));
    });
    window.addEventListener("resize", function () {
      setOpen(header.classList.contains("is-open"));
    });

    header.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var form = document.querySelector("[data-partner-form]");
  if (form) {
    var error = form.querySelector("[data-form-error]");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (error) {
        error.hidden = true;
        error.textContent = "";
      }
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      var email = form.querySelector('[name="email"]');
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
        if (error) {
          error.textContent = "Enter a work email.";
          error.hidden = false;
        }
        return;
      }
      window.location.href = "/thank-you.html";
    });
  }

  var loop = document.querySelector("[data-loop-form]");
  if (loop) {
    loop.addEventListener("submit", function (event) {
      event.preventDefault();
      window.location.href = "/thank-you.html";
    });
  }

  var login = document.querySelector("[data-login-form]");
  if (login) {
    login.addEventListener("submit", function (event) {
      event.preventDefault();
      window.location.href = "dashboard.html";
    });
  }
})();

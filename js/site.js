(function () {
  var cards = document.querySelectorAll("[data-card]");
  var nodes = document.querySelectorAll("[data-agent]");

  if (!cards.length || !nodes.length) {
    return;
  }

  function activate(id, move) {
    if (!id) {
      return;
    }

    nodes.forEach(function (node) {
      node.classList.toggle("is-active", node.getAttribute("data-agent") === id);
    });

    cards.forEach(function (card) {
      var match = card.getAttribute("data-card") === id;
      card.classList.toggle("is-active", match);
      if (match && move) {
        card.scrollIntoView({
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto"
            : "smooth",
          block: "start",
        });
      }
    });
  }

  nodes.forEach(function (node) {
    node.addEventListener("click", function () {
      var id = node.getAttribute("data-agent");
      if (history.replaceState) {
        history.replaceState(null, "", "#" + id);
      }
      activate(id, true);
    });
  });

  if (window.location.hash) {
    activate(window.location.hash.slice(1), true);
  }

  window.addEventListener("hashchange", function () {
    activate(window.location.hash.slice(1), true);
  });
})();

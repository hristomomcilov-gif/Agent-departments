(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function glowMarkup() {
    return (
      '<defs><filter id="wire-glow" x="-20%" y="-20%" width="140%" height="140%">' +
      '<feGaussianBlur stdDeviation="2.2" result="b"/>' +
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>' +
      "</filter></defs>"
    );
  }

  function point(el, rootBox, edge) {
    var box = el.getBoundingClientRect();
    return {
      x: box.left + box.width / 2 - rootBox.left,
      y: edge === "bottom" ? box.bottom - rootBox.top : box.top - rootBox.top,
    };
  }

  function wire(root, animate) {
    var svg = root.querySelector(".org-wires");
    if (!svg) {
      return;
    }

    var rootBox = root.getBoundingClientRect();
    var width = root.clientWidth;
    var height = root.clientHeight;
    if (width < 2 || height < 2) {
      return;
    }
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);

    var paths = [];
    root.querySelectorAll("[data-parent]").forEach(function (child) {
      var parent = root.querySelector('[data-id="' + child.getAttribute("data-parent") + '"]');
      if (!parent) {
        return;
      }
      var a = point(parent, rootBox, "bottom");
      var b = point(child, rootBox, "top");
      var mid = (a.y + b.y) / 2;
      paths.push(
        "M " +
          a.x.toFixed(1) +
          " " +
          a.y.toFixed(1) +
          " V " +
          mid.toFixed(1) +
          " H " +
          b.x.toFixed(1) +
          " V " +
          b.y.toFixed(1)
      );
    });

    svg.innerHTML =
      glowMarkup() +
      paths
        .map(function (d, i) {
          var cls = animate && !reduce ? ' class="is-draw" style="animation-delay:' + i * 0.08 + 's"' : "";
          return '<path pathLength="1" d="' + d + '"' + cls + "></path>";
        })
        .join("");
  }

  document.querySelectorAll("[data-org]").forEach(function (root) {
    var first = true;
    var lastKey = "";
    var timer;
    var draw = function () {
      var key = root.clientWidth + "x" + root.clientHeight;
      if (key === lastKey) {
        return;
      }
      lastKey = key;
      wire(root, first);
      first = false;
    };
    var schedule = function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(draw, 40);
    };
    draw();
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(schedule);
      ro.observe(root);
    } else {
      window.addEventListener("resize", schedule);
    }
    window.addEventListener("load", schedule);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(schedule);
    }
  });

  var cards = document.querySelectorAll("[data-card]");
  var nodes = document.querySelectorAll("[data-agent]");
  if (!cards.length || !nodes.length) {
    return;
  }

  function activate(id, move) {
    if (!id) {
      return;
    }

    var found = false;
    nodes.forEach(function (node) {
      var on = node.getAttribute("data-agent") === id;
      node.classList.toggle("is-active", on);
      if (on) {
        found = true;
      }
    });
    if (!found) {
      return;
    }

    cards.forEach(function (card) {
      var match = card.getAttribute("data-card") === id;
      card.classList.toggle("is-live", match);
      if (match) {
        card.removeAttribute("hidden");
        if (move) {
          card.scrollIntoView({
            behavior: reduce ? "auto" : "smooth",
            block: "nearest",
          });
        }
      } else {
        card.setAttribute("hidden", "");
      }
    });
  }

  nodes.forEach(function (node) {
    node.addEventListener("click", function (event) {
      event.preventDefault();
      var id = node.getAttribute("data-agent");
      if (history.replaceState) {
        history.replaceState(null, "", "#" + id);
      }
      activate(id, true);
    });
  });

  var start = window.location.hash ? window.location.hash.slice(1) : "coordinator";
  activate(start, Boolean(window.location.hash));

  window.addEventListener("hashchange", function () {
    activate(window.location.hash.slice(1) || "coordinator", true);
  });
})();

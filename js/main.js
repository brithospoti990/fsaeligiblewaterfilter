/* nav toggle + subtle reveal (respects reduced motion) */
(function () {
  var btn = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (btn && links) {
    btn.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    var els = document.querySelectorAll("[data-reveal]");
    els.forEach(function (el) { el.style.opacity = "0"; el.style.transform = "translateY(14px)"; el.style.transition = "opacity .5s ease, transform .5s ease"; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.style.opacity = "1"; e.target.style.transform = "none"; io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    els.forEach(function (el) { io.observe(el); });
  }
})();

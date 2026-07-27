// Subtle 3D tilt on the glass panel, following the cursor (mouse) or gently idling (touch).
(function () {
  const panel = document.getElementById("panel");
  const orbWrap = document.getElementById("orbWrap");
  if (!panel) return;

  const MAX_TILT = 6; // degrees

  function handleMove(e) {
    const rect = panel.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width; // 0..1
    const y = (e.clientY - rect.top) / rect.height; // 0..1

    const rotY = (x - 0.5) * MAX_TILT * 2;
    const rotX = (0.5 - y) * MAX_TILT * 2;

    panel.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;

    if (orbWrap) {
      const px = (x - 0.5) * 16;
      const py = (y - 0.5) * 10;
      orbWrap.style.transform = `translate(${px}px, ${py}px)`;
    }
  }

  function reset() {
    panel.style.transform = "rotateX(0deg) rotateY(0deg)";
    if (orbWrap) orbWrap.style.transform = "translate(0,0)";
  }

  window.addEventListener("mousemove", handleMove);
  window.addEventListener("mouseleave", reset);

  // Respect reduced motion preference
  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;
  if (prefersReduced) {
    window.removeEventListener("mousemove", handleMove);
  }
})();

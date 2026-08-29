/* ==========================================================================
   Blair's Portfolio — shared behaviour
   No frameworks, no build step — plain DOM APIs only.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initNavToggle();
  initActiveNavLink();
  initNavScrollState();
  initScrollReveal();
  initSkillBars();
  initContactForm();
});

/* ---------- Mobile nav ---------- */
function initNavToggle() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("open");
    toggle.classList.toggle("open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  links.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      links.classList.remove("open");
      toggle.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

/* ---------- Highlight current page in nav ---------- */
function initActiveNavLink() {
  const current = document.body.dataset.page;
  if (!current) return;
  document.querySelectorAll(".nav-links a[data-page]").forEach((link) => {
    if (link.dataset.page === current) link.classList.add("active");
  });
}

/* ---------- Nav bar background strengthens on scroll ---------- */
function initNavScrollState() {
  const nav = document.querySelector(".site-nav");
  if (!nav) return;
  const onScroll = () => {
    nav.style.background = window.scrollY > 40
      ? "rgba(10, 10, 12, 0.82)"
      : "rgba(10, 10, 12, 0.55)";
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

/* ---------- Scroll-triggered reveal for anything with .reveal ---------- */
function initScrollReveal() {
  const items = document.querySelectorAll(".reveal");
  if (!items.length) return;

  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  items.forEach((el) => observer.observe(el));
}

/* ---------- Animate skill progress bars when visible ---------- */
function initSkillBars() {
  const bars = document.querySelectorAll(".skill-bar-fill");
  if (!bars.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const target = entry.target.dataset.value || "0";
          entry.target.style.width = `${target}%`;
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.3 }
  );

  bars.forEach((bar) => observer.observe(bar));
}

/* ---------- Contact form: client-side validation + fetch to /api/contact ---------- */
function initContactForm() {
  const form = document.querySelector("#contact-form");
  const status = document.querySelector("#form-status");
  if (!form || !status) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.className = "form-status";
    status.textContent = "";

    const data = Object.fromEntries(new FormData(form).entries());

    if (!data.name || !data.email || !data.message) {
      status.textContent = "Please fill in your name, email, and message.";
      status.classList.add("error");
      return;
    }

    const submitBtn = form.querySelector("button[type='submit']");
    const originalLabel = submitBtn.textContent;
    submitBtn.textContent = "Sending…";
    submitBtn.disabled = true;

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await res.json();

      if (res.ok && result.success) {
        status.textContent = result.message || "Thanks — your message has been sent.";
        status.classList.add("success");
        form.reset();
      } else {
        status.textContent = result.message || "Something went wrong. Please try again.";
        status.classList.add("error");
      }
    } catch (err) {
      status.textContent = "Network error — please try again in a moment.";
      status.classList.add("error");
    } finally {
      submitBtn.textContent = originalLabel;
      submitBtn.disabled = false;
    }
  });
}
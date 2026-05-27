// Elements & State Configuration
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");
const counter = document.getElementById("slide-current");
const bar = document.getElementById("progress-bar");
const DURATION = 3500; // ms per slide
let current = 0;
let timer, progTimer, progStart;

// Function to navigate between slides
function goTo(idx) {
    slides[current].classList.remove("active");
    dots[current].classList.remove("active");
    dots[current].setAttribute("aria-selected", "false");

    current = (idx + slides.length) % slides.length;

    slides[current].classList.add("active");
    dots[current].classList.add("active");
    dots[current].setAttribute("aria-selected", "true");
    counter.textContent = String(current + 1).padStart(2, "0");
    startProgress();
}

// Function to handle automatic progress bar animation
function startProgress() {
    bar.style.transition = "none";
    bar.style.width = "0%";
    clearTimeout(timer);
    cancelAnimationFrame(progTimer);

    // Trigger reflow to restart animation smoothly
    void bar.offsetWidth;
    bar.style.transition = `width ${DURATION}ms linear`;
    bar.style.width = "100%";
    timer = setTimeout(() => goTo(current + 1), DURATION);
}

// Event Listeners: Dot Clicks
dots.forEach((dot) => {
    dot.addEventListener("click", () => {
        clearTimeout(timer);
        goTo(parseInt(dot.dataset.slide));
    });
});

// Event Listeners: Arrow Clicks
document.getElementById("prev-btn").addEventListener("click", () => {
    clearTimeout(timer);
    goTo(current - 1);
});

document.getElementById("next-btn").addEventListener("click", () => {
    clearTimeout(timer);
    goTo(current + 1);
});

// Pause Carousel on Hover
const section = document.querySelector("section");
section.addEventListener("mouseenter", () => {
    clearTimeout(timer);
    bar.style.transition = "none";
});
section.addEventListener("mouseleave", () => startProgress());

// Swipe Support for Touch Devices
let touchX = null;
section.addEventListener("touchstart", (e) => {
    touchX = e.touches[0].clientX;
}, {passive: true});

section.addEventListener("touchend", (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) {
        clearTimeout(timer);
        goTo(dx < 0 ? current + 1 : current - 1);
    }
    touchX = null;
}, {passive: true});

// Mobile Menu Toggle Logic
const mobToggle = document.getElementById("mob-toggle");
const mobMenu = document.getElementById("mob-menu");
const mobClose = document.getElementById("mob-close");

function closeMobileMenu() {
    mobMenu.classList.add("hidden");
    mobToggle.setAttribute("aria-expanded", "false");
}

function openMobileMenu() {
    mobMenu.classList.remove("hidden");
    mobToggle.setAttribute("aria-expanded", "true");
}

mobToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = !mobMenu.classList.contains("hidden");
    if (isOpen) closeMobileMenu();
    else openMobileMenu();
});

mobClose.addEventListener("click", closeMobileMenu);

// Close menu when clicking outside or pressing Escape
document.addEventListener("click", (e) => {
    const isOpen = !mobMenu.classList.contains("hidden");
    if (!isOpen) return;
    if (mobMenu.contains(e.target) || mobToggle.contains(e.target)) return;
    closeMobileMenu();
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMobileMenu();
});

mobMenu.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", closeMobileMenu)
);

// Initialize Hero Carousel
startProgress();

// ── About Section Fade-In Observer ──
const aboutFades = document.querySelectorAll(".about-fade");
const fadeObs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
        if (e.isIntersecting) {
            e.target.classList.add("visible");
            fadeObs.unobserve(e.target);
        }
    });
}, {threshold: 0.12});

aboutFades.forEach((el) => fadeObs.observe(el));

// ── Number Counter Animation ──
function animateCount(el) {
    const target = parseInt(el.dataset.target);
    const suffix = el.dataset.suffix || "";
    const duration = 1600;
    const step = 16;
    const increment = target / (duration / step);
    let current = 0;

    const tick = () => {
        current = Math.min(current + increment, target);
        el.textContent = Math.floor(current) + suffix;
        if (current < target) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
}

const statEls = document.querySelectorAll("[data-target]");
let counted = false;

const statObs = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting) && !counted) {
        counted = true;
        statEls.forEach((el, i) => setTimeout(() => animateCount(el), i * 120));
        statObs.disconnect();
    }
}, {threshold: 0.3});

if (document.getElementById("stats-section")) {
    statObs.observe(document.getElementById("stats-section"));
}


const whyRevealEls = document.querySelectorAll(".why-reveal");
const whyObs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
        if (e.isIntersecting) {
            e.target.classList.add("visible");
            whyObs.unobserve(e.target);
        }
    });
}, {threshold: 0.12});

whyRevealEls.forEach((el) => whyObs.observe(el));
// --- 1. INITIAL LOAD LOGIC ---
// Put this high up in your <head> if possible to prevent flashing.
// It checks local storage first. If empty, it checks the OS system preference.
if (
    localStorage.theme === 'dark' ||
    (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

// --- 2. BUTTON TOGGLE LOGIC ---
// This runs after your DOM is loaded and attaches the click event.
document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById('theme-toggle');

    themeToggleBtn.addEventListener('click', () => {
        const htmlEl = document.documentElement;

        // Toggle the class on the HTML element
        if (htmlEl.classList.contains('dark')) {
            htmlEl.classList.remove('dark');
            localStorage.setItem('theme', 'light'); // Save preference
        } else {
            htmlEl.classList.add('dark');
            localStorage.setItem('theme', 'dark'); // Save preference
        }
    });
});
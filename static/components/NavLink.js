
document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll(".navLinks a");
    const toggle = document.querySelector(".nav-toggle");
    const nav = document.getElementById("siteNav");
    const header = document.querySelector(".navbar");

    function setOpen(open) {
        nav?.classList.toggle("is-open", open);
        document.body.classList.toggle("nav-open", open);
        toggle?.setAttribute("aria-expanded", String(open));
        toggle?.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }

    function closeNav() {
        setOpen(false);
    }

    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            document.querySelector(".navLinks a.active")?.classList.remove("active");
            link.classList.add("active");
            closeNav();
        });
    });

    toggle?.addEventListener("click", (event) => {
        event.stopPropagation();
        const open = !nav.classList.contains("is-open");
        setOpen(open);
    });

    document.addEventListener("click", (event) => {
        if (!nav?.classList.contains("is-open")) return;
        if (header?.contains(event.target)) return;
        closeNav();
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeNav();
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) closeNav();
    });
});

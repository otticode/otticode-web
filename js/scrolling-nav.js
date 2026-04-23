// Collapse navbar on scroll
window.addEventListener('scroll', function() {
    var navbar = document.querySelector('#mainNav');
    if (!navbar) return;
    if (window.scrollY > 50) {
        navbar.classList.add('top-nav-collapse');
    } else {
        navbar.classList.remove('top-nav-collapse');
    }
});

// Smooth scroll for page-scroll / nav links and collapse mobile navbar
document.addEventListener('DOMContentLoaded', function() {
    function closeNavbar() {
        var navCollapse = document.querySelector('#navbarCollapse');
        if (!navCollapse) return;
        var bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
        if (!bsCollapse) {
            bsCollapse = new bootstrap.Collapse(navCollapse, { toggle: false });
        }
        if (navCollapse.classList.contains('show')) {
            bsCollapse.hide();
        }
    }

    function smoothScrollTo(targetEl) {
        var offset = 70; // fixed navbar height
        var targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - offset;
        var startPosition = window.pageYOffset;
        var distance = targetPosition - startPosition;
        var duration = 500; // ms
        var startTime = null;

        function animationStep(timestamp) {
            if (!startTime) startTime = timestamp;
            var elapsed = timestamp - startTime;
            var progress = Math.min(elapsed / duration, 1);
            // ease-in-out
            var ease = progress < 0.5
                ? 2 * progress * progress
                : -1 + (4 - 2 * progress) * progress;
            window.scrollTo(0, startPosition + distance * ease);
            if (elapsed < duration) {
                requestAnimationFrame(animationStep);
            }
        }
        requestAnimationFrame(animationStep);
    }

    document.querySelectorAll('a.page-scroll, .navbar-nav a').forEach(function(link) {
        link.addEventListener('click', function(e) {
            var href = this.getAttribute('href');
            if (!href || href === '#') return;
            var target = document.querySelector(href);
            if (!target) return;

            // Prevent default only for internal anchor links
            if (href.startsWith('#')) {
                e.preventDefault();
                smoothScrollTo(target);
                closeNavbar();
            }
        });
    });
});

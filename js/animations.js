document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.animate-on-scroll');

    cards.forEach(function(el, index) {
        el.style.transitionDelay = (index * 0.1).toFixed(1) + 's';
    });

    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(function(el) {
            observer.observe(el);
        });
    } else {
        cards.forEach(function(el) {
            el.classList.add('visible');
        });
    }
});

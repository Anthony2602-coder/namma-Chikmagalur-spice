document.addEventListener('DOMContentLoaded', () => {
    initLoader();
    initCarousel();
    initMobileMenu();
    initScrollAnimations();
    initSearch();
    initHeaderScroll();
});

function initLoader() {
    const loader = document.getElementById('pageLoader');
    if (!loader) return;
    window.addEventListener('load', () => {
        setTimeout(() => loader.classList.add('hidden'), 600);
    });
    setTimeout(() => loader.classList.add('hidden'), 3000);
}

function initCarousel() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.dot');
    if (slides.length <= 1) return;

    let current = 0;
    const show = (index) => {
        slides.forEach((s, i) => s.classList.toggle('active', i === index));
        dots.forEach((d, i) => d.classList.toggle('active', i === index));
        current = index;
    };

    dots.forEach(dot => {
        dot.addEventListener('click', () => show(parseInt(dot.dataset.index)));
    });

    setInterval(() => show((current + 1) % slides.length), 5000);
}

function initMobileMenu() {
    const btn = document.getElementById('mobileMenuBtn');
    const drawer = document.getElementById('mobileDrawer');
    const close = document.getElementById('drawerClose');
    const overlay = document.getElementById('drawerOverlay');
    if (!btn || !drawer) return;

    const toggle = (open) => drawer.classList.toggle('open', open);
    btn.addEventListener('click', () => toggle(true));
    close?.addEventListener('click', () => toggle(false));
    overlay?.addEventListener('click', () => toggle(false));
}

function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    elements.forEach(el => observer.observe(el));
}

function initSearch() {
    const input = document.getElementById('searchInput');
    const suggestions = document.getElementById('searchSuggestions');
    if (!input || !suggestions) return;

    let debounce;
    input.addEventListener('input', () => {
        clearTimeout(debounce);
        const q = input.value.trim();
        if (q.length < 2) {
            suggestions.classList.remove('active');
            return;
        }
        debounce = setTimeout(async () => {
            try {
                const res = await fetch(`/api/search/?q=${encodeURIComponent(q)}`);
                const data = await res.json();
                suggestions.innerHTML = data.results.map(r => `
                    <a href="/product/${r.slug}/" class="search-suggestion-item">
                        ${r.image ? `<img src="${r.image}" alt="">` : ''}
                        <div><strong>${r.name}</strong><br><small>₹${r.price}</small></div>
                    </a>
                `).join('');
                suggestions.classList.toggle('active', data.results.length > 0);
            } catch (e) {
                suggestions.classList.remove('active');
            }
        }, 300);
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !suggestions.contains(e.target)) {
            suggestions.classList.remove('active');
        }
    });
}

function initHeaderScroll() {
    const header = document.getElementById('siteHeader');
    if (!header) return;
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const current = window.scrollY;
        header.style.transform = current > lastScroll && current > 200 ? 'translateY(-100%)' : 'translateY(0)';
        lastScroll = current;
    }, { passive: true });
}

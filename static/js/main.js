class OfertasApp {
    constructor() {
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.loadTheme();
        this.setupEventListeners();
        this.animateCards();
    }

    loadTheme() {
        if (localStorage.getItem('theme') === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
            const icon = document.getElementById('theme-icon');
            if (icon) icon.className = 'fas fa-sun';
        }
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const category = e.currentTarget.getAttribute('data-category');
                this.filterByCategory(category);
            });
        });
    }

    toggleTheme() {
        const body = document.body;
        const icon = document.getElementById('theme-icon');
        
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            icon.className = 'fas fa-moon';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            icon.className = 'fas fa-sun';
            localStorage.setItem('theme', 'dark');
        }
    }

    filterByCategory(category) {
        this.currentFilter = category;
        
        // Update active button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');

        // Show/hide sections
        document.querySelectorAll('.category-section').forEach(section => {
            if (category === 'all') {
                section.classList.remove('hidden');
            } else {
                const sectionCategory = section.getAttribute('data-category');
                if (sectionCategory === category) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            }
        });

        // Re-animate visible cards
        this.animateCards();
    }

    animateCards() {
        const visibleCards = document.querySelectorAll('.category-section:not(.hidden) .product-card');
        
        visibleCards.forEach((card, index) => {
            card.classList.remove('visible');
            setTimeout(() => {
                card.classList.add('visible');
            }, index * 50);
        });
    }

    // Utility method for smooth scrolling
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    // Method to handle image loading errors
    handleImageError(img) {
        img.src = 'https://via.placeholder.com/280x280/6366f1/ffffff?text=Sin+Imagen';
        img.alt = 'Imagen no disponible';
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ofertasApp = new OfertasApp();
    
    // Handle image errors globally
    document.addEventListener('error', (e) => {
        if (e.target.tagName === 'IMG') {
            window.ofertasApp.handleImageError(e.target);
        }
    }, true);
});

// Add scroll to top functionality
window.addEventListener('scroll', () => {
    const scrollButton = document.getElementById('scroll-top');
    if (scrollButton) {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
});
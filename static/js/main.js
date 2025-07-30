class OfertasApp {
    constructor() {
        this.currentFilter = 'moda-mujer';
        this.itemsPerPage = 30;
        this.currentPage = 1;
        this.currentSort = 'none';
        this.init();
    }

    init() {
        this.loadTheme();
        this.setupEventListeners();
        this.setInitialFilter();
        this.updateDisplay();
    }

    setInitialFilter() {
        // Set moda-mujer as active by default
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        const modaMujerBtn = document.querySelector('[data-category="moda-mujer"]');
        if (modaMujerBtn) {
            modaMujerBtn.classList.add('active');
        }
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

        // Filter buttons (both in categories panel and controls)
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const category = e.currentTarget.getAttribute('data-category');
                this.filterByCategory(category);
            });
        });

        // Sort buttons
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const sortType = e.currentTarget.getAttribute('data-sort');
                this.sortProducts(sortType);
            });
        });

        // Pagination buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('page-btn')) {
                const page = parseInt(e.target.dataset.page);
                this.goToPage(page);
            } else if (e.target.classList.contains('prev-btn')) {
                this.goToPage(this.currentPage - 1);
            } else if (e.target.classList.contains('next-btn')) {
                this.goToPage(this.currentPage + 1);
            }
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
        this.currentPage = 1;
        
        // Update active button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-category="${category}"]`).classList.add('active');

        this.updateDisplay();
    }

    sortProducts(sortType) {
        this.currentSort = sortType;
        this.currentPage = 1;
        
        // Update active sort button
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-sort="${sortType}"]`).classList.add('active');

        this.applySorting();
        this.updateDisplay();
    }

    applySorting() {
        if (this.currentSort === 'none') return;

        const sections = document.querySelectorAll('.category-section');
        sections.forEach(section => {
            const grid = section.querySelector('.products-grid');
            const cards = Array.from(grid.querySelectorAll('.product-card'));
            
            cards.sort((a, b) => {
                if (this.currentSort === 'discount') {
                    const discountA = parseInt(a.querySelector('.discount-badge').textContent.replace(/[-%]/g, ''));
                    const discountB = parseInt(b.querySelector('.discount-badge').textContent.replace(/[-%]/g, ''));
                    return discountB - discountA;
                } else if (this.currentSort === 'price') {
                    const priceA = parseFloat(a.querySelector('.price-current').textContent.replace(/[S/.\s,]/g, ''));
                    const priceB = parseFloat(b.querySelector('.price-current').textContent.replace(/[S/.\s,]/g, ''));
                    return priceA - priceB;
                }
                return 0;
            });
            
            cards.forEach(card => grid.appendChild(card));
        });
    }

    animateCards() {
        const visibleCards = document.querySelectorAll('.product-card:not(.hidden)');
        
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

    // Pagination methods
    getAllVisibleCards() {
        if (this.currentFilter === 'all') {
            return document.querySelectorAll('.product-card');
        } else {
            return document.querySelectorAll(`.category-section[data-category="${this.currentFilter}"] .product-card`);
        }
    }

    updateDisplay() {
        const allCards = this.getAllVisibleCards();
        const totalItems = allCards.length;
        const totalPages = Math.ceil(totalItems / this.itemsPerPage);
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;

        // Show/hide sections based on filter
        document.querySelectorAll('.category-section').forEach(section => {
            const sectionCategory = section.getAttribute('data-category');
            const categoryHeader = section.querySelector('.category-header');
            
            if (this.currentFilter === 'all') {
                section.classList.add('hidden');
                if (categoryHeader) categoryHeader.classList.add('hidden');
            } else {
                section.classList.toggle('hidden', sectionCategory !== this.currentFilter);
                if (categoryHeader) categoryHeader.classList.toggle('hidden', sectionCategory !== this.currentFilter);
            }
        });

        // Show/hide cards based on pagination
        allCards.forEach((card, index) => {
            card.classList.toggle('hidden', index < startIndex || index >= endIndex);
        });

        this.updatePagination(totalPages);
        this.animateCards();
        this.scrollToTop();
    }

    updatePagination(totalPages) {
        const paginationContainer = document.querySelector('.pagination');
        if (!paginationContainer || totalPages <= 1) {
            if (paginationContainer) paginationContainer.classList.add('hidden');
            return;
        }

        paginationContainer.classList.remove('hidden');
        const isMobile = window.innerWidth <= 480;
        
        if (isMobile) {
            // Mobile structure
            let paginationHTML = `
                <div class="pagination-controls">
                    <button class="pagination-btn prev-btn" ${this.currentPage === 1 ? 'disabled' : ''}>
                        <i class="fas fa-chevron-left"></i> Anterior
                    </button>
                    <button class="pagination-btn next-btn" ${this.currentPage === totalPages ? 'disabled' : ''}>
                        Siguiente <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
                <div class="pagination-numbers">`;
            
            // Show current page and adjacent pages
            const startPage = Math.max(1, this.currentPage - 1);
            const endPage = Math.min(totalPages, this.currentPage + 1);
            
            if (startPage > 1) {
                paginationHTML += `<button class="pagination-btn page-btn" data-page="1">1</button>`;
                if (startPage > 2) paginationHTML += `<span class="pagination-dots">...</span>`;
            }
            
            for (let i = startPage; i <= endPage; i++) {
                paginationHTML += `<button class="pagination-btn page-btn ${i === this.currentPage ? 'active' : 'adjacent'}" data-page="${i}">${i}</button>`;
            }
            
            if (endPage < totalPages) {
                if (endPage < totalPages - 1) paginationHTML += `<span class="pagination-dots">...</span>`;
                paginationHTML += `<button class="pagination-btn page-btn" data-page="${totalPages}">${totalPages}</button>`;
            }
            
            paginationHTML += `</div>`;
            paginationContainer.innerHTML = paginationHTML;
        } else {
            // Desktop structure
            let paginationHTML = '';
            
            paginationHTML += `<button class="pagination-btn prev-btn" ${this.currentPage === 1 ? 'disabled' : ''}>
                <i class="fas fa-chevron-left"></i>
            </button>`;
            
            const maxVisiblePages = 5;
            let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2));
            let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
            
            if (endPage - startPage + 1 < maxVisiblePages) {
                startPage = Math.max(1, endPage - maxVisiblePages + 1);
            }
            
            if (startPage > 1) {
                paginationHTML += `<button class="pagination-btn page-btn" data-page="1">1</button>`;
                if (startPage > 2) paginationHTML += `<span class="pagination-dots">...</span>`;
            }
            
            for (let i = startPage; i <= endPage; i++) {
                paginationHTML += `<button class="pagination-btn page-btn ${i === this.currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
            }
            
            if (endPage < totalPages) {
                if (endPage < totalPages - 1) paginationHTML += `<span class="pagination-dots">...</span>`;
                paginationHTML += `<button class="pagination-btn page-btn" data-page="${totalPages}">${totalPages}</button>`;
            }
            
            paginationHTML += `<button class="pagination-btn next-btn" ${this.currentPage === totalPages ? 'disabled' : ''}>
                <i class="fas fa-chevron-right"></i>
            </button>`;
            
            paginationContainer.innerHTML = paginationHTML;
        }
    }

    goToPage(page) {
        const totalItems = this.getAllVisibleCards().length;
        const totalPages = Math.ceil(totalItems / this.itemsPerPage);
        
        if (page >= 1 && page <= totalPages) {
            this.currentPage = page;
            this.updateDisplay();
        }
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

// Update pagination on window resize
window.addEventListener('resize', () => {
    if (window.ofertasApp) {
        const totalItems = window.ofertasApp.getAllVisibleCards().length;
        const totalPages = Math.ceil(totalItems / window.ofertasApp.itemsPerPage);
        window.ofertasApp.updatePagination(totalPages);
    }
});
document.addEventListener("DOMContentLoaded", function() {
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    const imageInput = document.getElementById('message-image-input');
    const previewContainer = document.getElementById('image-preview-container');
    const previewImage = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-image-btn');

    if (imageInput && previewContainer && previewImage && removeBtn) {
        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewContainer.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });

        removeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            imageInput.value = '';
            previewContainer.style.display = 'none';
            previewImage.src = '';
        });
    }

    let currentZoom = parseFloat(localStorage.getItem('userZoom')) || 1;
    let isHighContrast = localStorage.getItem('userContrast') === 'true';

    document.body.style.zoom = currentZoom;
    if (isHighContrast) {
        document.documentElement.classList.add('high-contrast');
    }

    const btnIncrease = document.getElementById('btn-increase-font');
    const btnDecrease = document.getElementById('btn-decrease-font');
    const btnReset = document.getElementById('btn-reset-font');
    const btnContrast = document.getElementById('btn-toggle-contrast');

    if (btnIncrease) {
        btnIncrease.addEventListener('click', function () {
            if (currentZoom < 1.3) {
                currentZoom += 0.1;
                document.body.style.zoom = currentZoom;
                localStorage.setItem('userZoom', currentZoom);
            }
        });
    }

    if (btnDecrease) {
        btnDecrease.addEventListener('click', function () {
            if (currentZoom > 0.8) {
                currentZoom -= 0.1;
                document.body.style.zoom = currentZoom;
                localStorage.setItem('userZoom', currentZoom);
            }
        });
    }

    if (btnReset) {
        btnReset.addEventListener('click', function () {
            currentZoom = 1;
            document.body.style.zoom = 1;
            localStorage.setItem('userZoom', 1);
        });
    }

    if (btnContrast) {
        btnContrast.addEventListener('click', function () {
            document.documentElement.classList.toggle('high-contrast');
            const active = document.documentElement.classList.contains('high-contrast');
            localStorage.setItem('userContrast', active);
        });
    }

    const accToggleBtn = document.getElementById('acc-dropdown-toggle');
    const accMenu = document.getElementById('acc-menu');

    if (accToggleBtn && accMenu) {
        accToggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            accMenu.classList.toggle('show');
        });

        document.addEventListener('click', function (e) {
            if (!accMenu.contains(e.target) && e.target !== accToggleBtn) {
                accMenu.classList.remove('show');
            }
        });
    }
});

function flipCard(button) {
    const card = button.closest('.product-card');
    if (card) {
        card.classList.toggle('flipped');
    }
}

function filterProducts() {
    const query = document.getElementById('search-input')?.value.toLowerCase().trim() || '';
    const cards = document.querySelectorAll('.product-card');
    let hasVisibleCard = false;
    cards.forEach(card => {
        const title = card.querySelector('h3')?.innerText.toLowerCase() || '';
        const category = card.querySelector('.product-tybe')?.innerText.toLowerCase() || '';
        const desc = card.querySelector('.product-brief')?.innerText.toLowerCase() || '';

        if (title.includes(query) || category.includes(query) || desc.includes(query)) {
            card.style.display = 'block';
            hasVisibleCard = true;
        } else {
            card.style.display = 'none';
        }
    });

    const container = document.getElementById('products-container');
    let noResultsMsg = document.getElementById('no-results-msg');

    if (!hasVisibleCard) {
        if (!noResultsMsg && container) {
            noResultsMsg = document.createElement('div');
            noResultsMsg.id = 'no-results-msg';
            noResultsMsg.className = 'no-results';
            noResultsMsg.innerText = 'عذراً، لم يتم العثور على منتجات تطابق بحثك.';
            container.appendChild(noResultsMsg);
        }
    } else if (noResultsMsg) {
        noResultsMsg.remove();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const userBtn = document.getElementById('user-dropdown-btn');
    const dropdownMenu = document.getElementById('userDropdownMenu');
    const logoutLink = document.getElementById('logout-link');
    const logoutForm = document.getElementById('logout-form');

    if (userBtn && dropdownMenu) {
        userBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show-dropdown');
        });

        document.addEventListener('click', function (e) {
            if (!dropdownMenu.contains(e.target) && e.target !== userBtn) {
                dropdownMenu.classList.remove('show-dropdown');
            }
        });
    }

    if (logoutLink && logoutForm) {
        logoutLink.addEventListener('click', function (e) {
            e.preventDefault();
            const confirmAction = confirm('هل أنت متأكد من أنك تريد تسجيل الخروج؟');
            if (confirmAction) {
                logoutForm.submit();
            }
        });
    }
});

const menuToggle = document.getElementById('menu-toggle');
const navMenu = document.getElementById('nav-menu');

menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

const userBtn = document.getElementById('user-dropdown-btn');
const userMenu = document.getElementById('userDropdownMenu');

if (userBtn && userMenu) {
    userBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userMenu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
        userMenu.classList.remove('show');
    });
}

function toggleAdminDropdown(event) {
            event.stopPropagation();
            var menu = document.getElementById('adminDropdownMenu');
            menu.classList.toggle('show');
        }

       
        document.addEventListener('click', function(event) {
            var menu = document.getElementById('adminDropdownMenu');
            if (menu && menu.classList.contains('show')) {
                menu.classList.remove('show');
            }
        });
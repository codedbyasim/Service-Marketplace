/*
 * Service-Marketplace/static/js/main.js
 * -------------------------------------
 * Global JavaScript functionalities for the marketplace.
 * Uses vanilla JavaScript primarily, as Bootstrap handles many interactive elements.
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. Auto-Fade Django Messages ---
    const messages = document.querySelectorAll('.alert');
    if (messages.length > 0) {
        messages.forEach(function(message) {
            // Check if the alert is not a persistent error/warning (optional)
            if (!message.classList.contains('alert-danger') && !message.classList.contains('alert-warning')) {
                setTimeout(function() {
                    // Use Bootstrap's own closing mechanism if available
                    if (message.classList.contains('fade')) {
                        const bsAlert = new bootstrap.Alert(message);
                        bsAlert.close();
                    } else {
                        message.style.display = 'none';
                    }
                }, 5000); // Fade out after 5 seconds
            }
        });
    }

    // --- 2. Scroll-to-Top Button Functionality ---
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '&#9650;'; // Up arrow
    scrollToTopBtn.id = 'scrollToTopBtn';
    scrollToTopBtn.classList.add('btn', 'btn-primary', 'shadow-lg');
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: none;
        z-index: 1000;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        font-size: 1.2rem;
        padding: 0;
    `;
    document.body.appendChild(scrollToTopBtn);

    // Show button when scrolling down
    window.onscroll = function() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            scrollToTopBtn.style.display = "block";
        } else {
            scrollToTopBtn.style.display = "none";
        }
    };

    // Scroll to the top when clicked
    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });


    // --- 3. Simple Active Link Highlighting (if using plain HTML links) ---
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        // Check if the link href matches the current URL path
        if (link.href === window.location.href) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });

    // --- 4. Custom Star Rating Input Helper (Example for Review Form) ---
    const ratingSelect = document.getElementById('id_rating'); // Assuming your form field ID is id_rating

    if (ratingSelect) {
        // Add a visual indicator next to the select box
        const ratingDisplay = document.createElement('span');
        ratingDisplay.classList.add('ms-3', 'text-warning', 'fw-bold', 'rating-stars');
        ratingSelect.parentNode.insertBefore(ratingDisplay, ratingSelect.nextSibling);

        function updateRatingDisplay() {
            const ratingValue = parseInt(ratingSelect.value);
            if (ratingValue >= 1 && ratingValue <= 5) {
                // Display stars corresponding to the selected rating
                ratingDisplay.innerHTML = '⭐'.repeat(ratingValue) + ' (' + ratingValue + '/5)';
            } else {
                ratingDisplay.innerHTML = '';
            }
        }

        ratingSelect.addEventListener('change', updateRatingDisplay);
        // Initial update
        updateRatingDisplay();
    }
});
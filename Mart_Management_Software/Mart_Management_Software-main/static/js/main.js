/* Nepal Mart Management Software - Main JavaScript */

document.addEventListener('DOMContentLoaded', function() {

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete/clear actions
    const confirmForms = document.querySelectorAll('[data-confirm]');
    confirmForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm(form.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Quantity input validation
    const qtyInputs = document.querySelectorAll('input[type="number"][name="quantity"]');
    qtyInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const min = parseInt(this.getAttribute('min')) || 1;
            const max = parseInt(this.getAttribute('max')) || 9999;
            let value = parseInt(this.value);

            if (isNaN(value) || value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });

    // Search form - prevent empty submissions
    const searchForms = document.querySelectorAll('form[action*="product"]');
    searchForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const searchInput = form.querySelector('input[name="q"]');
            if (searchInput && searchInput.value.trim() === '') {
                // Allow form submission without search query (shows all products)
            }
        });
    });

    // Tooltip initialization
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

});

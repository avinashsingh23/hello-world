// Concertiv Travel Ops Portal JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirm dialogs for dangerous actions
    var dangerousButtons = document.querySelectorAll('[data-confirm]');
    dangerousButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Loading states for buttons
    var loadingButtons = document.querySelectorAll('[data-loading]');
    loadingButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status"></span>Loading...';
            this.disabled = true;
            
            // Re-enable after 3 seconds (fallback)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });

    // Real-time clock for dashboard
    function updateClock() {
        var now = new Date();
        var timeString = now.toLocaleString();
        var clockElement = document.getElementById('current-time');
        if (clockElement) {
            clockElement.textContent = timeString;
        }
    }
    
    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock();

    // Auto-refresh dashboard every 5 minutes
    if (window.location.pathname === '/') {
        setInterval(function() {
            if (document.visibilityState === 'visible') {
                window.location.reload();
            }
        }, 300000); // 5 minutes
    }

    // File upload validation
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var file = this.files[0];
            if (file) {
                var allowedTypes = ['application/vnd.ms-excel', 
                                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                 'text/csv'];
                var maxSize = 10 * 1024 * 1024; // 10MB
                
                if (!allowedTypes.includes(file.type) && !file.name.match(/\.(xlsx|xls|csv)$/i)) {
                    alert('Please select a valid Excel (.xlsx, .xls) or CSV file.');
                    this.value = '';
                    return;
                }
                
                if (file.size > maxSize) {
                    alert('File size must be less than 10MB.');
                    this.value = '';
                    return;
                }
            }
        });
    });

    // Form validation enhancement
    var forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var isValid = true;
            var requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Table sorting functionality
    var sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            var table = this.closest('table');
            var tbody = table.querySelector('tbody');
            var rows = Array.from(tbody.querySelectorAll('tr'));
            var index = Array.from(this.parentNode.children).indexOf(this);
            var isAscending = this.classList.contains('sort-asc');
            
            // Remove all sort classes
            sortableHeaders.forEach(function(h) {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add appropriate sort class
            this.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
            
            // Sort rows
            rows.sort(function(a, b) {
                var aText = a.cells[index].textContent.trim();
                var bText = b.cells[index].textContent.trim();
                
                // Try to parse as numbers
                var aNum = parseFloat(aText.replace(/[$,]/g, ''));
                var bNum = parseFloat(bText.replace(/[$,]/g, ''));
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return isAscending ? bNum - aNum : aNum - bNum;
                } else {
                    return isAscending ? bText.localeCompare(aText) : aText.localeCompare(bText);
                }
            });
            
            // Reorder rows in DOM
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });

    // Search functionality for tables
    var searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var searchTerm = this.value.toLowerCase();
            var targetTable = document.querySelector(this.dataset.search);
            var rows = targetTable.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Export functionality
    window.exportTableToCSV = function(tableId, filename) {
        var table = document.getElementById(tableId);
        var csv = [];
        var rows = table.querySelectorAll('tr');
        
        for (var i = 0; i < rows.length; i++) {
            var row = [];
            var cols = rows[i].querySelectorAll('td, th');
            
            for (var j = 0; j < cols.length; j++) {
                var text = cols[j].innerText.replace(/"/g, '""');
                row.push('"' + text + '"');
            }
            
            csv.push(row.join(','));
        }
        
        var csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
        var downloadLink = document.createElement('a');
        downloadLink.download = filename || 'export.csv';
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    };

    // Print functionality
    window.printTable = function(tableId) {
        var printWindow = window.open('', '', 'height=600,width=800');
        var table = document.getElementById(tableId);
        
        printWindow.document.write('<html><head><title>Print</title>');
        printWindow.document.write('<style>table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid #ddd; padding: 8px; text-align: left; } th { background-color: #f2f2f2; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write(table.outerHTML);
        printWindow.document.write('</body></html>');
        
        printWindow.document.close();
        printWindow.print();
    };

    // Progress bar for file uploads
    var uploadForms = document.querySelectorAll('form[enctype="multipart/form-data"]');
    uploadForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var submitButton = form.querySelector('button[type="submit"]');
            var originalText = submitButton.innerHTML;
            
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Uploading...';
            submitButton.disabled = true;
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            var searchInput = document.querySelector('input[type="search"], input[data-search]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            var openModal = document.querySelector('.modal.show');
            if (openModal) {
                var modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });

    // Status polling for real-time updates
    function pollStatus() {
        if (window.location.pathname === '/' && document.visibilityState === 'visible') {
            // Poll for status updates every 30 seconds
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    // Update KPIs if they exist
                    updateKPIs(data);
                })
                .catch(error => {
                    console.log('Status polling failed:', error);
                });
        }
    }
    
    function updateKPIs(data) {
        // Update KPI cards with new data
        var kpiElements = {
            'total_requests': document.querySelector('.card.bg-primary .card-title'),
            'received': document.querySelector('.card.bg-success .card-title'),
            'pending': document.querySelector('.card.bg-warning .card-title'),
            'overdue': document.querySelector('.card.bg-danger .card-title')
        };
        
        Object.keys(kpiElements).forEach(function(key) {
            if (kpiElements[key] && data[key] !== undefined) {
                kpiElements[key].textContent = data[key];
            }
        });
    }
    
    // Start status polling
    setInterval(pollStatus, 30000);
});

// Utility functions
window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
};

window.formatDate = function(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

window.showToast = function(message, type = 'info') {
    var toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    var toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    var bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
};
// dashboard.js - Main dashboard functionality

// Risk color mapping - All 4 levels
const riskColors = {
    0: { color: '#28a745', label: 'No Risk', icon: '✓', meaning: 'Safe' },
    1: { color: '#ffc107', label: 'Low', icon: '!', meaning: 'Monitor' },
    2: { color: '#fd7e14', label: 'Medium', icon: '!!', meaning: 'Caution' },
    3: { color: '#dc3545', label: 'High', icon: '!!!', meaning: 'EVACUATE' }
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initialized');
    
    // Fetch districts data
    fetchDistricts();
    
    // Set up event listeners
    setupEventListeners();
});

function fetchDistricts() {
    fetch('/api/districts/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Districts fetched:', data.data);
                window.districts = data.data;
            }
        })
        .catch(error => console.error('Error fetching districts:', error));
}

function fetchPredictions() {
    fetch('/api/predictions/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Predictions fetched:', data.data);
                window.predictions = data.data;
            }
        })
        .catch(error => console.error('Error fetching predictions:', error));
}

function setupEventListeners() {
    // Add any global event listeners here
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Create risk level badge
function createRiskBadge(riskCode) {
    const risk = riskColors[riskCode] || riskColors[0];
    return `<span class="badge" style="background-color: ${risk.color};">${risk.label}</span>`;
}

// Format number with thousands separator
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Convert risk code to percentage
function riskCodeToPercentage(riskCode) {
    return (riskCode / 3) * 100;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show loading spinner
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    }
}

// Hide loading spinner
function hideLoading() {
    // Implement as needed
}

// Display error message
function showError(message, containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="alert alert-danger" role="alert">${message}</div>`;
    }
}

// Display success message
function showSuccess(message, containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="alert alert-success" role="alert">${message}</div>`;
    }
}

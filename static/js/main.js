// AgroControl - Main JavaScript

// API helper
const API = {
    baseURL: window.location.origin,

    async request(url, options = {}) {
        const token = localStorage.getItem('access_token');

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(this.baseURL + url, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Token muddati tugagan
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }

        return response;
    },

    async get(url) {
        return this.request(url, { method: 'GET' });
    },

    async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Auth tekshirish
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const currentPath = window.location.pathname;

    if (!token && !['/login', '/register'].includes(currentPath)) {
        window.location.href = '/login';
    }

    if (token && ['/login', '/register'].includes(currentPath)) {
        window.location.href = '/dashboard';
    }
}

// Sahifa yuklanganda
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

// Global export
window.API = API;

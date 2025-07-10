// API Configuration
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINTS = {
    // Menu endpoints
    categories: '/menu/categories/',
    menuItems: '/menu/menu-items/',
    customizations: '/menu/customizations/',
    
    // Order endpoints
    orders: '/order/orders/',
    
    // Inventory endpoints
    inventoryCategories: '/inventory/categories/',
    inventoryItems: '/inventory/inventory-items/',
    lowStockItems: '/inventory/inventory-items/low-stock/',
    
    // Auth endpoint
    auth: '/api-token-auth/'
};

// API utility class
class API {
    constructor() {
        this.token = localStorage.getItem('authToken');
    }

    // Get authorization headers
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Token ${this.token}`;
        }
        
        return headers;
    }

    // Handle API responses
    async handleResponse(response) {
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    // Generic GET request
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'GET',
                headers: this.getHeaders(),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    }

    // Generic POST request
    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    }

    // Generic PUT request
    async put(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('PUT request failed:', error);
            throw error;
        }
    }

    // Generic PATCH request
    async patch(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PATCH',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('PATCH request failed:', error);
            throw error;
        }
    }

    // Generic DELETE request
    async delete(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'DELETE',
                headers: this.getHeaders(),
            });
            
            if (response.status === 204) {
                return { success: true };
            }
            
            return await this.handleResponse(response);
        } catch (error) {
            console.error('DELETE request failed:', error);
            throw error;
        }
    }

    // Authentication
    async login(username, password) {
        try {
            const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.auth}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            
            const data = await this.handleResponse(response);
            this.token = data.token;
            localStorage.setItem('authToken', this.token);
            return data;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    // Logout
    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Menu API methods
    async getCategories() {
        return await this.get(API_ENDPOINTS.categories);
    }

    async getMenuItems() {
        return await this.get(API_ENDPOINTS.menuItems);
    }

    async getMenuItem(id) {
        return await this.get(`${API_ENDPOINTS.menuItems}${id}/`);
    }

    async createMenuItem(data) {
        return await this.post(API_ENDPOINTS.menuItems, data);
    }

    async updateMenuItem(id, data) {
        return await this.put(`${API_ENDPOINTS.menuItems}${id}/`, data);
    }

    async deleteMenuItem(id) {
        return await this.delete(`${API_ENDPOINTS.menuItems}${id}/`);
    }

    async getCustomizations() {
        return await this.get(API_ENDPOINTS.customizations);
    }

    // Order API methods
    async getOrders() {
        return await this.get(API_ENDPOINTS.orders);
    }

    async getOrder(id) {
        return await this.get(`${API_ENDPOINTS.orders}${id}/`);
    }

    async createOrder(data) {
        return await this.post(API_ENDPOINTS.orders, data);
    }

    async updateOrder(id, data) {
        return await this.put(`${API_ENDPOINTS.orders}${id}/`, data);
    }

    async updateOrderStatus(id, status) {
        return await this.patch(`${API_ENDPOINTS.orders}${id}/`, { status });
    }

    async deleteOrder(id) {
        return await this.delete(`${API_ENDPOINTS.orders}${id}/`);
    }

    // Inventory API methods
    async getInventoryCategories() {
        return await this.get(API_ENDPOINTS.inventoryCategories);
    }

    async getInventoryItems() {
        return await this.get(API_ENDPOINTS.inventoryItems);
    }

    async getInventoryItem(id) {
        return await this.get(`${API_ENDPOINTS.inventoryItems}${id}/`);
    }

    async createInventoryItem(data) {
        return await this.post(API_ENDPOINTS.inventoryItems, data);
    }

    async updateInventoryItem(id, data) {
        return await this.put(`${API_ENDPOINTS.inventoryItems}${id}/`, data);
    }

    async deleteInventoryItem(id) {
        return await this.delete(`${API_ENDPOINTS.inventoryItems}${id}/`);
    }

    async getLowStockItems() {
        return await this.get(API_ENDPOINTS.lowStockItems);
    }
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-remove alert after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }
}

function showLoading(element) {
    element.innerHTML = '<div class="loading">Loading...</div>';
}

function formatCurrency(amount) {
    return `$${parseFloat(amount).toFixed(2)}`;
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function getStatusBadge(status, statusChoices) {
    const statusMap = {
        'A': { class: 'badge-success', text: 'Available' },
        'O': { class: 'badge-danger', text: 'Occupied' },
        'R': { class: 'badge-info', text: 'Received' },
        'P': { class: 'badge-warning', text: 'Preparing' },
        'C': { class: 'badge-success', text: 'Completed' }
    };
    
    const statusInfo = statusMap[status] || { class: 'badge-secondary', text: status };
    return `<span class="badge ${statusInfo.class}">${statusInfo.text}</span>`;
}

// Create global API instance
const api = new API();

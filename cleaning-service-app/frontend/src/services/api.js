const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth methods
  async register(userData) {
    const response = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    if (response.token) {
      localStorage.setItem('token', response.token);
    }
    
    return response;
  }

  async login(credentials) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    if (response.token) {
      localStorage.setItem('token', response.token);
    }
    
    return response;
  }

  async verifyToken() {
    return this.request('/auth/verify');
  }

  logout() {
    localStorage.removeItem('token');
  }

  // User methods
  async getUserProfile() {
    return this.request('/users/profile');
  }

  async updateUserProfile(userData) {
    return this.request('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async changePassword(passwords) {
    return this.request('/users/change-password', {
      method: 'PUT',
      body: JSON.stringify(passwords),
    });
  }

  async getUserBookings(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/users/bookings?${queryString}`);
  }

  async deleteAccount(password) {
    return this.request('/users/account', {
      method: 'DELETE',
      body: JSON.stringify({ password }),
    });
  }

  // Service methods
  async getServices() {
    return this.request('/services');
  }

  async getServiceById(id) {
    return this.request(`/services/${id}`);
  }

  async getServicePricing(id, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/services/${id}/pricing?${queryString}`);
  }

  async checkAvailability(serviceId, date, duration) {
    return this.request(`/services/${serviceId}/availability?date=${date}&duration=${duration}`);
  }

  async getCleaners() {
    return this.request('/services/cleaners');
  }

  // Booking methods
  async createBooking(bookingData) {
    return this.request('/bookings', {
      method: 'POST',
      body: JSON.stringify(bookingData),
    });
  }

  async getBookings(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/bookings?${queryString}`);
  }

  async getBookingById(id) {
    return this.request(`/bookings/${id}`);
  }

  async updateBooking(id, bookingData) {
    return this.request(`/bookings/${id}`, {
      method: 'PUT',
      body: JSON.stringify(bookingData),
    });
  }

  async cancelBooking(id, reason) {
    return this.request(`/bookings/${id}/cancel`, {
      method: 'PUT',
      body: JSON.stringify({ cancellation_reason: reason }),
    });
  }

  // Contact methods
  async submitContactForm(contactData) {
    return this.request('/contact/submit', {
      method: 'POST',
      body: JSON.stringify(contactData),
    });
  }

  // Admin methods (if needed later)
  async getContactMessages(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/contact/messages?${queryString}`);
  }

  async updateContactMessageStatus(id, status) {
    return this.request(`/contact/messages/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async getContactStats() {
    return this.request('/contact/stats');
  }
}

export default new ApiService();

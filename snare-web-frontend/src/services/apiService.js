import Config from '../config/config.js';

class ApiService {
  constructor() {
    this.baseUrl = Config.apiBaseUrl;
    this.timeout = 30000; // 30 seconds timeout
  }

  async makeRequest(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseUrl}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: this.timeout,
    };

    const requestOptions = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    };

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      const response = await fetch(url, {
        ...requestOptions,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout - please check your connection and try again');
      }
      
      if (error.message.includes('fetch')) {
        throw new Error('Unable to connect to server - please check if the backend is running');
      }
      
      throw error;
    }
  }

  async checkListing(url) {
    return this.makeRequest(Config.endpoints.checkListing, {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async checkManualListing(listingData) {
    return this.makeRequest('/check_manual_listing', {
      method: 'POST',
      body: JSON.stringify(listingData),
    });
  }

  async healthCheck() {
    return this.makeRequest(Config.endpoints.health, {
      method: 'GET',
    });
  }
}

// Create singleton instance
const apiService = new ApiService();

export default apiService;

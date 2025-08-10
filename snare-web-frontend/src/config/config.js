// Configuration utility for environment variables
class Config {
  static get apiBaseUrl() {
    return import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
  }

  static get appName() {
    return import.meta.env.VITE_APP_NAME || 'SNARE';
  }

  static get appVersion() {
    return import.meta.env.VITE_APP_VERSION || '1.0.0';
  }

  static get isDevelopment() {
    return import.meta.env.DEV;
  }

  static get isProduction() {
    return import.meta.env.PROD;
  }

  // API endpoints
  static get endpoints() {
    return {
      checkListing: `${this.apiBaseUrl}/check_listing`,
      health: `${this.apiBaseUrl}/`,
    };
  }

  // Log current configuration (for debugging)
  static logConfig() {
    if (this.isDevelopment) {
      console.log('🔧 SNARE Configuration:', {
        apiBaseUrl: this.apiBaseUrl,
        appName: this.appName,
        appVersion: this.appVersion,
        environment: this.isDevelopment ? 'development' : 'production',
        endpoints: this.endpoints,
      });
    }
  }
}

export default Config;

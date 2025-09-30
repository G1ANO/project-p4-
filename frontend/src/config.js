// API Configuration for WiFi Portal Frontend

// Get API URL from environment variable or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Remove trailing slash if present
export const API_BASE_URL = API_URL.replace(/\/$/, '');

// API endpoints
export const API_ENDPOINTS = {
  LOGIN: `${API_BASE_URL}/login`,
  REGISTER: `${API_BASE_URL}/register`,
  PLANS: `${API_BASE_URL}/plans`,
  SUBSCRIPTIONS: `${API_BASE_URL}/subscriptions`,
  USER_SUBSCRIPTIONS: (userId) => `${API_BASE_URL}/subscriptions/${userId}`,
  CANCEL_SUBSCRIPTION: (subId) => `${API_BASE_URL}/subscriptions/${subId}`,
  USERS: `${API_BASE_URL}/users`,
  USER_PLAN_HISTORY: `${API_BASE_URL}/user-plan-history`,
};

// Helper function for API calls with better error handling
export const apiCall = async (url, options = {}) => {
  try {
    console.log(`🌐 API Call: ${options.method || 'GET'} ${url}`);

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    console.log(`📡 Response Status: ${response.status} ${response.statusText}`);

    // Check if response is HTML (error page) instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && !contentType.includes('application/json')) {
      const text = await response.text();
      console.error('❌ Expected JSON but got:', contentType);
      console.error('Response body:', text.substring(0, 200) + '...');
      throw new Error(`Server returned ${contentType} instead of JSON. Check if backend is running.`);
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('🚨 API Call Failed:', error);
    throw error;
  }
};

// Export for debugging
console.log('API Configuration:', {
  API_URL: import.meta.env.VITE_API_URL,
  API_BASE_URL,
  NODE_ENV: import.meta.env.MODE
});

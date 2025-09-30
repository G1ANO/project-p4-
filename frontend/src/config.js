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

// Export for debugging
console.log('API Configuration:', {
  API_URL: import.meta.env.VITE_API_URL,
  API_BASE_URL,
  NODE_ENV: import.meta.env.MODE
});

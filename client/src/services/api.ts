/**
 * API Service - Client-side API communication
 * 
 * This module handles all HTTP requests to the backend server.
 * Uses axios for HTTP client with TypeScript types.
 */

import axios from 'axios';
import type { AxiosInstance } from 'axios';

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: '/api', // Vite proxy handles forwarding to http://localhost:8000/api
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging (development only)
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🔵 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('🔴 API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging (development only)
apiClient.interceptors.response.use(
  (response) => {
    console.log(`🟢 API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('🔴 API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

/**
 * API Service - All backend communication methods
 */
export const api = {
  /**
   * Health Check
   * Verifies the server is running and configured properly
   */
  async healthCheck() {
    const response = await apiClient.get('/health');
    return response.data;
  },

  /**
   * Get Configuration
   * Retrieves server configuration and available features
   */
  async getConfig() {
    const response = await apiClient.get('/config');
    return response.data;
  },

  // Placeholder for future chat endpoint
  // async sendMessage(message: string) {
  //   const response = await apiClient.post('/chat', { message });
  //   return response.data;
  // },
};

export default api;
/**
 * @file apiClient.js
 * @brief Axios HTTP client with JWT authentication and token refresh.
 * 
 * @details Configures axios instance with automatic JWT token injection,
 * token refresh on 401 errors, and request/response interceptors.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * @brief Configured axios instance for API requests.
 * 
 * @details Includes request interceptor for adding JWT tokens and
 * response interceptor for automatic token refresh on expiration.
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor для додавання JWT токену
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor для обробки помилок та оновлення токенів
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Якщо токен протерміновано (401) і ще не намагались оновити
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        // Повторити оригінальний запит з новим токеном
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Якщо не вдалось оновити токен - виходимо
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;

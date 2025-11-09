import apiClient from './apiClient';

// Auth API
export const authAPI = {
  register: (data) => apiClient.post('/auth/register/', data),
  login: (data) => apiClient.post('/auth/login/', data),
  logout: (refreshToken) => apiClient.post('/auth/logout/', { refresh_token: refreshToken }),
  getProfile: () => apiClient.get('/auth/profile/'),
  updateProfile: (data) => apiClient.patch('/auth/profile/', data),
  changePassword: (data) => apiClient.post('/auth/change_password/', data),
};

// Learning Plans API
export const learningAPI = {
  generatePlan: (data) => apiClient.post('/learning/plans/generate/', data),
  getPlans: () => apiClient.get('/learning/plans/'),
  getLessons: (planId) => apiClient.get(`/learning/plans/${planId}/lessons/`),
  getLessonDetail: (lessonId) => apiClient.get(`/learning/lessons/${lessonId}/`),
  completeLesson: (lessonId) => apiClient.post(`/learning/lessons/${lessonId}/complete/`),
};

export default {
  auth: authAPI,
  learning: learningAPI,
};

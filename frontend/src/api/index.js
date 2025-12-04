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
  
  // Quiz API
  generateQuiz: (lessonId, numQuestions = 5) => 
    apiClient.post(`/learning/lessons/${lessonId}/quiz/generate/`, { num_questions: numQuestions }),
  getQuiz: (quizId) => apiClient.get(`/learning/quiz/${quizId}/`),
  submitQuiz: (quizId, answers) => apiClient.post(`/learning/quiz/${quizId}/submit/`, { answers }),
  
  // Notes API
  getNotes: (lessonId) => apiClient.get(`/learning/lessons/${lessonId}/notes/`),
  createNote: (lessonId, content) => 
    apiClient.post(`/learning/lessons/${lessonId}/notes/`, { content }),
  updateNote: (noteId, content) => apiClient.patch(`/learning/notes/${noteId}/`, { content }),
  deleteNote: (noteId) => apiClient.delete(`/learning/notes/${noteId}/`),
  
  // Analytics API
  getAnalytics: () => apiClient.get('/learning/analytics/'),
  
  // Streak API
  getStreak: () => apiClient.get('/learning/streak/'),
};

export default {
  auth: authAPI,
  learning: learningAPI,
};

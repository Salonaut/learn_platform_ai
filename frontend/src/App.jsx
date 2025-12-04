import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import ChangePasswordPage from './pages/ChangePasswordPage';
import PlansListPage from './pages/PlansListPage';
import CreatePlanPage from './pages/CreatePlanPage';
import LessonsListPage from './pages/LessonsListPage';
import LessonDetailPage from './pages/LessonDetailPage';
import QuizPage from './pages/QuizPage';
import AnalyticsPage from './pages/AnalyticsPage';
import StreakPage from './pages/StreakPage';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Layout>
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Protected routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <PlansListPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/change-password"
                element={
                  <ProtectedRoute>
                    <ChangePasswordPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/plans/create"
                element={
                  <ProtectedRoute>
                    <CreatePlanPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/plans/:planId/lessons"
                element={
                  <ProtectedRoute>
                    <LessonsListPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/lessons/:lessonId"
                element={
                  <ProtectedRoute>
                    <LessonDetailPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/quiz/:lessonId"
                element={
                  <ProtectedRoute>
                    <QuizPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/analytics"
                element={
                  <ProtectedRoute>
                    <AnalyticsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/streak"
                element={
                  <ProtectedRoute>
                    <StreakPage />
                  </ProtectedRoute>
                }
              />

              {/* Catch all - redirect to home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Layout>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;

/**
 * @file StreakPage.jsx
 * @brief Study streak tracker with activity heatmap calendar.
 * 
 * @details Displays current streak, longest streak, and GitHub-style
 * activity calendar showing daily learning activity.
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Tooltip,
} from '@mui/material';
import {
  LocalFireDepartment,
  EmojiEvents,
  CalendarMonth,
} from '@mui/icons-material';
import { learningAPI } from '../api';

const StreakPage = () => {
  const [loading, setLoading] = useState(true);
  const [streakData, setStreakData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStreakData();
  }, []);

  const fetchStreakData = async () => {
    try {
      const response = await learningAPI.getStreak();
      setStreakData(response.data);
    } catch (err) {
      setError('Помилка завантаження статистики streak');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStreakMessage = (status) => {
    const messages = {
      active_today: 'Ви навчалися сьогодні!',
      active_yesterday: 'Навчалися вчора',
      active: 'Streak активний',
      inactive: 'Почніть новий streak!',
    };
    return messages[status] || messages.inactive;
  };

  const getHeatColor = (count) => {
    if (count === 0) return '#ebedf0';
    if (count <= 2) return '#9be9a8';
    if (count <= 5) return '#40c463';
    if (count <= 8) return '#30a14e';
    return '#216e39';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('uk-UA', {
      day: 'numeric',
      month: 'short',
    });
  };

  const renderActivityCalendar = () => {
    if (!streakData?.activity_calendar) return null;

    // Group by weeks
    const weeks = [];
    let currentWeek = [];
    
    streakData.activity_calendar.forEach((day, index) => {
      currentWeek.push(day);
      if ((index + 1) % 7 === 0 || index === streakData.activity_calendar.length - 1) {
        weeks.push(currentWeek);
        currentWeek = [];
      }
    });

    return (
      <Box sx={{ overflowX: 'auto', mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Календар активності
        </Typography>
        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
          {weeks.map((week, weekIndex) => (
            <Box key={weekIndex} sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
              {week.map((day) => (
                <Tooltip
                  key={day.date}
                  title={
                    <div>
                      <div>{formatDate(day.date)}</div>
                      <div>Уроків: {day.lessons}</div>
                      <div>Квізів: {day.quizzes}</div>
                      <div>Нотаток: {day.notes}</div>
                      <div>Активність: {day.count}</div>
                    </div>
                  }
                >
                  <Box
                    sx={{
                      width: 12,
                      height: 12,
                      backgroundColor: getHeatColor(day.count),
                      borderRadius: 0.5,
                      cursor: 'pointer',
                      '&:hover': {
                        opacity: 0.8,
                        transform: 'scale(1.2)',
                      },
                      transition: 'all 0.2s',
                    }}
                  />
                </Tooltip>
              ))}
            </Box>
          ))}
        </Box>
        
        {/* Legend */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 2, fontSize: '0.875rem' }}>
          <Typography variant="caption">Менше</Typography>
          {[0, 2, 5, 8, 10].map((val) => (
            <Box
              key={val}
              sx={{
                width: 12,
                height: 12,
                backgroundColor: getHeatColor(val),
                borderRadius: 0.5,
              }}
            />
          ))}
          <Typography variant="caption">Більше</Typography>
        </Box>
      </Box>
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !streakData) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error">{error || 'Дані недоступні'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Study Streak Tracker
        </Typography>

        {/* Status Message */}
        <Alert 
          severity={streakData.streak_status === 'active_today' ? 'success' : 'info'} 
          sx={{ mb: 3 }}
        >
          {getStreakMessage(streakData.streak_status)}
        </Alert>

        {/* Stats Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={4}>
            <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'error.light' }}>
              <LocalFireDepartment sx={{ fontSize: 60, color: 'error.dark', mb: 1 }} />
              <Typography variant="h3" fontWeight="bold">
                {streakData.current_streak}
              </Typography>
              <Typography variant="h6">Поточний streak</Typography>
              <Typography variant="caption">днів підряд</Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={4}>
            <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'warning.light' }}>
              <EmojiEvents sx={{ fontSize: 60, color: 'warning.dark', mb: 1 }} />
              <Typography variant="h3" fontWeight="bold">
                {streakData.longest_streak}
              </Typography>
              <Typography variant="h6">Найдовший streak</Typography>
              <Typography variant="caption">рекорд</Typography>
            </Paper>
          </Grid>

          <Grid item xs={12} sm={4}>
            <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'success.light' }}>
              <CalendarMonth sx={{ fontSize: 60, color: 'success.dark', mb: 1 }} />
              <Typography variant="h3" fontWeight="bold">
                {streakData.total_active_days}
              </Typography>
              <Typography variant="h6">Активних днів</Typography>
              <Typography variant="caption">всього</Typography>
            </Paper>
          </Grid>
        </Grid>

        {/* Activity Calendar */}
        <Paper sx={{ p: 3 }}>
          {renderActivityCalendar()}
        </Paper>

        {/* Motivation */}
        <Paper sx={{ p: 3, mt: 3, textAlign: 'center', bgcolor: 'primary.light' }}>
          <Typography variant="h6" gutterBottom>
            Порада
          </Typography>
          <Typography>
            {streakData.current_streak === 0
              ? 'Почніть свій streak сьогодні! Завершіть хоча б один урок.'
              : streakData.current_streak < 7
              ? 'Продовжуйте! Перші 7 днів - найважчі.'
              : streakData.current_streak < 30
              ? 'Чудово! Ви формуєте звичку навчання.'
              : 'Неймовірно! Ви - справжній майстер постійності!'}
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default StreakPage;

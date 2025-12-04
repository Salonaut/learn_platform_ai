/**
 * @file AnalyticsPage.jsx
 * @brief Progress analytics dashboard component.
 * 
 * @details Displays comprehensive learning statistics including
 * completion rates, time spent, quiz scores, and activity timeline.
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
} from '@mui/material';
import {
  TrendingUp,
  Timer,
  CheckCircle,
  School,
  Stars,
  CalendarToday,
} from '@mui/icons-material';
import { learningAPI } from '../api';

const AnalyticsPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await learningAPI.getAnalytics();
      setAnalytics(response.data);
    } catch (err) {
      setError('Помилка завантаження аналітики');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}г ${mins}хв` : `${mins}хв`;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('uk-UA', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !analytics) {
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
          📊 Аналітика прогресу
        </Typography>

        {/* Statistics Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', bgcolor: 'primary.light' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <School sx={{ mr: 1, color: 'primary.dark' }} />
                  <Typography variant="h6">Плани навчання</Typography>
                </Box>
                <Typography variant="h3">{analytics.total_plans}</Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', bgcolor: 'success.light' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <CheckCircle sx={{ mr: 1, color: 'success.dark' }} />
                  <Typography variant="h6">Завершено уроків</Typography>
                </Box>
                <Typography variant="h3">
                  {analytics.completed_lessons}/{analytics.total_lessons}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', bgcolor: 'warning.light' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Timer sx={{ mr: 1, color: 'warning.dark' }} />
                  <Typography variant="h6">Часу витрачено</Typography>
                </Box>
                <Typography variant="h3">
                  {formatTime(analytics.total_time_spent)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', bgcolor: 'info.light' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Stars sx={{ mr: 1, color: 'info.dark' }} />
                  <Typography variant="h6">Середній бал квізів</Typography>
                </Box>
                <Typography variant="h3">{analytics.average_quiz_score}%</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Overall Progress */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            <TrendingUp sx={{ verticalAlign: 'middle', mr: 1 }} />
            Загальний прогрес
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
            <Box sx={{ flex: 1, mr: 2 }}>
              <LinearProgress
                variant="determinate"
                value={analytics.completion_rate}
                sx={{ height: 20, borderRadius: 1 }}
              />
            </Box>
            <Typography variant="h6">{analytics.completion_rate}%</Typography>
          </Box>
        </Paper>

        <Grid container spacing={3}>
          {/* Plans Progress */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Прогрес по планах
              </Typography>
              <List>
                {analytics.plans_progress.map((plan) => (
                  <React.Fragment key={plan.plan_id}>
                    <ListItem
                      button
                      onClick={() => navigate(`/plans/${plan.plan_id}/lessons`)}
                      sx={{ flexDirection: 'column', alignItems: 'flex-start' }}
                    >
                      <Box sx={{ width: '100%', mb: 1 }}>
                        <Box
                          sx={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                          }}
                        >
                          <Typography variant="subtitle1" fontWeight="bold">
                            {plan.topic}
                          </Typography>
                          <Chip
                            label={`${plan.progress}%`}
                            size="small"
                            color={plan.progress === 100 ? 'success' : 'primary'}
                          />
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          {plan.completed_lessons} з {plan.total_lessons} уроків
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={plan.progress}
                        sx={{ width: '100%', height: 8, borderRadius: 1 }}
                      />
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </Paper>
          </Grid>

          {/* Recent Activity */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                <CalendarToday sx={{ verticalAlign: 'middle', mr: 1 }} />
                Остання активність
              </Typography>
              <List>
                {analytics.recent_activity.length > 0 ? (
                  analytics.recent_activity.map((activity, index) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={activity.lesson_title}
                          secondary={
                            <>
                              <Typography
                                component="span"
                                variant="body2"
                                color="text.primary"
                              >
                                {formatDate(activity.completed_at)}
                              </Typography>
                              {' — '}
                              <Typography
                                component="span"
                                variant="body2"
                                color="text.secondary"
                              >
                                {formatTime(activity.time_spent)}
                              </Typography>
                            </>
                          }
                        />
                        <CheckCircle color="success" />
                      </ListItem>
                      {index < analytics.recent_activity.length - 1 && <Divider />}
                    </React.Fragment>
                  ))
                ) : (
                  <ListItem>
                    <ListItemText
                      primary="Немає завершених уроків"
                      secondary="Почніть навчання, щоб побачити активність"
                    />
                  </ListItem>
                )}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default AnalyticsPage;

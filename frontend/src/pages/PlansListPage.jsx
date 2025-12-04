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
  CardActions,
  Button,
  CircularProgress,
  Alert,
  LinearProgress,
  Chip,
} from '@mui/material';
import { School, AccessTime, TrendingUp } from '@mui/icons-material';
import { learningAPI } from '../api';

const PlansListPage = () => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await learningAPI.getPlans();
      // Бекенд повертає пагінований результат
      const plansData = response.data.results || response.data;
      setPlans(Array.isArray(plansData) ? plansData : []);
    } catch (err) {
      console.error('Error fetching plans:', err);
      setError('Помилка завантаження планів навчання');
      setPlans([]);
    } finally {
      setLoading(false);
    }
  };

  const getKnowledgeLevelLabel = (level) => {
    const labels = {
      beginner: 'Початківець',
      intermediate: 'Середній',
      experienced: 'Досвідчений',
    };
    return labels[level] || level;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Мої плани навчання
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/plans/create')}
          >
            Створити новий план
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {plans.length === 0 ? (
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <School sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              У вас ще немає планів навчання
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Створіть свій перший план навчання з допомогою AI
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate('/plans/create')}
            >
              Створити план
            </Button>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {Array.isArray(plans) && plans.map((plan) => (
              <Grid item xs={12} md={6} key={plan.id}>
                <Card elevation={2}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {plan.topic}
                    </Typography>
                    
                    <Box sx={{ mb: 2 }}>
                      <Chip
                        label={getKnowledgeLevelLabel(plan.knowledge_level)}
                        size="small"
                        color="primary"
                        sx={{ mr: 1 }}
                      />
                      <Chip
                        icon={<AccessTime />}
                        label={`${plan.time_commitment_per_week} год/день`}
                        size="small"
                        variant="outlined"
                      />
                    </Box>

                    <Box sx={{ mb: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">
                          Прогрес
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {plan.progress.toFixed(0)}%
                        </Typography>
                      </Box>
                      <LinearProgress variant="determinate" value={plan.progress} />
                    </Box>

                    <Typography variant="caption" color="text.secondary">
                      Створено: {new Date(plan.created_at).toLocaleDateString('uk-UA')}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => navigate(`/plans/${plan.id}/lessons`)}
                    >
                      Переглянути уроки
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Container>
  );
};

export default PlansListPage;

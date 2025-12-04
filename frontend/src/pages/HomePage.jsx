import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Button,
  Paper,
  Grid,
} from '@mui/material';
import { School, AutoAwesome, TrendingUp } from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const HomePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <School sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
          <Typography variant="h2" component="h1" gutterBottom>
            Learning Platform AI
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            Персоналізовані плани навчання на базі штучного інтелекту
          </Typography>
          <Box sx={{ mt: 4 }}>
            {isAuthenticated ? (
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/dashboard')}
              >
                Мої плани навчання
              </Button>
            ) : (
              <>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/register')}
                  sx={{ mr: 2 }}
                >
                  Почати навчання
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={() => navigate('/login')}
                >
                  Вхід
                </Button>
              </>
            )}
          </Box>
        </Box>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%', textAlign: 'center' }}>
              <AutoAwesome sx={{ fontSize: 50, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                AI-генерація планів
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Опишіть що хочете вивчити, і AI створить персоналізований план навчання
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%', textAlign: 'center' }}>
              <School sx={{ fontSize: 50, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Структуроване навчання
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Отримайте чіткий план з теорією, практичними завданнями та тестами
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%', textAlign: 'center' }}>
              <TrendingUp sx={{ fontSize: 50, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Відстеження прогресу
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Контролюйте свій прогрес та завершуйте уроки крок за кроком
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default HomePage;

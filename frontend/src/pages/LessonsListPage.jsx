import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Alert,
  Chip,
  IconButton,
  Divider,
} from '@mui/material';
import {
  CheckCircle,
  RadioButtonUnchecked,
  AccessTime,
  ArrowBack,
  MenuBook,
  Code,
  Quiz,
  Work,
} from '@mui/icons-material';
import { learningAPI } from '../api';

const LessonsListPage = () => {
  const { planId } = useParams();
  const navigate = useNavigate();
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLessons();
  }, [planId]);

  const fetchLessons = async () => {
    try {
      const response = await learningAPI.getLessons(planId);
      // Бекенд повертає пагінований результат
      const lessonsData = response.data.results || response.data;
      setLessons(Array.isArray(lessonsData) ? lessonsData : []);
    } catch (err) {
      setError('Помилка завантаження уроків');
      setLessons([]);
    } finally {
      setLoading(false);
    }
  };

  const getLessonIcon = (type) => {
    const icons = {
      theory: <MenuBook />,
      practice: <Code />,
      quiz: <Quiz />,
      project: <Work />,
    };
    return icons[type] || <MenuBook />;
  };

  const getLessonTypeLabel = (type) => {
    const labels = {
      theory: 'Теорія',
      practice: 'Практика',
      quiz: 'Тест',
      project: 'Проект',
    };
    return labels[type] || type;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <IconButton onClick={() => navigate('/dashboard')} sx={{ mr: 2 }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" component="h1">
            Уроки плану навчання
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Paper elevation={2}>
          <List>
            {Array.isArray(lessons) && lessons.map((lesson, index) => (
              <React.Fragment key={lesson.id}>
                <ListItem disablePadding>
                  <ListItemButton
                    onClick={() => navigate(`/lessons/${lesson.id}`)}
                  >
                    <ListItemIcon>
                      {lesson.is_completed ? (
                        <CheckCircle color="success" />
                      ) : (
                        <RadioButtonUnchecked color="action" />
                      )}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body1">
                            День {lesson.day_number}: {lesson.title}
                          </Typography>
                        </Box>
                      }
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                          <Chip
                            icon={getLessonIcon(lesson.lesson_type)}
                            label={getLessonTypeLabel(lesson.lesson_type)}
                            size="small"
                            variant="outlined"
                          />
                          <Chip
                            icon={<AccessTime />}
                            label={`${lesson.time_estimate} хв`}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                      }
                    />
                  </ListItemButton>
                </ListItem>
                {index < lessons.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      </Box>
    </Container>
  );
};

export default LessonsListPage;

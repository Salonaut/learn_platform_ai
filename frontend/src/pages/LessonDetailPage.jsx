import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Alert,
  Chip,
  IconButton,
  Divider,
  Link,
} from '@mui/material';
import {
  ArrowBack,
  CheckCircle,
  AccessTime,
  LinkOutlined,
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { learningAPI } from '../api';

const LessonDetailPage = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    fetchLesson();
  }, [lessonId]);

  const fetchLesson = async () => {
    try {
      const response = await learningAPI.getLessonDetail(lessonId);
      setLesson(response.data);
    } catch (err) {
      setError('Помилка завантаження уроку');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteToggle = async () => {
    setCompleting(true);
    try {
      await learningAPI.completeLesson(lessonId);
      // Оновлюємо статус локально
      setLesson({ ...lesson, is_completed: !lesson.is_completed });
    } catch (err) {
      setError('Помилка зміни статусу уроку');
    } finally {
      setCompleting(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!lesson) {
    return (
      <Container maxWidth="md">
        <Alert severity="error" sx={{ mt: 4 }}>
          Урок не знайдено
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <IconButton onClick={() => navigate(-1)} sx={{ mr: 2 }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h4" component="h1">
            День {lesson.day_number}
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Paper elevation={2} sx={{ p: 3 }}>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              {lesson.title}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <Chip
                label={lesson.lesson_type}
                color="primary"
                size="small"
              />
              <Chip
                icon={<AccessTime />}
                label={`${lesson.time_estimate} хвилин`}
                size="small"
                variant="outlined"
              />
              {lesson.is_completed && (
                <Chip
                  icon={<CheckCircle />}
                  label="Завершено"
                  color="success"
                  size="small"
                />
              )}
            </Box>
          </Box>

          <Divider sx={{ mb: 3 }} />

          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Теорія
            </Typography>
            <Box sx={{ 
              '& h1': { fontSize: '1.5rem', mt: 2, mb: 1 },
              '& h2': { fontSize: '1.3rem', mt: 2, mb: 1 },
              '& h3': { fontSize: '1.1rem', mt: 2, mb: 1 },
              '& p': { mb: 1 },
              '& code': { 
                backgroundColor: '#f5f5f5', 
                padding: '2px 6px', 
                borderRadius: '4px',
                fontSize: '0.9em'
              },
              '& pre': { 
                backgroundColor: '#f5f5f5', 
                padding: '12px', 
                borderRadius: '4px',
                overflow: 'auto'
              },
              '& ul, & ol': { pl: 3, mb: 1 },
            }}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {lesson.theory_md}
              </ReactMarkdown>
            </Box>
          </Box>

          <Divider sx={{ mb: 3 }} />

          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Завдання
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
              {lesson.task}
            </Typography>
          </Box>

          {lesson.extra_links && lesson.extra_links.length > 0 && (
            <>
              <Divider sx={{ mb: 3 }} />
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Додаткові матеріали
                </Typography>
                {lesson.extra_links.map((link, index) => (
                  <Box key={index} sx={{ mb: 1 }}>
                    <Link
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                      sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
                    >
                      <LinkOutlined fontSize="small" />
                      {link}
                    </Link>
                  </Box>
                ))}
              </Box>
            </>
          )}

          <Divider sx={{ mb: 3 }} />

          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="contained"
              color={lesson.is_completed ? 'warning' : 'success'}
              size="large"
              onClick={handleCompleteToggle}
              disabled={completing}
              startIcon={completing ? <CircularProgress size={20} /> : <CheckCircle />}
            >
              {lesson.is_completed ? 'Позначити як незавершений' : 'Завершити урок'}
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default LessonDetailPage;

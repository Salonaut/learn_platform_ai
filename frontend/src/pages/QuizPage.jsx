/**
 * @file QuizPage.jsx
 * @brief Quiz page component for taking and submitting quizzes.
 * 
 * @details Displays quiz questions with multiple choice options,
 * handles answer submission, and shows results with explanations.
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Divider,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  CheckCircle,
  Cancel,
  ArrowBack,
  Send,
} from '@mui/icons-material';
import { learningAPI } from '../api';

const QuizPage = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    generateOrFetchQuiz();
  }, [lessonId]);

  const generateOrFetchQuiz = async () => {
    try {
      setLoading(true);
      // This endpoint will return existing quiz or generate new one
      const response = await learningAPI.generateQuiz(lessonId, 5);
      setQuiz(response.data);
    } catch (err) {
      setError('Помилка завантаження квізу');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length !== quiz.questions.length) {
      setError('Будь ласка, дайте відповідь на всі питання');
      return;
    }

    try {
      setLoading(true);
      const response = await learningAPI.submitQuiz(quiz.id, answers);
      setResults(response.data);
      setSubmitted(true);
    } catch (err) {
      setError('Помилка відправки квізу');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'error';
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!quiz) {
    return (
      <Container maxWidth="md">
        <Alert severity="error">Квіз не знайдено</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate(-1)}
            sx={{ mr: 2 }}
          >
            Назад
          </Button>
          <Typography variant="h4" component="h1">
            {quiz.title}
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        {/* Results Summary */}
        {submitted && results && (
          <Paper sx={{ p: 3, mb: 3, bgcolor: 'background.default' }}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h5" gutterBottom>
                Результати
              </Typography>
              <Chip
                label={`${results.score}%`}
                color={getScoreColor(results.score)}
                size="large"
                sx={{ fontSize: '1.5rem', py: 3, px: 2, mb: 2 }}
              />
              <Typography variant="body1">
                Правильних відповідей: {results.correct_count} з {results.total_questions}
              </Typography>
              <LinearProgress
                variant="determinate"
                value={results.score}
                color={getScoreColor(results.score)}
                sx={{ mt: 2, height: 10, borderRadius: 1 }}
              />
            </Box>
          </Paper>
        )}

        {/* Questions */}
        {quiz.questions.map((question, index) => {
          const questionResult = submitted
            ? results.results.find(r => r.question_id === question.id)
            : null;

          return (
            <Card key={question.id} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Питання {index + 1}
                </Typography>
                <Typography variant="body1" sx={{ mb: 2, fontWeight: 500 }}>
                  {question.question_text}
                </Typography>

                <FormControl component="fieldset" fullWidth disabled={submitted}>
                  <RadioGroup
                    value={answers[question.id] || ''}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  >
                    {['A', 'B', 'C', 'D'].map((option) => {
                      const optionText = question[`option_${option.toLowerCase()}`];
                      const isCorrect = questionResult?.correct_answer === option;
                      const isUserAnswer = questionResult?.user_answer === option;

                      return (
                        <FormControlLabel
                          key={option}
                          value={option}
                          control={<Radio />}
                          label={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Typography>{optionText}</Typography>
                              {submitted && isCorrect && (
                                <CheckCircle color="success" sx={{ ml: 1 }} />
                              )}
                              {submitted && isUserAnswer && !isCorrect && (
                                <Cancel color="error" sx={{ ml: 1 }} />
                              )}
                            </Box>
                          }
                          sx={{
                            p: 1,
                            borderRadius: 1,
                            bgcolor: submitted
                              ? isCorrect
                                ? 'success.light'
                                : isUserAnswer
                                ? 'error.light'
                                : 'transparent'
                              : 'transparent',
                          }}
                        />
                      );
                    })}
                  </RadioGroup>
                </FormControl>

                {submitted && questionResult && (
                  <>
                    <Divider sx={{ my: 2 }} />
                    <Box sx={{ bgcolor: 'info.light', p: 2, borderRadius: 1 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Пояснення:
                      </Typography>
                      <Typography variant="body2">
                        {questionResult.explanation}
                      </Typography>
                    </Box>
                  </>
                )}
              </CardContent>
            </Card>
          );
        })}

        {/* Submit Button */}
        {!submitted && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <Button
              variant="contained"
              size="large"
              endIcon={<Send />}
              onClick={handleSubmit}
              disabled={Object.keys(answers).length !== quiz.questions.length}
            >
              Відправити відповіді
            </Button>
          </Box>
        )}

        {submitted && (
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', mt: 3 }}>
            <Button
              variant="contained"
              onClick={() => navigate(-1)}
            >
              Повернутись до уроку
            </Button>
            <Button
              variant="outlined"
              onClick={() => {
                setAnswers({});
                setSubmitted(false);
                setResults(null);
              }}
            >
              Пройти ще раз
            </Button>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default QuizPage;

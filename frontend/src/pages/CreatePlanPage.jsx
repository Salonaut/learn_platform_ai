import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { learningAPI } from '../api';

const CreatePlanPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    prompt: '',
    knowledge_level: 'beginner',
    daily_hours: 1,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await learningAPI.generatePlan(formData);
      const planId = response.data.plan_id;
      navigate(`/plans/${planId}/lessons`);
    } catch (err) {
      setError(err.response?.data?.error || 'Помилка створення плану навчання');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ padding: 4 }}>
          <Typography component="h1" variant="h4" gutterBottom>
            Створити план навчання
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Опишіть що ви хочете вивчити, і AI створить для вас персоналізований план навчання
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="prompt"
              label="Що ви хочете вивчити?"
              name="prompt"
              multiline
              rows={4}
              placeholder="Наприклад: Хочу вивчити основи React та створити свій перший веб-додаток"
              value={formData.prompt}
              onChange={handleChange}
            />

            <FormControl fullWidth margin="normal">
              <InputLabel id="knowledge-level-label">Рівень знань</InputLabel>
              <Select
                labelId="knowledge-level-label"
                id="knowledge_level"
                name="knowledge_level"
                value={formData.knowledge_level}
                label="Рівень знань"
                onChange={handleChange}
              >
                <MenuItem value="beginner">Початківець</MenuItem>
                <MenuItem value="intermediate">Середній</MenuItem>
                <MenuItem value="experienced">Досвідчений</MenuItem>
              </Select>
            </FormControl>

            <TextField
              margin="normal"
              required
              fullWidth
              id="daily_hours"
              label="Годин на день для навчання"
              name="daily_hours"
              type="number"
              inputProps={{ min: 1, max: 24 }}
              value={formData.daily_hours}
              onChange={handleChange}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Згенерувати план'}
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default CreatePlanPage;

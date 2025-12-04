/**
 * @file NotesSection.jsx
 * @brief Component for displaying and managing lesson notes.
 * 
 * @details Allows users to create, edit, and delete personal notes
 * associated with specific lessons.
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  CircularProgress,
  Alert,
  Divider,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Save,
  Cancel,
} from '@mui/icons-material';
import { learningAPI } from '../api';

const NotesSection = ({ lessonId }) => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newNoteContent, setNewNoteContent] = useState('');
  const [editingNoteId, setEditingNoteId] = useState(null);
  const [editContent, setEditContent] = useState('');
  const [showAddNote, setShowAddNote] = useState(false);

  useEffect(() => {
    fetchNotes();
  }, [lessonId]);

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const response = await learningAPI.getNotes(lessonId);
      // Backend returns paginated data: {count, results}
      const notesData = response.data.results || response.data;
      setNotes(notesData);
    } catch (err) {
      setError('Помилка завантаження нотаток');
      console.error('Error fetching notes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = async () => {
    if (!newNoteContent.trim()) {
      setError('Нотатка не може бути порожньою');
      return;
    }

    try {
      await learningAPI.createNote(lessonId, newNoteContent);
      setNewNoteContent('');
      setShowAddNote(false);
      await fetchNotes();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.response?.data?.content?.[0] || 'Помилка створення нотатки';
      setError(errorMsg);
      console.error('Error creating note:', err.response?.data);
    }
  };

  const handleUpdateNote = async (noteId) => {
    if (!editContent.trim()) {
      setError('Нотатка не може бути порожньою');
      return;
    }

    try {
      await learningAPI.updateNote(noteId, editContent);
      setEditingNoteId(null);
      setEditContent('');
      fetchNotes();
    } catch (err) {
      setError('Помилка оновлення нотатки');
      console.error(err);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('Ви впевнені, що хочете видалити цю нотатку?')) {
      return;
    }

    try {
      await learningAPI.deleteNote(noteId);
      fetchNotes();
    } catch (err) {
      setError('Помилка видалення нотатки');
      console.error(err);
    }
  };

  const startEditing = (note) => {
    setEditingNoteId(note.id);
    setEditContent(note.content);
  };

  const cancelEditing = () => {
    setEditingNoteId(null);
    setEditContent('');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('uk-UA', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ p: 3, mt: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">📝 Мої нотатки</Typography>
        {!showAddNote && (
          <Button
            variant="contained"
            startIcon={<Add />}
            size="small"
            onClick={() => setShowAddNote(true)}
          >
            Додати нотатку
          </Button>
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Add New Note Form */}
      {showAddNote && (
        <Box sx={{ mb: 3, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
          <TextField
            fullWidth
            multiline
            rows={4}
            placeholder="Введіть вашу нотатку..."
            value={newNoteContent}
            onChange={(e) => setNewNoteContent(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleCreateNote}
              disabled={!newNoteContent.trim()}
            >
              Зберегти
            </Button>
            <Button
              variant="outlined"
              startIcon={<Cancel />}
              onClick={() => {
                setShowAddNote(false);
                setNewNoteContent('');
              }}
            >
              Скасувати
            </Button>
          </Box>
        </Box>
      )}

      {/* Notes List */}
      {notes.length > 0 ? (
        <List>
          {notes.map((note, index) => (
            <React.Fragment key={note.id}>
              <ListItem
                alignItems="flex-start"
                sx={{
                  flexDirection: 'column',
                  bgcolor: 'background.default',
                  borderRadius: 1,
                  mb: 1,
                }}
              >
                {editingNoteId === note.id ? (
                  // Edit Mode
                  <Box sx={{ width: '100%' }}>
                    <TextField
                      fullWidth
                      multiline
                      rows={4}
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      sx={{ mb: 2 }}
                    />
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button
                        size="small"
                        variant="contained"
                        startIcon={<Save />}
                        onClick={() => handleUpdateNote(note.id)}
                      >
                        Зберегти
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={<Cancel />}
                        onClick={cancelEditing}
                      >
                        Скасувати
                      </Button>
                    </Box>
                  </Box>
                ) : (
                  // View Mode
                  <>
                    <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between' }}>
                      <ListItemText
                        primary={note.content}
                        secondary={
                          <>
                            Створено: {formatDate(note.created_at)}
                            {note.updated_at !== note.created_at && (
                              <> • Оновлено: {formatDate(note.updated_at)}</>
                            )}
                          </>
                        }
                        primaryTypographyProps={{
                          style: { whiteSpace: 'pre-wrap' },
                        }}
                      />
                      <Box>
                        <IconButton
                          size="small"
                          onClick={() => startEditing(note)}
                          color="primary"
                        >
                          <Edit />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteNote(note.id)}
                          color="error"
                        >
                          <Delete />
                        </IconButton>
                      </Box>
                    </Box>
                  </>
                )}
              </ListItem>
              {index < notes.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      ) : (
        <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
          Поки що немає нотаток. Додайте свою першу нотатку!
        </Typography>
      )}
    </Paper>
  );
};

export default NotesSection;

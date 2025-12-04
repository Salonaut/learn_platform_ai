from django.urls import path

from . import views


urlpatterns = [
    # Learning Plans
    path('plans/generate/', views.LearningPlanGenerateView.as_view(), name='generate_plan'),
    path('plans/', views.ListLearningPlanView.as_view(), name='list_plans'),
    path('plans/<int:pk>/lessons/', views.LessonListView.as_view(), name='list_lessons'),
    
    # Lessons
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:lesson_id>/complete/', views.LessonCompleteView.as_view(), name='lesson_complete'),
    
    # Quiz System
    path('lessons/<int:lesson_id>/quiz/generate/', views.QuizGenerateView.as_view(), name='quiz_generate'),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.QuizSubmitView.as_view(), name='quiz_submit'),
    
    # Notes System
    path('lessons/<int:lesson_id>/notes/', views.LessonNotesView.as_view(), name='lesson_notes'),
    path('notes/<int:pk>/', views.LessonNoteDetailView.as_view(), name='note_detail'),
    
    # Progress Analytics
    path('analytics/', views.ProgressAnalyticsView.as_view(), name='progress_analytics'),
    
    # Study Streak
    path('streak/', views.StudyStreakView.as_view(), name='study_streak'),
]

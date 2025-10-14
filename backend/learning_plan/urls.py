from django.urls import path

from . import views


urlpatterns = [
    path('plans/generate/', views.LearningPlanGenerateView.as_view(), name='generate_plan'),
    path('plans/', views.ListLearningPlanView.as_view(), name='list_plans'),
    path('plans/<int:pk>/lessons/', views.LessonListView.as_view(), name='list_lessons'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
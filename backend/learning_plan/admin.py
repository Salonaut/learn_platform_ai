from django.contrib import admin
from .models import LearningPlan, Lesson, UserProgress, Quiz, QuizQuestion, QuizAttempt, LessonNote, StudyStreak


@admin.register(LearningPlan)
class LearningPlanAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'knowledge_level', 'progress', 'created_at')
    list_filter = ('knowledge_level', 'created_at')
    search_fields = ('topic', 'user__email')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'plan', 'lesson_type', 'day_number', 'time_estimate')
    list_filter = ('lesson_type',)
    search_fields = ('title', 'plan__topic')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'time_spent', 'completed_at')
    list_filter = ('is_completed', 'completed_at')
    search_fields = ('user__email', 'lesson__title')


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'created_at')
    search_fields = ('title', 'lesson__title')
    inlines = [QuizQuestionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('user__email', 'quiz__title')


@admin.register(LessonNote)
class LessonNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'lesson__title', 'content')


@admin.register(StudyStreak)
class StudyStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'lessons_completed', 'quizzes_taken', 'notes_created', 'activity_score')
    list_filter = ('date',)
    search_fields = ('user__email',)
    readonly_fields = ('activity_score',)

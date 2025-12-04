from rest_framework import serializers

from .models import (
    LearningPlan, Lesson, UserProgress, 
    Quiz, QuizQuestion, QuizAttempt, LessonNote, StudyStreak
)



class LearningPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPlan
        fields = ('id', "topic", "progress", "created_at", "knowledge_level", "time_commitment_per_week")



class LessonItemSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', "title", "day_number", "time_estimate", "lesson_type", "is_completed")

    def get_is_completed(self, obj):
        user = self.context.get('user')
        if not user:
            return False
        return UserProgress.objects.filter(user=user, lesson=obj, is_completed=True).exists()



class LessonDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'theory_md',
            'task',
            'lesson_type',
            'time_estimate',
            'extra_links',
            'day_number',
            'is_completed'
        )

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if not request or not request.user:
            return False
        return UserProgress.objects.filter(user=request.user, lesson=obj, is_completed=True).exists()


class QuizQuestionSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions."""
    class Meta:
        model = QuizQuestion
        fields = ('id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'explanation')


class QuizQuestionWithAnswerSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions including correct answer (for results)."""
    class Meta:
        model = QuizQuestion
        fields = ('id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation')


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz with questions."""
    questions = QuizQuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ('id', 'lesson', 'title', 'created_at', 'questions', 'question_count')
    
    def get_question_count(self, obj):
        return obj.questions.count()


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Serializer for quiz attempts."""
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = ('id', 'quiz', 'quiz_title', 'score', 'answers', 'completed_at')
        read_only_fields = ('score', 'completed_at')


class QuizSubmitSerializer(serializers.Serializer):
    """Serializer for submitting quiz answers."""
    answers = serializers.JSONField(help_text="Dictionary of {question_id: 'A'/'B'/'C'/'D'}")


class LessonNoteSerializer(serializers.ModelSerializer):
    """Serializer for lesson notes."""
    class Meta:
        model = LessonNote
        fields = ('id', 'lesson', 'content', 'created_at', 'updated_at')
        read_only_fields = ('lesson', 'created_at', 'updated_at')


class ProgressAnalyticsSerializer(serializers.Serializer):
    """Serializer for progress analytics data."""
    total_plans = serializers.IntegerField()
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    total_time_spent = serializers.IntegerField(help_text="Total minutes")
    completion_rate = serializers.FloatField(help_text="Percentage")
    average_quiz_score = serializers.FloatField()
    recent_activity = serializers.ListField()
    plans_progress = serializers.ListField()


class StudyStreakSerializer(serializers.ModelSerializer):
    """Serializer for study streak data."""
    activity_score = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = StudyStreak
        fields = ('id', 'date', 'lessons_completed', 'quizzes_taken', 'notes_created', 'total_time_spent', 'activity_score')


class StreakStatsSerializer(serializers.Serializer):
    """Serializer for streak statistics."""
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    total_active_days = serializers.IntegerField()
    activity_calendar = serializers.ListField()
    streak_status = serializers.CharField()
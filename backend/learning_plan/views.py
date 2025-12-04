"""
@file views.py
@brief API views for learning plan management.

This module contains REST API views for managing learning plans,
lessons, and tracking user progress.
"""

from django.utils import timezone

from django.db.models import Count, Avg, Sum, Q

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import (
    LearningPlan, Lesson, UserProgress, 
    Quiz, QuizQuestion, QuizAttempt, LessonNote, StudyStreak
)
from .serializers import (
    LearningPlanSerializer, LessonItemSerializer, LessonDetailSerializer,
    QuizSerializer, QuizQuestionWithAnswerSerializer, QuizAttemptSerializer,
    QuizSubmitSerializer, LessonNoteSerializer, ProgressAnalyticsSerializer,
    StudyStreakSerializer, StreakStatsSerializer
)
from .services import generate_learning_plan, generate_quiz_questions


class ListLearningPlanView(ListAPIView):
    """
    @brief API view to list all learning plans for the authenticated user.
    
    @details Returns a list of all learning plans created by the current user.
    Requires authentication.
    """
    serializer_class = LearningPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        @brief Filter learning plans for the current user.
        @return QuerySet of LearningPlan objects belonging to the authenticated user.
        """
        return LearningPlan.objects.filter(user=self.request.user)


class LessonListView(ListAPIView):
    """
    @brief API view to list all lessons in a specific learning plan.
    
    @details Returns lessons for a given plan ID. Includes user progress
    information in the serializer context.
    """
    serializer_class = LessonItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        @brief Get lessons for a specific plan.
        @return QuerySet of Lesson objects for the given plan ID.
        """
        plan_id = self.kwargs.get('pk')
        return Lesson.objects.filter(plan_id=plan_id)

    def get_serializer_context(self):
        """
        @brief Add user context to serializer.
        @return Dictionary with user information for the serializer.
        """
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class LessonDetailView(RetrieveAPIView):
    """
    @brief API view to retrieve detailed information about a specific lesson.
    
    @details Provides full lesson details including theory, tasks, and user progress.
    Only accessible to the owner of the learning plan.
    """
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        @brief Filter lessons to only those owned by the authenticated user.
        @return QuerySet of Lesson objects.
        """
        return Lesson.objects.filter(plan__user=self.request.user)


class LearningPlanGenerateView(APIView):
    """
    @brief API view to generate a new AI-powered learning plan.
    
    @details Accepts user input (topic, knowledge level, time commitment)
    and uses AI to generate a structured learning plan with lessons.
    
    @see generate_learning_plan
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        @brief Generate a new learning plan based on user input.
        
        @param request HTTP request containing:
            - prompt: The learning topic
            - knowledge_level: User's current knowledge level
            - daily_hours: Time commitment per week
        
        @return Response with plan_id on success or error message on failure.
        
        @throws HTTP_500_INTERNAL_SERVER_ERROR if AI generation fails.
        """
        prompt = request.data.get('prompt')
        knowledge_level = request.data.get('knowledge_level')
        daily_hours = request.data.get('daily_hours')

        plan_data = generate_learning_plan(prompt, knowledge_level, daily_hours)
        if not plan_data:
            return Response({"error": "Failed to generate learning plan."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        learning_plan = LearningPlan.objects.create(
            user=request.user,
            topic=prompt,
            time_commitment_per_week=daily_hours,
            knowledge_level=knowledge_level,
        )


        for index, item_data in enumerate(plan_data):
            Lesson.objects.create(
                plan=learning_plan,
                title=item_data.get('title'),
                theory_md=item_data.get('theory_md'),
                task=item_data.get('task'),
                lesson_type=item_data.get('task_type'),
                time_estimate=item_data.get('time_estimate'),
                extra_links=item_data.get('extra_links'),
                day_number=item_data.get('day')
            )


        return Response({
            "message": "Learning plan was successfully created. ", "plan_id": learning_plan.id
        }, status=status.HTTP_201_CREATED)


class LessonCompleteView(GenericAPIView):
    """
    @brief API view to toggle lesson completion status.
    
    @details Marks a lesson as completed or incomplete, updates timestamps,
    and recalculates the overall learning plan progress.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lesson_id):
        """
        @brief Toggle completion status for a specific lesson.
        
        @param request HTTP request object
        @param lesson_id ID of the lesson to update
        
        @return Response containing lesson_id, completion status, and updated progress
        
        @throws HTTP_404_NOT_FOUND if lesson doesn't exist or user doesn't own it
        """
        try:
            lesson = Lesson.objects.get(pk=lesson_id, plan__user=request.user)
        except Lesson.DoesNotExist:
            return Response({
                "detail": "Lesson not found. "
            }, status=status.HTTP_404_NOT_FOUND)


        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

        progress.is_completed = not progress.is_completed
        progress.completed_at = timezone.now() if progress.is_completed else None
        
        # Set time_spent to lesson's time_estimate when completing
        if progress.is_completed and progress.time_spent == 0:
            progress.time_spent = lesson.time_estimate
        
        progress.save()

        lesson.plan.calculate_progress()
        
        # Update study streak if lesson completed
        if progress.is_completed:
            today = timezone.now().date()
            streak, _ = StudyStreak.objects.get_or_create(
                user=request.user,
                date=today,
                defaults={'lessons_completed': 0}
            )
            streak.lessons_completed += 1
            streak.save()

        return Response({
            'lesson_id': lesson.id,
            'is_completed': progress.is_completed,
            'progress': lesson.plan.progress
        }, status=status.HTTP_200_OK)


class QuizGenerateView(APIView):
    """
    @brief API view to generate AI quiz for a lesson.
    
    @details Creates a quiz with multiple-choice questions based on lesson theory.
    Uses AI to generate relevant questions automatically.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lesson_id):
        """
        @brief Generate quiz questions for a specific lesson.
        
        @param request HTTP request object
        @param lesson_id ID of the lesson to create quiz for
        
        @return Response with quiz data or error message
        """
        try:
            lesson = Lesson.objects.get(pk=lesson_id, plan__user=request.user)
        except Lesson.DoesNotExist:
            return Response({
                "detail": "Lesson not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if quiz already exists
        existing_quiz = Quiz.objects.filter(lesson=lesson).first()
        if existing_quiz:
            serializer = QuizSerializer(existing_quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Generate quiz questions using AI
        try:
            num_questions = request.data.get('num_questions', 5)
            questions_data = generate_quiz_questions(
                lesson.theory_md,
                lesson.title,
                num_questions
            )

            # Create quiz and questions
            quiz = Quiz.objects.create(
                lesson=lesson,
                title=f"Quiz: {lesson.title}"
            )

            for q_data in questions_data:
                QuizQuestion.objects.create(
                    quiz=quiz,
                    question_text=q_data['question'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'].upper(),
                    explanation=q_data.get('explanation', '')
                )

            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": f"Failed to generate quiz: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuizDetailView(RetrieveAPIView):
    """
    @brief API view to retrieve quiz details.
    
    @details Returns quiz with all questions (without correct answers).
    """
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(lesson__plan__user=self.request.user)


class QuizSubmitView(APIView):
    """
    @brief API view to submit quiz answers and get results.
    
    @details Accepts user answers, calculates score, and returns results
    with correct answers and explanations.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        """
        @brief Submit quiz answers and calculate score.
        
        @param request HTTP request with answers
        @param quiz_id ID of the quiz being submitted
        
        @return Response with score, correct answers, and explanations
        """
        try:
            quiz = Quiz.objects.get(pk=quiz_id, lesson__plan__user=request.user)
        except Quiz.DoesNotExist:
            return Response({
                "detail": "Quiz not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = QuizSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_answers = serializer.validated_data['answers']
        
        # Calculate score
        questions = quiz.questions.all()
        total_questions = questions.count()
        correct_count = 0
        results = []

        for question in questions:
            question_id = str(question.id)
            user_answer = user_answers.get(question_id, '').upper()
            is_correct = user_answer == question.correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_id': question.id,
                'question': question.question_text,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation
            })

        score = (correct_count / total_questions * 100) if total_questions > 0 else 0

        # Save attempt
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            answers=user_answers
        )

        # Track streak - increment quizzes_taken
        today = timezone.now().date()
        streak, created = StudyStreak.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={'quizzes_taken': 1}
        )
        if not created:
            streak.quizzes_taken += 1
            streak.save()

        return Response({
            'score': round(score, 2),
            'correct_count': correct_count,
            'total_questions': total_questions,
            'results': results
        }, status=status.HTTP_200_OK)


class LessonNotesView(ListCreateAPIView):
    """
    @brief API view to list and create lesson notes.
    
    @details Allows users to create and view their personal notes for lessons.
    """
    serializer_class = LessonNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return LessonNote.objects.filter(
            user=self.request.user,
            lesson_id=lesson_id
        )

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        serializer.save(user=self.request.user, lesson_id=lesson_id)
        
        # Track streak - increment notes_created
        today = timezone.now().date()
        streak, created = StudyStreak.objects.get_or_create(
            user=self.request.user,
            date=today,
            defaults={'notes_created': 1}
        )
        if not created:
            streak.notes_created += 1
            streak.save()


class LessonNoteDetailView(RetrieveUpdateDestroyAPIView):
    """
    @brief API view to retrieve, update, or delete a specific note.
    """
    serializer_class = LessonNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LessonNote.objects.filter(user=self.request.user)


class ProgressAnalyticsView(APIView):
    """
    @brief API view to get detailed progress analytics.
    
    @details Provides comprehensive statistics about user's learning progress,
    including completion rates, time spent, quiz scores, and activity timeline.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        @brief Get comprehensive progress analytics for the user.
        
        @return Response with analytics data including:
            - Total plans, lessons, completion rates
            - Time spent learning
            - Quiz performance
            - Recent activity
            - Per-plan progress breakdown
        """
        user = request.user

        # Get all user's plans
        plans = LearningPlan.objects.filter(user=user)
        total_plans = plans.count()

        # Get all lessons across all plans
        all_lessons = Lesson.objects.filter(plan__user=user)
        total_lessons = all_lessons.count()

        # Get completed lessons
        completed_progress = UserProgress.objects.filter(
            user=user,
            is_completed=True
        )
        completed_lessons = completed_progress.count()

        # Calculate completion rate
        completion_rate = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        # Total time spent
        total_time_spent = completed_progress.aggregate(
            total=Sum('time_spent')
        )['total'] or 0

        # Average quiz score
        quiz_attempts = QuizAttempt.objects.filter(user=user)
        avg_quiz_score = quiz_attempts.aggregate(
            avg=Avg('score')
        )['avg'] or 0

        # Recent activity (last 10 completed lessons)
        recent_activity = []
        recent_completions = UserProgress.objects.filter(
            user=user,
            is_completed=True
        ).select_related('lesson').order_by('-completed_at')[:10]

        for progress in recent_completions:
            recent_activity.append({
                'lesson_title': progress.lesson.title,
                'completed_at': progress.completed_at,
                'time_spent': progress.time_spent
            })

        # Per-plan progress
        plans_progress = []
        for plan in plans:
            plan_lessons = plan.items.count()
            plan_completed = UserProgress.objects.filter(
                user=user,
                lesson__plan=plan,
                is_completed=True
            ).count()
            
            plans_progress.append({
                'plan_id': plan.id,
                'topic': plan.topic,
                'progress': plan.progress,
                'total_lessons': plan_lessons,
                'completed_lessons': plan_completed,
                'created_at': plan.created_at
            })

        analytics_data = {
            'total_plans': total_plans,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'total_time_spent': total_time_spent,
            'completion_rate': round(completion_rate, 2),
            'average_quiz_score': round(avg_quiz_score, 2),
            'recent_activity': recent_activity,
            'plans_progress': plans_progress
        }

        serializer = ProgressAnalyticsSerializer(analytics_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudyStreakView(APIView):
    """
    @brief API view to get study streak statistics and activity calendar.
    
    @details Provides streak information including current streak, longest streak,
    and activity heatmap data for visualization.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        @brief Get study streak statistics.
        
        @return Response with streak stats and activity calendar data
        """
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        user = request.user
        today = timezone.now().date()
        
        # Get all user's study streaks
        streaks = StudyStreak.objects.filter(user=user).order_by('-date')
        
        if not streaks.exists():
            return Response({
                'current_streak': 0,
                'longest_streak': 0,
                'total_active_days': 0,
                'activity_calendar': [],
                'streak_status': 'inactive'
            })
        
        # Calculate current streak
        current_streak = 0
        check_date = today
        
        for i in range(365):  # Check up to 1 year
            if streaks.filter(date=check_date).exists():
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # Calculate longest streak
        all_dates = list(streaks.values_list('date', flat=True))
        longest_streak = 0
        temp_streak = 1
        
        for i in range(len(all_dates) - 1):
            if (all_dates[i] - all_dates[i + 1]).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak, current_streak)
        
        # Get activity calendar for last 365 days
        start_date = today - timedelta(days=364)
        activity_calendar = []
        
        for i in range(365):
            date = start_date + timedelta(days=i)
            streak = streaks.filter(date=date).first()
            
            activity_calendar.append({
                'date': date.isoformat(),
                'count': streak.activity_score if streak else 0,
                'lessons': streak.lessons_completed if streak else 0,
                'quizzes': streak.quizzes_taken if streak else 0,
                'notes': streak.notes_created if streak else 0,
            })
        
        # Determine streak status
        last_activity = streaks.first().date
        days_since_activity = (today - last_activity).days
        
        if days_since_activity == 0:
            streak_status = 'active_today'
        elif days_since_activity == 1 and current_streak > 0:
            streak_status = 'active_yesterday'
        elif current_streak > 0:
            streak_status = 'active'
        else:
            streak_status = 'inactive'
        
        stats_data = {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'total_active_days': streaks.count(),
            'activity_calendar': activity_calendar,
            'streak_status': streak_status
        }
        
        serializer = StreakStatsSerializer(stats_data)
        return Response(serializer.data, status=status.HTTP_200_OK)












"""
@file views.py
@brief API views for learning plan management.

This module contains REST API views for managing learning plans,
lessons, and tracking user progress.
"""

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import LearningPlan, Lesson, UserProgress
from .serializers import LearningPlanSerializer, LessonItemSerializer, LessonDetailSerializer
from .services import generate_learning_plan


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


        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

        progress.is_completed = not progress.is_completed
        progress.completed_at = timezone.now() if progress.is_completed else None
        progress.save()

        lesson.plan.calculate_progress()


        return Response({
            'lesson_id': lesson.id,
            'is_completed': progress.is_completed,
            'progress': lesson.plan.progress
        }, status=status.HTTP_200_OK)












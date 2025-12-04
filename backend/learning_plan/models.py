"""
@file models.py
@brief Models for learning plan management system.

This module contains Django models for managing learning plans, lessons, and user progress.
"""

from django.db import models
from django.conf import settings


class LearningPlan(models.Model):
    """
    @brief Main model representing a personalized learning plan for a user.
    
    @details LearningPlan stores information about a user's learning journey,
    including the topic, knowledge level, time commitment, and overall progress.
    Each plan contains multiple lessons and tracks completion status.
    
    @see Lesson
    @see UserProgress
    """
    KNOWLEDGE_LEVEL_CHOICES = [
        ('beginner', "Beginner"),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learn_plan')
    topic = models.CharField(max_length=255)
    time_commitment_per_week = models.IntegerField(default=5)
    knowledge_level = models.CharField(
        choices=KNOWLEDGE_LEVEL_CHOICES,
        default='beginner'
        )
    progress = models.FloatField(default=0.00, help_text='Progress %')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """
        @brief String representation of the learning plan.
        @return The topic name of the learning plan.
        """
        return self.topic

    def calculate_progress(self):
        """
        @brief Calculate and update the completion progress for this learning plan.
        
        @details This method calculates the percentage of completed lessons
        by comparing completed lessons to total lessons. Updates the progress
        field and saves the model.
        
        @return Progress percentage as a float (0.0 to 100.0).
        
        @example
        plan = LearningPlan.objects.get(id=1)
        current_progress = plan.calculate_progress()
        print(f"Progress: {current_progress}%")
        """
        total_lessons = self.items.count()
        if total_lessons == 0:
            return 0.0

        completed_lessons = UserProgress.objects.filter(
            lesson__plan=self,
            user=self.user,
            is_completed=True
        ).count()

        progress_percentage = (completed_lessons / total_lessons) * 100
        self.progress = round(progress_percentage, 2)
        self.save(update_fields=['progress'])
        return self.progress




class Lesson(models.Model):
    """
    @brief Model representing a single lesson within a learning plan.
    
    @details Each lesson contains educational content in Markdown format,
    associated tasks, time estimates, and type classification (theory,
    practice, quiz, or project).
    
    @see LearningPlan
    """
    ITEM_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practice', 'Practice'),
        ('quiz', 'Quiz'),
        ('project',  'Project'),
    ]


    plan = models.ForeignKey(LearningPlan, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255) # gpt response
    theory_md = models.TextField()  # теорія в Markdown
    task = models.TextField()
    lesson_type = models.CharField(choices=ITEM_TYPE_CHOICES, default='theory')
    time_estimate = models.IntegerField(help_text="minutes")
    day_number = models.IntegerField()
    extra_links = models.JSONField(default=list)



    def __str__(self):
        """
        @brief String representation of the lesson.
        @return The title of the lesson.
        """
        return self.title




class UserProgress(models.Model):
    """
    @brief Model tracking individual user progress for specific lessons.
    
    @details UserProgress records whether a user has completed a lesson
    and when it was completed. Used to calculate overall learning plan progress.
    
    @see LearningPlan
    @see Lesson
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
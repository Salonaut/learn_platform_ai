from django.db import models
from django.conf import settings


class LearningPlan(models.Model):
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
        return self.topic

    # after view for update make this automatically by update everytime when user finish lesson
    def calculate_progress(self):
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
        return self.title




class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
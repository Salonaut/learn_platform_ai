from rest_framework import serializers

from .models import LearningPlan, Lesson, UserProgress



class LearningPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPlan
        fields = ('id', "topic", "progress", "created_at")



class LessonItemSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', "title", "day_number", "time_estimate", "is_completed")

    def get_is_completed(self, obj):
        user = self.context.get('user')
        if not user:
            return False
        return UserProgress.objects.filter(user=user, lesson=obj, is_completed=True).exists()



class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'theory_md',
            'task',
            'time_estimate',
            'extra_links',
            'day_number'
        )
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import LearningPlan, Lesson
from .serializers import LearningPlanSerializer, LessonItemSerializer, LessonDetailSerializer
from .services import generate_learning_plan


class ListLearningPlanView(ListAPIView):
    serializer_class = LearningPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LearningPlan.objects.filter(user=self.request.user)


class LessonListView(ListAPIView):
    serializer_class = LessonItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        plan_id = self.kwargs.get('pk')
        return Lesson.objects.filter(id=plan_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class LessonDetailView(RetrieveAPIView):
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(plan__user=self.request.user)


class LearningPlanGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from . import views

# # Swagger conf
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Learn Platform API",
#       default_version='v1',
#       description="Документація для фронтенд-розробників",
#       contact=openapi.Contact(email="support@example.com"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger/OpenAPI
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

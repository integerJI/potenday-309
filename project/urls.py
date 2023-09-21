from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('app.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/kakao/login/callback/', views.KakaoSignInView.as_view(), name='login_with_kakao'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
schema_view = get_schema_view(
    openapi.Info(
        title="My Project API",
        default_version="v1",
        description="API documentation for My Project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"), license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns += [
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apis.views import (
    PostViewSet,
    GenerateCaptionAPIView,
    GenerateImageAPIView,
    GenerateTextVideoAPIView,
    CreatePostAPIView
)
from .views import (
    calendar_view,
    create_post
)

router = DefaultRouter()
# Provide a basename explicitly when the viewset does not define a default queryset attribute
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    # API endpoints via router
    path('api/', include(router.urls)),

    # Additional AI generation endpoints
    path('api/generate-caption/', GenerateCaptionAPIView.as_view(), name='generate_caption'),
    path('api/generate-image/', GenerateImageAPIView.as_view(), name='generate_image'),
    path('api/generate-video/', GenerateTextVideoAPIView.as_view(), name='generate_text_video'),
    path('api/create-post/', CreatePostAPIView.as_view(), name='create_post_api'),

    # Front-end views
    path('', calendar_view, name='calendar'),
    path('create-post/', create_post, name='create_post'),
]

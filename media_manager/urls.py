from django.urls import path

from .views import ImageView, CreateVideoView

urlpatterns = [
    path('image/', ImageView.as_view()),
    path('video/', CreateVideoView.as_view()),
]

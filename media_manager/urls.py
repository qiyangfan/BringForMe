from django.urls import path

from .views import ImageView, VideoView

urlpatterns = [
    path('image/', ImageView.as_view()),
    path('video/', VideoView.as_view()),
]

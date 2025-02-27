from django.urls import path

from message.views import MessageReceiverView,MessageView

urlpatterns = [
    path('receiver/', MessageReceiverView.as_view()),
    path('receiver/<int:receiver_id>/', MessageView.as_view()),
]

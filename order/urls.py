from django.urls import path

from .views import OrderCreateReadView, OrderUpdateView

urlpatterns = [
    path('', OrderCreateReadView.as_view()),
    path('{order_id}/', OrderUpdateView.as_view()),
]

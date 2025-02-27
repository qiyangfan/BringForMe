from django.urls import path

from .views import OrderCreateReadView, OrderUpdateDeleteView

urlpatterns = [
    path('', OrderCreateReadView.as_view()),
    path('{order_id}/', OrderUpdateDeleteView.as_view()),
]

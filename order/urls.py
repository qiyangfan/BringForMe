from django.urls import path

from .views import OrderCreateReadView, OrderUpdateDeleteView

urlpatterns = [
    path('', OrderCreateReadView.as_view()),
    path('<int:order_id>/', OrderUpdateDeleteView.as_view()),
]

from django.urls import path

from .views import FeedbackRateView

urlpatterns = [
    path("feedback-rate/", FeedbackRateView.as_view(), name="feedback_rate"),
]

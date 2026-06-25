from django.urls import path

from .views import ChatView,UpdatePersonalityView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('customize_personalization/',UpdatePersonalityView.as_view(), name='customize_personalization'),
]
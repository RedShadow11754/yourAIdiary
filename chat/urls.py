from django.urls import path

from .views import ChatView,UpdatePersonalityView,ChatHistoryView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('customize_personalization/',UpdatePersonalityView.as_view(), name='customize_personalization'),
    path('chat/history/', ChatHistoryView.as_view(), name='chat_history'),
]
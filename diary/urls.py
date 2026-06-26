from django.urls import path
from .views import DiaryEntryListView, DiaryEntryDetailView, DiaryEntryEditView

urlpatterns = [
    path("entries/", DiaryEntryListView.as_view()),
    path("entries/<int:pk>/", DiaryEntryDetailView.as_view()),
    path("entries/<int:pk>/edit/", DiaryEntryEditView.as_view()),
]
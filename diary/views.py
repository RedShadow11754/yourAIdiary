from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import DiaryEntry


class DiaryEntryListView(APIView):
    """Returns all diary entries for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = DiaryEntry.objects.filter(user=request.user)
        data = [
            {
                "id": e.id,
                "date": e.date,
                "mood": e.mood,
                "content": e.display_content,
                "is_edited": e.is_edited,
                "created_at": e.created_at,
            }
            for e in entries
        ]
        return Response(data)


class DiaryEntryDetailView(APIView):
    """Returns a single diary entry by id."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            entry = DiaryEntry.objects.get(pk=pk, user=request.user)
        except DiaryEntry.DoesNotExist:
            return Response({"error": "Not found."}, status=404)

        return Response({
            "id": entry.id,
            "date": entry.date,
            "mood": entry.mood,
            "content": entry.display_content,
            "is_edited": entry.is_edited,
            "created_at": entry.created_at,
        })


class DiaryEntryEditView(APIView):
    """Allows user to edit their diary entry."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            entry = DiaryEntry.objects.get(pk=pk, user=request.user)
        except DiaryEntry.DoesNotExist:
            return Response({"error": "Not found."}, status=404)

        edited_content = request.data.get("content", "").strip()
        if not edited_content:
            return Response({"error": "Content cannot be empty."}, status=400)

        entry.edited_content = edited_content
        entry.is_edited = True
        entry.save(update_fields=["edited_content", "is_edited", "updated_at"])

        return Response({"status": "success", "message": "Diary entry updated."})
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework.views import APIView
from .models import Message, UserPersonality, PersonalityPrompt
from .main import chat_service
from django.utils import timezone
from memory.logic import get_today_chats
from memory.session_tracker import get_or_create_session
from memory.episodic import retrieve_relevant_memories
from memory.models import UserCoreMemory


DEFAULT_PROMPTS = {
    "sassiness": {1: "Be gentle and soft-spoken. Never sassy.", 2: "Mild playful edge, light tease here and there.", 3: "Deliciously sassy. Roast with love.",},
    "warmth": {1: "Cool, calm, and composed.", 2: "Warm and caring without being over the top.", 3: "Deeply warm and affectionate. Make people feel seen.",},
    "banter": {1: "Keep things straightforward. No playful jabs.", 2: "Light banter and occasional jokes.", 3: "Banter machine. Witty comebacks and playful roasts.",},
    "directness": {1: "Gentle and indirect. Hint at things.", 2: "Fairly direct but cushion the blow.", 3: "Brutally honest. No sugarcoating.",},
    "verbosity": {1: "Short and punchy. One or two sentences.", 2: "Medium-length, enough detail.", 3: "Rich, detailed, thoughtful responses.",},
    "emoji": {1: "Never use emoji.", 2: "Use emoji sparingly.", 3: "Use emoji liberally. 💜✨🌼",},
}


def _get_prompt(personality, level):
    """Get prompt from DB, falling back to defaults if not seeded."""
    obj = PersonalityPrompt.objects.filter(personality=personality, level=level).first()
    if obj:
        return obj.prompt
    return DEFAULT_PROMPTS.get(personality, {}).get(level, "Be yourself.")


def promptConvertor(sassiness_level, warmth_level, banter_level, directness_level, emoji_level, verbosity_level):
    sassiness_prompt = _get_prompt("sassiness", sassiness_level)
    warmth_prompt = _get_prompt("warmth", warmth_level)
    banter_prompt = _get_prompt("banter", banter_level)
    directness_prompt = _get_prompt("directness", directness_level)
    emoji_prompt = _get_prompt("emoji", emoji_level)
    verbosity_prompt = _get_prompt("verbosity", verbosity_level)
    return sassiness_prompt, warmth_prompt, banter_prompt, directness_prompt, emoji_prompt, verbosity_prompt


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')

        # --- Memory: track session ---
        get_or_create_session(request.user)

        # --- Memory: pull core profile (always injected) ---
        core, _ = UserCoreMemory.objects.get_or_create(user=request.user)
        core_memory_str = core.to_prompt_string()
        print(f"core memory: {core_memory_str}")

        # --- Memory: retrieve relevant episodic memories ---
        try:
            episodic_memories_str = retrieve_relevant_memories(request.user, message)
        except Exception as e:
            print(f"[Chat] Episodic memory retrieval failed: {e}")
            episodic_memories_str = ""
        print(f"episodic memory: {episodic_memories_str}")

        # --- Build ultimate_info ---
        ultimate_info = ""
        if core_memory_str:
            ultimate_info += f"WHAT I KNOW ABOUT YOU:\n{core_memory_str}\n\n"
        if episodic_memories_str:
            ultimate_info += f"RELEVANT MEMORIES FROM OUR PAST CONVERSATIONS:\n{episodic_memories_str}"

        # --- Daily context (today's messages) ---
        daily_context, _ = get_today_chats(user=request.user)

        # --- Personality ---
        user_settings = UserPersonality.objects.get(user=request.user)
        sassiness_prompt, warmth_prompt, banter_prompt, directness_prompt, emoji_prompt, verbosity_prompt = promptConvertor(
            user_settings.sassiness,
            user_settings.warmth,
            user_settings.banter,
            user_settings.directness,
            user_settings.emoji,
            user_settings.verbosity,
        )

        # --- Call AI ---
        reply = chat_service.answer(
            message,
            daily_chats=daily_context,
            user_name=user_settings.user_name,
            sassiness_prompt=sassiness_prompt,
            warmth_prompt=warmth_prompt,
            banter_prompt=banter_prompt,
            verbosity_prompt=verbosity_prompt,
            emoji_prompt=emoji_prompt,
            custom_prompt=user_settings.custom_prompt,
            directness_prompt=directness_prompt,
            ultimate_info=ultimate_info,
        )

        # --- Save messages ---
        Message.objects.create(user=request.user, role="user", content=message)
        Message.objects.create(user=request.user, role="ai", content=reply)

        return Response({"reply": reply})

from django.db.models import Min
import json

class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns list of days the user has chatted, with full messages for each."""
        # Get all unique days this user has messages
        days = (
            Message.objects
            .filter(user=request.user, is_deleted=False)
            .values('day')
            .distinct()
            .order_by('-day')
        )

        result = []
        for entry in days:
            day = entry['day']
            messages = Message.objects.filter(
                user=request.user,
                day=day,
                is_deleted=False
            ).order_by('created_at').values('role', 'content', 'created_at')

            result.append({
                'date': str(day),
                'messages': [
                    {
                        'role': m['role'],
                        'content': m['content'],
                        'time': m['created_at'].strftime('%I:%M %p'),
                    }
                    for m in messages
                ]
            })

        return Response(result)

class UpdatePersonalityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        UserPersonality.objects.update_or_create(
            user=request.user,
            defaults={
                "user_name":    request.data.get('user_name') or 'user',
                "sassiness":    request.data.get('sassiness', 2),
                "warmth":       request.data.get('warmth', 2),
                "banter":       request.data.get('banter', 2),
                "directness":   request.data.get('directness', 2),
                "verbosity":    request.data.get('verbosity', 2),
                "emoji":        request.data.get('emoji', 2),
                "custom_prompt": request.data.get('custom_prompt') or None,
            }
        )
        return Response({"status": "success"})
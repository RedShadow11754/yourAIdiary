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


def promptConvertor(sassiness_level, warmth_level, banter_level, directness_level, emoji_level, verbosity_level):
    sassiness_prompt = PersonalityPrompt.objects.get(personality="sassiness", level=sassiness_level).prompt
    warmth_prompt = PersonalityPrompt.objects.get(personality="warmth", level=warmth_level).prompt
    banter_prompt = PersonalityPrompt.objects.get(personality="banter", level=banter_level).prompt
    directness_prompt = PersonalityPrompt.objects.get(personality="directness", level=directness_level).prompt
    emoji_prompt = PersonalityPrompt.objects.get(personality="emoji", level=emoji_level).prompt
    verbosity_prompt = PersonalityPrompt.objects.get(personality="verbosity", level=verbosity_level).prompt
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

        # --- Memory: retrieve relevant episodic memories ---
        episodic_memories_str = retrieve_relevant_memories(request.user, message)

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


class UpdatePersonalityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        UserPersonality.objects.update_or_create(
            user=request.user,
            defaults={
                "user_name": request.data.get('user_name'),
                "sassiness": request.data.get('sassiness', 2),
                "warmth": request.data.get('warmth', 2),
                "banter": request.data.get('banter', 2),
                "directness": request.data.get('directness', 2),
                "verbosity": request.data.get('verbosity', 2),
                "emoji": request.data.get('emoji', 2),
                "custom_prompt": request.data.get('custom_prompt'),
            }
        )
        return Response({"status": "success"})
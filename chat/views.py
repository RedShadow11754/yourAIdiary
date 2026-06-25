from tabnanny import verbose

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework.views import APIView
from .models import Message,UserPersonality,PersonalityPrompt
from .main import chat_service
from django.utils import timezone
from memory.logic import get_today_chats



def promptConvertor(sassiness_level,warmth_level,banter_level,directness_level,emoji_level,verbosity_level):
    sassiness_prompt = PersonalityPrompt.objects.get(
    personality="sassiness",
    level=sassiness_level,
).prompt
    warmth_prompt = PersonalityPrompt.objects.get(
        personality="warmth",
        level=warmth_level,
    ).prompt
    banter_prompt = PersonalityPrompt.objects.get(
        personality="banter",
        level=banter_level,
    ).prompt
    directness_prompt = PersonalityPrompt.objects.get(
        personality="directness",
        level=directness_level,
    ).prompt
    emoji_prompt = PersonalityPrompt.objects.get(
        personality="emoji",
        level=emoji_level,
    ).prompt
    verbosity_prompt = PersonalityPrompt.objects.get(
        personality="verbosity",
        level=verbosity_level,
    ).prompt
    return sassiness_prompt,warmth_prompt,banter_prompt,directness_prompt,emoji_prompt,verbosity_prompt



# Create your views here.
class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        message = request.data.get('message')
        # Daily context
        daily_context = get_today_chats(user=request.user)
        user_settings = UserPersonality.objects.get(user=request.user)
        personalities = PersonalityPrompt.objects.all()
        # Personality levels
        sassiness_level = user_settings.sassiness
        warmth_level = user_settings.warmth
        banter_level = user_settings.banter
        directness_level = user_settings.directness
        emoji_level = user_settings.emoji
        verbosity_level = user_settings.verbosity

        custom_prompt = user_settings.custom_prompt
        user_name = user_settings.user_name

        # Personality traits
        sassiness_prompt, warmth_prompt, banter_prompt, directness_prompt, emoji_prompt, verbosity_prompt = promptConvertor(sassiness_level,warmth_level,banter_level,directness_level,emoji_level,verbosity_level)

        reply = chat_service.answer(message,daily_chats=daily_context,user_name=user_name,sassiness_prompt=sassiness_prompt,warmth_prompt=warmth_prompt,banter_prompt=banter_prompt,verbosity_prompt=verbosity_prompt,emoji_prompt=emoji_prompt,custom_prompt=custom_prompt,directness_prompt=directness_prompt)
        Message.objects.create(user=request.user,role="user", content=message)
        Message.objects.create(user=request.user,role="ai", content=reply)

        return Response({"reply":reply})




class UpdatePersonalityView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_name = request.data.get('user_name')
        sassiness = request.data.get('sassiness',2)
        warmth = request.data.get('warmth',2)
        banter = request.data.get('banter',2)
        directness = request.data.get('directness',2)
        verbosity = request.data.get('verbosity',2)
        emoji = request.data.get('emoji',2)
        custom_prompt = request.data.get('custom_prompt')

        UserPersonality.objects.update_or_create(
            user=request.user,
            defaults={
                "user_name": user_name,
                "sassiness": sassiness,
                "warmth": warmth,
                "banter": banter,
                "directness": directness,
                "verbosity": verbosity,
                "emoji": emoji,
                "custom_prompt": custom_prompt,
            }
        )
        return Response({"status":"success"})


from django.utils import timezone
from chat.models import Message


def get_today_messages_for_chat(user):
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    return Message.objects.filter(
        user=user,
        created_at__gte=start_of_day,
        created_at__lte=now
    ).order_by("created_at")

def get_today_chats(user):

    my_list = list(
        Message.objects.filter(
            user=user,
            day=timezone.now().date()
        ).values("role", "content")
    )
    content = ""
    if len(my_list) > 40:
        my_list = my_list[:40]
    for msg in my_list:
        role = "user" if msg['role'] == 'user' else "AI"
        content += f"{role}: {msg['content']}\n\n"
    return content,len(my_list)

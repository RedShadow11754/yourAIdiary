from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"

    def ready(self):
        from memory.qdrant_client import ensure_collection_exists
        ensure_collection_exists()
from django.db import migrations
from pgvector.django import VectorExtension # <-- Add this import

class Migration(migrations.Migration):

    dependencies = [
        # This list will be auto-populated by Django; leave it as is
    ]

    operations = [
        VectorExtension(), # <-- Add this operation to turn on pgvector natively
    ]
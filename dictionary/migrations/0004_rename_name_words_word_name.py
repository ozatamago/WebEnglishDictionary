# Generated by Django 4.2.1 on 2023-06-15 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dictionary", "0003_words_collect"),
    ]

    operations = [
        migrations.RenameField(
            model_name="words",
            old_name="name",
            new_name="word_name",
        ),
    ]
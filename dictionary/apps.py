from django.apps import AppConfig
# from django.db.models.signals import post_migrate


class DictionaryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dictionary"

    # def ready(self):
    #     from .models import words
    #     post_migrate.connect(words, sender=self)

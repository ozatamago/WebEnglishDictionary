from django.contrib import admin
from .models import Word

# 管理サイトでmodels.pyで定義したものを操作できるようにする
admin.site.register(Word)
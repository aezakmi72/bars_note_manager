from django.contrib import admin

from .models import Note
from .models import Category


class NoteAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'category', 'creator', 'bookmark', 'published', 'dtcreate', 'dtupdate')


admin.site.register(Note, NoteAdmin)
admin.site.register(Category)

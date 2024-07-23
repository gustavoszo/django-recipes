from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'slug')
    search_fields = ('id', 'name', 'slug')
    list_per_page = 10
    list_editable = 'name',
    # O atributo prepopulated_fields é usado para indicar que o slug deve ser automaticamente preenchido com base no title
    prepopulated_fields = {
        'slug': ('name',)
    }

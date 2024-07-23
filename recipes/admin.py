from django.contrib import admin
from .models import Category, Recipe
# from django.contrib.contenttypes.admin import GenericStackedInline

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    ...

# class TagInline(GenericStackedInline):
#     model = Tag
#     fields = 'name',
#     extra = 1

@admin.register(Recipe)
class recipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'author')
    list_display_links = ('title', 'created_at')
    search_fields = ('id', 'title', 'description', 'slug')
    list_filter = ('category', 'author', 'is_published')
    list_per_page = 10
    list_editable = 'is_published',
    # O atributo prepopulated_fields é usado para indicar que o slug deve ser automaticamente preenchido com base no title
    prepopulated_fields = {
        'slug': ('title',)
    }

    # inlines = [TagInline, ]



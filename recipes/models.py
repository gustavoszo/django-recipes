from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag

from collections import defaultdict
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=65)

    # A class Meta é uma ferramenta poderosa e flexível no Django, usada para definir metadados e configurações adicionais tanto em modelos quanto em formulários.
    # No contexto do Django, metadados são usados para fornecer informações adicionais e configurações sobre modelos, formulários, e outros componentes
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)
    
class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Ao deletar uma categoria o atributo category recebe Null
    # blank=True equivale a permitir não receber valor no formulário
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    # class Meta:
    #     ordering = ['id']
    #     verbose_name = 'Recipe'
    #     verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title
 
    # Adiciona um link para a view do site no admin e serve como um atalho de reverse para alguma url, nesse caso: recipes:recipe
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id, ))

    def save(self, *args, **kwargs):
        if not self.slug:
            count = Recipe.objects.filter(title=self.title).count()
            if count != 0:
                slug = f'{slugify(self.title)}-{count}' 
            else:
                slug = slugify(self.title)
            self.slug = slug

        return super().save(*args, **kwargs)

    # Validação customizada
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipes_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipes_from_db:
            if recipes_from_db.pk != self.pk:
                error_messages['title'].append('Já existe uma receita com esse título')

        if error_messages:
            raise ValidationError(error_messages)
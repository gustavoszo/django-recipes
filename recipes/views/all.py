from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range, make_pagination
from django.contrib import messages

from recipes.models import Recipe
import os

PER_PAGE = int(os.environ.get('PER_PAGE'))

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/home.html', {'recipes': page_obj, 'pagination_range': pagination_range})

def category(request, category_id):
    # recipes = Recipe.objects.filter(category__id=category_id, is_published=True)
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True))
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/category.html', {'recipes': page_obj, 'pagination_range': pagination_range, 'title': recipes[0].category.name})

def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/recipe-view.html', {'is_details': True, 'recipe': recipe})

def search(request):
    # A funcão strip remove espaços em branco no inicio e fim
    search_term = request.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # A função Q() muda a condicional para OR
        Q(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/search.html', 
        {'page_title': f'Pequisa por "{search_term}"', 
        'search_term': search_term, 
        'recipes': page_obj, 'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
        })

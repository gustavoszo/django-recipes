from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from recipes.models import Recipe
from utils.pagination import make_pagination
from django.db.models import Q
from django.http import Http404

import os
PER_PAGE = int(os.environ.get('PER_PAGE'))

class RecipeListBaseView(ListView):
    
    model = Recipe
    context_object_name = 'recipes'
    ordering = ('-id')
    # template_name = 'recipes/home.html'
    
    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(is_published=True)

        #Melhora a perfomance. Na mesma consulta já busca o usuário e categoria com join
        qs.select_related('author', 'category')
        qs.prefetch_related('tags', 'author__profile')

        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)

        ctx.update({'recipes': page_obj, 'pagination_range': pagination_range})

        return ctx


class RecipeListViewHome(RecipeListBaseView):
    template_name = 'recipes/home.html'


class RecipeListViewCategory(RecipeListBaseView):
    template_name = 'recipes/category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(category__id=self.kwargs.get('category_id'))

        return qs
    

class RecipeListViewSearch(RecipeListBaseView):
    template_name = 'recipes/search.html'

    def get_queryset(self):
        qs = super().get_queryset()

        search_term = self.request.GET.get('q', '').strip()

        qs = qs.filter( Q(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term)
        ))

        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        search_term = self.request.GET.get('q', '').strip()
        
        ctx.update( 
            {
            'page_title': f'Pequisa por "{search_term}"', 
            'search_term': search_term, 
            'additional_url_query': f'&q={search_term}'
            }
        )

        return ctx


class RecipeDetailView(DetailView):    
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/recipe-view.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)

        if obj.is_published == False:
            raise Http404()

        return obj

    def get_context_data(self, *args, **kwargs: Any):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({'is_details': True})
        
        return ctx


class RecipeListViewTag(RecipeListBaseView):
    template_name = 'recipes/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(tags__slug=self.kwargs.get('slug'))

        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        
        ctx.update( 
            {
            'page_title': self.kwargs.get('slug'), 
            }
        )

        return ctx
        



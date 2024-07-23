from django.views import View
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class HelpClass:
    
    def get_recipe(self, id):
        recipe = None

        if id:
            recipe = get_object_or_404(Recipe, pk=id)

        return recipe

    def render_recipe(self, request, form):
        return render(request, 'authors/dashboard-recipe.html', {'form': form})

@method_decorator(
    login_required(login_url='authors:login'),
    # Nome do método que vai ser decorado (dispactch pq é ele que checa em todas as requisiçoes para qual método vai ser enviado)
    name='dispatch'
)
class DashboardRecipe(View, HelpClass):
    
    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(request, form)
    
    # Esta fazendo atualização e criação de recipe
    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.is_published = False
            recipe.preparation_steps_is_html = False

            recipe.save()
            if id:
                messages.success(request, 'Sua receita foi atualizada com sucesso!')
            else:
                messages.success(request, 'Sua receita foi criada com sucesso!')

            return redirect('authors:dashboard')

        return self.render_recipe(request, form)

@method_decorator(
    login_required(login_url='authors:login'),
    # Nome do método que vai ser decorado (dispactch pq é ele que checa em todas as requisiçoes para qual método vai ser enviado)
    name='dispatch'
)        
class DashboardRecipeDelete(View, HelpClass):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Sua receita foi deletada com sucesso')
        return redirect('authors:dashboard')

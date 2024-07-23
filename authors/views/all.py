from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from recipes.models import Recipe

def registerView(request):
    data = request.session.get('register_form_data', None)
    form = RegisterForm(data)
    return render(request, 'authors/register.html', {'form': form, 'form_action': 'authors:create'})

def registerCreate(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        # O método set_password do Django é usado para definir a senha de um usuário de forma segura. Quando você usa set_password, a senha que você passa como argumento é criptografada antes de ser armazenada no banco de dados.
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Sua conta foi criada com sucesso! Por favor, faça o login.')
        del(request.session['register_form_data'])
        return redirect('authors:login')
    
    return redirect('authors:register')

def loginView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.info(request, 'Você já esta logado')
            return redirect('recipes:home')

        form = LoginForm()
       
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            # A função authenticate do Django verifica as credenciais do usuário, geralmente username e password, na base de dados do model User padrão. Se as credenciais estiverem corretas, ela retorna o objeto de usuário correspondente.
            authenticate_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', '')
            )

            if authenticate_user is not None:
                login(request, authenticate_user)
                messages.success(request, 'Você está logado')
                return redirect('authors:dashboard')
            else:
                messages.error(request, 'Username e/ou senha inválido(s)')
        else:
            messages.error(request, 'Username e/ou senha inválido(s)')

    return render(request, 'authors/login.html', {'form': form, 'form_action': 'authors:login'})

@login_required(login_url='authors:login')
def logoutView(request):
    logout(request)
    return redirect('authors:login')

@login_required(login_url='authors:login')
def dashboard(request):
    recipes = Recipe.objects.filter(is_published=False, author=request.user)
    return render(request, 'authors/dashboard.html', {'recipes': recipes})

# Foi para CBV
# @login_required(login_url='authors:login')
# def dashboardRecipeEdit(request, id):
#     recipe = get_object_or_404(
#         Recipe.objects.filter(is_published=False, author=request.user, pk=id)
#     )
#     form = AuthorRecipeForm(
#         data=request.POST or None,
#         files=request.FILES or None,
#         instance=recipe
#         )

#     if request.method == 'POST': 
#         if form.is_valid():
#             recipe = form.save(commit=False)

#             recipe.author = request.user
#             recipe.is_published = False
#             recipe.preparation_steps_is_html = False

#             recipe.save()
#             messages.success(request, 'Sua receita foi atualizada com sucesso!')
#             return redirect('authors:dashboard')

#     return render(request, 'authors/dashboard-recipe.html', {'recipe': recipe, 'form': form})

# @login_required(login_url='authors:login')
# def dashboardRecipeCreate(request):
#     form = AuthorRecipeForm()

#     if request.method == 'POST':
#         form = AuthorRecipeForm(data=request.POST,files=request.FILES)
#         if form.is_valid():
#             recipe = form.save(commit=False)

#             recipe.author = request.user
#             recipe.is_published = False
#             recipe.preparation_steps_is_html = False

#             recipe.save()
#             messages.success(request, 'Sua receita foi criada com sucesso!')
#             return redirect('authors:dashboard')

#     return render(request, 'authors/dashboard-recipe.html', {'form': form, 'form_action': 'authors:dashboard_recipe_create'})

@login_required(login_url='authors:login')
def dashboardRecipeDelete(request):
    if request.method != 'POST':
        raise Http404()
    
    POST = request.POST
    recipe = get_object_or_404(Recipe, is_published=False, author=request.user, pk=POST.get('id'))

    recipe.delete()
    messages.success(request, 'Receita deletada com sucesso!')

    return redirect('authors:dashboard')
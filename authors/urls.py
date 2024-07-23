from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.registerView, name='register'),
    path('register/create/', views.registerCreate, name='create'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipe/create/', views.DashboardRecipe.as_view(), name='dashboard_recipe_create'),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/recipe/<int:id>/edit/', views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'),
    path('profile/edit', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
]
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView, UpdateView
from authors.models import Profile
from authors.forms import ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

class ProfileView(TemplateView):
    template_name = 'authors/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        profile_id = context.get('id')

        profile = get_object_or_404(Profile.objects.filter(
            pk=profile_id
        ).select_related('author'), pk=profile_id)
        
        return self.render_to_response({**context, 'profile': profile})

@method_decorator(
    login_required(login_url='authors:login'),
    name='dispatch'
)
class ProfileUpdateView(UpdateView):
    template_name = 'authors/profile-edit.html'
    form_class = ProfileForm
    success_url = reverse_lazy('authors:dashboard')

    def get_object(self, queryset=None) -> Model:
        profile = self.request.user.profile
        return profile
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return response



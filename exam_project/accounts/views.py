from django.contrib.auth import views as auth_views, get_user_model, login, authenticate

from django.urls import reverse_lazy
from exam_project.accounts.forms import ProfileCreateForm
from django.views import generic as views


UserModel = get_user_model()


class SignUpView(views.CreateView):
    form_class = ProfileCreateForm
    template_name = 'profile/create-profile.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class SignInView(auth_views.LoginView):
    template_name = 'profile/login_profile.html'


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class ProfileDetailsView(views.DetailView):
    template_name = 'profile/details-profile.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['games_count'] = self.object.gamemodel_set.count()
        return context


class ProfileDeleteView(views.DeleteView):
    template_name = 'profile/delete-profile.html'
    model = UserModel
    success_url = reverse_lazy('index')


class ProfileEditView(views.UpdateView):
    template_name = 'profile/edit-profile.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'money', 'profile_picture',)

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={
            'pk': self.request.user.pk,
        })

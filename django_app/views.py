from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from .models import User
from .forms import RegisterForm


# Create your views here.

class HomePageView(TemplateView):
    template_name = "user/homepage.html"


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "user/create_user.html"

    def form_valid(self, form):
        if form.is_valid():
            self.new_user = form.save(commit=False)  # doesn't save info but has created a new user
            form.save()
            login(self.request, self.new_user)
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("user_update", args=[self.new_user.username])


# class UserDetailView(DetailView):
#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"
#     template_name = "user/user_detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = DetailView.get_context_data(self, **kwargs)
#         return context


class UserUpdateView(UpdateView):
    model = User
    form_class = RegisterForm
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "user/user_detail.html"

    def get_context_data(self, **kwargs):
        context = UpdateView.get_context_data(self, **kwargs)
        # context['user_detail'] = DetailView.get_context_data(self, **kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())

        else:
            context = {
                'form': form
            }
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy("user_update", args=[self.get_object().username])


# class UserLoginView(LoginView):
#     model = User
#     form_class = RegisterForm
#     template_name = "registration/templates/user/login.html"
#
#     def login(self):
#         username = self.request.POST['username']
#         password = self.request.POST['password']
#         user = authenticate(self.request, username=username, password=password)
#
#         if user is not None:
#             login(self.request, user)
#             return reverse_lazy("user_update", args=[user.username])

class MyLoginView(LoginView):

    def get_success_url(self):
        url = self.get_redirect_url()
        return reverse_lazy("user_update", args=[self.request.user.username])

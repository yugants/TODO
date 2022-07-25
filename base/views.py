from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin   # Using this to restrict pages
'''Mixins are a language concept that allows a programmer to inject some code into a class'''

from django.urls import reverse_lazy


from .models import Task


# Creating Login
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' 
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm        # We are using this form in register.html
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # Blocking registered user to signin and register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')

        return super(RegisterPage, self).get(*args, **kwargs)



# Each class looks for their template by default, so we created them in templates/base/

class TaskList(LoginRequiredMixin,ListView):
    model = Task      # models class name
    context_object_name = 'tasks'   # renaming look for loop in template task_list 

    def get_context_data(self, **kwargs):               # With this we can filter User Specific Data
        context =  super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()


        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)   #title__startswith try it too
        
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'    # Creating another name for object variable 
    template_name = 'base/task.html'  # Locating renamed template name

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']  # We are listing all the items in the view
    success_url = reverse_lazy('tasks')   # After submitting it will take back to the list

    # So that a user can create task in only his account

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):       # We will use the tasks template for updating as well
    model = Task
    fields = ['title','description','complete'] 
    success_url = reverse_lazy('tasks')

 
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

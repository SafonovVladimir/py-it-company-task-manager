from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import Task


def index(request):
    """View function for the home page of the site."""
    user = request.user
    queryset = Task.objects.filter(assignees=user.id)
    num_tasks = queryset.count()
    num_high_priority_tasks = queryset.filter(
        priority__in=("Urgent", "High")
    ).count()
    num_finished_tasks = queryset.filter(is_completed=True).count()

    context = {
        "num_tasks": num_tasks,
        "num_high_priority_tasks": num_high_priority_tasks,
        "num_finished_tasks": num_finished_tasks,
    }

    return render(request, "task_manager/index.html", context=context)


class TasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    # paginate_by = 10


class TasksDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TasksCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "task_manager/task_list.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")

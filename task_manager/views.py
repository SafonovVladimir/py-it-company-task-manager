from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskNameSearchForm, WorkerPositionUpdateForm
from task_manager.models import Task, Worker


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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskNameSearchForm(initial={
            "name": name,
        })

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(assignees=user.id).prefetch_related(
            "assignees").select_related("task_type")
        form = TaskNameSearchForm(self.request.GET)

        order_by = self.request.GET.get("order_by")
        is_completed = self.request.GET.get("is_completed")
        priority = self.request.GET.get("priority")

        if form.is_valid():
            if order_by:
                return queryset.filter(
                    name__icontains=form.cleaned_data["name"]
                ).order_by(order_by)
            if is_completed:
                return queryset.filter(
                    name__icontains=form.cleaned_data["name"],
                    is_completed=is_completed
                )
            if priority:
                return queryset.filter(
                    name__icontains=form.cleaned_data["name"],
                    priority=priority
                )
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related("tasks")


class WorkerPositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("task_manager:worker-detail")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:task-list")


@login_required
def toggle_complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.is_completed:
        task.is_completed = 0
    else:
        task.is_completed = 1

    task.save()

    return HttpResponseRedirect(
        reverse_lazy("task_manager:task-detail", args=[pk])
    )

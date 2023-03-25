from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from task_manager.views import (
    index,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerDetailView,
    WorkerPositionUpdateView,
    WorkerDeleteView,
)

urlpatterns = [
    path("", index, name="index"),

    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/",
         TaskUpdateView.as_view(),
         name="task-update"),
    path("tasks/<int:pk>/delete/",
         TaskDeleteView.as_view(),
         name="task-delete"),

    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path(
        "worker/<int:pk>/update/",
        WorkerPositionUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "worker/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),

]

app_name = "task_manager"

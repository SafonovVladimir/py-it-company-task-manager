from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from task_manager.views import (
    index,
    TasksListView,
    TasksCreateView,
    TaskUpdateView,
    TaskDeleteView
)

urlpatterns = [
    path("", index, name="index"),

    path("tasks/", TasksListView.as_view(), name="task-list"),
    path("tasks/create/", TasksCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/",
         TaskUpdateView.as_view(),
         name="task-update"),
    path("tasks/<int:pk>/delete/",
         TaskDeleteView.as_view(),
         name="task-delete"),

]

app_name = "task_manager"

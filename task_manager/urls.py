from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from task_manager.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "task_manager"

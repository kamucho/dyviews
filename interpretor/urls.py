from django.contrib import admin
from django.urls import path

from core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('add/', add),
    path('function/<pk>/', exec_func),
    path('function/delete/<pk>/', delete),
    path('function/edit/<pk>/', edit),
    path('admin/', admin.site.urls),
]

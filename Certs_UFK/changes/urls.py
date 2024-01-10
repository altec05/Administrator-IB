from django.urls import path
from .views import changes_list

urlpatterns = [
    path('changes_list', changes_list, name='changes_list'),
]
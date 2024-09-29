from django.urls import path
from . import views
from .views import story_list_view
urlpatterns = [
    path('', views.index, name='index'),
    path('stories/', story_list_view, name='story_list'),
]
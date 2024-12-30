from django.urls import path

from . import views

app_name = 'diagram'

urlpatterns = [
    path('', views.diagram, name = 'diagram')
]

from django.urls import path

from . import views

urlpatterns = [
    # ex: /kurumsal/
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment')
]
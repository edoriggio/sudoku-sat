from django.urls import path

from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('solve', Solve.as_view(), name='solve')
]

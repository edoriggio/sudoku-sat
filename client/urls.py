from django.urls import path

from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('solve', Solve.as_view(), name='solve'),
    path('check', Check.as_view(), name='check')
]

from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('category/<str:name>', views.category_view, name='category'),
]

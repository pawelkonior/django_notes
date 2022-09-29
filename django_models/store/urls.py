from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('category/<str:name>', views.category_view, name='category'),
    path('alamakots/<int:pk>', views.DetailProductView.as_view(), name='product-detail'),
]

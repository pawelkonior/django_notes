from django.shortcuts import render
from django.views.generic import DetailView

from . import models


def category_view(request, name):
    products = models.Product.objects.filter(categories__name=name)
    return render(request, 'store/category.html', {'products': products, 'category_name': name})


class DetailProductView(DetailView):
    template_name = 'store/detail_product.html'
    model = models.Product
    context_object_name = 'product'

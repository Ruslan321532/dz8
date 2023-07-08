from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView


from products.models import Product, Category
from products.forms import ProductCreateForm, CategoryCreateForm
from products.constants import PAGINATION_LIMIT


# Create your views here.

class MainCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductsCBV(ListView):
    model = Product
    template_name = 'products/products.html'

    def get(self, request, *args, **kwargs):
        products = self.model.objects.all()
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        pproducts = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        if search_text:
            pproducts = products.filter(Q(title__contains=search_text) | Q(description__contains=search_text))

        context_data = {
            'products': pproducts,
            'user': request.user,
            'pages': range(1, max_page + 1)
        }
        return render(request, self.template_name, context=context_data)


class CategoriesCBV(ListView):
    model = Category
    template_name = 'products/categories.html'

    def get(self, request, *args, **kwargs):
        categories = self.model.objects.all()
        context_data = {'categories': categories
                        }

        return render(request, self.template_name, context=context_data)


class ProductDetailCBV(ListView):
    model = Product
    template_name = 'products/detail.html'

    def get(self, request, pk, *args, **kwargs):
        try:
            product = self.model.objects.get(id=pk)
        except Product.DoesNotExist:
            return render(request, self.template_name)
        context_data = {
            'product': product
        }
        return render(request, self.template_name, context=context_data)


class ProductCreateCBV(CreateView):
    model = Product
    template_name = 'products/create.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('/products/')

        else:
            context_data = {
                'form': ProductCreateForm
            }
            return render(request, self.template_name, context=context_data)

    def post(self, request, *args, **kwargs):
        data, file = request.POST, request.FILES
        form = ProductCreateForm(data, file)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price')
            )

            return redirect('/products/')
        return render(request, self.template_name, context={'form': form})


class CategoryCreateCBV(CreateView):
    model = Category
    template_name = 'products/categories.html'

    def get(self, request, *args, **kwargs):
        context_data = {
            'form': CategoryCreateForm
        }
        return render(request, self.template_name, context=context_data)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = CategoryCreateForm(data)

        if form.is_valid():
            Category.objects.create(
                title=form.cleaned_data.get('title')
            )
            return redirect('/products/')
        return render(request, self.template_name, context={'form': form})


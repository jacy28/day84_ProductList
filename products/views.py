# views.py
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product

def product_list(request):
    query = request.GET.get('q','')
    min_price = request.GET.get('min_price','')
    max_price = request.GET.get('max_price','')
    is_available = request.GET.get('is_available','')

    filters = Q()

    # Search by product name or brand
    if query:
        filters &= Q(name__icontains=query) | Q(brand__icontains=query)

    # Filter by price range
    if min_price:
        filters &= Q(price__gte=min_price)
    if max_price:
        filters &= Q(price__lte=max_price)

    # Filter by availability
    if is_available in ['true', 'false']:
        filters &= Q(is_available=(is_available == 'true'))

    product_queryset = Product.objects.filter(filters).order_by('id')
    total_results = product_queryset.count()

    # Paginate 10 per page
    paginator = Paginator(product_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_results': total_results,
    }

    return render(request, 'products/product_list.html', context)

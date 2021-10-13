from django.shortcuts import redirect, get_object_or_404, render
from .models import Item, OrderItem,Order
from django.utils import timezone
from django.views.generic import ListView,DetailView


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

def products(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request,"product.html",context)


class HomeView(ListView):
    model = Item
    # paginate_by = 10
    template_name = 'home.html'



def checkout (request):
    return render(request,'checkout.html')

def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,created = OrderItem.objects.get_or_create( 
        item=item,
        user=request.user,
        ordered=False
        )
    order_queryset = Order.objects.filter(user=request.user,ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,order_date=ordered_date)
        order.items.add(order_item)

    return redirect("core:product",slug=slug)


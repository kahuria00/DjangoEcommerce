from django.shortcuts import redirect, get_object_or_404, render
from .models import Item, OrderItem,Order
from django.contrib import messages
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
            messages.info(request,"Item quantity was updated to your cart")
            return redirect("core:product",slug=slug)
        else:
            messages.info(request,"Item was added to yourcart")
            order.items.add(order_item)
            return redirect("core:product",slug=slug)
            
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,order_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item was added to your cart")
        return redirect("core:product",slug=slug)
    
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_queryset = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_queryset.exists():
        order = order_queryset[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter( 
            item=item,
            user=request.user,
            ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"Item was removed from your cart")
            return redirect("core:product",slug=slug)
        else:
            messages.info(request,"Item was not in your cart")
            return redirect("core:product",slug=slug)
            
    else:
        messages.info(request,"you don't have an active order")
        return redirect("core:product",slug=slug)
    


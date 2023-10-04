from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .filter import OrderFilter
from .forms import OrderForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Register Success " + user
                                 )
                return redirect('login_account')
        context = {
            'form': form
        }
        return render(request, 'accounts/auth/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or password is incorrect!")
                return render(request, 'accounts/auth/login.html')
        return render(request, 'accounts/auth/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login_account')


@login_required()
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders[:5],
        'customers': customers[:5],
        'total_orders': total_order,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required()
def products(req):
    products = Product.objects.all()

    return render(req, 'accounts/products.html', {
        'products': products
    })


@login_required()
def customer(req, customer):
    data = Customer.objects.get(id=customer)
    orders = Order.objects.filter(customer=customer)

    myFilter = OrderFilter(req.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': data,
        'orders': orders,
        'order_count': orders.count(),
        'order_filter': myFilter
    }
    return render(req, 'accounts/customers.html', context)


@login_required()
def createOrder(req, customer):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=customer)
    if (customer):
        formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    else:
        formset = OrderFormSet(queryset=Order.objects.none())

    if req.method == 'POST':
        formset = OrderFormSet(req.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'formset': formset,
        'customer': customer,

    }
    return render(req, 'accounts/utility/order_form.html', context)


@login_required()
def updateOrder(req, order):
    order = Order.objects.get(id=order)
    form = OrderForm(instance=order)
    if req.method == 'POST':
        form = OrderForm(req.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(req, 'accounts/utility/order_form.html', context)


@login_required()
def deleteOrder(req, order):
    order = Order.objects.get(id=order)
    if req.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(req, 'accounts/utility/delete.html', context)

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render

from .decorators import unauthenticated_user, allow_users, admin_only
from .filter import OrderFilter
from .forms import OrderForm, CreateUserForm, CustomerForm
from .models import *


# Create your views here.
@unauthenticated_user  # Custom decorator to allow only unauthenticated users
def registerPage(request):
    """
    Display and process user registration.

    This view function allows unauthenticated users to register for an account.
    It displays a registration form, processes the form data upon submission,
    and creates a new user account if the provided information is valid.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders a registration page or redirects to the login page
      upon successful registration.

    Usage:
    - Access this view using an appropriate URL.

    Example URL: '/register/'  # Replace with the actual URL for registration.
    """
    # Create a registration form
    form = CreateUserForm()

    # Handle form submission
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Save the user and extract the username
            user = form.save()
            username = form.cleaned_data.get('username')

            # Display a success message and redirect to the login page
            messages.success(request, "Registration successful for " + username)
            return redirect('login_account')

    # Prepare context data to pass to the template
    context = {
        'form': form
    }

    # Render the registration page template
    return render(request, 'accounts/auth/register.html', context)


@unauthenticated_user
def loginPage(request):
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


@login_required(login_url='login')
@allow_users(allowed_roles=['admin', 'customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_order,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/user.html', context)


@login_required()  # Decorator to ensure the user is logged in
@admin_only  # Custom decorator to allow only admin users
def home(request):
    """
    Display a dashboard with statistics related to customers and orders.

    This view function allows an authorized user with the 'admin' role
    to view a dashboard with statistics related to customers and orders.
    It retrieves data from the database and calculates statistics such as
    the total number of customers, total number of orders, delivered orders,
    and pending orders.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders a dashboard page with statistics.

    Usage:
    - Access this view using an appropriate URL.

    Example URL: '/dashboard/'  # Replace with the actual URL for the dashboard.
    """
    # Retrieve all customers and orders from the database
    customers = Customer.objects.all()
    orders = Order.objects.all()

    # Calculate statistics
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # Prepare context data to pass to the template
    context = {
        'orders': orders[:5],
        'customers': customers[:5],
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending
    }

    # Render the dashboard page template
    return render(request, 'accounts/dashboard.html', context)


@login_required()  # Decorator to ensure the user is logged in
@allow_users(allowed_roles=['admin'])  # Custom decorator to check user roles
def products(req):
    """
    Display a list of products.

    This view function allows an authorized user with the 'admin' role
    to view a list of all products available in the system.

    Parameters:
    - req (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders a product listing page with a list of products.

    Usage:
    - Access this view using an appropriate URL.

    Example URL: '/products/'  # Replace with the actual URL for listing products.
    """
    # Retrieve all products from the database
    all_products = Product.objects.all()

    # Prepare context data to pass to the template
    context = {
        'products': all_products
    }

    # Render the products listing page template
    return render(req, 'accounts/products.html', context)


@login_required()  # Decorator to ensure the user is logged in
@allow_users(allowed_roles=['admin'])  # Custom decorator to check user roles
def customer(req, customer):
    """
    Display customer details and their orders.

    This view function allows an authorized user with the 'admin' role
    to view details about a specific customer and list their associated orders.
    It may also provide filtering functionality for the orders.

    Parameters:
    - req (HttpRequest): The HTTP request object.
    - customer (int): The ID of the customer to be displayed.

    Returns:
    - HttpResponse: Renders a customer details page with associated orders and
      potentially filter options.

    Usage:
    - Access this view with a URL that includes the 'customer' parameter.

    Example URL: '/customer/789/'  # Replace '789' with the actual customer ID.
    """
    # Retrieve customer data based on the provided customer ID
    data = Customer.objects.get(id=customer)

    # Retrieve orders associated with the customer
    orders = Order.objects.filter(customer=customer)

    # Create an order filter using a filtering form, potentially provided by 'OrderFilter'
    myFilter = OrderFilter(req.GET, queryset=orders)
    orders = myFilter.qs

    # Prepare context data to pass to the template
    context = {
        'customer': data,
        'orders': orders,
        'order_count': orders.count(),
        'order_filter': myFilter
    }

    # Render the customer details page template
    return render(req, 'accounts/customers.html', context)


@login_required()  # Decorator to ensure the user is logged in
@allow_users(allowed_roles=['admin'])  # Custom decorator to check user roles
def createOrder(req, customer):
    """
    Create an order for a customer.

    This view function allows an authorized user with the 'admin' role
    to create an order for a specific customer. It uses a formset to handle
    multiple order entries and saves them to the database.

    Parameters:
    - req (HttpRequest): The HTTP request object.
    - customer (int): The ID of the customer for whom the order is being created.

    Returns:
    - HttpResponse: Redirects to the home page on successful form submission or
      renders an order creation form.

    Usage:
    - Access this view with a URL that includes the 'customer' parameter.

    Example URL: '/create_order/123/'  # Replace '123' with the actual customer ID.
    """
    # Create an order formset using inlineformset_factory
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)

    # Retrieve the customer object based on the provided ID
    customer = Customer.objects.get(id=customer)

    # Check if the customer exists
    if customer:
        formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    else:
        formset = OrderFormSet(queryset=Order.objects.none())

    # Handle form submission
    if req.method == 'POST':
        formset = OrderFormSet(req.POST, instance=customer)
        if formset.is_valid():
            # Save the order data to the database
            formset.save()
            # Redirect to the home page after successful submission
            return redirect('/')

    # Prepare the context for rendering the order creation form
    context = {
        'formset': formset,
        'customer': customer,
    }

    # Render the order creation form template
    return render(req, 'accounts/utility/order_form.html', context)


@login_required()  # Decorator to ensure the user is logged in
@allow_users(allowed_roles=['admin'])  # Custom decorator to check user roles
def updateOrder(req, order):
    """
    Update an existing order.

    This view function allows an authorized user with the 'admin' role
    to update an existing order. It retrieves the order from the database,
    populates an order form with its data, and saves the updated data
    back to the database upon form submission.

    Parameters:
    - req (HttpRequest): The HTTP request object.
    - order (int): The ID of the order to be updated.

    Returns:
    - HttpResponse: Redirects to the home page on successful form submission or
      renders an order update form.

    Usage:
    - Access this view with a URL that includes the 'order' parameter.

    Example URL: '/update_order/456/'  # Replace '456' with the actual order ID.
    """
    # Retrieve the order object based on the provided order ID
    order = Order.objects.get(id=order)

    # Create an order form and populate it with the order's data
    form = OrderForm(instance=order)

    # Handle form submission
    if req.method == 'POST':
        form = OrderForm(req.POST, instance=order)
        if form.is_valid():
            # Save the updated order data to the database
            form.save()
            # Redirect to the home page after successful submission
            return redirect('/')

    # Prepare the context for rendering the order update form
    context = {
        'form': form
    }

    # Render the order update form template
    return render(req, 'accounts/utility/order_form.html', context)


@login_required()
@allow_users(allowed_roles=['admin'])
def deleteOrder(req, order):
    order = Order.objects.get(id=order)
    if req.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(req, 'accounts/utility/delete.html', context)


@login_required()
@allow_users(allowed_roles=['customer'])
def userSetting(request):
    user = request.user.customer
    form = CustomerForm(instance=user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/utility/settings.html', context)

from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),

    path('products/',views.products,name='products'),

    path('customer/<str:customer>/',views.customer, name='customer'),
    path('user/',views.userPage,name='user'),

    path('create_order/<str:customer>',views.createOrder,name="create_order"),
    path('update_order/<str:order>',views.updateOrder,name="update_order"),
    path('delete_order/<str:order>',views.deleteOrder,name="delete_order"),

    path('register',views.registerPage,name="register_account"),
    path('login',views.loginPage,name='login_account'),
    path('logout',views.logoutUser,name='logout_account')
]

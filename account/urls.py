from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('products/', views.products, name='products'),

    path('customer/<str:customer>/', views.customer, name='customer'),
    path('user/', views.userPage, name='user'),
    path('settings/', views.userSetting, name='settings'),

    path('create_order/<str:customer>', views.createOrder, name="create_order"),
    path('update_order/<str:order>', views.updateOrder, name="update_order"),
    path('delete_order/<str:order>', views.deleteOrder, name="delete_order"),

    path('register', views.registerPage, name="register_account"),
    path('login', views.loginPage, name='login_account'),
    path('logout', views.logoutUser, name='logout_account'),

    #     reset accounts
    path('reset_password/', auth_view.PasswordResetView.as_view(template_name='accounts/auth/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_view.PasswordResetDoneView.as_view(template_name='accounts/auth/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(template_name='accounts/auth/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name='accounts/auth/password_reset_done.html'),
         name='password_reset_complete')
]

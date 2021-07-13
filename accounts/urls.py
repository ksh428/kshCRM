from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.loginPage,name="login"),
    path('account/',views.accountSettings,name="account"),
    path('user/',views.userPage,name="user-page"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('products/',views.products,name="products"),
    path('customer/<str:pk>/',views.customer,name="customer"),
    path('create_order/<str:pk>/',views.createOrder,name="create_order"),
    path('update_order/<str:pk>/',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk>/',views.deleteOrder,name="delete_order")


]

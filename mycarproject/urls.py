from django.urls import path
#from .views import home, cars, add_car, about, dashboard, contact_view, login_view, register_view, logout_view, create_customer,  create_order_with_details
from .import views  
urlpatterns=[
    path('', views.home,name='home'),
    path('cars/', views.cars,name='cars'),
    path('add_car/', views.add_car,name='add_car'),
    path('contact/', views.contact_view,name='contact'),
    path('mark_delivered/<int:pk>/', views.mark_delivered, name='mark_delivered'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_order_with_details/<int:id>/', views.create_order_with_details, name='create_order_with_details'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('one',views.customer_page,name='one'),
   

] 
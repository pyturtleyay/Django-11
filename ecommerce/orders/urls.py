
from django.urls import path
from . import views
 


app_name = 'orders'

urlpatterns = [
    # 'create/' with order_create function, path name is 'order_create'
      path('create/', views.order_create, name='order_create')

]
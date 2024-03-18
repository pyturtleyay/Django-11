from django.urls import path
from . import views


from django.urls import path
from django.urls import include
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings
app_name = 'shop'


urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('login/', views.user_login, name="login"),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

    # change password urls

    path('password-change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb54>/<token>',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset/confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

#-----------------Store-------------------#
    #Home Page
    path('', views.product_list, name="product_list"),

    #Product Detail
    path('product_detail/<int:id>/<slug:slug>/',
         views.product_detail, name="product_detail"),

    #Profile
    path('profile/',
         views.profile, name="profile"),

    #Category
    path('c/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),

#-----------------Payment-------------------#
     # path process
    path('process/', views.payment_process, name='process'),

	# path completed
    path('canceled/', views.payment_canceled, name='canceled'),

	# path canceled
    path('completed/', views.payment_completed, name='completed'),

#-----------------Order-------------------#
    # 'create/' with order_create function, path name is 'order_create
     path('create/', views.order_create, name='order_create'),

#-----------------Cart-------------------#
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),

    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove')

]

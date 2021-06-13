from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
urlpatterns = [


    path('',views.ProductView.as_view(),name="home"),   
    # path('', views.home),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.showCart,name="showCart"),
    path('minuscart/',views.minuscart,name="minuscart"),
    path('pluscart/',views.pluscart,name="pluscart"),
    path('removecart/',views.removecart,name="removecart"),


    path('buy/', views.buy_now, name='buy-now'),
    path('accounts/profile/',views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('test/', views.test, name='test'),

    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',
    form_class=PasswordChangeForm,success_url='/passwordchangedone/'),name="changepassword"),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name="passwordchangedone"),

    

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="password_reset_form.html",form_class=PasswordResetForm),
    name="password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
    name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",form_class=SetPasswordForm),
    name="password_reset_confirm"),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
    name="password_reset_complete"),







    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobile_data'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm),name="login"),
    path('accounts/logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),


    path('registration/', views.RegisterationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_done/', views.payment_done, name='payment_done'),



]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


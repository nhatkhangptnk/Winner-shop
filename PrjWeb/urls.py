"""PrjWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from Home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.SiteLoginView.as_view(), name='login'),
    path('register/', views.SiteRegisterView.as_view(), name='register'),
    path('register/done/', views.SiteRegisterDoneView.as_view(), name='register_done'),
    path('logout/', views.SiteLogOutView.as_view(), name='logout'),
    path('accounts/profile/', views.EditProfileView.as_view(), name='profile'),
    path('changepassword', views.SiteChangePassword.as_view(), name='changepassword'),
    path('changepassworddone', views.SiteChangePassDoneView.as_view(), name='password_change_done'),
    path('editprofile', views.SiteEditProfile.as_view(), name='editprofile'),
    path('addcart/', views.addcart, name='addcart'),
    path('updatecart/', views.updatecart, name='updatecart'),
    path('deletecart/', views.deletecart, name='deletecart'),
    path('allproduct/',views.allproduct, name='allproduct'),
    path('products/brands/<str:id>', views.BrandItems),
    path('products/categories/<str:id>', views.CategoryItems),
    path('cart/', views.InCart, name='cart'),
    path('doneorder/', views.OrderCart, name='doneorder'),
    path('userorder/', views.OderDT, name='userorder'),
    path('<str:cate_name>/<str:id>', views.ProductCategory),
    path('product<str:id>/', views.productdetail),
    path('blog/', views.Blog, name='blog'),
    path('blog-single/', views.BLog_Single, name='blog-single'),
    path('addfavorite/', views.addfavorite, name='addfavorite'),
    path('remove<str:productID>/', views.deletefavorite, name='deletefavorite'),
    path('addreview/', views.ReviewProduct, name='reviewproduct'),
    path('favorite/', views.Sitefavorite, name='favorite'),
    path('search/', views.search, name='search'),
    path('resultsearchprice/', views.SPResult, name='resultsearchprice'),
    path('saleproduct/',views.saleproduct, name='saleproduct'),
    path('paymentmth/',views.SitePTTT, name='paymentmth'),
    path('', views.home, name='home')
]
handler404= 'Home.views.error_404'

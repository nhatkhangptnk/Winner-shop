from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from Home.models import *
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import random
def home(request):
    return redirect('http://127.0.0.1:8000/')
def index(request):
    n = random.randint(0, 27)
    cateParent = Category.objects.filter(cate_parent_id=0)
    featureItems = Product.objects.filter(product_status=1)[n:n+6]
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    maxprice = Product.objects.order_by('-product_price').first().product_price
    context = {
        'parents': cateParent,
        'brandItems': brandItems,
        'featureItems': featureItems,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem,
        'MaxPrice': maxprice
    }
    return render(request, "Home/index.html", context)

def SPResult(request):
    pr = str(request.GET['pr'])
    if(len(pr)==0):
        pr = '0,2000000'
    FromPrice, ToPrice = pr.split(',')
    ResultSP = Product.objects.filter(product_price_sale__gte=float(FromPrice), product_price_sale__lte=float(ToPrice))
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    cateParent = Category.objects.filter(cate_parent_id=0)
    context = {
        'parents': cateParent,
        'brandItems': brandItems,
        'ItemActive': recommendedItemActive,
        'ResultSP': ResultSP,
        'FromPrice': FromPrice,
        'ToPrice': ToPrice,
        'Item': recommendedItem
    }
    return render(request, "Home/searchprice.html", context)

def login(request):
    return render(request, "Home/login.html")

class SiteLoginView(LoginView):
    template_name = 'Home/login.html'
    next_page = 'http://127.0.0.1:8000/'

class SiteChangePassword(PasswordChangeView):
    template_name = 'Home/changepassword.html'

class SiteEditProfile(UpdateView):
    form_class = UserChangeForm
    template_name = 'Home/editprofile.html'
    success_url = 'http://127.0.0.1:8000/accounts/profile/'

    def get_object(self, queryset=None):
        return self.request.user
class SiteChangePassDoneView(PasswordChangeDoneView):
    template_name = 'Home/changepassworddone.html'

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {"username": UsernameField}
        widgets = {
            'email': forms.EmailInput(attrs={'required': True})
        }

class SiteRegisterView(FormView):
    template_name = 'Home/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        # Kiểm tra xác thực
        data = form.cleaned_data
        new_user = User.objects.create_user(
            username=data['username'],
            password=data['password1'],
            email=data['email']
        )
        url = f"{reverse('register_done')}?username={new_user.username}"
        return redirect(url)

class SiteRegisterDoneView(TemplateView):
    template_name = 'Home/register_done.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['username'] = self.request.GET.get('username')
        return contex

class SiteLogOutView(LogoutView):
    template_name = 'Home/logout.html'
class EditProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'Home/profile.html'

def ProductCategory(request,cate_name, id):
    cateParent = Category.objects.filter(cate_parent_id=0)
    ProductCategory = Product.objects.filter(cate_id=id)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    context = {
        'parents': cateParent,
        'ProductCategory': ProductCategory,
        'brandItems': brandItems,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem
    }
    return render(request, 'Home/ProductCategory.html', context)

def CategoryItems(request, id):
    cateParent = Category.objects.filter(cate_parent_id=0)
    ProductCategory = Product.objects.filter(cate_id=id)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    context = {
        'parents': cateParent,
        'ProductCategory': ProductCategory,
        'brandItems': brandItems,
        'ItemActive':recommendedItemActive,
        'Item':recommendedItem
    }
    return render(request, 'Home/ProductCategory.html', context)

def BrandItems(request,id):
    cateParent = Category.objects.filter(cate_parent_id=0)
    ProductBrand = Product.objects.filter(brand_id=id)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    context = {
        'ProductBrand': ProductBrand,
        'brandItems': brandItems,
        'parents': cateParent,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem
    }
    return render(request, 'Home/ProductBrand.html', context)
def productdetail(request,id):
    cateParent = Category.objects.filter(cate_parent_id=0)
    ProductDetail = Product.objects.get(id=id)
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter(cate_id=ProductDetail.cate_id)[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[0:3]
    review = Review.objects.filter(ID_Product=id)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    context = {
        'parents': cateParent,
        'brandItems': brandItems,
        'ProductDetail': ProductDetail,
        'AllReview': review,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem
    }
    return render(request, 'Home/product-details.html', context)

def addcart(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        Id = request.POST.get('id')
        Num = request.POST.get('num')
        ProDetail = Product.objects.get(id=Id)
        if (Id, request.user.username) in Usercart.objects.values_list('id_product', 'username'):
            HUC=Usercart.objects.get(id_product=Id, username=request.user.username)
            Usercart.objects.filter(id_product=Id, username=request.user.username).update(num=HUC.num+int(Num), total=(HUC.num+int(Num))*HUC.price)
        else:
            Usercart.objects.create(
                username=request.user.username,
                id_product=Id,
                price=ProDetail.product_price_sale,
                image=ProDetail.product_image,
                num=int(Num),
                total=int(Num)*int(ProDetail.product_price_sale),
                name_product=ProDetail.product_name
            )
        CartInfo = {'CartInfo': Usercart.objects.filter(username=request.user.username)}
        return render(request, 'Home/addcart.html', CartInfo)

def addfavorite(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        Id = request.POST.get('id')
        ProDetail = Product.objects.get(id=Id)
        Favorite.objects.create(
            username=request.user.username,
            productID=Id,
            productname=ProDetail.product_name,
            productimage=ProDetail.product_image,
            productprice=ProDetail.product_price_sale,
            saleoff=ProDetail.saleoff
        )
        return redirect("addfavorite")
def Sitefavorite(request):
    favorite = Favorite.objects.filter(username=request.user.username)
    cateParent = Category.objects.filter(cate_parent_id=0)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    context = {
        'brandItems': brandItems,
        'Favorite': favorite,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem,
        'parents': cateParent
    }
    return render(request, 'Home/favorite.html', context)

def deletefavorite(request, productID):
    Favorite.objects.filter(productID=productID, username=request.user.username).delete()
    return HttpResponseRedirect("/favorite")
def deletecart(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        Id = request.POST.get('id')
        Usercart.objects.filter(id_product=Id, username=request.user.username).delete()
    return redirect("deletecart")

def updatecart(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        Id = request.POST.get('id')
        Num = request.POST.get('num')
        if int(Num) == 0:
            deletecart(request)
        elif int(Num)<0:
            return redirect("updatecart")
        else:
            HUC = Usercart.objects.get(id_product=Id, username=request.user.username)
            Usercart.objects.filter(id_product=Id, username=request.user.username).update(num=int(Num), total=int(Num) * HUC.price)
    return redirect("updatecart")

class SiteCart(LoginRequiredMixin, TemplateView):
    template_name = "Home/cart.html"

def OrderCart(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        Shipname = request.POST.get('shipname')
        Shipphone = request.POST.get('shipphone')
        Shipaddress = request.POST.get('shipaddress')
        Totalcart = request.POST.get('totalcart')
        Totalcart = Totalcart.replace(',', '')
        Totalcart = int(Totalcart.rstrip('vnd'))
        Cart = Usercart.objects.filter(username=request.user.username)
        sum=0
        if len(Order.objects.values_list('id'))>0:
            Id = len(Order.objects.values_list('id'))+1
        else:
            Id=1
        for i in Cart:
            sum += int(i.total)
            Product.objects.filter(id=i.id_product).update(product_quantity=Product.objects.get(id=i.id_product).product_quantity-i.num,quantity_sold= Product.objects.get(id=i.id_product).quantity_sold+i.num)
        Order.objects.create(
            id=str(Id),
            ship_name=str(Shipname),
            ship_address=str(Shipaddress),
            ship_phone=str(Shipphone),
            ordered_date=str(datetime.date(datetime.now())),
            total_amount=Totalcart,
            order_status=1,
            user_order=request.user.username
        )
        for i in Cart:
            Orderdetail.objects.create(
                order_id=str(Id),
                id_product=i.id_product,
                product_price=i.price,
                product_quantity=i.num,
                amount=i.price*i.num,
                username=request.user.username
            )
        Usercart.objects.filter(username=request.user.username).delete()
    return render(request, "Home/doneorder.html")

def OderDT(request):
    ordDT = Orderdetail.objects.filter(username=request.user.username).values('product_quantity','product_price','amount','id_product')
    prd = Product.objects.filter(id__in=Orderdetail.objects.values_list('id_product', flat=True)).values('product_name','product_image', 'id')
    for i in range(0, len(ordDT)):
        for j in range(0, len(ordDT)):
            if ordDT[i].get('id_product') == prd[j].get('id'):
                ordDT[i].update(prd[j])
    return render(request, "Home/userorder.html", {'OrderDt': ordDT})

def InCart(request):
    sum = 0
    shippingcost = 30000
    percent = 0
    voucher = ''
    if 'http://127.0.0.1:8000/cart/' in request.META.get('HTTP_REFERER') and 'voucher' in request.build_absolute_uri():
        voucher = request.GET['voucher']
    if voucher in Voucher.objects.values_list('Code', flat=True):
        getvch = Voucher.objects.get(Code=voucher)
        #Voucher.objects.filter(Code=voucher).delete()
        percent = getvch.Percent
    Cart = Usercart.objects.filter(username=request.user.username)
    if Cart:
        for i in Cart:
            sum += int(i.total)
        discount = int(sum*percent/100)
        return render(request, "Home/cart.html", {'sum': sum, 'Cart': Cart, 'shippingcost': shippingcost, 'Discount':discount})
    else:
        return render(request, "Home/cart.html")

def allproduct(request):
    AllProduct = Product.objects.filter()
    cateParent = Category.objects.filter(cate_parent_id=0)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    context = {
        'brandItems': brandItems,
        'AllProduct': AllProduct,
        'parents': cateParent,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem
    }
    return render(request, "Home/allproduct.html", context)

def Blog(request):
    cateParent = Category.objects.filter(cate_parent_id=0)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    context = {
        'brandItems': brandItems,
        'parents': cateParent
    }
    return render(request, 'Home/blog.html', context)

def BLog_Single(request):
    cateParent = Category.objects.filter(cate_parent_id=0)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    context = {
        'brandItems': brandItems,
        'parents': cateParent
    }
    return render(request, 'Home/blog-single.html', context)
def ReviewProduct(request):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        Id = request.POST.get('id')
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Comment = request.POST.get('comment')
        Review.objects.create(
            ID_Product=Id,
            Name=Name,
            Email=Email,
            Comment=Comment,
            Time=datetime.today().strftime("%H:%M:%S"),
            Date=datetime.today().strftime('%Y-%m-%d')
        )

        return redirect("reviewproduct")

def search(request):
    q=request.GET['q']
    data = Product.objects.filter(brand_name__icontains=q).order_by('id') or \
          Product.objects.filter(product_name__icontains=q).order_by('id') or \
          Product.objects.filter(product_keyword__icontains=q).order_by('id')
    AllProduct = Product.objects.filter()
    cateParent = Category.objects.filter(cate_parent_id=0)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    context = {
        'brandItems': brandItems,
        'AllProduct': AllProduct,
        'parents': cateParent,
        'data': data
    }
    return render(request, 'Home/search.html', context)

def saleproduct(request):
    SaleProduct = Product.objects.filter(saleoff__gt=0)
    cateParent = Category.objects.filter(cate_parent_id=0)
    brandItems = Product.objects.values_list('brand_id', 'brand_name', named=True).order_by('brand_id').distinct()
    recommendedItemActive = Product.objects.order_by('-quantity_sold').filter()[:3]
    recommendedItem = Product.objects.order_by('-quantity_sold').filter()[3:6]
    context = {
        'brandItems': brandItems,
        'SaleProduct': SaleProduct,
        'parents': cateParent,
        'ItemActive': recommendedItemActive,
        'Item': recommendedItem
    }
    return render(request, "Home/product_sale.html", context)

def SitePTTT(request):
    return render(request, "Home/pttt.html")

def error_404(request, exception):
    return render(request, 'Home/404.html', {'message': exception})

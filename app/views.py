from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import query
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse,JsonResponse
from app.models import Cart, Customer, OrderPlaced, Product
from django.shortcuts import redirect, render
from django.views import View
from .forms import CustomerProfileForm, RegistrationForm,LoginForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):    
    def get(self,request):
        if request.user.is_authenticated:
            topwears = Product.objects.filter(category='TW')
            Bottomwears = Product.objects.filter(category='BW')
            Mobile = Product.objects.filter(category='M')
            total_product = Cart.objects.filter(user=request.user).count()

        else:
            topwears = Product.objects.filter(category='TW')
            Bottomwears = Product.objects.filter(category='BW')
            Mobile = Product.objects.filter(category='M')
            total_product = 0
        
        return render(request,'app/home.html',{'topwears':topwears,'Bottomwears':Bottomwears,'Mobile':Mobile,'total_product':total_product})
        



# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        
        if request.user.is_authenticated:
         total_product = Cart.objects.filter(user=request.user).count()
         product_in_cart = False 
         product_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
         return render(request,'app/productdetail.html',{'product':product,'product_in_cart':product_in_cart,'total_product':total_product})
        else:
         return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        user_id = request.user.id
        pk = request.GET.get('product_id')
        product = Product.objects.get(id=pk)
        Cart(user=user,product=product,userid=user_id).save()
        return redirect(showCart)
    else:   
        return redirect('login')

def showCart(request):
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    
    if request.user.is_authenticated:
        total_product = Cart.objects.filter(user=request.user).count()
        cart = Cart.objects.filter(user=request.user)
        if cart:
            for p in cart:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
            totalamount = shipping_amount + amount     
            return render(request,'app/addtocart.html',{'cart':cart,'totalamount':totalamount,'amount':amount,'total_product':total_product}) 
        else:
            messages.warning(request,'You have no Product in Your Cart !!')
    else:
        messages.warning(request,'You have no Product in Your Cart !! You have Not Logged In !!')
        total_product = 0
    return render(request,'app/addtocart.html',{'totalamount':totalamount,'amount':amount,'total_product':total_product})


@login_required
def checkout(request):

    customer = Customer.objects.filter(user=request.user)
    products = Cart.objects.filter(user=request.user)
    tempamount = 0.0
    totalamount = 0.0
    if products:
        for i in products:
            tempamount=(i.quantity * i.product.discounted_price)
            totalamount += tempamount
    totalamount += 70 
    return render(request, 'app/checkout.html',{'customer':customer,'products':products,'totalamount':totalamount})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customerObj = Customer.objects.get(id=custid)
    cartproducts = Cart.objects.filter(user=user)
    for i in cartproducts:
        orderDetail = OrderPlaced(user=user,customer=customerObj,product=i.product,quantity=i.quantity)
        orderDetail.save()
    return render(request,'app/orders.html')










def buy_now(request):
 return render(request, 'app/buynow.html')


def pluscart(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        c = Cart.objects.get(Q(product=id) & Q(user=request.user))
        c.quantity  += 1
        c.save()
        quantity = c.quantity
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount      

        data = {
            'quantity':quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)

def minuscart(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        c = Cart.objects.get(Q(product=id) & Q(user=request.user))
        c.quantity  -= 1
        c.save()
        quantity = c.quantity
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount      
        
        if totalamount == 70:
            totalamount = 0   
        
        
        data = {
            'quantity':quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)   
    

def removecart(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        c = Cart.objects.get(Q(product=id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount      
        
        if totalamount == 70:
            totalamount = 0   
        total_product = Cart.objects.filter(user=request.user).count()
        
        data = {
            'total_product':total_product,
            'amount':amount,
            'totalamount':totalamount
        }
        
    return JsonResponse(data)   




@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        
        profiledata = User.objects.get(username=request.user)
        
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','profiledata':profiledata})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        profiledata = User.objects.get(username=request.user)
        
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'New address registered ! Shop and Enjoy ! ')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','profiledata':profiledata})

@login_required
def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'active':'btn-primary','address':address})

def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)
    total_product = Cart.objects.filter(user=request.user).count()

    return render(request, 'app/orders.html',{'orders':orders,'total_product':total_product})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'vivo' or data == 'redmi' or data == 'mi' or data == 'apple' or data == 'samsung':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Below':
        mobile = Product.objects.filter(category='M').filter(discounted_price__lt= 10000)
    elif data == 'above':
        mobile = Product.objects.filter(category='M').filter(discounted_price__gt=10000)        

    return render(request, 'app/mobile.html',{'mobile':mobile})



# def customerregistration(request):
#     form = RegistrationForm()
#     return render(request, 'app/customerregistration.html',{'form':form})
class RegisterationView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congrats !! Registered Successfully. ')
        return render(request,'app/customerregistration.html',{'form':form})    




def test(request):
    return render(request,'app/test.html')
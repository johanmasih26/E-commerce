from django.contrib.auth import login
from django.db.models import query
from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse,JsonResponse
from app.models import Cart, Customer, Product
from django.shortcuts import redirect, render
from django.views import View
from .forms import CustomerProfileForm, RegistrationForm,LoginForm
from django.contrib import messages
from django.db.models import Q



class ProductView(View):    
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        Bottomwears = Product.objects.filter(category='BW')
        Mobile = Product.objects.filter(category='M')
        # total_product = Cart.objects.filter(user=request.user).count()
        
        return render(request,'app/home.html',{'topwears':topwears,'Bottomwears':Bottomwears,'Mobile':Mobile})
        



# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
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
    total_product = Cart.objects.filter(user=request.user).count()
    print(total_product)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(userid=request.user.id)
        if cart:
            for p in cart:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
            totalamount = shipping_amount + amount     
            return render(request,'app/addtocart.html',{'cart':cart,'totalamount':totalamount,'amount':amount,'total_product':total_product}) 
        else:
            messages.warning(request,'You have no Product in Your Cart !!')

    return render(request,'app/addtocart.html',{'cart':cart,'totalamount':totalamount,'amount':amount})


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





class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'New address registered !!')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'active':'btn-primary','address':address})

def orders(request):
 return render(request, 'app/orders.html')

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



def checkout(request):
 return render(request, 'app/checkout.html')


def test(request):
    return render(request,'app/test.html')
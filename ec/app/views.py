from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Product,Customer, Cart, OrderPlaced,Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages         # thông báo 
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    return render(request,"app/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    wishitem= 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    return render(request,"app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    return render(request,"app/contact.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val): 
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user= request.user))
            wishitem = len(Wishlist.objects.filter(user= request.user))      
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())  #locals() :built-in function trong Python trả về một dictionary chứa tất cả các biến cục bộ được định nghĩa trong function hiện tại.
        #đối số 3 nhận 1 dict -> truyền tất cả biến cục bộ vào template dc render

@method_decorator(login_required, name='dispatch')     
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user= request.user))
            wishitem = len(Wishlist.objects.filter(user= request.user))   
        product= Product.objects.filter(title= val)
        title = Product.objects.filter(category= product[0].category).values('title')
        return render(request, 'app/category.html',locals())
    
@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist= Wishlist.objects.filter(Q(product=product)& Q(user=request.user))
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user= request.user))
            wishitem = len(Wishlist.objects.filter(user= request.user))
        return render(request, "app/productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratutations ! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())
    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user= request.user))
            wishitem = len(Wishlist.objects.filter(user= request.user)) 
            form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user= request.user
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            mobile= form.cleaned_data['mobile']
            state= form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']
            reg= Customer(user= user, name= name, locality= locality, mobile= mobile, state= state, zipcode= zipcode)
            reg.save()
            messages.success(request,"Congratutations ! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())

@login_required
def address(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    add= Customer.objects.filter(user= request.user)
    return render(request, 'app/address.html',locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self,request, pk):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user= request.user))
            wishitem = len(Wishlist.objects.filter(user= request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)   # Tự động diền vào form
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add= Customer.objects.get(pk=pk)
            add.name= form.cleaned_data['name']
            add.locality= form.cleaned_data['locality']
            add.mobile= form.cleaned_data['mobile']
            add.state= form.cleaned_data['state']
            add.zipcode= form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratutations ! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

@login_required
def add_to_cart(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user, product= product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    user = request.user
    cart= Cart.objects.filter(user= user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount= amount +   40000  # 40 là phí vận chuyển
    return render(request, 'app/addtocart.html', locals())

@login_required
def show_wishlist(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))
    user= request.user
    product = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html",locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        wishitem=0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user= request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount+ value
        totalamount = famount + 40
        return render(request, "app/checkout.html", locals())

@login_required  
def orders(request):
    wishitem=0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user= request.user))
    order_placed = OrderPlaced.objects.filter(user= request.user)
    return render(request, 'app/orders.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c=  Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity +=1
        c.save()
        user = request.user
        cart=  Cart.objects.filter(user=user)
        amount = 0 
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount+= value
        totalamount = amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c=  Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity -=1
        c.save()
        user = request.user
        cart=  Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount+= value
        totalamount = amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
        if request.method == 'GET':
            prod_id= request.GET['prod_id']
            c=  Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
            c.delete()
            user = request.user
            cart=  Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount+= value
            totalamount = amount + 40
            data={
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
        return JsonResponse(data)

def plus_wishlist(request):
    if request.method == "GET":
        prod_id =request.GET['prod_id']
        product = Product.objects.get(id= prod_id)
        user = request.user
        Wishlist(user= user, product = product).save()
        data= {
            'message': 'Whishlist Added Successfully'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == "GET":
        prod_id =request.GET['prod_id']
        product = Product.objects.get(id= prod_id)
        user = request.user
        Wishlist.objects.filter(user= user, product = product).delete()
        data= {
            'message': 'Whishlist Remove Successfully'
        }
        return JsonResponse(data)

@login_required
def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains= query))  #title__icontains chứa 2 dấu _
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user= request.user))
        wishitem = len(Wishlist.objects.filter(user= request.user))

    return render(request, "app/search.html",locals())

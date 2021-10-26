from django.shortcuts import render, redirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView,ListView, DetailView, CreateView, UpdateView
from .forms import RegistrationForm,LoginForm,UpdateForm,ReviewForm,PlaceOrderForm,UserForm
from .models import Cart,Review,Orders,Address,Userdetails
from seller.models import Products,Brand
from .decorators import signin_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.db.models import IntegerField, Case, Value, When,Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class RegistrationView(TemplateView):
    form_class = RegistrationForm
    template_name = "registration.html"
    model = User
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cust_signin")


class SignInView(TemplateView):
    template_name = "login.html"
    form_class = LoginForm
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("customer_home")
            else:
                self.context["form"] = form
                return render(request, self.template_name, self.context)


@method_decorator(signin_required, name="dispatch")
class HomePageView(ListView):
    template_name = 'homepage.html'
    model = Products
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = Products.objects.all()
        paginator = Paginator(products, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            page_products = paginator.page(page)
        except PageNotAnInteger:
            page_products = paginator.page(1)
        except EmptyPage:
            page_products = paginator.page(paginator.num_pages)

        context['products'] = page_products
        return context

def search(request):
    search = request.GET['q']
    product = Products.objects.filter(product_name__icontains=search)
    context = {'product': product}
    return render(request, 'search.html', context)

@signin_required
def signout(request):
    logout(request)
    return redirect("cust_signin")


@signin_required
def mobiles(request):
    mobiles = Products.objects.filter(category='mobile')
    context = {'mobiles': mobiles}
    return render(request, 'category.html', context)
@signin_required
def laptops(request):
    laptops = Products.objects.filter(category="laptop")
    context = {'laptops': laptops}
    return render(request, 'category.html', context)
@signin_required
def tablets(request):
    tablets = Products.objects.filter(category="tablet")
    context = {'tablets': tablets}
    return render(request, 'category.html', context)
@signin_required
def price_low_to_high(request):
    low = Products.objects.all().order_by('price')
    context = {'low': low}
    return render(request, 'price_range.html', context)
@signin_required
def price_high_to_low(request):
    high = Products.objects.all().order_by('-price')
    context = {'high': high}
    return render(request, 'price_range.html', context)

# @signin_required
# def apple(request):
#     apple = Products.objects.filter(brand='apple')
#     context = {'apple': apple}
#     return render(request, 'category.html', context)
#
# @signin_required
# def lenovo(request):
#     lenovo = Products.objects.filter(brand='lenovo')
#     context = {'lenovo': lenovo}
#     return render(request, 'category.html', context)
#
# @signin_required
# def oppo(request):
#     oppo = Products.objects.filter(brand='oppo')
#     context = {'oppo': oppo}
#     return render(request, 'category.html', context)
#
# @signin_required
# def oneplus(request):
#     oneplus = Products.objects.filter(brand='oneplus')
#     context = {'oneplus': oneplus}
#     return render(request, 'category.html', context)
#
# @signin_required
# def redmi(request):
#     redmi = Products.objects.filter(brand='redmi')
#     context = {'redmi': redmi}
#     return render(request, 'category.html', context)
#
# @signin_required
# def samsung(request):
#     samsung = Products.objects.filter(brand='samsung')
#     context = {'samsung': samsung}
#     return render(request, 'category.html', context)

# @method_decorator(signin_required, name="dispatch")
def ViewDetails(request):
    dets=Userdetails.objects.filter(user=request.user)
    return render(request,'my_profile.html',{'dets':dets})

class EditDetails(TemplateView):
    user_form = UserForm
    profile_form = UpdateForm
    template_name = "user_details.html"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = UpdateForm(post_data, file_data, instance=request.user)
        #profile_form = UpdateForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('view_profile'))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)

        return self.render_to_response(context)




@method_decorator(signin_required, name="dispatch")
class ViewProduct(TemplateView):
    template_name = 'productdetail.html'
    context = {}

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        product = Products.objects.get(id=id)
        reviews = Review.objects.filter(product=product)
        similar_products=Products.objects.filter(brand=product.brand,category=product.category)
        self.context['product'] = product
        self.context['reviews'] = reviews
        self.context['similar_products']=similar_products
        return render(request, self.template_name, self.context)

def cart_count(user):
    cnt=Cart.objects.filter(user=user,status='ordernotplaced').count()
    return cnt

@signin_required
def add_to_cart(request, *args, **kwargs):
    print(kwargs)
    id = kwargs['id']
    product = Products.objects.get(id=id)
    if Cart.objects.filter(product=product, user=request.user, status='ordernotplaced').exists():
        cart = Cart.objects.get(product=product, user=request.user)
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart(product=product, user=request.user)
        cart.save()
        print('product added')
    return redirect('mycart')

@method_decorator(signin_required, name="dispatch")
class MyCart(TemplateView):
    template_name = 'cart.html'
    context = {}

    def get(self, request, *args, **kwargs):
        cart_products = Cart.objects.filter(user=request.user, status='ordernotplaced')
        # total = Cart.objects.filter(status="ordernotplaced", user=request.user).aggregate(Sum('product__price'))
        total = 0
        for cart in cart_products:
            total += cart.product.price * cart.quantity
        print(total)

        self.context['cart_products'] = cart_products
        self.context['total'] = total
        # self.context['cnt']=cart_count(request.user)
        return render(request, self.template_name, self.context)

@method_decorator(signin_required, name="dispatch")
class DeleteFromCart(TemplateView):
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        cart_product = Cart.objects.get(id=id)
        cart_product.delete()
        return redirect('mycart')


@method_decorator(signin_required, name="dispatch")
class WriteReview(TemplateView):
    template_name = 'review.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        product = Products.objects.get(id=id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            new_review = Review(user=request.user, product=product, review=review)
            new_review.save()
            return redirect('viewproduct', product.id)
@signin_required
def place_order(request, *args, **kwargs):
    pid = kwargs["pid"]
    product = Products.objects.get(id=pid)
    instance = {
        "product": product.product_name
    }
    form = PlaceOrderForm(initial=instance)
    context = {}
    brands = Brand.objects.all()
    context['brands'] = brands
    context["form"] = form

    if request.method == "POST":
        cid = kwargs["cid"]
        cart = Cart.objects.get(id=cid)
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            product = product
            order = Orders(address=address, product=product, user=request.user)
            order.save()
            cart.status = "orderplaced"
            cart.save()
            return redirect("customer_home")

    return render(request, "placeorder.html", context)
@signin_required
def view_orders(request,*args,**kwargs):
    orders = Orders.objects.filter(user=request.user, status="ordered")
    brands = Brand.objects.all()

    context = {
        "orders": orders,
        "brands": brands
    }
    return render(request, "vieworders.html", context)
@signin_required
def cancel_order(request,*args,**kwargs):
    id=kwargs.get("id")
    order=Orders.objects.get(id=id)
    order.status="cancelled"
    order.save()
    return redirect("vieworders")

class BasePage(TemplateView):
    template_name = 'cust_base.html'
    context = {}

    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        self.context['brands'] = brands
        return render(request, self.template_name, self.context)

class FilterByBrand(TemplateView):
    template_name = 'brandfilter.html'
    context={}
    def get(self, request, *args, **kwargs):
        id=kwargs['pk']
        brand=Brand.objects.get(id=id)
        products=Products.objects.filter(brand=brand)
        self.context['products']=products
        return render(request,self.template_name,self.context)

def cart_plus(request,*args,**kwargs):
    id=kwargs['pk']
    cart=Cart.objects.get(id=id)
    cart.quantity+=1
    cart.save()
    return redirect('mycart')

def cart_minus(request,*args,**kwargs):
    id=kwargs['pk']
    cart=Cart.objects.get(id=id)
    cart.quantity-=1
    cart.save()
    if cart.quantity<1:
        return redirect('deletecart',cart.id)
    return redirect('mycart')

def CheckoutView(request):
    address = Address.objects.filter(user=request.user)
    print('data :',address)
    print(address)

    addr=[]
    for i in address:
        data={}
        print(i.name)
        data['name']=i.name
        data['mob']=i.mob_no
        data['address']='{}, {}, {}, {}, India, {} '.format(i.house,i.street,i.town,i.state,i.pin)
        data['landmark']='{}'.format(i.landmark)
        data['id']=i.id
        addr.append(data)
    print('addresses :', addr)
    context = {
                'address':addr
            }
    if request.method == "POST":
        print(request.POST)
        x=request.POST
        new_address=Address()
        new_address.user=request.user
        new_address.name=x['name']
        new_address.mob_no=x['mob_no']
        new_address.house=x['house']
        new_address.street=x['street_address']
        new_address.town=x['town']
        new_address.state=x['state']
        new_address.pin=x['pin']
        new_address.landmark=x['landmark']
        if( Address.objects.filter(house=x['house'],pin=x['pin']).exists()):
            print('already exists')
        else:
            new_address.save()
            print(new_address.street)
            return redirect("checkout")
    return render(request, 'checkout.html', context)

def summery(request,*args,**kwargs):
    Orders.objects.filter(user=request.user,status='pending').delete()
    print(kwargs.get('id'))
    print(request.user)
    cart_item=Cart.objects.filter(user=request.user,status='ordernotplaced')
    address = Address.objects.get(id=kwargs.get('id'))
    ad = '{},{},{}, {}, {}, {}, India, {} '.format(address.name, address.mob_no, address.house, address.street,
                                                   address.town, address.state, address.pin, address.landmark)
    for i in cart_item:
        print(Products.objects.get(id=i.product.id).id)
        order=Orders()
        if(Orders.objects.filter(product=Products.objects.get(id=i.product.id),user=request.user,address=ad)).exists():
            print('already exists')
        else:
            order.product=Products.objects.get(id=i.product.id)
            order.user=request.user
            order.seller=Products.objects.get(id=i.product.id).user
            order.address=ad
            order.quantity=i.quantity
            order.save()
            print(order.date)
            print("saved")
    # address = Orders.objects.filter(user=request.user,status='pending')[0].address
    print(address)
    print("hi")
    sum=0
    qty=0
    data=[]
    for i in cart_item:
        content={}
        product=Products.objects.get(id=i.product_id)
        print(Products.objects.get(id=i.product_id).image.url)
        content['image']=product.image.url
        content['name']=product.product_name.capitalize()
        content['color']=product.color
        content['seller']=product.user
        content['price']=product.price
        content['offer']=product.offer
        content['quantity']=i.quantity
        sum += (product.price*i.quantity)
        qty+=i.quantity
        data.append(content)

    return render(request,'order_summery.html',{'data':data,'address':ad,'sum':sum,'qty':qty})

class DeleteAddress(TemplateView):
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        address = Address.objects.get(id=id)
        address.delete()
        return redirect('checkout')

def editaddress(request,*args,**kwargs):
    id = kwargs['id']
    address = Address.objects.get(user=request.user,id=id)
    print(address.name)
    context={'address': address}

    if request.method=="POST":
        print(request.POST)
        x = request.POST
        new_address = Address.objects.get(user=request.user,id=id)
        new_address.user = request.user
        new_address.name = x['name']
        new_address.mob_no = x['mob_no']
        new_address.house = x['house']
        new_address.street = x['street_address']
        new_address.town = x['town']
        new_address.state = x['state']
        new_address.pin = x['pin']
        new_address.landmark = x['landmark']
        if (Address.objects.filter(house=x['house'], pin=x['pin']).exists()):
            print('already exists')
        else:
            new_address.save()
            print(new_address.street)
            return redirect("checkout")
    return render(request, 'editaddress.html', context)

class GatewayView(TemplateView):
    template_name = "stripe.html"

    def get_context_data(self, **kwargs):
        total = Cart.objects.filter(status="ordernotplaced", user=self.request.user).aggregate(Sum('product__price'))
        context = super().get_context_data(**kwargs)
        context['total'] = total
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):
    if request.method == "POST":
        charge = stripe.Charge.create(
            amount=10,
            currency="INR",
            description="Payment of product",
            source=request.POST['stripeToken']
        )
        cart_items = Cart.objects.filter(status="ordernotplaced", user=request.user)
        ordered_items=Orders.objects.filter(status="pending",user=request.user)
        for item in cart_items:
            item.status="orderplaced"
            item.product.stock=item.product.stock-item.quantity
            # print(item.product.stock)
        for item in ordered_items:
            item.status="ordered"

        return render(request, 'payment.html',charge)
    return render(request, 'payment.html')
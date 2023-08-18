from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf.urls.static import static
from .form import *
from .models import *
from .filters import *
import random

from django.contrib.auth.models import User, Group


from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

#Constant
HOT_GAMES = 4
RELATED_GAMES = 5

# Create your views here.
#====================HOME PAGE==========================
def home(request):
    user = request.user
    products = Product.objects.all()
    platforms = Platform.objects.all()

    hot_games = get_hot_games(products)
    categories = get_categories(platforms, products)
    cart_items = count_cart_item(request.user)
    
   
    is_logged_in = False

    if user == None:
        is_logged_in = False
    else:
        is_logged_in = True

    context = {'is_logged_in': is_logged_in, 'products' : products, 'platforms': platforms, 'categories': categories,
               'hot_games' : hot_games, 'cart_items' : cart_items
               }

    return render(request, 'home.html', context)


def get_categories(platforms, products):
    categories = []

    for i in platforms:
        list_product = products.filter(platForm = i)
        temp_dict = {'platform' : i, 'products' : list_product}
        categories.append(temp_dict)

    return categories

def get_hot_games(products):
    items = list(products)
    hot_games = random.sample(items, HOT_GAMES)

    return hot_games


def get_all_games():
    return None

    

#==========================END HOME PAGE============================

#==========================PRODUCT PAGE=============================
def product(request, id):
    product = Product.objects.get(id = id)
    images = ProductImages.objects.filter(product = product)
    tag = product.tag.first()
    favor = is_favor(request.user, product)
    status = get_status(id)
    cart_items = count_cart_item(request.user)


    related_games = get_related_products(sample = product)

    context = {'product' : product, 'images' : images, 'tag' : tag, 'related_games' : related_games,
               'favor' : favor, 'status' : status, 'cart_items' : cart_items
               }

    return render(request, 'product.html', context)


def is_favor(user, product):
    if user.is_anonymous:
        return 'False'
    
    if user.groups.filter(name='admin').exists():
        return 'False'

    customer = Customer.objects.get(user = user).name
    if FavoriteProduct.objects.filter(customer = customer, product = product).exists():
        return 'True'
    else:
       return 'False'

    

def get_related_products(sample):
    related_games = []
    sample_tag = sample.tag.all()

    count = 0

    products = Product.objects.all()

    try:
        for product in products:
            if count == RELATED_GAMES:
                break
            if product != sample:
                tag = product.tag.all()
                for i in tag:
                    if i in sample_tag:
                        related_games.append(product)
                        count += 1
                        break

        return related_games
    except:
        return None

def add_to_favorite(request, id):
    product = Product.objects.get(id = id)

    customer = Customer.objects.get(user = request.user).name

    if FavoriteProduct.objects.filter(customer = customer, product = product).exists():
        favor = FavoriteProduct.objects.filter(customer = customer, product = product)
        favor.delete()
    else:
        FavoriteProduct.objects.create(customer = customer, product = product)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def get_status(id):
    product = Product.objects.get(id = id)

    if Account.objects.filter(product = product).exists():
        account = Account.objects.filter(product = product)

        for item in account:
            if item.status == 'Available':
                return 'Instock'
            
        return 'Stockout'
    else:
        return 'Stockout'

def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    customer = Customer.objects.get(user = request.user)

    cart = Order.objects.get(customer = customer)

    cart_items = OrderProduct.objects.filter(order = cart)

    for item in cart_items:
        if product == item.product:
            quantity = item.quantity + 1
            item.quantity = quantity
            item.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    OrderProduct.objects.create(order = cart, product = product, quantity = 1, type = 'Buy')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


    

def count_cart_item(user):
    if user.is_anonymous:
        return '0'
    if user.groups.filter(name='admin').exists():
        return '0'
    
    customer = Customer.objects.get(user = user)
    order = Order.objects.get(customer = customer)

    items = OrderProduct.objects.filter(order = order)

    total = 0

    for item in items:
        total += item.quantity

    return str(total)

def buy(request, id):
    product = Product.objects.get(id = id)
    customer = Customer.objects.get(user = request.user)

    order = Order.objects.get(customer = customer)

    list_items = OrderProduct.objects.filter(order = order)

    
    found = False

    for item in list_items:
        if product == item.product and item.type == 'Buy':
            quantity = item.quantity + 1
            item.quantity = quantity
            item.save()
            found = True

    if found == False:
        OrderProduct.objects.create(order = order, product = product, quantity = 1, type = 'Buy')

    
    cart_items = count_cart_item(user=request.user)

    items, total = get_cart_item(customer=customer)

    

    context = {
        'items' : items,
        'cart_items' : cart_items,
        'total' : total
    }

    return cart(request, request.user.username)

def rent(request, id):
    product = Product.objects.get(id = id)
    customer = Customer.objects.get(user = request.user)

    order = Order.objects.get(customer = customer)

    list_items = OrderProduct.objects.filter(order = order)

    
    found = False

    for item in list_items:
        if product == item.product and item.type == 'Rent':
            quantity = item.quantity + 1
            item.quantity = quantity
            item.save()
            found = True

    if found == False:
        OrderProduct.objects.create(order = order, product = product, quantity = 1, type = 'Rent')

    
    cart_items = count_cart_item(user=request.user)

    items, total = get_cart_item(customer=customer)

    

    context = {
        'items' : items,
        'cart_items' : cart_items,
        'total' : total
    }

    return cart(request, request.user.username)



#==========================END PRODUCT PAGE=========================



#==========================CART PAGE================================

def cart(request, name):
    user = User.objects.get(username = name)
    customer = Customer.objects.get(user= user)

    cart_items = count_cart_item(user=user)

    items, total = get_cart_item(customer=customer)

    phone_card_form = PhoneCardForm()
    bank_account_form = BankAccountForm()

    if request.method == "POST":
        check, message, value = None, None, 0
        if request.POST.get('form-type') == 'phone_card':
            phone_card_form = PhoneCardForm(request.POST)
            check, message = check_card_payment(phone_card_form)
            value = phone_card_form['value'].value()
        elif request.POST.get('form-type') == 'bank_account':
            bank_account_form = BankAccountForm(request.POST)
            check, message = check_bank_payment(bank_account_form)
            value = bank_account_form['value'].value()
        if check == False:
            messages.info(request, message)
        else:
            customer.coins += int(value)
            customer.save()
            message = "Paying successfully! Now you have " + str(customer.coins) + " coins, let's go shopping"
            messages.info(request, message)

    context = {
        'items' : items,
        'cart_items' : cart_items,
        'total' : total,
        'phone_card_form' : phone_card_form,
        'bank_account_form' : bank_account_form
    }

    return render(request, 'cart.html', context)

def get_cart_item(customer):
    order = Order.objects.get(customer = customer)
    items = OrderProduct.objects.filter(order=order)

    total = 0

    

    for item in items:
        if item.type == 'Buy':
            total += item.quantity * item.product.sell_price
        else:
            total += item.quantity * item.product.rent_price

    return items, round(total, 4)

def check_card_payment(form = PhoneCardForm, value = any):
    serial_code = form['serial_code'].value()
    card_code = form['card_code'].value()

    if len(serial_code) != 15 or len(card_code) != 14:
        message = 'Length of Serial code or Card code is wrong!'
        return False, message
    
    return (serial_code.isdigit() and card_code.isdigit()), None

def check_bank_payment(form = BankAccountForm):
    account = form['account'].value()
    value = form['value'].value()

    if len(account) < 9 or len(account) > 15:
        message = 'Length of account is wrong! (9 - 15 digits)'
        return False, message
    
    if value.isdigit() and int(value) <= 0:
        message = 'Value must be a positive integer'
        return False, message

    return (account.isdigit() and value.isdigit()), None


def delete_cart_item(request, name, type):
    customer = Customer.objects.get(user = request.user)
    order_item, total  = get_cart_item(customer=customer)

    for item in order_item:
        if item.product.name == name and item.type == type:
            item.delete()
            break

    return cart(request, request.user.username)

def purchase(request):
    customer = Customer.objects.get(user = request.user)
    order_items, total = get_cart_item(customer)
    fail = False

    if customer.coins < total:
        messages.info(request, 'You do not have enough coins! You can buy more coins below')
        return cart(request, request.user.username)


    group = []
    for item in order_items:
        found = False
        for element in group:

            if element[0] == item.product.name:           
                temp = list(element)
                temp[1] += item.quantity
                group.remove(element)
                new_element = tuple(temp)
                group.append(new_element)
                found = True
                break

        if found == False:
            group.append((item.product.name, item.quantity))
    
    for item in group:
        item_name = item[0]
        item_count = item[1]
        product = Product.objects.get(name=item_name)
        accounts  = Account.objects.filter(product=product, status='Available')

        if accounts.__len__() < item_count:
            messages.info(request, 'Not enough accounts for ' + item_name + '! We have only ' + str(accounts.__len__()) + ' left')
            fail = True
            

    if fail:
        return cart(request, request.user.username)
    else:
        for item in group:
            item_name = item[0]
            item_count = item[1]
            product = Product.objects.get(name=item_name)
            accounts  = Account.objects.filter(product=product, status='Available')

            accounts = list(accounts)

            for i in range(item_count):
                choose_account = random.sample(accounts, 1)
                choose_account[0].status = 'Sold'
                choose_account[0].save()
                PurchasedItem.objects.create(customer=request.user.username, account=choose_account[0], product =product)

        for item in order_items:
            item.delete()

        customer.coins -= total
        customer.save()
        messages.success(request, 'Purchase successfully! You can get your account from Game library now')
    
    return cart(request, request.user.username)


#==========================END CART PAGE=============================


#==========================CATEGORY PAGE=============================

def category(request, name):
    platform = Platform.objects.get(platform = name)
    products = Product.objects.filter(platForm = platform)
    cart_items = count_cart_item(request.user)


    context = {'cart_items' : cart_items, 'products': products, 'platform': platform}

    return render(request, 'category.html', context)
#==========================END CATEGORY PAGE=========================


#==========================SEARCH PAGE===============================
def search(request):
    cart_items = count_cart_item(request.user)
    product = None
    
    if request.method == 'POST':
        searched = request.POST['searchKeyword']
        product = Product.objects.filter(name__contains = searched)
        
    filter = ProductFilter(request.GET, queryset=product)
    product = filter.qs

    context = {'cart_items' : cart_items, 'products': product, 'filter' : filter}


    return render(request, 'search.html', context)

#==========================END SEARCH PAGE===========================

def register(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)    

        if register_form.is_valid():
            user = register_form.save()

            username = register_form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            customer = Customer.objects.create(user = user, name = username)
            Order.objects.create(customer= customer)
            return redirect('home')

        else:
            print(register_form.error_messages)

    context = {"form" : register_form}
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        group = None

        user = authenticate(request, username=username, password = password)
        if user is not None:
            auth_login(request, user)

            return redirect('home')
        else:
            messages.info(request, "Username or Password incorrect")

    return render(request, 'login.html')

def customer(request, name):
    user = User.objects.get(username = name)
    customer = Customer.objects.get(user=user)
    cart_items = count_cart_item(user)

    try:
        purchased_item = PurchasedItem.objects.filter(customer = name)
        print(purchased_item)
    except:
        purchased_item = None
    context = {'customer' : customer, 'purchased_item' : purchased_item, 'cart_items' : cart_items}

    return render(request, 'customer.html', context)

def logout(request):
    auth_logout(request)

    return redirect('home')
    

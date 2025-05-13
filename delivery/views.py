from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user, Cart, CartItem, Item, Restaurant
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import CartItem

import razorpay
from django.conf import settings

def appwelcome(request):
    return render(request, 'delivery/home.html')

def open_signup(request):
    return render(request, "delivery/signup.html")

def open_signin(request):
    return render(request, 'delivery/signin.html') 

def sign_up(request):
     if request.method == "POST":
         username = request.POST.get("username")
         password = request.POST.get("password")
         number = request.POST.get("number")
         email = request.POST.get("email")
         
         try:
             user1 = user.objects.get(username = username)
             return HttpResponse("This Account is already exist...")
         except:
             user1 = user(username = username, password = password, phonenumber = number, email = email)
             user1.save()
             return render(request, "delivery/signin.html")
         
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user1 = user.objects.get(username = username)
            if user1.username == username and user1.password == password:
                if username == "admin":
                    return render(request, 'delivery/adminhome.html')
                else:
                    restaurant = Restaurant.objects.all()
                    return render(request, "delivery/customerhome.html", {"username" : username, "restaurant" : restaurant})
            else:
                return HttpResponse("Please enter the correct password")

        except:
            return HttpResponse("User does not exist with this username") 
    else:
        return render(request, "delivery/signin.html")
        
def open_add_restaurant(request):
    return render(request, "delivery/openaddrestaurant.html")
def show_restaurant(request):
    restaurant = Restaurant.objects.all()
    return render(request, "delivery/showrestaurant.html", {"restaurant" : restaurant})

def add_restaurant(request):
    if request.method == "POST":
        name = request.POST.get("name")
        
        try:
            ref = Restaurant.objects.get(name = name)
            return HttpResponse("Restaurant is Already Exist")
        except:
             picture = request.POST.get("picture")
             cuisine = request.POST.get("cuisine")
             rating = request.POST.get("rating")

             restaurant1 = Restaurant(name = name, picture = picture, cuisine = cuisine, rating = rating)
             restaurant1.save()
             return render(request, "delivery/openaddrestaurant.html")
        
def open_update_restaurant(request, name):
    restaurant = Restaurant.objects.get(name = name)
    return render(request, "delivery/update_restaurant.html", {"restaurant": restaurant})

def update_restaurant(request):
    if request.method == "POST":
        name = request.POST.get("name")
        picture = request.POST.get("picture")
        cuisine = request.POST.get("cuisine")
        rating = request.POST.get("rating")

        ref = Restaurant.objects.get(name = name)
        ref.name = name
        ref.picture = picture
        ref.cuisine = cuisine
        ref.rating = rating
        ref.save()
    
    restaurant = Restaurant.objects.all()
    return render(request, "delivery/showrestaurant.html", {"restaurant" : restaurant}) 

def delete_restaurant(request, name):
    ref = Restaurant.objects.get(name = name)
    ref.delete()

    restaurant = Restaurant.objects.all()
    return render(request, "delivery/showrestaurant.html", {"restaurant" : restaurant}) 

def open_add_menu(request, name):
    ref = Restaurant.objects.get(name = name)
    item = ref.items.all()

    return render(request, "delivery/addmenu.html" , {"items" : item, "restaurant" : ref})

def add_menu(request, rname):
    ref = Restaurant.objects.get(name = rname)
    menu = ref.items.all()

    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        price = request.POST.get("price")
        veg = request.POST.get("veg") == 'on'
        picture = request.POST.get("picture")

        try:
            ref.items.get(name = name)
            return HttpResponse("The Item is already in the Menu")
        except:
            item = Item(restaurant = ref, name = name, desc = desc, price = price, veg = veg, picture = picture)
            item.save()
            return render(request, "delivery/addmenu.html" , {"items" : menu, "restaurant" : ref})

def open_menu(request, rname, uname):
    ref = Restaurant.objects.get(name = rname)
    itemlist = ref.items.all()

    return render(request, "delivery/openmenu.html", {"items" : itemlist, "rname": rname, "uname": uname})

def add_to_cart(request, uname, rname, iname):
    ref = Restaurant.objects.get(name=rname)
    itemlist = ref.items.all()
    user1 = user.objects.get(username=uname)
    item1 = Item.objects.get(name=iname)
    cart, created = Cart.objects.get_or_create(customer=user1)

    # Check if cart already has items from another restaurant
    if cart.cart_items.exists():
        first_item = cart.cart_items.first().item
        if first_item.restaurant != ref:
            cart.cart_items.all().delete()  # Clear the cart if restaurant changes

    # Check if item already in cart, if yes, increase quantity
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item1)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart_items = cart.cart_items.all()  # Add this in your view

    # Pass it in the context:
    return render(request, "delivery/openmenu.html", {
        "items": itemlist,
        "rname": rname,
        "uname": uname,
        "cart_items": cart_items,
    })


from django.shortcuts import render, get_object_or_404
from .models import user, Cart, CartItem

def show_cart_page(request, username):
    # Use a different variable name to avoid shadowing the model 'user'
    current_user = get_object_or_404(user, username=username)

    # Fetch carts belonging to the current user
    user_carts = Cart.objects.filter(customer=current_user)

    # Fetch all items from those carts
    cart_items = CartItem.objects.filter(cart__in=user_carts)

    # Calculate total price
    total_price = 0
    for item in cart_items:
        item.subtotal = item.item.price * item.quantity
        total_price += item.subtotal

    return render(request, 'delivery/show_cart_page.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
    })


def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('show_cart_page', username=cart_item.cart.customer.username)

def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove the item if quantity goes to 0
    return redirect('show_cart_page', username=cart_item.cart.customer.username)

def checkout(request, name):
    # Fetch customer by username
    customer = get_object_or_404(user, username=name)

    # Get the customer's cart
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.cart_items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    # If the cart is empty, show an error message
    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': 1,
    }
    order = client.order.create(data=order_data)

    # Render the checkout page with all needed details
    return render(request, 'delivery/checkout.html', {
        'username': name,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
        'amount': total_price,
    })

def orders(request, username):
    # Get the customer object based on the username
    customer = get_object_or_404(user, username=username)
    
    # Get the customer's cart
    cart = Cart.objects.filter(customer=customer).first()
    
    # If cart exists, get its items and total price
    if cart:
        cart_items = cart.cart_items.all()
        total_price = cart.total_price()
        cart.cart_items.all().delete()  # Clear the cart
    else:
        cart_items = []
        total_price = 0

    # Render the orders template
    return render(request, 'delivery/orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })

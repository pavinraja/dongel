from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user, Restaurant, Item, Cart
from django.contrib import messages

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

    if cart.item.exists():
        first_item = cart.item.first()
        if first_item.restaurant != ref:
            cart.item.clear()

    cart.item.add(item1)

    return render(request, "delivery/openmenu.html", {
        "items": itemlist,
        "rname": rname,
        "uname": uname
    })


def show_cart_page(request, name):
    customer = user.objects.get(username = name)
    
    try:
        cart = Cart.objects.get(customer = customer)
        items = cart.item.all()
        total_price = cart.total_price()
    except:
        items = []
        total_price = 0

    return render(request, "delivery/cart.html", {
        "items" : items,
        "total_price" : total_price,
        "username" : name,
    })
    




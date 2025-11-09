from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Costumer
from dotenv import load_dotenv
import requests
import os

load_dotenv()

TOKEN = os.getenv("TG_API")
CHAT_ID = os.getenv("USER_ID")

def home(request: HttpRequest)->HttpResponse:
    return render(request=request, template_name="index.html")

def support(request:HttpRequest)->HttpResponse:
    if request.method == "POST":
        name = request.POST.get("ism")
        telefon = request.POST.get("telefon")
        message = request.POST.get("xabar")


        user_message = f"👤: {name} \n 📱:{telefon} \n 📩:{message}"


        urls = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": user_message
        }

        requests.post(url=urls, params=payload)

        return render(request=request, template_name="support.html")
    
    return render(request=request, template_name="support.html")

def register_seller(request: HttpRequest)->HttpResponse:
    if request.method == "POST":
        result = Costumer(
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            phone_number = request.POST.get("phone_number"),
            email = request.POST.get("email"),
            password = request.POST.get("password"),
            market_name = request.POST.get("market_name"),
            location = request.POST.get("location"),
            product_category = request.POST.get("product_category")
        )

        result.save()
        return redirect("home")
    return render(request=request, template_name="register_seller.html")


def login(request:HttpRequest)->HttpResponse:
    if request.method =="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Costumer.objects.filter(email=email).first()
        if not user:
            return render(request, "login.html")
        elif user.password == password:
            return render(request=request, template_name="seller_dashboard.html")
    return render(request=request, template_name="login.html")

@login_required
def seller_dashboard(request: HttpRequest)->HttpResponse:
    seller = request.user.costumer
    products = Product.objects.filter(seller=seller)

    context = {
        "seller": seller,
        "products": products,
        "views_total": sum([p.id * 2 for p in products]),
    }

    return render(request=request, template_name="seller_dashboard.html")


   

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Ticket, Review, UserFollows


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("flux")
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")

    form = AuthenticationForm()
    return render(request, "home.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès.")
            return redirect("flux")
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("login")


def flux_view(request):
    context = {"tickets" : Ticket.objects.all()}
    return render(request, "flux.html", context)

def suscribes_view(request):
    return render(request, "suscribes.html")

def createTicket_view(request):
    return render(request, "create_ticket.html")

def createCritical_view(request):
    return render(request, "create_critical.html")

def createCriticalResponse_view(request):
    return render(request, "create_critical_res.html")

def post_view(request):
    return render(request, "post.html")

def editReview_view(request):
    return render(request, "edit_review.html")

def editTicket_view(request):
    return render(request, "edit_ticket.html")
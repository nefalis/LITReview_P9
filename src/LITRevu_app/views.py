from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm


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
        return render(request, 'home.html')
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

@login_required
def flux_view(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    items = list(tickets) + list(reviews)
    # Trier par date de création
    items.sort(key=lambda x: x.time_created, reverse=True)
    context = {"items": items}
    return render(request, "flux.html", context)

def suscribes_view(request):
    return render(request, "suscribes.html")

@login_required
def createTicket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Ticket créé avec succès.")
            return redirect('flux')
    else:
        form = TicketForm()

    return render(request, "create_ticket.html", {'form': form})

@login_required
def deleteTicket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST' and ticket.user == request.user:
        ticket.delete()
    return redirect('post')

@login_required
def createCritical_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Critique créée avec succès.")
            return redirect('flux')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    
    return render(request, "create_critical.html", {'ticket_form': ticket_form, 'review_form': review_form})

def createCriticalResponse_view(request):
    return render(request, "create_critical_res.html")

@login_required
def post_view(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    items = list(user_tickets) + list(user_reviews)
    # Trier par date de création
    items.sort(key=lambda x: x.time_created, reverse=True)
    return render(request, "post.html", {"items": items})

def editReview_view(request):
    return render(request, "edit_review.html")

@login_required
def editTicket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user != request.user:
        return redirect('post')

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('post')
    else:
        form = TicketForm(instance=ticket)

    return render(request, "edit_ticket.html", {'form': form})

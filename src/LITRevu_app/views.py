from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, registerForm, AuthenticationForm


def login_user(request):
    """ Gestion de la connexion utilisateur """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("flux")
            else:
                messages.info(request, "Identifiant ou mot de passe incorrect")
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect")
    else:
        form = AuthenticationForm()
    return render(request, "home.html", {"form": form})


def register_user(request):
    """ Gestion de l'inscription utilisateur """
    # creation formulaire creation utilisateur
    if request.method == "POST":
        form = registerForm(request.POST)
        # si valide on sauvegarde, connecte et envoyer sur flux
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("flux")
    else:
        form = registerForm()

    return render(request, "register.html", {"form": form})


def logout_user(request):
    """ Gestion de la déconnexion de l'utilisateur """
    logout(request)
    return redirect("login")


@login_required
def flux_view(request):
    """ Affichage des tickets et critiques sur la page flux """
    # Avoir les utilisateurs que l'utilisateur actuel suit
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Avoir tickets et critiques de l'utilisateur et de ceux qu'il suit
    tickets = Ticket.objects.filter(user__in=[request.user.id] + list(followed_users))
    reviews = Review.objects.filter(user__in=[request.user.id] + list(followed_users))

    # Filtrer les tickets sans critiques
    tickets_with_reviews_ids = reviews.values_list('ticket_id', flat=True)
    tickets_without_reviews = tickets.exclude(id__in=tickets_with_reviews_ids)

    # Trier les items par date de création
    items = sorted(list(tickets_without_reviews) + list(reviews), key=lambda x: x.time_created, reverse=True)

    context = {
        "items": items,
    }
    return render(request, "flux.html", context)


@login_required
def subscribes_view(request):
    """ Affichage des abonnements """
    subscriptions = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    return render(request, "subscribes.html", {"subscriptions": subscriptions, "followers": followers})


@login_required
def follow_user(request):
    """ Gestion de suivi des utilisateurs entre eux """
    if request.method == "POST":
        # on récupere le nom utilisateur du formulaire
        username = request.POST.get("username")
        try:
            # cherche l'utilisateur
            user_to_follow = User.objects.get(username=username)
            # verif que l'utilisateur ne suit pas la personne
            if user_to_follow != request.user:
                UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
                messages.success(request, f"Vous suivez maintenant {username}.")
            else:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
        except User.DoesNotExist:
            messages.error(request, f"L'utilisateur {username} n'existe pas.")
        return redirect("subscribes")


@login_required
def unfollow_user(request, user_id):
    """ Permet à l'utilisateur de ne plus suivre un autre utilisateur """
    # cherche l'utilisateur a ne plus suivre
    user_to_unfollow = User.objects.get(id=user_id)
    follow_relation = UserFollows.objects.get(user=request.user, followed_user=user_to_unfollow)
    # supprime la relation
    follow_relation.delete()
    messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")
    return redirect("subscribes")


@login_required
def createTicket_view(request):
    """ Gestion de la création d'un ticket """
    if request.method == 'POST':
        # creation formulaire ticket
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # assigne l'utilisateur au ticket
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = TicketForm()

    return render(request, "create_ticket.html", {'form': form})


@login_required
def createCritical_view(request):
    """ Permet a l'utilisateur de créer une critique """
    if request.method == 'POST':
        # crée un formulaire ticket
        ticket_form = TicketForm(request.POST, request.FILES)
        # crée un formulaire critique
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, "create_critical.html", {'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def createCriticalResponse_view(request, ticket_id):
    """ Création d'une critique en réponse à un ticket """
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user == request.user:
        return redirect('flux')

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
    else:
        review_form = ReviewForm()

    context = {
        'ticket': ticket,
        'review_form': review_form
    }
    return render(request, "create_critical_res.html", context)


@login_required
def post_view(request):
    """ Affichage des tickets et critique de l'utilisateur sur la page post """
    # recupère ticket et critique de l'utilisateur
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    items = list(user_tickets) + list(user_reviews)
    # Trier par date de création
    items.sort(key=lambda x: x.time_created, reverse=True)
    return render(request, "post.html", {"items": items})


@login_required
def editReview_view(request, review_id):
    """ Permet la modification d'une critique """
    review = Review.objects.get(id=review_id)
    ticket = review.ticket
    if review.user != request.user:
        return redirect('post')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('post')
    else:
        form = ReviewForm(instance=review)

    return render(request, "edit_review.html", {'form': form, 'ticket': ticket})


@login_required
def deleteReview_view(request, review_id):
    """ Permet de supprimer une critique """
    review = Review.objects.get(id=review_id)
    if review.user == request.user:
        review.delete()
    return redirect('post')


@login_required
def editTicket_view(request, ticket_id):
    """ Permet la modifier un ticket """
    # recupere le ticket par son id
    ticket = Ticket.objects.get(id=ticket_id)
    # verif que le ticket appartient a l'utilisateur
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


@login_required
def deleteTicket_view(request, ticket_id):
    """ Permet de supprimer un ticket """
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST' and ticket.user == request.user:
        ticket.delete()
    return redirect('post')

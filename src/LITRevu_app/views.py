from django.shortcuts import render


def login_view(request):
    return render(request, "home.html")

def signup_view(request):
    return render(request, "signup.html")

def flux_view(request):
    return render(request, "flux.html")

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
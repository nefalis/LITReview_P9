
from django.contrib import admin
from django.urls import path
from LITRevu_app import views


# chemin par defaut
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_user ),
    path('login/', views.login_user, name= 'login'),
    path('register/', views.register_user, name = 'register'),
    path('logout/', views.logout_user, name = 'logout'),
    path('flux/', views.flux_view, name = 'flux'),
    path('suscribes/', views.suscribes_view),
    path('create_ticket/', views.createTicket_view),
    path('create_critical/', views.createTicket_view),
    path('create_critical_response', views.createCriticalResponse_view),
    path('post/', views.post_view),
    path('edit_review/', views.editReview_view),
    path('edit_ticket/', views.editTicket_view),
]

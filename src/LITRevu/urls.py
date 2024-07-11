
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from LITRevu_app import views


# chemin par defaut
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_user, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('flux/', views.flux_view, name='flux'),
    path('subscribes/', views.subscribes_view, name='subscribes'),
    path('create_ticket/', views.createTicket_view, name='create_ticket'),
    path('create_critical/', views.createCritical_view, name='create_critical'),
    path(
        'create_critical_response/<int:ticket_id>/',
        views.createCriticalResponse_view,
        name='create_critical_response'
    ),
    path('post/', views.post_view, name='post'),
    path('edit_review/<int:review_id>/', views.editReview_view, name='edit_review'),
    path('delete_review/<int:review_id>/', views.deleteReview_view, name='delete_review'),
    path('edit_ticket/<int:ticket_id>/', views.editTicket_view, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/', views.deleteTicket_view, name='delete_ticket'),
    path('follow_user/', views.follow_user, name='follow_user'),
    path('unfollow_user/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

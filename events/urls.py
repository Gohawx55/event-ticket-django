from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('buy/<int:event_id>/', views.buy_ticket, name='buy_ticket'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/profile/'), name='password_change'),
    path('download-ticket/<int:ticket_id>/', views.download_ticket_pdf, name='download_ticket_pdf'),

]


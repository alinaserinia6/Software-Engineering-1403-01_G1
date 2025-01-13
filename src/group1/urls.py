from django.urls import path
from . import views

app_name = 'group1'

urlpatterns = [
    # User Management
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Private Chat
    path('private-chat/create/', views.create_private_chat, name='create_private_chat'),
    path('private-chat/send-message/', views.send_private_message, name='send_private_message'),

    # Group Chat
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/send-message/', views.send_group_message, name='send_group_message'),
    path('group/<int:group_id>/add-member/', views.add_group_member, name='add_group_member'),
    path('group/<int:group_id>/remove-member/', views.remove_group_member, name='remove_group_member'),

    # Language Partner Matching
    path('language-partners/search/', views.search_language_partners, name='search_language_partners'),
    path('language-partners/request/', views.send_partner_request, name='send_partner_request'),

    # Reporting and Blocking
    path('report/', views.report_user, name='report_user'),
    path('block/', views.block_user, name='block_user'),

    # Home Page
    path('', views.home, name='home'),
]
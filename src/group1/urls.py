# urls.py
from django.urls import path
from . import views

app_name = 'group1'

urlpatterns = [
    # User Management APIs
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Private Chat APIs
    path('private-chat/create/', views.create_private_chat, name='create_private_chat'),
    path('private-chat/send-message/', views.send_private_message, name='send_private_message'),
    path('private-chat/<int:chat_id>/', views.get_single_chat, name='get_single_chat'),

    # Group Chat APIs
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/send-message/', views.send_group_message, name='send_group_message'),
    path('group/<int:group_id>/add-member/', views.add_group_member, name='add_group_member'),
    path('group/<int:group_id>/remove-member/', views.remove_group_member, name='remove_group_member'),

    # Language Partner Matching
    path('language-partners/search/', views.search_language_partners, name='search_language_partners'),
    path('language-partners/request/', views.send_partner_request, name='send_partner_request'),
    path('language-partners/accept/', views.accept_partner_request, name='accept_partner_request'),

    # Reporting and Blocking
    path('report/', views.report_user, name='report_user'),
    path('block/', views.block_user, name='block_user'),

    # User Retrieval APIs
    path('users/', views.get_all_users, name='get_all_users'),
    path('users/<int:user_id>/', views.get_single_user, name='get_single_user'),

    # Chat Retrieval APIs
    path('chats/', views.get_all_chats, name='get_all_chats'),

    # Additional APIs
    path('user/avatar/<int:user_id>/', views.get_user_avatar, name='get_user_avatar'),
    path('user/details/<int:user_id>/', views.get_user_details, name='get_user_details'),

    # Message APIs
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),

    # Home Page
    path('', views.home, name='group1'),

]
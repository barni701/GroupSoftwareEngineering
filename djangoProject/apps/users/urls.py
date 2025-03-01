from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [ 
    path("", views.landing, name='landing'),
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", views.signup, name='signup'),
    path("delete-account/", views.delete_account, name='delete_account'),
    path('terms-and-conitions/', views.terms_and_conditions, name='terms_and_conditions'),
    path("profile/", views.profile_view, name='profile'),
    path("user-data/", views.user_data_view, name="user_data"),
    path("privacy-policy", views.privacy_policy, name="privacy_policy"),
    path("add-currency/", views.add_currency, name="add_currency"),
    path("spend-currency/", views.spend_currency, name="spend_currency"),
    path("transaction-history/", views.transaction_history, name="transaction_history"),
    path('logout/', views.logout_user, name='logout'),
]
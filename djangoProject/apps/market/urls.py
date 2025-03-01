from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('home/', views.market_home, name='market_home'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    path('company/<int:pk>/invest/', views.invest_in_company, name='invest'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('investment/<int:investment_id>/sell/', views.sell_investment, name='sell_investment'),
    path('events/', views.market_events, name='market_events'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/portfolio/', views.portfolio_data_api, name='portfolio_data_api'),
    path('about-eco-score/', views.about_eco_score, name='about_eco_score'),
    path('company/<int:company_id>/price-history/', views.price_history_api, name='price_history_api'),
]
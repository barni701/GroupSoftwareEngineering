from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('home/', views.market_home, name='market_home'),
    path('company/<int:pk>/', views.company_detail, name='company_detail'),
    path('company/<int:pk>/invest/', views.invest_in_company, name='invest'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('investment/company/<int:company_pk>/sell/', views.sell_investment_for_company, name='sell_investment_company'),
    path('events/', views.market_events, name='market_events'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/portfolio/', views.portfolio_data_api, name='portfolio_data_api'),
    path('about-eco-score/', views.about_eco_score, name='about_eco_score'),
    path('company/<int:company_id>/price-history/', views.price_history_api, name='price_history_api'),
    path('api/portfolio-analytics/', views.portfolio_analytics_api, name='portfolio_analytics_api'),
    path('portfolio-analytics/', views.portfolio_analytics, name='portfolio_analytics'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('api/portfolio-breakdown/', views.portfolio_breakdown_api, name='portfolio_breakdown_api'),
    path('api/event-impact/', views.event_impact_api, name='event_impact_api'),
]
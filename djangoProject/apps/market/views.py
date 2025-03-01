from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Company, Investment, MarketEvent
from .forms import InvestmentForm, SellInvestmentForm
from ..users.models import UserProfile
from django.utils import timezone


from django.shortcuts import render

def market_home(request):
    return render(request, 'market/market_home.html')

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'market/company_list.html', {'companies': companies})

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    # Get active events for this company
    active_events = company.market_events.filter(
        event_date__lte=timezone.now()
    )
    active_events = [event for event in active_events if event.is_active()]
    return render(request, 'market/company_detail.html', {
        'company': company,
        'active_events': active_events
    })

@login_required
def invest_in_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.company = company
            investment.purchase_price = company.current_stock_price
            # Calculate total cost of the investment
            total_cost = company.current_stock_price * investment.shares
            # Check if the user has enough currency (assuming a UserProfile with currency_balance)
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.currency_balance >= total_cost:
                user_profile.currency_balance -= total_cost
                user_profile.save()
                investment.save()
                return redirect('market:company_detail', pk=company.pk)
            else:
                form.add_error(None, "Insufficient funds to make this investment.")
    else:
        form = InvestmentForm()
    return render(request, 'market/invest.html', {'company': company, 'form': form})


@login_required
def portfolio(request):
    investments = Investment.objects.filter(user=request.user)
    portfolio_data = []
    total_invested = Decimal('0.00')
    current_value = Decimal('0.00')
    green_impact_score = Decimal('0.00')

    for investment in investments:
        invested_amount = investment.purchase_price * investment.shares
        current_amount = investment.company.current_stock_price * investment.shares
        total_invested += invested_amount
        current_value += current_amount
        green_impact_score += investment.company.sustainability_rating * investment.shares

        portfolio_data.append({
            'company': investment.company,
            'shares': investment.shares,
            'invested_amount': invested_amount,
            'current_amount': current_amount,
            'investment_id': investment.id,  # Include investment id here
        })

    context = {
        'portfolio_data': portfolio_data,
        'total_invested': total_invested,
        'current_value': current_value,
        'green_impact_score': green_impact_score,
    }
    return render(request, 'market/portfolio.html', context)


@login_required
def sell_investment(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id, user=request.user)

    if request.method == 'POST':
        form = SellInvestmentForm(request.POST)
        if form.is_valid():
            shares_to_sell = form.cleaned_data['shares']
            if shares_to_sell > investment.shares:
                form.add_error('shares', 'You cannot sell more shares than you own.')
            else:
                sale_value = investment.company.current_stock_price * shares_to_sell
                # Update user's currency balance
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.currency_balance += sale_value
                user_profile.save()
                # Update the investment record
                investment.shares -= shares_to_sell
                if investment.shares == 0:
                    investment.delete()
                else:
                    investment.save()
                return redirect('market:portfolio')
    else:
        form = SellInvestmentForm()

    return render(request, 'market/sell_investment.html', {'investment': investment, 'form': form})

def market_events(request):
    events = MarketEvent.objects.order_by('-event_date')[:10]  # Show the latest 10 events
    return render(request, 'market/market_events.html', {'events': events})

def leaderboard(request):
    # Fetch all user profiles and sort by a calculated Green Impact Score.
    # For this example, let's assume the UserProfile has a method `calculate_green_impact()`
    # that sums the sustainability impact of all investments.
    profiles = UserProfile.objects.all()
    profiles = sorted(profiles, key=lambda p: p.calculate_green_impact() if hasattr(p, 'calculate_green_impact') else Decimal('0.00'), reverse=True)
    return render(request, 'market/leaderboard.html', {'profiles': profiles})

@login_required
def portfolio_data_api(request):
    investments = Investment.objects.filter(user=request.user)
    data = []
    for inv in investments:
        data.append({
            'company': inv.company.name,
            'shares': inv.shares,
            'invested_amount': str(inv.purchase_price * inv.shares),
            'current_amount': str(inv.company.current_stock_price * inv.shares),
            'investment_id': inv.id,
        })
    return JsonResponse({'portfolio': data})

def about_eco_score(request):
    """
    Renders a page that explains how the Green Impact Score is calculated.
    """
    return render(request, 'market/about_eco_score.html')

def price_history_api(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    history = company.price_history.order_by('date').values('date', 'price')
    # Convert the date to a string for JSON serialization
    data = [{'date': h['date'].strftime('%Y-%m-%d %H:%M:%S'), 'price': str(h['price'])} for h in history]
    return JsonResponse({'history': data})
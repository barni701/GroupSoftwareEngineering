from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from django.utils.dateparse import parse_date

from .models import Company, Investment, MarketEvent, Transaction
from .forms import InvestmentForm, SellInvestmentForm
from ..users.models import UserProfile
from django.utils import timezone
from apps.market.utils import record_portfolio_snapshot



from django.shortcuts import render

def market_home(request):
    return render(request, 'market/market_home.html')


@login_required
def company_list(request):
    companies = Company.objects.all().order_by('-sustainability_rating')

    # Paginate the companies (10 per page)
    paginator = Paginator(companies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_company_ids = Investment.objects.filter(user=request.user).values_list('company__pk', flat=True)

    context = {
        'companies': page_obj,
        'user_company_ids': list(user_company_ids),
    }
    return render(request, 'market/company_list.html', context)

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.market.models import Company, MarketEvent, Investment

@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)

    # Retrieve market events affecting this company that have started.
    events = MarketEvent.objects.filter(
        companies_affected=company,
        event_date__lte=timezone.now()
    ).order_by('-event_date')

    # Further filter events by checking if each event is active.
    active_events = [event for event in events if event.is_active()]

    # Check if the user holds any stock in this company.
    user_has_investment = Investment.objects.filter(user=request.user, company=company).exists()

    context = {
        'company': company,
        'active_events': active_events,
        'user_has_investment': user_has_investment,
    }
    return render(request, 'market/company_detail.html', context)

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
                record_portfolio_snapshot(request.user)
                return redirect('market:company_detail', pk=company.pk)
            else:
                form.add_error(None, "Insufficient funds to make this investment.")
    else:
        form = InvestmentForm()
    return render(request, 'market/invest.html', {'company': company, 'form': form})

@login_required
def portfolio(request):
    investments = Investment.objects.filter(user=request.user)
    grouped = {}
    for inv in investments:
        company_id = inv.company.pk
        if company_id in grouped:
            grouped[company_id]['shares'] += inv.shares
            grouped[company_id]['invested_amount'] += inv.purchase_price * inv.shares
            grouped[company_id]['current_amount'] = inv.company.current_stock_price * grouped[company_id]['shares']
        else:
            grouped[company_id] = {
                'company': inv.company,
                'shares': inv.shares,
                'invested_amount': inv.purchase_price * inv.shares,
                'current_amount': inv.company.current_stock_price * inv.shares,
            }
    portfolio_data = list(grouped.values())

    total_invested = sum(item['invested_amount'] for item in portfolio_data)
    current_value = sum(item['current_amount'] for item in portfolio_data)
    green_impact_score = sum(item['company'].sustainability_rating * item['shares'] for item in portfolio_data)

    roi = 0
    if total_invested > 0:
        roi = ((current_value - total_invested) / total_invested) * 100

    total_shares = sum(item['shares'] for item in portfolio_data)
    avg_sustainability = 0
    if total_shares > 0:
        avg_sustainability = sum(
            item['company'].sustainability_rating * item['shares'] for item in portfolio_data) / total_shares

    # Debug prints (remove in production)
    print("Total Invested:", total_invested)
    print("Current Value:", current_value)
    print("ROI:", roi)
    print("Avg Sustainability:", avg_sustainability)

    context = {
        'portfolio_data': portfolio_data,
        'total_invested': total_invested,
        'current_value': current_value,
        'green_impact_score': green_impact_score,
        'roi': roi,
        'avg_sustainability': avg_sustainability,
    }
    return render(request, 'market/portfolio.html', context)

@login_required
def sell_investment(request, company_pk):
    # Retrieve all investments for the user in the given company
    investments = Investment.objects.filter(user=request.user, company__pk=company_pk).order_by('id')
    if not investments.exists():
        raise Http404("No investment found for this company.")

    # Sum the total shares owned for this company
    total_shares = sum(inv.shares for inv in investments)

    if request.method == 'POST':
        form = SellInvestmentForm(request.POST)
        if form.is_valid():
            shares_to_sell = form.cleaned_data['shares']
            if shares_to_sell > total_shares:
                form.add_error('shares', 'You cannot sell more shares than you own.')
            else:
                current_price = investments.first().company.current_stock_price
                sale_value = current_price * shares_to_sell
                # Update user's balance
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.currency_balance += sale_value
                user_profile.save()

                # Process the sale from the aggregated investments (FIFO: sell from the oldest first)
                remaining_to_sell = shares_to_sell
                for inv in investments:
                    if remaining_to_sell <= 0:
                        break
                    if inv.shares <= remaining_to_sell:
                        remaining_to_sell -= inv.shares
                        inv.delete()
                    else:
                        inv.shares -= remaining_to_sell
                        inv.save()
                        remaining_to_sell = 0

                # Record portfolio snapshot
                record_portfolio_snapshot(request.user)
                return redirect('market:portfolio')
    else:
        form = SellInvestmentForm()

    # Pass the aggregated information to the template for display
    context = {
        'company': investments.first().company,
        'total_shares': total_shares,
        'form': form
    }
    return render(request, 'market/sell_investment.html', context)

@login_required
def market_events(request):
    events = MarketEvent.objects.order_by('-event_date')[:10]  # Show the latest 10 events
    user_companies = Investment.objects.filter(user=request.user).values_list('company__pk', flat=True).distinct()
    context = {
        'events': events,
        'user_companies': list(user_companies),
    }
    return render(request, 'market/market_events.html', context)

@login_required
def leaderboard(request):
    profiles = UserProfile.objects.all()

    # Define a helper function to calculate green impact score if not already defined
    def calculate_green_impact(profile):
        total = Decimal('0.00')
        # Assuming the Investment model has a related name 'investments'
        for inv in profile.user.investments.all():
            total += inv.company.sustainability_rating * inv.shares
        return total

    # Annotate each profile with total portfolio value and green impact score.
    leaderboard_data = []
    for profile in profiles:
        total_value = sum(inv.company.current_stock_price * inv.shares for inv in profile.user.investments.all())
        green_impact = calculate_green_impact(profile)
        leaderboard_data.append({
            'user': profile.user,
            'balance': profile.currency_balance,
            'portfolio_value': total_value,
            'green_impact': green_impact,
        })

    # Sort profiles by green impact score descending (you can change to portfolio_value if desired)
    leaderboard_data = sorted(leaderboard_data, key=lambda x: x['green_impact'], reverse=True)

    return render(request, 'market/leaderboard.html', {'leaderboard': leaderboard_data})

@login_required
def portfolio_data_api(request):
    investments = Investment.objects.filter(user=request.user)
    data = []
    for inv in investments:
        data.append({
            'company': inv.company.name,
            'company_pk': inv.company.pk,  # Include the primary key here
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

@login_required
def portfolio_analytics_api(request):
    snapshots = request.user.portfolio_snapshots.order_by('timestamp')

    # Get optional start and end dates from query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date_parsed = parse_date(start_date)
        if start_date_parsed:
            snapshots = snapshots.filter(timestamp__date__gte=start_date_parsed)
    if end_date:
        end_date_parsed = parse_date(end_date)
        if end_date_parsed:
            snapshots = snapshots.filter(timestamp__date__lte=end_date_parsed)

    data = [
        {
            'timestamp': s.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'total_value': str(s.total_value)
        }
        for s in snapshots
    ]
    return JsonResponse({'snapshots': data})

@login_required
def portfolio_analytics(request):
    return render(request, 'market/portfolio_analytics.html')

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'market/transaction_history.html', {'transactions': transactions})

@login_required
def portfolio_breakdown_api(request):
    investments = Investment.objects.filter(user=request.user)
    grouped = {}
    for inv in investments:
        company_id = inv.company.pk
        if company_id in grouped:
            grouped[company_id]['invested_amount'] += inv.purchase_price * inv.shares
        else:
            grouped[company_id] = {
                'company': inv.company.name,
                'invested_amount': inv.purchase_price * inv.shares,
            }
    data = list(grouped.values())
    return JsonResponse({'breakdown': data})

@login_required
def event_impact_api(request):
    # Get all events up to now, ordered chronologically
    events = MarketEvent.objects.filter(event_date__lte=timezone.now()).order_by('event_date')
    data = []
    cumulative_impact = 0
    for event in events:
        cumulative_impact += float(event.impact_factor)
        data.append({
            'timestamp': event.event_date.strftime('%Y-%m-%d %H:%M:%S'),
            'cumulative_impact': cumulative_impact,
            'title': event.title,
            'impact_factor': float(event.impact_factor),
        })
    return JsonResponse({'data': data})

TAX_RATE = Decimal("0.18")

@login_required
def sell_investment_for_company(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    # Retrieve all investments for this company by the current user, FIFO (oldest first)
    investments = Investment.objects.filter(user=request.user, company=company).order_by('id')
    if not investments.exists():
        raise Http404("No investment found for this company.")

    # Aggregate total shares owned
    total_shares = sum(inv.shares for inv in investments)

    if request.method == 'POST':
        form = SellInvestmentForm(request.POST)
        if form.is_valid():
            shares_to_sell = form.cleaned_data['shares']
            if shares_to_sell > total_shares:
                form.add_error('shares', 'You cannot sell more shares than you own.')
            else:
                # Calculate gross sale value
                sale_value = shares_to_sell * company.current_stock_price
                # Calculate tax and net sale value
                tax_amount = sale_value * TAX_RATE
                net_sale_value = sale_value - tax_amount

                # Update the user's balance with net proceeds
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.currency_balance += net_sale_value
                user_profile.save()

                # Process the sale (FIFO: sell from the oldest investment first)
                remaining_to_sell = shares_to_sell
                for inv in investments:
                    if remaining_to_sell <= 0:
                        break
                    if inv.shares <= remaining_to_sell:
                        remaining_to_sell -= inv.shares
                        inv.delete()
                    else:
                        inv.shares -= remaining_to_sell
                        inv.save()
                        remaining_to_sell = 0

                # Record a portfolio snapshot (if you have such functionality)
                record_portfolio_snapshot(request.user)
                return redirect('market:portfolio')
    else:
        form = SellInvestmentForm(initial={'shares': total_shares})

    context = {
        'company': company,
        'form': form,
        'total_shares': total_shares,
        'sale_price': company.current_stock_price,
        'tax_rate': float(TAX_RATE * 100),  # Display as percentage (e.g., 5.0 for 5%)
    }
    return render(request, 'market/sell_investment_company.html', context)
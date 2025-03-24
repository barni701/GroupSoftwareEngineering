def green_fund_context(request):
    """Make Green Fund data available to all templates."""
    from apps.casino.models import GreenFund  # Import inside the function

    fund, created = GreenFund.objects.get_or_create(id=1)
    return {"green_fund": fund}
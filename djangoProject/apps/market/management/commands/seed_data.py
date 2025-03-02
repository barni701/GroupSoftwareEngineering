import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.market.models import Company, StockPriceHistory, MarketEvent


class Command(BaseCommand):
    help = "Seed the database with sample companies and market events for the market app"

    def handle(self, *args, **options):
        # Optional: Clear out existing data
        Company.objects.all().delete()
        MarketEvent.objects.all().delete()
        StockPriceHistory.objects.all().delete()

        companies_data = [
            {
                "name": "EcoGreen Energy",
                "description": "A renewable energy company focusing on wind and solar power solutions.",
                "sustainability_rating": Decimal("9.0"),
                "current_stock_price": Decimal("150.00"),
            },
            {
                "name": "Sustainable Farms",
                "description": "An enterprise practicing organic and regenerative farming.",
                "sustainability_rating": Decimal("8.5"),
                "current_stock_price": Decimal("120.00"),
            },
            {
                "name": "Green Urban Solutions",
                "description": "Innovative sustainable urban planning and green construction.",
                "sustainability_rating": Decimal("7.5"),
                "current_stock_price": Decimal("200.00"),
            },
            {
                "name": "EcoTech Innovations",
                "description": "Develops cutting-edge eco-friendly technology products.",
                "sustainability_rating": Decimal("8.0"),
                "current_stock_price": Decimal("180.00"),
            },
            {
                "name": "Renewable Power Inc.",
                "description": "Specializes in wind and solar power installations.",
                "sustainability_rating": Decimal("9.2"),
                "current_stock_price": Decimal("210.00"),
            },
            {
                "name": "Clean Air Initiatives",
                "description": "Works on reducing air pollution through innovative technology.",
                "sustainability_rating": Decimal("7.8"),
                "current_stock_price": Decimal("160.00"),
            },
            {
                "name": "BioGreen Solutions",
                "description": "Focuses on biotechnological solutions for environmental cleanup.",
                "sustainability_rating": Decimal("8.3"),
                "current_stock_price": Decimal("175.00"),
            },
            {
                "name": "WaterWise Systems",
                "description": "Develops sustainable water management and conservation technologies.",
                "sustainability_rating": Decimal("8.6"),
                "current_stock_price": Decimal("190.00"),
            },
            {
                "name": "Green Future Materials",
                "description": "Produces environmentally friendly building materials.",
                "sustainability_rating": Decimal("7.9"),
                "current_stock_price": Decimal("155.00"),
            },
            {
                "name": "Eco-Friendly Transport",
                "description": "Invests in electric and hybrid transportation solutions.",
                "sustainability_rating": Decimal("8.1"),
                "current_stock_price": Decimal("165.00"),
            },
            {
                "name": "SolarWave Energy",
                "description": "Focuses on advanced solar panel technology and energy storage.",
                "sustainability_rating": Decimal("9.1"),
                "current_stock_price": Decimal("205.00"),
            },
            {
                "name": "Nature's Touch",
                "description": "Promotes sustainable and organic personal care products.",
                "sustainability_rating": Decimal("7.4"),
                "current_stock_price": Decimal("140.00"),
            },
            {
                "name": "Urban Eco Systems",
                "description": "Provides eco-friendly urban landscaping and waste management solutions.",
                "sustainability_rating": Decimal("8.0"),
                "current_stock_price": Decimal("165.00"),
            },
            {
                "name": "Green Horizon Ventures",
                "description": "Invests in next-generation sustainable technology startups.",
                "sustainability_rating": Decimal("8.7"),
                "current_stock_price": Decimal("220.00"),
            },
            {
                "name": "Pure Earth Resources",
                "description": "Specializes in recycling and sustainable resource management.",
                "sustainability_rating": Decimal("7.8"),
                "current_stock_price": Decimal("150.00"),
            },
        ]

        self.stdout.write("Creating companies...")
        companies = []
        for data in companies_data:
            company = Company.objects.create(**data)
            companies.append(company)
            # Create an initial stock price history record for each company
            StockPriceHistory.objects.create(company=company, price=company.current_stock_price)
        self.stdout.write(self.style.SUCCESS(f"Created {len(companies)} companies."))

        # Optionally, create a few sample market events (if needed)
        events_data = [
            {
                "title": "Government Green Subsidy",
                "description": "A new subsidy for renewable energy boosts investor confidence.",
                "impact_factor": Decimal("0.10"),
                "duration": 6,
            },
            {
                "title": "Environmental Scandal",
                "description": "A company is caught in an environmental scandal, causing stock prices to drop.",
                "impact_factor": Decimal("-0.15"),
                "duration": 9,
            },
            {
                "title": "Sustainability Award",
                "description": "A company wins a prestigious sustainability award, spiking its stock price.",
                "impact_factor": Decimal("0.12"),
                "duration": 6,
            },
            {
                "title": "Technological Breakthrough",
                "description": "A breakthrough in eco-friendly technology improves prospects for green companies.",
                "impact_factor": Decimal("0.08"),
                "duration": 4,
            },
            {
                "title": "Policy Change",
                "description": "A new government policy supports sustainable practices across the board.",
                "impact_factor": Decimal("0.05"),
                "duration": 7,
            },
        ]

        self.stdout.write("Creating sample market events...")
        for event_data in events_data:
            event = MarketEvent.objects.create(**event_data)
            # Randomly assign affected companies
            if companies:
                num = random.randint(1, len(companies))
                affected = random.sample(companies, k=num)
                event.companies_affected.set(affected)
            event.save()
            self.stdout.write(self.style.SUCCESS(f"Created event: {event.title}"))

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
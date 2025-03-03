import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.market.models import Company, StockPriceHistory, MarketEvent


class Command(BaseCommand):
    help = "Seed the database with sample companies and market events for the market app"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding.'
        )
        parser.add_argument(
            '--company-count',
            type=int,
            default=25,  # Increased number of companies
            help='Number of companies to create (default is 25).'
        )
        parser.add_argument(
            '--event-count',
            type=int,
            default=5,
            help='Number of market events to create (default is 5).'
        )

    def handle(self, *args, **options):
        clear_data = options['clear']
        company_count = options['company_count']
        event_count = options['event_count']

        if clear_data:
            self.stdout.write("Clearing existing companies, events, and stock history...")
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
            # Additional companies:
            {
                "name": "Eco Innovations Group",
                "description": "A leader in eco-friendly product design and sustainable development.",
                "sustainability_rating": Decimal("8.2"),
                "current_stock_price": Decimal("170.00"),
            },
            {
                "name": "Green Tech Solutions",
                "description": "Provides smart, sustainable tech solutions for urban challenges.",
                "sustainability_rating": Decimal("8.4"),
                "current_stock_price": Decimal("185.00"),
            },
            {
                "name": "Sustainable Logistics",
                "description": "Focuses on eco-friendly logistics and supply chain optimization.",
                "sustainability_rating": Decimal("7.6"),
                "current_stock_price": Decimal("145.00"),
            },
            {
                "name": "Organic Harvest Co.",
                "description": "Produces organic foods and supports sustainable farming practices.",
                "sustainability_rating": Decimal("8.0"),
                "current_stock_price": Decimal("130.00"),
            },
            {
                "name": "Renewable Innovations",
                "description": "Researches and develops breakthrough renewable energy technologies.",
                "sustainability_rating": Decimal("8.9"),
                "current_stock_price": Decimal("195.00"),
            },
        ]

        # Limit the companies based on the company_count argument
        companies_data = companies_data[:company_count]

        self.stdout.write("Creating companies...")
        companies = []
        for data in companies_data:
            company = Company.objects.create(**data)
            companies.append(company)
            # Create an initial stock price history record for each company
            StockPriceHistory.objects.create(company=company, price=company.current_stock_price)
        self.stdout.write(self.style.SUCCESS(f"Created {len(companies)} companies."))

        # Sample events data - setting durations around 5 minutes
        events_data = [
            {
                "title": "Government Green Subsidy",
                "description": "A new subsidy for renewable energy boosts investor confidence.",
                "impact_factor": Decimal("0.10"),
                "duration": 5,  # 5 minutes duration
            },
            {
                "title": "Environmental Scandal",
                "description": "A company is caught in an environmental scandal, causing stock prices to drop.",
                "impact_factor": Decimal("-0.15"),
                "duration": 5,
            },
            {
                "title": "Sustainability Award",
                "description": "A company wins a prestigious sustainability award, spiking its stock price.",
                "impact_factor": Decimal("0.12"),
                "duration": 5,
            },
            {
                "title": "Technological Breakthrough",
                "description": "A breakthrough in eco-friendly technology improves prospects for green companies.",
                "impact_factor": Decimal("0.08"),
                "duration": 5,
            },
            {
                "title": "Policy Change",
                "description": "A new government policy supports sustainable practices across the board.",
                "impact_factor": Decimal("0.05"),
                "duration": 5,
            },
        ]

        # Limit events based on the event_count argument
        events_data = events_data[:event_count]

        self.stdout.write("Creating sample market events...")
        for event_data in events_data:
            event = MarketEvent.objects.create(**event_data)
            # Randomly assign a subset of companies to this event
            if companies:
                num = random.randint(1, len(companies))
                affected = random.sample(companies, k=num)
                event.companies_affected.add(*affected)
                self.stdout.write(self.style.SUCCESS(
                    f"Assigned {len(affected)} companies to event '{event.title}'"
                ))
            else:
                self.stdout.write("No companies available to assign.")
            event.save()
            self.stdout.write(self.style.SUCCESS(f"Created event: {event.title}"))

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))
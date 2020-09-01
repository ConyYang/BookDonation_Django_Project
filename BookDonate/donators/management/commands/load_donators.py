from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from donators.models import Book, Award
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y %H:%M'

AWARDS_NAMES = [
    'NobelAward',
    'BestSellerAward',
    'NewYorkAward',
    'GreatWritterAward',
    'EnjoyReadingAward',
    'CoolLiteratuerAward',
    'LoveAndPeaceAward'
]

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the donator information from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Book_Data.csv into our donator mode"

    def handle(self, *args, **options):
        if Award.objects.exists() or Book.objects.exists():
            print('Book data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Creating award data")
        for award_name in AWARDS_NAMES:
            awa = Award(name=award_name)
            awa.save()

        print("Loading book data for book that are donated")
        for row in DictReader(open('./Book_data.csv')):
            book = Book()
            book.name = row['Name']
            book.donator = row['Donator']
            book.category = row['Category']
            book.author = row['Author']
            book.description = row['Description']
            book.language = row['Language']
            book.rate = row['Rating']
            raw_donate_date = row['DonateDate']
            donate_date = UTC.localize(
                datetime.strptime(raw_donate_date, DATETIME_FORMAT))
            book.donate_date = donate_date
            book.save()
            
            raw_award_names = row['Award']
            award_names = [name for name in raw_award_names.split('| ') if name]
            for awa_name in award_names:
                awa = Award.objects.get(name=awa_name)
                book.prices.add(awa)
            book.save()

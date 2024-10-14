from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import get_todays_extractions

class Command(BaseCommand):
    help = "Should print jsons of current days extractions"

    def handle(self, *args, **kwargs):
        result = get_todays_extractions()
        self.stdout.write(str(result))
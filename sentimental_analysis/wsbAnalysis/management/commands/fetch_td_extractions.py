from django.core.management.base import BaseCommand
from wsbAnalysis.reddit import get_todays_extractions, compare_td_with_top
from wsbAnalysis.data import fmp_key

class Command(BaseCommand):
    help = "Should print jsons of current days extractions"

    def handle(self, *args, **kwargs):
        result = get_todays_extractions()
        output = compare_td_with_top(fmp_key, result)
        self.stdout.write(str(result))
        self.stdout.write(str(output))
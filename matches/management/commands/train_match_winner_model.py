import pandas as pd
from django.core.management.base import BaseCommand

from matches.models import Match

pd.set_option("future.no_silent_downcasting", True)


class Command(BaseCommand):
    help = "Train match winner model"

    def handle(self, *args, **options) -> None:
        """
        Execute the command to train the match winner model
        """

        self.stdout.write(self.style.HTTP_INFO("Downloading match data..."))
        matches_df = self._get_matches_df()

        print(matches_df)

    def _get_matches_df(self) -> pd.DataFrame:
        """
        Get matches from database as a DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with matches
        """

        return pd.DataFrame.from_records(Match.objects.all().values(), index="id")

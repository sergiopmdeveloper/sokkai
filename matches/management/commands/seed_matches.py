import pandas as pd
from django.core.management.base import BaseCommand, CommandError

SOCCER_MATCHES_URL = (
    "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"
)


class Command(BaseCommand):
    help = "Command for seeding the matches table in the database"

    _matches_df: pd.DataFrame

    def handle(self, *args, **options) -> None:
        """
        Executes the command
        """

        self.stdout.write("Downloading matches data...")
        self._download_matches_data()

    def _download_matches_data(self) -> None:
        """
        Downloads the matches data from the URL

        Raises
        ------
        CommandError
            If there is an error downloading the data
        """

        try:
            self._matches_df = pd.read_csv(SOCCER_MATCHES_URL)
        except Exception:
            raise CommandError("Error downloading matches data")

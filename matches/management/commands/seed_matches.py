import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from matches.constants import MatchFields
from matches.models import Match

SOCCER_MATCHES_URL = (
    "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"
)


class Command(BaseCommand):
    help = "Command for seeding the table `matches` in the database"

    _match_df: pd.DataFrame
    _match_instances: list[Match]

    def handle(self, *args, **options) -> None:
        """
        Executes the command
        """

        self.stdout.write("Downloading match data...")
        self._download_match_data()

        self.stdout.write("Extracting columns...")
        self._extract_columns()

        self.stdout.write("Formatting columns...")
        self._format_columns()

        self.stdout.write("Generating match instances...")
        self._generate_match_instances()

    def _download_match_data(self) -> None:
        """
        Downloads the match data from the URL

        Raises
        ------
        CommandError
            If there is an error downloading the data
        """

        try:
            self._match_df = pd.read_csv(SOCCER_MATCHES_URL)
        except Exception:
            raise CommandError("Error downloading matches data")

    def _extract_columns(self) -> None:
        """
        Extracts the columns from the match DataFrame
        """

        self._match_df = self._match_df[MatchFields.field_list()]

    def _format_columns(self) -> None:
        """
        Formats the columns of the match DataFrame
        """

        self._match_df[MatchFields.SEASON] = self._match_df[MatchFields.SEASON].astype(
            str
        )

    def _generate_match_instances(self) -> None:
        """
        Generates the match instances from the match DataFrame
        """

        self._match_instances = [
            Match(**match) for match in self._match_df.to_dict("records")
        ]

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

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

        self.stdout.write("Generating match instances...")
        self._generate_match_instances()

        self.stdout.write("Saving match instances...")
        self._save_match_instances()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {len(self._match_instances)} matches"
            )
        )

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

    def _generate_match_instances(self) -> None:
        """
        Generates the match instances from the match DataFrame
        """

        self._match_instances = [
            Match(**match) for match in self._match_df.to_dict("records")
        ]

    def _save_match_instances(self) -> None:
        """
        Saves the match instances to the database
        """

        if Match.objects.exists():
            Match.objects.all().delete()

            with connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM sqlite_sequence WHERE name='{Match._meta.db_table}';"
                )

        Match.objects.bulk_create(self._match_instances)

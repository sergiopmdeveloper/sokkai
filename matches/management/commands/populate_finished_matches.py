from urllib.error import HTTPError

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import connection

from matches.constants import MATCH_DATA_URL, MatchFields, MatchFieldTypes
from matches.exceptions import DownloadError, FieldsNotFound
from matches.models import Match
from utils import extract_keys_from_key_error

pd.set_option("future.no_silent_downcasting", True)


class Command(BaseCommand):
    help = "Populate finished matches"

    def handle(self, *args, **options) -> None:
        """
        Execute the command to populate finished matches
        """

        self.stdout.write(self.style.HTTP_INFO("Downloading match data..."))
        self._download_match_data()

        self.stdout.write(self.style.HTTP_INFO("Extracting match columns..."))
        self._extract_match_columns()

        self.stdout.write(self.style.HTTP_INFO("Filtering finished matches..."))
        self._filter_finished_matches()

        self.stdout.write(self.style.HTTP_INFO("Dropping NaN values..."))
        self._drop_nan_values()

        self.stdout.write(self.style.HTTP_INFO("Setting match column types..."))
        self._set_match_column_types()

        self.stdout.write(self.style.HTTP_INFO("Generating match instances..."))
        self._generate_match_instances()

        self.stdout.write(self.style.HTTP_INFO("Inserting matches in database..."))
        self._insert_matches_in_db()

    def _download_match_data(self) -> None:
        """
        Download match data

        Raises
        ------
        DownloadError
            If an error occurs downloading match data
        """

        try:
            self._match_df = pd.read_csv(MATCH_DATA_URL)
        except HTTPError:
            raise DownloadError("Error downloading match data")

    def _extract_match_columns(self) -> None:
        """
        Extract columns from match data

        Raises
        ------
        FieldsNotFound
            If one or multiple fields are not found in the match data
        """

        try:
            self._match_df = self._match_df[
                [
                    MatchFields.date.value,
                    MatchFields.league.value,
                    MatchFields.season.value,
                    MatchFields.team1.value,
                    MatchFields.team2.value,
                    MatchFields.spi1.value,
                    MatchFields.spi2.value,
                    MatchFields.prob1.value,
                    MatchFields.prob2.value,
                    MatchFields.probtie.value,
                    MatchFields.proj_score1.value,
                    MatchFields.proj_score2.value,
                    MatchFields.score1.value,
                    MatchFields.score2.value,
                ]
            ]
        except KeyError as e:
            raise FieldsNotFound(
                f"Fields {extract_keys_from_key_error(e)} not found in match data"
            )

    def _filter_finished_matches(self) -> None:
        """
        Filter finished matches
        """

        self._match_df = self._match_df[
            (self._match_df[MatchFields.score1.value].notnull())
            & (self._match_df[MatchFields.score2.value].notnull())
        ]

    def _drop_nan_values(self) -> None:
        """
        Drop NaN values
        """

        self._match_df = self._match_df.dropna().reset_index(drop=True)

    def _set_match_column_types(self) -> None:
        """
        Set match column types
        """

        match_field_types = dict(MatchFieldTypes.__members__.items())

        for column in self._match_df.columns.to_list():
            self._match_df[column] = self._match_df[column].astype(
                match_field_types[column].value
            )

    def _generate_match_instances(self) -> None:
        """
        Generate match instances
        """

        self._match_instances = [
            Match(**match) for match in self._match_df.to_dict(orient="records")
        ]

    def _insert_matches_in_db(self) -> None:
        """
        Insert matches in database
        """

        Match.objects.all().delete()
        self._reset_sequence_of_table_matches()

        Match.objects.bulk_create(self._match_instances)

        self.stdout.write(
            self.style.SUCCESS("Finished populating matches in database!")
        )

    def _reset_sequence_of_table_matches(self) -> None:
        """
        Reset the sequence of the table matches
        """

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='" + Match._meta.db_table + "';"
            )

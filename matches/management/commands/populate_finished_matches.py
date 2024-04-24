from urllib.error import HTTPError

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import connection

from matches.constants import MATCHES_DATA_URL, MatchFields, MatchFieldsTypes
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

        self.stdout.write(self.style.HTTP_INFO("Downloading matches data..."))
        self.__download_matches_data()

        self.stdout.write(self.style.HTTP_INFO("Extracting matches columns..."))
        self.__extract_matches_columns()

        self.stdout.write(self.style.HTTP_INFO("Filtering finished matches..."))
        self.__filter_finished_matches()

        self.stdout.write(self.style.HTTP_INFO("Dropping NaN values..."))
        self.__drop_nan_values()

        self.stdout.write(self.style.HTTP_INFO("Inserting matches in database..."))
        self.__insert_matches_in_db()

    def __download_matches_data(self) -> None:
        """
        Download matches data

        Raises
        ------
        DownloadError
            If an error occurs downloading matches data
        """

        try:
            self.matches_df = pd.read_csv(MATCHES_DATA_URL)
        except HTTPError:
            raise DownloadError("Error downloading matches data")

    def __extract_matches_columns(self) -> None:
        """
        Extract columns from matches data

        Raises
        ------
        FieldsNotFound
            If one or multiple fields are not found in the matches data
        """

        try:
            self.matches_df = self.matches_df[
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
                f"Fields {extract_keys_from_key_error(e)} not found in matches data"
            )

    def __filter_finished_matches(self) -> None:
        """
        Filter finished matches

        Raises
        ------
        FieldsNotFound
            If one or multiple fields are not found in the matches data
        """

        try:
            self.matches_df = self.matches_df[
                (self.matches_df[MatchFields.score1.value].notnull())
                & (self.matches_df[MatchFields.score2.value].notnull())
            ]
        except KeyError as e:
            raise FieldsNotFound(f"Field {e} not found in matches data")

    def __drop_nan_values(self) -> None:
        """
        Drop NaN values
        """

        self.matches_df = self.matches_df.dropna().reset_index(drop=True)

    def __insert_matches_in_db(self) -> None:
        """
        Insert matches in database
        """

        Match.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='" + Match._meta.db_table + "';"
            )

        for column in self.matches_df.columns.to_list():
            self.matches_df[column] = self.matches_df[column].astype(
                MatchFieldsTypes[column].value
            )

        matches_to_insert = [
            Match(**match) for match in self.matches_df.to_dict(orient="records")
        ]

        Match.objects.bulk_create(matches_to_insert)

        self.stdout.write(
            self.style.SUCCESS("Finished populating matches in database!")
        )

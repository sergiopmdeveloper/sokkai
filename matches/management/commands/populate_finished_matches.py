from urllib.error import HTTPError

import pandas as pd
from django.core.management.base import BaseCommand

from matches.constants import MATCHES_DATA_URL, MatchFields
from matches.exceptions import DownloadError, FieldsNotFound
from utils import extract_keys_from_key_error


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

        return

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
                    MatchFields.DATE.value,
                    MatchFields.LEAGUE.value,
                    MatchFields.SEASON.value,
                    MatchFields.TEAM1.value,
                    MatchFields.TEAM2.value,
                    MatchFields.SPI1.value,
                    MatchFields.SPI2.value,
                    MatchFields.PROB1.value,
                    MatchFields.PROB2.value,
                    MatchFields.PROBTIE.value,
                    MatchFields.PROJSCORE1.value,
                    MatchFields.PROJSCORE2.value,
                    MatchFields.SCORE1.value,
                    MatchFields.SCORE2.value,
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
                (self.matches_df[MatchFields.SCORE1.value].notnull())
                & (self.matches_df[MatchFields.SCORE2.value].notnull())
            ]
        except KeyError as e:
            raise FieldsNotFound(f"Field {e} not found in matches data")

    def __drop_nan_values(self) -> None:
        """
        Drop NaN values
        """

        self.matches_df = self.matches_df.dropna().reset_index(drop=True)

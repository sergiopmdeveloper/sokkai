import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.pipeline import Pipeline

from ai.preprocessing import SplitXY
from matches.constants import MatchFields
from matches.models import Match

pd.set_option("future.no_silent_downcasting", True)


class Command(BaseCommand):
    help = "Train match winner model"

    def handle(self, *args, **options) -> None:
        """
        Execute the command to train the match winner model
        """

        self.stdout.write(self.style.HTTP_INFO("Downloading match data..."))
        self._get_match_df()

        self.stdout.write(self.style.HTTP_INFO("Initializing pipeline steps..."))
        self._initialize_pipeline_steps()

        self.stdout.write(self.style.HTTP_INFO("Add split X and y step to pipeline..."))
        self._add_split_xy_step()

        self.stdout.write(self.style.HTTP_INFO("Executing pipeline..."))
        self._execute_pipeline()

    def _get_match_df(self) -> None:
        """
        Get matches from database as a DataFrame
        """

        self._match_df = pd.DataFrame.from_records(
            Match.objects.all().values(), index="id"
        )

    def _initialize_pipeline_steps(self) -> None:
        """
        Initialize the pipeline
        """

        self._pipeline_steps = []

    def _add_split_xy_step(self) -> None:
        """
        Add split X and y step to pipeline
        """

        feature_columns = [
            MatchFields.spi1.value,
            MatchFields.spi2.value,
            MatchFields.prob1.value,
            MatchFields.prob2.value,
            MatchFields.probtie.value,
            MatchFields.proj_score1.value,
            MatchFields.proj_score2.value,
        ]

        target_columns = [
            MatchFields.score1.value,
            MatchFields.score2.value,
        ]

        split_xy_transformer = SplitXY(
            feature_columns=feature_columns, target_columns=target_columns
        )

        self._pipeline_steps.append(("split_x_and_y", split_xy_transformer))

    def _execute_pipeline(self) -> None:
        """
        Execute the pipeline
        """

        self._pipeline = Pipeline(self._pipeline_steps)
        self._pipeline.fit_transform(self._match_df)

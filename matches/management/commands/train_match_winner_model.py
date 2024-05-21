import os

import pandas as pd
from django.core.management.base import BaseCommand

from ai.custom import generate_match_winner_column
from ai.interfaces import PipelineGenericWithModel
from ai.preprocessing import split_xy
from matches.constants import MatchFields
from matches.models import Match

pd.set_option("future.no_silent_downcasting", True)

MATCH_WINNER_PIPELINE_DIR = os.getcwd() + "/ai/pipelines/match_winner"


class Command(BaseCommand, PipelineGenericWithModel):
    help = "Train match winner model"

    def handle(self, *args, **options) -> None:
        """
        Execute the command to train the match winner model
        """

        self.stdout.write(self.style.HTTP_INFO("Creating pipeline directory..."))
        os.makedirs(MATCH_WINNER_PIPELINE_DIR, exist_ok=True)

        self.stdout.write(self.style.HTTP_INFO("Downloading match data..."))
        self._get_match_df()

        self.stdout.write(self.style.HTTP_INFO("Splitting X and y..."))
        self._split_xy()

        self.stdout.write(self.style.HTTP_INFO("Generating match winner column..."))
        self._generate_match_winner_column()

        self.stdout.write(self.style.HTTP_INFO("Initializing pipeline steps..."))
        self._initialize_pipeline_steps()

        self.stdout.write(self.style.HTTP_INFO("Adding steps to pipeline..."))
        self._add_steps_to_pipeline(steps=["numerical_scaler"])

        self.stdout.write(self.style.HTTP_INFO("Initializing pipeline..."))
        self._initialize_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Injecting model in pipeline..."))
        self._inject_model_in_pipeline(model="logistic_regression")

        self.stdout.write(self.style.HTTP_INFO("Generating pipeline metrics..."))
        self._generate_pipeline_metrics(model_type="classification")

        self.stdout.write(self.style.HTTP_INFO("Executing pipeline..."))
        self._execute_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Exporting pipeline..."))
        self._export_pipeline(pipeline_dir=MATCH_WINNER_PIPELINE_DIR)

        self.stdout.write(self.style.HTTP_INFO("Exporting pipeline metrics..."))
        self._export_pipeline_metrics(pipeline_dir=MATCH_WINNER_PIPELINE_DIR)

    def _get_match_df(self) -> None:
        """
        Get matches from database as a DataFrame
        """

        self._match_df = pd.DataFrame.from_records(
            Match.objects.all().values(), index="id"
        )

    def _split_xy(self) -> None:
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

        self.X, self.y = split_xy(
            df=self._match_df,
            feature_columns=feature_columns,
            target_columns=target_columns,
        )

    def _generate_match_winner_column(self) -> None:
        """
        Generate match winner column
        """

        y = self.y.copy()

        self.y = generate_match_winner_column(df=y)

    def _execute_pipeline(self) -> None:
        """
        Execute the pipeline
        """

        self._pipeline_with_model.fit(self.X, self.y)

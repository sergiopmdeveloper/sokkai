import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.pipeline import Pipeline

from ai.custom import generate_match_winner_column
from ai.preprocessing import NumericalScaler, split_xy
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

        self.stdout.write(self.style.HTTP_INFO("Splitting X and y..."))
        self._split_xy()

        self.stdout.write(self.style.HTTP_INFO("Initializing pipeline steps..."))
        self._initialize_pipeline_steps()

        self.stdout.write(self.style.HTTP_INFO("Generating match winner column..."))
        self._generate_match_winner_column()

        self.stdout.write(self.style.HTTP_INFO("Adding scale features step..."))
        self._add_scale_features_step()

        self.stdout.write(self.style.HTTP_INFO("Executing pipeline..."))
        self._execute_pipeline()

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

    def _initialize_pipeline_steps(self) -> None:
        """
        Initialize the pipeline
        """

        self._pipeline_steps = []

    def _generate_match_winner_column(self) -> None:
        """
        Generate match winner column
        """

        y = self.y.copy()

        self.y = generate_match_winner_column(df=y)

    def _add_scale_features_step(self) -> None:
        """
        Add scale features step to pipeline
        """

        numerical_scaler_transformer = NumericalScaler()

        self._pipeline_steps.append(("scale_features", numerical_scaler_transformer))

    def _execute_pipeline(self) -> None:
        """
        Execute the pipeline
        """

        self._pipeline = Pipeline(self._pipeline_steps)
        self._pipeline.fit_transform(self.X, self.y)

import json
import os

import joblib
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

from ai.custom import generate_match_winner_column
from ai.interfaces import AbstractPipelineWithModel
from ai.preprocessing import NumericalScaler, split_xy
from matches.constants import MatchFields
from matches.models import Match

pd.set_option("future.no_silent_downcasting", True)

MATCH_WINNER_MODEL_DIR = os.getcwd() + "/ai/pipelines/match_winner"


class Command(BaseCommand, AbstractPipelineWithModel):
    help = "Train match winner model"

    def handle(self, *args, **options) -> None:
        """
        Execute the command to train the match winner model
        """

        self.stdout.write(self.style.HTTP_INFO("Creating pipeline directory..."))
        os.makedirs(MATCH_WINNER_MODEL_DIR, exist_ok=True)

        self.stdout.write(self.style.HTTP_INFO("Downloading match data..."))
        self._get_match_df()

        self.stdout.write(self.style.HTTP_INFO("Splitting X and y..."))
        self._split_xy()

        self.stdout.write(self.style.HTTP_INFO("Generating match winner column..."))
        self._generate_match_winner_column()

        self.stdout.write(self.style.HTTP_INFO("Initializing pipeline steps..."))
        self._initialize_pipeline_steps()

        self.stdout.write(self.style.HTTP_INFO("Adding steps to pipeline..."))
        self._add_steps_to_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Initializing pipeline..."))
        self._initialize_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Injecting model in pipeline..."))
        self._inject_model_in_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Generating pipeline metrics..."))
        self._generate_pipeline_metrics()

        self.stdout.write(self.style.HTTP_INFO("Executing pipeline..."))
        self._execute_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Exporting pipeline..."))
        self._export_pipeline()

        self.stdout.write(self.style.HTTP_INFO("Exporting pipeline metrics..."))
        self._export_pipeline_metrics()

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

    def _initialize_pipeline_steps(self) -> None:
        """
        Initialize the pipeline
        """

        self._pipeline_steps = []

    def _add_steps_to_pipeline(self) -> None:
        """
        Add steps to pipeline
        """

        numerical_scaler_transformer = NumericalScaler()

        self._pipeline_steps.append(("scale_features", numerical_scaler_transformer))

    def _initialize_pipeline(self) -> None:
        """
        Initialize the pipeline
        """

        self._pipeline = Pipeline(self._pipeline_steps)

    def _inject_model_in_pipeline(self) -> None:
        """
        Inject model in pipeline
        """

        self._pipeline_with_model = Pipeline(
            [("pipeline", self._pipeline), ("model", LogisticRegression())]
        )

    def _generate_pipeline_metrics(self) -> None:
        """
        Generate pipeline metrics
        """

        self._metrics = {
            "accuracy": cross_val_score(
                self._pipeline_with_model, self.X, self.y, cv=5, scoring="accuracy"
            ).mean(),
            "precision": cross_val_score(
                self._pipeline_with_model, self.X, self.y, cv=5, scoring="precision"
            ).mean(),
            "recall": cross_val_score(
                self._pipeline_with_model, self.X, self.y, cv=5, scoring="recall"
            ).mean(),
            "f1": cross_val_score(
                self._pipeline_with_model, self.X, self.y, cv=5, scoring="f1"
            ).mean(),
        }

    def _execute_pipeline(self) -> None:
        """
        Execute the pipeline
        """

        self._pipeline_with_model.fit(self.X, self.y)

    def _export_pipeline(self) -> None:
        """
        Export pipeline
        """

        joblib.dump(
            self._pipeline_with_model, f"{MATCH_WINNER_MODEL_DIR}/pipeline.joblib"
        )

    def _export_pipeline_metrics(self) -> None:
        """
        Export pipeline metrics
        """

        with open(f"{MATCH_WINNER_MODEL_DIR}/metrics.json", "w") as file:
            json.dump(self._metrics, file, indent=4)
            file.write("\n")

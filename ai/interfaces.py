import json

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

from ai.preprocessing import NumericalScaler


class PipelineGeneric:
    """
    PipelineGeneric class

    Methods
    -------
    _initialize_pipeline_steps() -> None
        Initialize the pipeline steps
    _add_steps_to_pipeline(steps: list[str]) -> None
        Add steps to pipeline
    _initialize_pipeline() -> None
        Initialize the pipeline
    _execute_pipeline() -> None
        Execute the pipeline
    _export_pipeline(pipeline_dir: str) -> None
        Export the pipeline
    """

    def _initialize_pipeline_steps(self) -> None:
        """
        Initialize the pipeline steps
        """

        self._pipeline_steps = []

    def _add_steps_to_pipeline(self, steps: list[str]) -> None:
        """
        Add steps to pipeline

        Parameters
        ----------
        steps : list[str]
            List of steps to add to the pipeline
        """

        AVAILABLE_STEPS = {
            "numerical_scaler": ("scale_features", NumericalScaler()),
        }

        for step in steps:
            try:
                self._pipeline_steps.append(AVAILABLE_STEPS[step])
            except KeyError:
                raise KeyError(f"Step {step} not available")

    def _initialize_pipeline(self) -> None:
        """
        Initialize the pipeline
        """

        self._pipeline = Pipeline(self._pipeline_steps)

    def _execute_pipeline(self) -> None:
        """
        Execute the pipeline
        """

        try:
            self._pipeline.fit_transform(self.X)
        except AttributeError:
            raise AttributeError("X is not defined")

    def _export_pipeline(self, pipeline_dir: str) -> None:
        """
        Export the pipeline

        Parameters
        ----------
        pipeline_dir : str
            Pipeline directory to export
        """

        joblib.dump(self._pipeline, f"{pipeline_dir}/pipeline.joblib")


class PipelineGenericWithModel(PipelineGeneric):
    """
    PipelineGenericWithModel class

    Methods
    -------
    _inject_model_in_pipeline(model: str) -> None
        Inject model in pipeline
    _generate_pipeline_metrics(model_type: str) -> None
        Generate pipeline metrics
    _execute_pipeline() -> None
        Execute the pipeline
    _export_pipeline(pipeline_dir: str) -> None
        Export pipeline
    _export_pipeline_metrics(pipeline_dir: str) -> None
        Export pipeline metrics
    """

    def _inject_model_in_pipeline(self, model: str) -> None:
        """
        Inject model in pipeline

        Parameters
        ----------
        model : str
            Model to inject in the pipeline
        """

        AVAILABLE_MODELS = {
            "logistic_regression": LogisticRegression(),
        }

        try:
            self._pipeline_with_model = Pipeline(
                [("pipeline", self._pipeline), ("model", AVAILABLE_MODELS[model])]
            )
        except KeyError:
            raise KeyError(f"Model {model} not available")

    def _generate_pipeline_metrics(self, model_type: str) -> None:
        """
        Generate pipeline metrics

        Parameters
        ----------
        model_type : str
            Model type to generate metrics

        Raises
        ------
        AttributeError
            If X or y is not defined
        """

        try:
            self.X, self.y
        except AttributeError as e:
            raise AttributeError(f"{e.name} is not defined")

        if model_type == "classification":
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

    def _export_pipeline(self, pipeline_dir: str) -> None:
        """
        Export pipeline

        Parameters
        ----------
        pipeline_dir : str
            Pipeline directory to export pipeline
        """

        joblib.dump(self._pipeline_with_model, f"{pipeline_dir}/pipeline.joblib")

    def _export_pipeline_metrics(self, pipeline_dir: str) -> None:
        """
        Export pipeline metrics

        Parameters
        ----------
        pipeline_dir : str
            Pipeline directory to export metrics
        """

        with open(f"{pipeline_dir}/metrics.json", "w") as file:
            json.dump(self._metrics, file, indent=4)
            file.write("\n")

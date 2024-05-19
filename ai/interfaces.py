from abc import ABC, abstractmethod


class AbstractPipeline(ABC):
    """
    Abstract class for pipeline

    Methods
    -------
    _initialize_pipeline_steps() -> None
        Abstract method to initialize the pipeline steps
    _initialize_pipeline() -> None
        Abstract method to initialize the pipeline
    _execute_pipeline() -> None
        Abstract method to execute the pipeline
    _export_pipeline() -> None
        Abstract method to export the pipeline
    """

    @abstractmethod
    def _initialize_pipeline_steps(self) -> None:
        """
        Abstract method to initialize the pipeline steps
        """

        pass

    @abstractmethod
    def _initialize_pipeline(self) -> None:
        """
        Abstract method to initialize the pipeline
        """

        pass

    @abstractmethod
    def _execute_pipeline(self) -> None:
        """
        Abstract method to execute the pipeline
        """

        pass

    @abstractmethod
    def _export_pipeline(self) -> None:
        """
        Abstract method to export the pipeline
        """

        pass


class AbstractPipelineWithModel(AbstractPipeline):
    """
    Abstract class for pipeline with model

    Methods
    -------
    _inject_model_in_pipeline() -> None
        Abstract method to inject model in pipeline
    _generate_pipeline_metrics() -> None
        Abstract method to generate pipeline metrics
    _export_pipeline_metrics() -> None
        Abstract method to export pipeline metrics
    """

    @abstractmethod
    def _inject_model_in_pipeline(self) -> None:
        """
        Abstract method to inject model in pipeline
        """

        pass

    @abstractmethod
    def _generate_pipeline_metrics(self) -> None:
        """
        Abstract method to generate pipeline metrics
        """

        pass

    @abstractmethod
    def _export_pipeline_metrics(self) -> None:
        """
        Abstract method to export pipeline metrics
        """

        pass

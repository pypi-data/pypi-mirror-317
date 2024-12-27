"""
Type annotations for neptunedata service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_neptunedata.client import NeptuneDataClient

    session = get_session()
    async with session.create_client("neptunedata") as client:
        client: NeptuneDataClient
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, Mapping

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CancelGremlinQueryInputRequestTypeDef,
    CancelGremlinQueryOutputTypeDef,
    CancelLoaderJobInputRequestTypeDef,
    CancelLoaderJobOutputTypeDef,
    CancelMLDataProcessingJobInputRequestTypeDef,
    CancelMLDataProcessingJobOutputTypeDef,
    CancelMLModelTrainingJobInputRequestTypeDef,
    CancelMLModelTrainingJobOutputTypeDef,
    CancelMLModelTransformJobInputRequestTypeDef,
    CancelMLModelTransformJobOutputTypeDef,
    CancelOpenCypherQueryInputRequestTypeDef,
    CancelOpenCypherQueryOutputTypeDef,
    CreateMLEndpointInputRequestTypeDef,
    CreateMLEndpointOutputTypeDef,
    DeleteMLEndpointInputRequestTypeDef,
    DeleteMLEndpointOutputTypeDef,
    DeletePropertygraphStatisticsOutputTypeDef,
    DeleteSparqlStatisticsOutputTypeDef,
    ExecuteFastResetInputRequestTypeDef,
    ExecuteFastResetOutputTypeDef,
    ExecuteGremlinExplainQueryInputRequestTypeDef,
    ExecuteGremlinExplainQueryOutputTypeDef,
    ExecuteGremlinProfileQueryInputRequestTypeDef,
    ExecuteGremlinProfileQueryOutputTypeDef,
    ExecuteGremlinQueryInputRequestTypeDef,
    ExecuteGremlinQueryOutputTypeDef,
    ExecuteOpenCypherExplainQueryInputRequestTypeDef,
    ExecuteOpenCypherExplainQueryOutputTypeDef,
    ExecuteOpenCypherQueryInputRequestTypeDef,
    ExecuteOpenCypherQueryOutputTypeDef,
    GetEngineStatusOutputTypeDef,
    GetGremlinQueryStatusInputRequestTypeDef,
    GetGremlinQueryStatusOutputTypeDef,
    GetLoaderJobStatusInputRequestTypeDef,
    GetLoaderJobStatusOutputTypeDef,
    GetMLDataProcessingJobInputRequestTypeDef,
    GetMLDataProcessingJobOutputTypeDef,
    GetMLEndpointInputRequestTypeDef,
    GetMLEndpointOutputTypeDef,
    GetMLModelTrainingJobInputRequestTypeDef,
    GetMLModelTrainingJobOutputTypeDef,
    GetMLModelTransformJobInputRequestTypeDef,
    GetMLModelTransformJobOutputTypeDef,
    GetOpenCypherQueryStatusInputRequestTypeDef,
    GetOpenCypherQueryStatusOutputTypeDef,
    GetPropertygraphStatisticsOutputTypeDef,
    GetPropertygraphStreamInputRequestTypeDef,
    GetPropertygraphStreamOutputTypeDef,
    GetPropertygraphSummaryInputRequestTypeDef,
    GetPropertygraphSummaryOutputTypeDef,
    GetRDFGraphSummaryInputRequestTypeDef,
    GetRDFGraphSummaryOutputTypeDef,
    GetSparqlStatisticsOutputTypeDef,
    GetSparqlStreamInputRequestTypeDef,
    GetSparqlStreamOutputTypeDef,
    ListGremlinQueriesInputRequestTypeDef,
    ListGremlinQueriesOutputTypeDef,
    ListLoaderJobsInputRequestTypeDef,
    ListLoaderJobsOutputTypeDef,
    ListMLDataProcessingJobsInputRequestTypeDef,
    ListMLDataProcessingJobsOutputTypeDef,
    ListMLEndpointsInputRequestTypeDef,
    ListMLEndpointsOutputTypeDef,
    ListMLModelTrainingJobsInputRequestTypeDef,
    ListMLModelTrainingJobsOutputTypeDef,
    ListMLModelTransformJobsInputRequestTypeDef,
    ListMLModelTransformJobsOutputTypeDef,
    ListOpenCypherQueriesInputRequestTypeDef,
    ListOpenCypherQueriesOutputTypeDef,
    ManagePropertygraphStatisticsInputRequestTypeDef,
    ManagePropertygraphStatisticsOutputTypeDef,
    ManageSparqlStatisticsInputRequestTypeDef,
    ManageSparqlStatisticsOutputTypeDef,
    StartLoaderJobInputRequestTypeDef,
    StartLoaderJobOutputTypeDef,
    StartMLDataProcessingJobInputRequestTypeDef,
    StartMLDataProcessingJobOutputTypeDef,
    StartMLModelTrainingJobInputRequestTypeDef,
    StartMLModelTrainingJobOutputTypeDef,
    StartMLModelTransformJobInputRequestTypeDef,
    StartMLModelTransformJobOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("NeptuneDataClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BadRequestException: type[BotocoreClientError]
    BulkLoadIdNotFoundException: type[BotocoreClientError]
    CancelledByUserException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ClientTimeoutException: type[BotocoreClientError]
    ConcurrentModificationException: type[BotocoreClientError]
    ConstraintViolationException: type[BotocoreClientError]
    ExpiredStreamException: type[BotocoreClientError]
    FailureByQueryException: type[BotocoreClientError]
    IllegalArgumentException: type[BotocoreClientError]
    InternalFailureException: type[BotocoreClientError]
    InvalidArgumentException: type[BotocoreClientError]
    InvalidNumericDataException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    LoadUrlAccessDeniedException: type[BotocoreClientError]
    MLResourceNotFoundException: type[BotocoreClientError]
    MalformedQueryException: type[BotocoreClientError]
    MemoryLimitExceededException: type[BotocoreClientError]
    MethodNotAllowedException: type[BotocoreClientError]
    MissingParameterException: type[BotocoreClientError]
    ParsingException: type[BotocoreClientError]
    PreconditionsFailedException: type[BotocoreClientError]
    QueryLimitExceededException: type[BotocoreClientError]
    QueryLimitException: type[BotocoreClientError]
    QueryTooLargeException: type[BotocoreClientError]
    ReadOnlyViolationException: type[BotocoreClientError]
    S3Exception: type[BotocoreClientError]
    ServerShutdownException: type[BotocoreClientError]
    StatisticsNotAvailableException: type[BotocoreClientError]
    StreamRecordsNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TimeLimitExceededException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]
    UnsupportedOperationException: type[BotocoreClientError]


class NeptuneDataClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NeptuneDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#generate_presigned_url)
        """

    async def cancel_gremlin_query(
        self, **kwargs: Unpack[CancelGremlinQueryInputRequestTypeDef]
    ) -> CancelGremlinQueryOutputTypeDef:
        """
        Cancels a Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_gremlin_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#cancel_gremlin_query)
        """

    async def cancel_loader_job(
        self, **kwargs: Unpack[CancelLoaderJobInputRequestTypeDef]
    ) -> CancelLoaderJobOutputTypeDef:
        """
        Cancels a specified load job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_loader_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#cancel_loader_job)
        """

    async def cancel_ml_data_processing_job(
        self, **kwargs: Unpack[CancelMLDataProcessingJobInputRequestTypeDef]
    ) -> CancelMLDataProcessingJobOutputTypeDef:
        """
        Cancels a Neptune ML data processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_ml_data_processing_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#cancel_ml_data_processing_job)
        """

    async def cancel_ml_model_training_job(
        self, **kwargs: Unpack[CancelMLModelTrainingJobInputRequestTypeDef]
    ) -> CancelMLModelTrainingJobOutputTypeDef:
        """
        Cancels a Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_ml_model_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#cancel_ml_model_training_job)
        """

    async def cancel_ml_model_transform_job(
        self, **kwargs: Unpack[CancelMLModelTransformJobInputRequestTypeDef]
    ) -> CancelMLModelTransformJobOutputTypeDef:
        """
        Cancels a specified model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_ml_model_transform_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#cancel_ml_model_transform_job)
        """

    async def cancel_open_cypher_query(
        self, **kwargs: Unpack[CancelOpenCypherQueryInputRequestTypeDef]
    ) -> CancelOpenCypherQueryOutputTypeDef:
        """
        Cancels a specified openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/cancel_open_cypher_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#cancel_open_cypher_query)
        """

    async def create_ml_endpoint(
        self, **kwargs: Unpack[CreateMLEndpointInputRequestTypeDef]
    ) -> CreateMLEndpointOutputTypeDef:
        """
        Creates a new Neptune ML inference endpoint that lets you query one specific
        model that the model-training process constructed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/create_ml_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#create_ml_endpoint)
        """

    async def delete_ml_endpoint(
        self, **kwargs: Unpack[DeleteMLEndpointInputRequestTypeDef]
    ) -> DeleteMLEndpointOutputTypeDef:
        """
        Cancels the creation of a Neptune ML inference endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/delete_ml_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#delete_ml_endpoint)
        """

    async def delete_propertygraph_statistics(self) -> DeletePropertygraphStatisticsOutputTypeDef:
        """
        Deletes statistics for Gremlin and openCypher (property graph) data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/delete_propertygraph_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#delete_propertygraph_statistics)
        """

    async def delete_sparql_statistics(self) -> DeleteSparqlStatisticsOutputTypeDef:
        """
        Deletes SPARQL statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/delete_sparql_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#delete_sparql_statistics)
        """

    async def execute_fast_reset(
        self, **kwargs: Unpack[ExecuteFastResetInputRequestTypeDef]
    ) -> ExecuteFastResetOutputTypeDef:
        """
        The fast reset REST API lets you reset a Neptune graph quicky and easily,
        removing all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_fast_reset.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#execute_fast_reset)
        """

    async def execute_gremlin_explain_query(
        self, **kwargs: Unpack[ExecuteGremlinExplainQueryInputRequestTypeDef]
    ) -> ExecuteGremlinExplainQueryOutputTypeDef:
        """
        Executes a Gremlin Explain query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_gremlin_explain_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#execute_gremlin_explain_query)
        """

    async def execute_gremlin_profile_query(
        self, **kwargs: Unpack[ExecuteGremlinProfileQueryInputRequestTypeDef]
    ) -> ExecuteGremlinProfileQueryOutputTypeDef:
        """
        Executes a Gremlin Profile query, which runs a specified traversal, collects
        various metrics about the run, and produces a profile report as output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_gremlin_profile_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#execute_gremlin_profile_query)
        """

    async def execute_gremlin_query(
        self, **kwargs: Unpack[ExecuteGremlinQueryInputRequestTypeDef]
    ) -> ExecuteGremlinQueryOutputTypeDef:
        """
        This commands executes a Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_gremlin_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#execute_gremlin_query)
        """

    async def execute_open_cypher_explain_query(
        self, **kwargs: Unpack[ExecuteOpenCypherExplainQueryInputRequestTypeDef]
    ) -> ExecuteOpenCypherExplainQueryOutputTypeDef:
        """
        Executes an openCypher <code>explain</code> request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_open_cypher_explain_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#execute_open_cypher_explain_query)
        """

    async def execute_open_cypher_query(
        self, **kwargs: Unpack[ExecuteOpenCypherQueryInputRequestTypeDef]
    ) -> ExecuteOpenCypherQueryOutputTypeDef:
        """
        Executes an openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/execute_open_cypher_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#execute_open_cypher_query)
        """

    async def get_engine_status(self) -> GetEngineStatusOutputTypeDef:
        """
        Retrieves the status of the graph database on the host.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_engine_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_engine_status)
        """

    async def get_gremlin_query_status(
        self, **kwargs: Unpack[GetGremlinQueryStatusInputRequestTypeDef]
    ) -> GetGremlinQueryStatusOutputTypeDef:
        """
        Gets the status of a specified Gremlin query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_gremlin_query_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_gremlin_query_status)
        """

    async def get_loader_job_status(
        self, **kwargs: Unpack[GetLoaderJobStatusInputRequestTypeDef]
    ) -> GetLoaderJobStatusOutputTypeDef:
        """
        Gets status information about a specified load job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_loader_job_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_loader_job_status)
        """

    async def get_ml_data_processing_job(
        self, **kwargs: Unpack[GetMLDataProcessingJobInputRequestTypeDef]
    ) -> GetMLDataProcessingJobOutputTypeDef:
        """
        Retrieves information about a specified data processing job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_data_processing_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_ml_data_processing_job)
        """

    async def get_ml_endpoint(
        self, **kwargs: Unpack[GetMLEndpointInputRequestTypeDef]
    ) -> GetMLEndpointOutputTypeDef:
        """
        Retrieves details about an inference endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_ml_endpoint)
        """

    async def get_ml_model_training_job(
        self, **kwargs: Unpack[GetMLModelTrainingJobInputRequestTypeDef]
    ) -> GetMLModelTrainingJobOutputTypeDef:
        """
        Retrieves information about a Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_model_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_ml_model_training_job)
        """

    async def get_ml_model_transform_job(
        self, **kwargs: Unpack[GetMLModelTransformJobInputRequestTypeDef]
    ) -> GetMLModelTransformJobOutputTypeDef:
        """
        Gets information about a specified model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_ml_model_transform_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_ml_model_transform_job)
        """

    async def get_open_cypher_query_status(
        self, **kwargs: Unpack[GetOpenCypherQueryStatusInputRequestTypeDef]
    ) -> GetOpenCypherQueryStatusOutputTypeDef:
        """
        Retrieves the status of a specified openCypher query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_open_cypher_query_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_open_cypher_query_status)
        """

    async def get_propertygraph_statistics(self) -> GetPropertygraphStatisticsOutputTypeDef:
        """
        Gets property graph statistics (Gremlin and openCypher).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_propertygraph_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_propertygraph_statistics)
        """

    async def get_propertygraph_stream(
        self, **kwargs: Unpack[GetPropertygraphStreamInputRequestTypeDef]
    ) -> GetPropertygraphStreamOutputTypeDef:
        """
        Gets a stream for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_propertygraph_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_propertygraph_stream)
        """

    async def get_propertygraph_summary(
        self, **kwargs: Unpack[GetPropertygraphSummaryInputRequestTypeDef]
    ) -> GetPropertygraphSummaryOutputTypeDef:
        """
        Gets a graph summary for a property graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_propertygraph_summary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_propertygraph_summary)
        """

    async def get_rdf_graph_summary(
        self, **kwargs: Unpack[GetRDFGraphSummaryInputRequestTypeDef]
    ) -> GetRDFGraphSummaryOutputTypeDef:
        """
        Gets a graph summary for an RDF graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_rdf_graph_summary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_rdf_graph_summary)
        """

    async def get_sparql_statistics(self) -> GetSparqlStatisticsOutputTypeDef:
        """
        Gets RDF statistics (SPARQL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_sparql_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_sparql_statistics)
        """

    async def get_sparql_stream(
        self, **kwargs: Unpack[GetSparqlStreamInputRequestTypeDef]
    ) -> GetSparqlStreamOutputTypeDef:
        """
        Gets a stream for an RDF graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/get_sparql_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#get_sparql_stream)
        """

    async def list_gremlin_queries(
        self, **kwargs: Unpack[ListGremlinQueriesInputRequestTypeDef]
    ) -> ListGremlinQueriesOutputTypeDef:
        """
        Lists active Gremlin queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_gremlin_queries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_gremlin_queries)
        """

    async def list_loader_jobs(
        self, **kwargs: Unpack[ListLoaderJobsInputRequestTypeDef]
    ) -> ListLoaderJobsOutputTypeDef:
        """
        Retrieves a list of the <code>loadIds</code> for all active loader jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_loader_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_loader_jobs)
        """

    async def list_ml_data_processing_jobs(
        self, **kwargs: Unpack[ListMLDataProcessingJobsInputRequestTypeDef]
    ) -> ListMLDataProcessingJobsOutputTypeDef:
        """
        Returns a list of Neptune ML data processing jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_data_processing_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_ml_data_processing_jobs)
        """

    async def list_ml_endpoints(
        self, **kwargs: Unpack[ListMLEndpointsInputRequestTypeDef]
    ) -> ListMLEndpointsOutputTypeDef:
        """
        Lists existing inference endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_ml_endpoints)
        """

    async def list_ml_model_training_jobs(
        self, **kwargs: Unpack[ListMLModelTrainingJobsInputRequestTypeDef]
    ) -> ListMLModelTrainingJobsOutputTypeDef:
        """
        Lists Neptune ML model-training jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_model_training_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_ml_model_training_jobs)
        """

    async def list_ml_model_transform_jobs(
        self, **kwargs: Unpack[ListMLModelTransformJobsInputRequestTypeDef]
    ) -> ListMLModelTransformJobsOutputTypeDef:
        """
        Returns a list of model transform job IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_ml_model_transform_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_ml_model_transform_jobs)
        """

    async def list_open_cypher_queries(
        self, **kwargs: Unpack[ListOpenCypherQueriesInputRequestTypeDef]
    ) -> ListOpenCypherQueriesOutputTypeDef:
        """
        Lists active openCypher queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/list_open_cypher_queries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#list_open_cypher_queries)
        """

    async def manage_propertygraph_statistics(
        self, **kwargs: Unpack[ManagePropertygraphStatisticsInputRequestTypeDef]
    ) -> ManagePropertygraphStatisticsOutputTypeDef:
        """
        Manages the generation and use of property graph statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/manage_propertygraph_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#manage_propertygraph_statistics)
        """

    async def manage_sparql_statistics(
        self, **kwargs: Unpack[ManageSparqlStatisticsInputRequestTypeDef]
    ) -> ManageSparqlStatisticsOutputTypeDef:
        """
        Manages the generation and use of RDF graph statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/manage_sparql_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#manage_sparql_statistics)
        """

    async def start_loader_job(
        self, **kwargs: Unpack[StartLoaderJobInputRequestTypeDef]
    ) -> StartLoaderJobOutputTypeDef:
        """
        Starts a Neptune bulk loader job to load data from an Amazon S3 bucket into a
        Neptune DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_loader_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#start_loader_job)
        """

    async def start_ml_data_processing_job(
        self, **kwargs: Unpack[StartMLDataProcessingJobInputRequestTypeDef]
    ) -> StartMLDataProcessingJobOutputTypeDef:
        """
        Creates a new Neptune ML data processing job for processing the graph data
        exported from Neptune for training.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_ml_data_processing_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#start_ml_data_processing_job)
        """

    async def start_ml_model_training_job(
        self, **kwargs: Unpack[StartMLModelTrainingJobInputRequestTypeDef]
    ) -> StartMLModelTrainingJobOutputTypeDef:
        """
        Creates a new Neptune ML model training job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_ml_model_training_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#start_ml_model_training_job)
        """

    async def start_ml_model_transform_job(
        self, **kwargs: Unpack[StartMLModelTransformJobInputRequestTypeDef]
    ) -> StartMLModelTransformJobOutputTypeDef:
        """
        Creates a new model transform job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata/client/start_ml_model_transform_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/#start_ml_model_transform_job)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptunedata.html#NeptuneData.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptunedata/client/)
        """

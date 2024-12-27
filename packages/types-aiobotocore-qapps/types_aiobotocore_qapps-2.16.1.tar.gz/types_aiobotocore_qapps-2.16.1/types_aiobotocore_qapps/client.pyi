"""
Type annotations for qapps service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qapps.client import QAppsClient

    session = get_session()
    async with session.create_client("qapps") as client:
        client: QAppsClient
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, Mapping, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListLibraryItemsPaginator, ListQAppsPaginator
from .type_defs import (
    AssociateLibraryItemReviewInputRequestTypeDef,
    AssociateQAppWithUserInputRequestTypeDef,
    BatchCreateCategoryInputRequestTypeDef,
    BatchDeleteCategoryInputRequestTypeDef,
    BatchUpdateCategoryInputRequestTypeDef,
    CreateLibraryItemInputRequestTypeDef,
    CreateLibraryItemOutputTypeDef,
    CreatePresignedUrlInputRequestTypeDef,
    CreatePresignedUrlOutputTypeDef,
    CreateQAppInputRequestTypeDef,
    CreateQAppOutputTypeDef,
    DeleteLibraryItemInputRequestTypeDef,
    DeleteQAppInputRequestTypeDef,
    DescribeQAppPermissionsInputRequestTypeDef,
    DescribeQAppPermissionsOutputTypeDef,
    DisassociateLibraryItemReviewInputRequestTypeDef,
    DisassociateQAppFromUserInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportQAppSessionDataInputRequestTypeDef,
    ExportQAppSessionDataOutputTypeDef,
    GetLibraryItemInputRequestTypeDef,
    GetLibraryItemOutputTypeDef,
    GetQAppInputRequestTypeDef,
    GetQAppOutputTypeDef,
    GetQAppSessionInputRequestTypeDef,
    GetQAppSessionMetadataInputRequestTypeDef,
    GetQAppSessionMetadataOutputTypeDef,
    GetQAppSessionOutputTypeDef,
    ImportDocumentInputRequestTypeDef,
    ImportDocumentOutputTypeDef,
    ListCategoriesInputRequestTypeDef,
    ListCategoriesOutputTypeDef,
    ListLibraryItemsInputRequestTypeDef,
    ListLibraryItemsOutputTypeDef,
    ListQAppSessionDataInputRequestTypeDef,
    ListQAppSessionDataOutputTypeDef,
    ListQAppsInputRequestTypeDef,
    ListQAppsOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PredictQAppInputRequestTypeDef,
    PredictQAppOutputTypeDef,
    StartQAppSessionInputRequestTypeDef,
    StartQAppSessionOutputTypeDef,
    StopQAppSessionInputRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateLibraryItemInputRequestTypeDef,
    UpdateLibraryItemMetadataInputRequestTypeDef,
    UpdateLibraryItemOutputTypeDef,
    UpdateQAppInputRequestTypeDef,
    UpdateQAppOutputTypeDef,
    UpdateQAppPermissionsInputRequestTypeDef,
    UpdateQAppPermissionsOutputTypeDef,
    UpdateQAppSessionInputRequestTypeDef,
    UpdateQAppSessionMetadataInputRequestTypeDef,
    UpdateQAppSessionMetadataOutputTypeDef,
    UpdateQAppSessionOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("QAppsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    ContentTooLargeException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class QAppsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps.html#QApps.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QAppsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps.html#QApps.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#generate_presigned_url)
        """

    async def associate_library_item_review(
        self, **kwargs: Unpack[AssociateLibraryItemReviewInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a rating or review for a library item with the user submitting the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/associate_library_item_review.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#associate_library_item_review)
        """

    async def associate_q_app_with_user(
        self, **kwargs: Unpack[AssociateQAppWithUserInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation creates a link between the user's identity calling the operation
        and a specific Q App.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/associate_q_app_with_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#associate_q_app_with_user)
        """

    async def batch_create_category(
        self, **kwargs: Unpack[BatchCreateCategoryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates Categories for the Amazon Q Business application environment instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/batch_create_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#batch_create_category)
        """

    async def batch_delete_category(
        self, **kwargs: Unpack[BatchDeleteCategoryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes Categories for the Amazon Q Business application environment instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/batch_delete_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#batch_delete_category)
        """

    async def batch_update_category(
        self, **kwargs: Unpack[BatchUpdateCategoryInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates Categories for the Amazon Q Business application environment instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/batch_update_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#batch_update_category)
        """

    async def create_library_item(
        self, **kwargs: Unpack[CreateLibraryItemInputRequestTypeDef]
    ) -> CreateLibraryItemOutputTypeDef:
        """
        Creates a new library item for an Amazon Q App, allowing it to be discovered
        and used by other allowed users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/create_library_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#create_library_item)
        """

    async def create_presigned_url(
        self, **kwargs: Unpack[CreatePresignedUrlInputRequestTypeDef]
    ) -> CreatePresignedUrlOutputTypeDef:
        """
        Creates a presigned URL for an S3 POST operation to upload a file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/create_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#create_presigned_url)
        """

    async def create_q_app(
        self, **kwargs: Unpack[CreateQAppInputRequestTypeDef]
    ) -> CreateQAppOutputTypeDef:
        """
        Creates a new Amazon Q App based on the provided definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/create_q_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#create_q_app)
        """

    async def delete_library_item(
        self, **kwargs: Unpack[DeleteLibraryItemInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a library item for an Amazon Q App, removing it from the library so it
        can no longer be discovered or used by other users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/delete_library_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#delete_library_item)
        """

    async def delete_q_app(
        self, **kwargs: Unpack[DeleteQAppInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Q App owned by the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/delete_q_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#delete_q_app)
        """

    async def describe_q_app_permissions(
        self, **kwargs: Unpack[DescribeQAppPermissionsInputRequestTypeDef]
    ) -> DescribeQAppPermissionsOutputTypeDef:
        """
        Describes read permissions for a Amazon Q App in Amazon Q Business application
        environment instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/describe_q_app_permissions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#describe_q_app_permissions)
        """

    async def disassociate_library_item_review(
        self, **kwargs: Unpack[DisassociateLibraryItemReviewInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a rating or review previously submitted by the user for a library item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/disassociate_library_item_review.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#disassociate_library_item_review)
        """

    async def disassociate_q_app_from_user(
        self, **kwargs: Unpack[DisassociateQAppFromUserInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a Q App from a user removing the user's access to run the Q App.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/disassociate_q_app_from_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#disassociate_q_app_from_user)
        """

    async def export_q_app_session_data(
        self, **kwargs: Unpack[ExportQAppSessionDataInputRequestTypeDef]
    ) -> ExportQAppSessionDataOutputTypeDef:
        """
        Exports the collected data of a Q App data collection session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/export_q_app_session_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#export_q_app_session_data)
        """

    async def get_library_item(
        self, **kwargs: Unpack[GetLibraryItemInputRequestTypeDef]
    ) -> GetLibraryItemOutputTypeDef:
        """
        Retrieves details about a library item for an Amazon Q App, including its
        metadata, categories, ratings, and usage statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/get_library_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#get_library_item)
        """

    async def get_q_app(self, **kwargs: Unpack[GetQAppInputRequestTypeDef]) -> GetQAppOutputTypeDef:
        """
        Retrieves the full details of an Q App, including its definition specifying the
        cards and flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/get_q_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#get_q_app)
        """

    async def get_q_app_session(
        self, **kwargs: Unpack[GetQAppSessionInputRequestTypeDef]
    ) -> GetQAppSessionOutputTypeDef:
        """
        Retrieves the current state and results for an active session of an Amazon Q
        App.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/get_q_app_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#get_q_app_session)
        """

    async def get_q_app_session_metadata(
        self, **kwargs: Unpack[GetQAppSessionMetadataInputRequestTypeDef]
    ) -> GetQAppSessionMetadataOutputTypeDef:
        """
        Retrieves the current configuration of a Q App session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/get_q_app_session_metadata.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#get_q_app_session_metadata)
        """

    async def import_document(
        self, **kwargs: Unpack[ImportDocumentInputRequestTypeDef]
    ) -> ImportDocumentOutputTypeDef:
        """
        Uploads a file that can then be used either as a default in a
        <code>FileUploadCard</code> from Q App definition or as a file that is used
        inside a single Q App run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/import_document.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#import_document)
        """

    async def list_categories(
        self, **kwargs: Unpack[ListCategoriesInputRequestTypeDef]
    ) -> ListCategoriesOutputTypeDef:
        """
        Lists the categories of a Amazon Q Business application environment instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/list_categories.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#list_categories)
        """

    async def list_library_items(
        self, **kwargs: Unpack[ListLibraryItemsInputRequestTypeDef]
    ) -> ListLibraryItemsOutputTypeDef:
        """
        Lists the library items for Amazon Q Apps that are published and available for
        users in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/list_library_items.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#list_library_items)
        """

    async def list_q_app_session_data(
        self, **kwargs: Unpack[ListQAppSessionDataInputRequestTypeDef]
    ) -> ListQAppSessionDataOutputTypeDef:
        """
        Lists the collected data of a Q App data collection session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/list_q_app_session_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#list_q_app_session_data)
        """

    async def list_q_apps(
        self, **kwargs: Unpack[ListQAppsInputRequestTypeDef]
    ) -> ListQAppsOutputTypeDef:
        """
        Lists the Amazon Q Apps owned by or associated with the user either because
        they created it or because they used it from the library in the past.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/list_q_apps.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#list_q_apps)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with an Amazon Q Apps resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#list_tags_for_resource)
        """

    async def predict_q_app(
        self, **kwargs: Unpack[PredictQAppInputRequestTypeDef]
    ) -> PredictQAppOutputTypeDef:
        """
        Generates an Amazon Q App definition based on either a conversation or a
        problem statement provided as input.The resulting app definition can be used to
        call <code>CreateQApp</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/predict_q_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#predict_q_app)
        """

    async def start_q_app_session(
        self, **kwargs: Unpack[StartQAppSessionInputRequestTypeDef]
    ) -> StartQAppSessionOutputTypeDef:
        """
        Starts a new session for an Amazon Q App, allowing inputs to be provided and
        the app to be run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/start_q_app_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#start_q_app_session)
        """

    async def stop_q_app_session(
        self, **kwargs: Unpack[StopQAppSessionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops an active session for an Amazon Q App.This deletes all data related to
        the session and makes it invalid for future uses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/stop_q_app_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#stop_q_app_session)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Associates tags with an Amazon Q Apps resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates tags from an Amazon Q Apps resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#untag_resource)
        """

    async def update_library_item(
        self, **kwargs: Unpack[UpdateLibraryItemInputRequestTypeDef]
    ) -> UpdateLibraryItemOutputTypeDef:
        """
        Updates the library item for an Amazon Q App.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/update_library_item.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#update_library_item)
        """

    async def update_library_item_metadata(
        self, **kwargs: Unpack[UpdateLibraryItemMetadataInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the verification status of a library item for an Amazon Q App.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/update_library_item_metadata.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#update_library_item_metadata)
        """

    async def update_q_app(
        self, **kwargs: Unpack[UpdateQAppInputRequestTypeDef]
    ) -> UpdateQAppOutputTypeDef:
        """
        Updates an existing Amazon Q App, allowing modifications to its title,
        description, and definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/update_q_app.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#update_q_app)
        """

    async def update_q_app_permissions(
        self, **kwargs: Unpack[UpdateQAppPermissionsInputRequestTypeDef]
    ) -> UpdateQAppPermissionsOutputTypeDef:
        """
        Updates read permissions for a Amazon Q App in Amazon Q Business application
        environment instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/update_q_app_permissions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#update_q_app_permissions)
        """

    async def update_q_app_session(
        self, **kwargs: Unpack[UpdateQAppSessionInputRequestTypeDef]
    ) -> UpdateQAppSessionOutputTypeDef:
        """
        Updates the session for a given Q App <code>sessionId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/update_q_app_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#update_q_app_session)
        """

    async def update_q_app_session_metadata(
        self, **kwargs: Unpack[UpdateQAppSessionMetadataInputRequestTypeDef]
    ) -> UpdateQAppSessionMetadataOutputTypeDef:
        """
        Updates the configuration metadata of a session for a given Q App
        <code>sessionId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/update_q_app_session_metadata.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#update_q_app_session_metadata)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_library_items"]
    ) -> ListLibraryItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_q_apps"]
    ) -> ListQAppsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps.html#QApps.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qapps.html#QApps.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qapps/client/)
        """

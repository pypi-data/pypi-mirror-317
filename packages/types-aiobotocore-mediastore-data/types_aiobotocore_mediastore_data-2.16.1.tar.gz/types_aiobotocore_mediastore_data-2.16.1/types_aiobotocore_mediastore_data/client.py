"""
Type annotations for mediastore-data service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediastore_data.client import MediaStoreDataClient

    session = get_session()
    async with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient
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

from .paginator import ListItemsPaginator
from .type_defs import (
    DeleteObjectRequestRequestTypeDef,
    DescribeObjectRequestRequestTypeDef,
    DescribeObjectResponseTypeDef,
    GetObjectRequestRequestTypeDef,
    GetObjectResponseTypeDef,
    ListItemsRequestRequestTypeDef,
    ListItemsResponseTypeDef,
    PutObjectRequestRequestTypeDef,
    PutObjectResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("MediaStoreDataClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ContainerNotFoundException: type[BotocoreClientError]
    InternalServerError: type[BotocoreClientError]
    ObjectNotFoundException: type[BotocoreClientError]
    RequestedRangeNotSatisfiableException: type[BotocoreClientError]


class MediaStoreDataClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaStoreDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#generate_presigned_url)
        """

    async def delete_object(
        self, **kwargs: Unpack[DeleteObjectRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an object at the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/delete_object.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#delete_object)
        """

    async def describe_object(
        self, **kwargs: Unpack[DescribeObjectRequestRequestTypeDef]
    ) -> DescribeObjectResponseTypeDef:
        """
        Gets the headers for an object at the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/describe_object.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#describe_object)
        """

    async def get_object(
        self, **kwargs: Unpack[GetObjectRequestRequestTypeDef]
    ) -> GetObjectResponseTypeDef:
        """
        Downloads the object at the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/get_object.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#get_object)
        """

    async def list_items(
        self, **kwargs: Unpack[ListItemsRequestRequestTypeDef]
    ) -> ListItemsResponseTypeDef:
        """
        Provides a list of metadata entries about folders and objects in the specified
        folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/list_items.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#list_items)
        """

    async def put_object(
        self, **kwargs: Unpack[PutObjectRequestRequestTypeDef]
    ) -> PutObjectResponseTypeDef:
        """
        Uploads an object to the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/put_object.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#put_object)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_items"]
    ) -> ListItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)
        """

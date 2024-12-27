"""
Type annotations for connect-contact-lens service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connect_contact_lens.client import ConnectContactLensClient

    session = get_session()
    async with session.create_client("connect-contact-lens") as client:
        client: ConnectContactLensClient
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
    ListRealtimeContactAnalysisSegmentsRequestRequestTypeDef,
    ListRealtimeContactAnalysisSegmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("ConnectContactLensClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServiceException: type[BotocoreClientError]
    InvalidRequestException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]

class ConnectContactLensClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens.html#ConnectContactLens.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectContactLensClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens.html#ConnectContactLens.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/#generate_presigned_url)
        """

    async def list_realtime_contact_analysis_segments(
        self, **kwargs: Unpack[ListRealtimeContactAnalysisSegmentsRequestRequestTypeDef]
    ) -> ListRealtimeContactAnalysisSegmentsResponseTypeDef:
        """
        Provides a list of analysis segments for a real-time analysis session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens/client/list_realtime_contact_analysis_segments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/#list_realtime_contact_analysis_segments)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens.html#ConnectContactLens.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect-contact-lens.html#ConnectContactLens.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect_contact_lens/client/)
        """

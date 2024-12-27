"""
Type annotations for iotsecuretunneling service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_iotsecuretunneling.client import IoTSecureTunnelingClient

    session = Session()
    client: IoTSecureTunnelingClient = session.client("iotsecuretunneling")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CloseTunnelRequestRequestTypeDef,
    DescribeTunnelRequestRequestTypeDef,
    DescribeTunnelResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTunnelsRequestRequestTypeDef,
    ListTunnelsResponseTypeDef,
    OpenTunnelRequestRequestTypeDef,
    OpenTunnelResponseTypeDef,
    RotateTunnelAccessTokenRequestRequestTypeDef,
    RotateTunnelAccessTokenResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("IoTSecureTunnelingClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]


class IoTSecureTunnelingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTSecureTunnelingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#generate_presigned_url)
        """

    def close_tunnel(self, **kwargs: Unpack[CloseTunnelRequestRequestTypeDef]) -> dict[str, Any]:
        """
        Closes a tunnel identified by the unique tunnel id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/close_tunnel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#close_tunnel)
        """

    def describe_tunnel(
        self, **kwargs: Unpack[DescribeTunnelRequestRequestTypeDef]
    ) -> DescribeTunnelResponseTypeDef:
        """
        Gets information about a tunnel identified by the unique tunnel id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/describe_tunnel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#describe_tunnel)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#list_tags_for_resource)
        """

    def list_tunnels(
        self, **kwargs: Unpack[ListTunnelsRequestRequestTypeDef]
    ) -> ListTunnelsResponseTypeDef:
        """
        List all tunnels for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/list_tunnels.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#list_tunnels)
        """

    def open_tunnel(
        self, **kwargs: Unpack[OpenTunnelRequestRequestTypeDef]
    ) -> OpenTunnelResponseTypeDef:
        """
        Creates a new tunnel, and returns two client access tokens for clients to use
        to connect to the IoT Secure Tunneling proxy server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/open_tunnel.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#open_tunnel)
        """

    def rotate_tunnel_access_token(
        self, **kwargs: Unpack[RotateTunnelAccessTokenRequestRequestTypeDef]
    ) -> RotateTunnelAccessTokenResponseTypeDef:
        """
        Revokes the current client access token (CAT) and returns new CAT for clients
        to use when reconnecting to secure tunneling to access the same tunnel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/rotate_tunnel_access_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#rotate_tunnel_access_token)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> dict[str, Any]:
        """
        A resource tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsecuretunneling/client/#untag_resource)
        """

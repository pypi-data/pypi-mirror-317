"""
Type annotations for inspector-scan service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/type_defs/)

Usage::

    ```python
    from mypy_boto3_inspector_scan.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, Mapping

from .literals import OutputFormatType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = ("ResponseMetadataTypeDef", "ScanSbomRequestRequestTypeDef", "ScanSbomResponseTypeDef")

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ScanSbomRequestRequestTypeDef(TypedDict):
    sbom: Mapping[str, Any]
    outputFormat: NotRequired[OutputFormatType]

class ScanSbomResponseTypeDef(TypedDict):
    sbom: dict[str, Any]
    ResponseMetadata: ResponseMetadataTypeDef

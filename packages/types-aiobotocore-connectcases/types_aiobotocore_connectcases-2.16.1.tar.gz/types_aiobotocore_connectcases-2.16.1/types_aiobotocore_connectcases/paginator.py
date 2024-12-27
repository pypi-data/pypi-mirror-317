"""
Type annotations for connectcases service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connectcases.client import ConnectCasesClient
    from types_aiobotocore_connectcases.paginator import (
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = get_session()
    with session.create_client("connectcases") as client:
        client: ConnectCasesClient

        search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
        search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    SearchCasesRequestPaginateTypeDef,
    SearchCasesResponseTypeDef,
    SearchRelatedItemsRequestPaginateTypeDef,
    SearchRelatedItemsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SearchCasesPaginator", "SearchRelatedItemsPaginator")


if TYPE_CHECKING:
    _SearchCasesPaginatorBase = AioPaginator[SearchCasesResponseTypeDef]
else:
    _SearchCasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchCasesPaginator(_SearchCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchCases.html#ConnectCases.Paginator.SearchCases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/paginators/#searchcasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchCasesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchCases.html#ConnectCases.Paginator.SearchCases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/paginators/#searchcasespaginator)
        """


if TYPE_CHECKING:
    _SearchRelatedItemsPaginatorBase = AioPaginator[SearchRelatedItemsResponseTypeDef]
else:
    _SearchRelatedItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchRelatedItemsPaginator(_SearchRelatedItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchRelatedItems.html#ConnectCases.Paginator.SearchRelatedItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/paginators/#searchrelateditemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchRelatedItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectcases/paginator/SearchRelatedItems.html#ConnectCases.Paginator.SearchRelatedItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/paginators/#searchrelateditemspaginator)
        """

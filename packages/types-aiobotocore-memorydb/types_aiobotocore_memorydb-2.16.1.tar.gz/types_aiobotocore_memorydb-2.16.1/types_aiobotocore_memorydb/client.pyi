"""
Type annotations for memorydb service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_memorydb.client import MemoryDBClient

    session = get_session()
    async with session.create_client("memorydb") as client:
        client: MemoryDBClient
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

from .paginator import (
    DescribeACLsPaginator,
    DescribeClustersPaginator,
    DescribeEngineVersionsPaginator,
    DescribeEventsPaginator,
    DescribeMultiRegionClustersPaginator,
    DescribeParameterGroupsPaginator,
    DescribeParametersPaginator,
    DescribeReservedNodesOfferingsPaginator,
    DescribeReservedNodesPaginator,
    DescribeServiceUpdatesPaginator,
    DescribeSnapshotsPaginator,
    DescribeSubnetGroupsPaginator,
    DescribeUsersPaginator,
)
from .type_defs import (
    BatchUpdateClusterRequestRequestTypeDef,
    BatchUpdateClusterResponseTypeDef,
    CopySnapshotRequestRequestTypeDef,
    CopySnapshotResponseTypeDef,
    CreateACLRequestRequestTypeDef,
    CreateACLResponseTypeDef,
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateMultiRegionClusterRequestRequestTypeDef,
    CreateMultiRegionClusterResponseTypeDef,
    CreateParameterGroupRequestRequestTypeDef,
    CreateParameterGroupResponseTypeDef,
    CreateSnapshotRequestRequestTypeDef,
    CreateSnapshotResponseTypeDef,
    CreateSubnetGroupRequestRequestTypeDef,
    CreateSubnetGroupResponseTypeDef,
    CreateUserRequestRequestTypeDef,
    CreateUserResponseTypeDef,
    DeleteACLRequestRequestTypeDef,
    DeleteACLResponseTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteMultiRegionClusterRequestRequestTypeDef,
    DeleteMultiRegionClusterResponseTypeDef,
    DeleteParameterGroupRequestRequestTypeDef,
    DeleteParameterGroupResponseTypeDef,
    DeleteSnapshotRequestRequestTypeDef,
    DeleteSnapshotResponseTypeDef,
    DeleteSubnetGroupRequestRequestTypeDef,
    DeleteSubnetGroupResponseTypeDef,
    DeleteUserRequestRequestTypeDef,
    DeleteUserResponseTypeDef,
    DescribeACLsRequestRequestTypeDef,
    DescribeACLsResponseTypeDef,
    DescribeClustersRequestRequestTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeEngineVersionsRequestRequestTypeDef,
    DescribeEngineVersionsResponseTypeDef,
    DescribeEventsRequestRequestTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeMultiRegionClustersRequestRequestTypeDef,
    DescribeMultiRegionClustersResponseTypeDef,
    DescribeParameterGroupsRequestRequestTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersRequestRequestTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeReservedNodesOfferingsRequestRequestTypeDef,
    DescribeReservedNodesOfferingsResponseTypeDef,
    DescribeReservedNodesRequestRequestTypeDef,
    DescribeReservedNodesResponseTypeDef,
    DescribeServiceUpdatesRequestRequestTypeDef,
    DescribeServiceUpdatesResponseTypeDef,
    DescribeSnapshotsRequestRequestTypeDef,
    DescribeSnapshotsResponseTypeDef,
    DescribeSubnetGroupsRequestRequestTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    DescribeUsersRequestRequestTypeDef,
    DescribeUsersResponseTypeDef,
    FailoverShardRequestRequestTypeDef,
    FailoverShardResponseTypeDef,
    ListAllowedMultiRegionClusterUpdatesRequestRequestTypeDef,
    ListAllowedMultiRegionClusterUpdatesResponseTypeDef,
    ListAllowedNodeTypeUpdatesRequestRequestTypeDef,
    ListAllowedNodeTypeUpdatesResponseTypeDef,
    ListTagsRequestRequestTypeDef,
    ListTagsResponseTypeDef,
    PurchaseReservedNodesOfferingRequestRequestTypeDef,
    PurchaseReservedNodesOfferingResponseTypeDef,
    ResetParameterGroupRequestRequestTypeDef,
    ResetParameterGroupResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TagResourceResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UntagResourceResponseTypeDef,
    UpdateACLRequestRequestTypeDef,
    UpdateACLResponseTypeDef,
    UpdateClusterRequestRequestTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateMultiRegionClusterRequestRequestTypeDef,
    UpdateMultiRegionClusterResponseTypeDef,
    UpdateParameterGroupRequestRequestTypeDef,
    UpdateParameterGroupResponseTypeDef,
    UpdateSubnetGroupRequestRequestTypeDef,
    UpdateSubnetGroupResponseTypeDef,
    UpdateUserRequestRequestTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("MemoryDBClient",)

class Exceptions(BaseClientExceptions):
    ACLAlreadyExistsFault: type[BotocoreClientError]
    ACLNotFoundFault: type[BotocoreClientError]
    ACLQuotaExceededFault: type[BotocoreClientError]
    APICallRateForCustomerExceededFault: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ClusterAlreadyExistsFault: type[BotocoreClientError]
    ClusterNotFoundFault: type[BotocoreClientError]
    ClusterQuotaForCustomerExceededFault: type[BotocoreClientError]
    DefaultUserRequired: type[BotocoreClientError]
    DuplicateUserNameFault: type[BotocoreClientError]
    InsufficientClusterCapacityFault: type[BotocoreClientError]
    InvalidACLStateFault: type[BotocoreClientError]
    InvalidARNFault: type[BotocoreClientError]
    InvalidClusterStateFault: type[BotocoreClientError]
    InvalidCredentialsException: type[BotocoreClientError]
    InvalidKMSKeyFault: type[BotocoreClientError]
    InvalidMultiRegionClusterStateFault: type[BotocoreClientError]
    InvalidNodeStateFault: type[BotocoreClientError]
    InvalidParameterCombinationException: type[BotocoreClientError]
    InvalidParameterGroupStateFault: type[BotocoreClientError]
    InvalidParameterValueException: type[BotocoreClientError]
    InvalidSnapshotStateFault: type[BotocoreClientError]
    InvalidSubnet: type[BotocoreClientError]
    InvalidUserStateFault: type[BotocoreClientError]
    InvalidVPCNetworkStateFault: type[BotocoreClientError]
    MultiRegionClusterAlreadyExistsFault: type[BotocoreClientError]
    MultiRegionClusterNotFoundFault: type[BotocoreClientError]
    MultiRegionParameterGroupNotFoundFault: type[BotocoreClientError]
    NoOperationFault: type[BotocoreClientError]
    NodeQuotaForClusterExceededFault: type[BotocoreClientError]
    NodeQuotaForCustomerExceededFault: type[BotocoreClientError]
    ParameterGroupAlreadyExistsFault: type[BotocoreClientError]
    ParameterGroupNotFoundFault: type[BotocoreClientError]
    ParameterGroupQuotaExceededFault: type[BotocoreClientError]
    ReservedNodeAlreadyExistsFault: type[BotocoreClientError]
    ReservedNodeNotFoundFault: type[BotocoreClientError]
    ReservedNodeQuotaExceededFault: type[BotocoreClientError]
    ReservedNodesOfferingNotFoundFault: type[BotocoreClientError]
    ServiceLinkedRoleNotFoundFault: type[BotocoreClientError]
    ServiceUpdateNotFoundFault: type[BotocoreClientError]
    ShardNotFoundFault: type[BotocoreClientError]
    ShardsPerClusterQuotaExceededFault: type[BotocoreClientError]
    SnapshotAlreadyExistsFault: type[BotocoreClientError]
    SnapshotNotFoundFault: type[BotocoreClientError]
    SnapshotQuotaExceededFault: type[BotocoreClientError]
    SubnetGroupAlreadyExistsFault: type[BotocoreClientError]
    SubnetGroupInUseFault: type[BotocoreClientError]
    SubnetGroupNotFoundFault: type[BotocoreClientError]
    SubnetGroupQuotaExceededFault: type[BotocoreClientError]
    SubnetInUse: type[BotocoreClientError]
    SubnetNotAllowedFault: type[BotocoreClientError]
    SubnetQuotaExceededFault: type[BotocoreClientError]
    TagNotFoundFault: type[BotocoreClientError]
    TagQuotaPerResourceExceeded: type[BotocoreClientError]
    TestFailoverNotAvailableFault: type[BotocoreClientError]
    UserAlreadyExistsFault: type[BotocoreClientError]
    UserNotFoundFault: type[BotocoreClientError]
    UserQuotaExceededFault: type[BotocoreClientError]

class MemoryDBClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MemoryDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#generate_presigned_url)
        """

    async def batch_update_cluster(
        self, **kwargs: Unpack[BatchUpdateClusterRequestRequestTypeDef]
    ) -> BatchUpdateClusterResponseTypeDef:
        """
        Apply the service update to a list of clusters supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/batch_update_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#batch_update_cluster)
        """

    async def copy_snapshot(
        self, **kwargs: Unpack[CopySnapshotRequestRequestTypeDef]
    ) -> CopySnapshotResponseTypeDef:
        """
        Makes a copy of an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/copy_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#copy_snapshot)
        """

    async def create_acl(
        self, **kwargs: Unpack[CreateACLRequestRequestTypeDef]
    ) -> CreateACLResponseTypeDef:
        """
        Creates an Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_acl)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_cluster)
        """

    async def create_multi_region_cluster(
        self, **kwargs: Unpack[CreateMultiRegionClusterRequestRequestTypeDef]
    ) -> CreateMultiRegionClusterResponseTypeDef:
        """
        Creates a new multi-Region cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_multi_region_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_multi_region_cluster)
        """

    async def create_parameter_group(
        self, **kwargs: Unpack[CreateParameterGroupRequestRequestTypeDef]
    ) -> CreateParameterGroupResponseTypeDef:
        """
        Creates a new MemoryDB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_parameter_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_parameter_group)
        """

    async def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestRequestTypeDef]
    ) -> CreateSnapshotResponseTypeDef:
        """
        Creates a copy of an entire cluster at a specific moment in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_snapshot)
        """

    async def create_subnet_group(
        self, **kwargs: Unpack[CreateSubnetGroupRequestRequestTypeDef]
    ) -> CreateSubnetGroupResponseTypeDef:
        """
        Creates a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_subnet_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_subnet_group)
        """

    async def create_user(
        self, **kwargs: Unpack[CreateUserRequestRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a MemoryDB user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/create_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_user)
        """

    async def delete_acl(
        self, **kwargs: Unpack[DeleteACLRequestRequestTypeDef]
    ) -> DeleteACLResponseTypeDef:
        """
        Deletes an Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_acl)
        """

    async def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_cluster)
        """

    async def delete_multi_region_cluster(
        self, **kwargs: Unpack[DeleteMultiRegionClusterRequestRequestTypeDef]
    ) -> DeleteMultiRegionClusterResponseTypeDef:
        """
        Deletes an existing multi-Region cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_multi_region_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_multi_region_cluster)
        """

    async def delete_parameter_group(
        self, **kwargs: Unpack[DeleteParameterGroupRequestRequestTypeDef]
    ) -> DeleteParameterGroupResponseTypeDef:
        """
        Deletes the specified parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_parameter_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_parameter_group)
        """

    async def delete_snapshot(
        self, **kwargs: Unpack[DeleteSnapshotRequestRequestTypeDef]
    ) -> DeleteSnapshotResponseTypeDef:
        """
        Deletes an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_snapshot)
        """

    async def delete_subnet_group(
        self, **kwargs: Unpack[DeleteSubnetGroupRequestRequestTypeDef]
    ) -> DeleteSubnetGroupResponseTypeDef:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_subnet_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_subnet_group)
        """

    async def delete_user(
        self, **kwargs: Unpack[DeleteUserRequestRequestTypeDef]
    ) -> DeleteUserResponseTypeDef:
        """
        Deletes a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/delete_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_user)
        """

    async def describe_acls(
        self, **kwargs: Unpack[DescribeACLsRequestRequestTypeDef]
    ) -> DescribeACLsResponseTypeDef:
        """
        Returns a list of ACLs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_acls.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_acls)
        """

    async def describe_clusters(
        self, **kwargs: Unpack[DescribeClustersRequestRequestTypeDef]
    ) -> DescribeClustersResponseTypeDef:
        """
        Returns information about all provisioned clusters if no cluster identifier is
        specified, or about a specific cluster if a cluster name is supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_clusters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_clusters)
        """

    async def describe_engine_versions(
        self, **kwargs: Unpack[DescribeEngineVersionsRequestRequestTypeDef]
    ) -> DescribeEngineVersionsResponseTypeDef:
        """
        Returns a list of the available Redis OSS engine versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_engine_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_engine_versions)
        """

    async def describe_events(
        self, **kwargs: Unpack[DescribeEventsRequestRequestTypeDef]
    ) -> DescribeEventsResponseTypeDef:
        """
        Returns events related to clusters, security groups, and parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_events)
        """

    async def describe_multi_region_clusters(
        self, **kwargs: Unpack[DescribeMultiRegionClustersRequestRequestTypeDef]
    ) -> DescribeMultiRegionClustersResponseTypeDef:
        """
        Returns details about one or more multi-Region clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_multi_region_clusters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_multi_region_clusters)
        """

    async def describe_parameter_groups(
        self, **kwargs: Unpack[DescribeParameterGroupsRequestRequestTypeDef]
    ) -> DescribeParameterGroupsResponseTypeDef:
        """
        Returns a list of parameter group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_parameter_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_parameter_groups)
        """

    async def describe_parameters(
        self, **kwargs: Unpack[DescribeParametersRequestRequestTypeDef]
    ) -> DescribeParametersResponseTypeDef:
        """
        Returns the detailed parameter list for a particular parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_parameters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_parameters)
        """

    async def describe_reserved_nodes(
        self, **kwargs: Unpack[DescribeReservedNodesRequestRequestTypeDef]
    ) -> DescribeReservedNodesResponseTypeDef:
        """
        Returns information about reserved nodes for this account, or about a specified
        reserved node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_reserved_nodes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_reserved_nodes)
        """

    async def describe_reserved_nodes_offerings(
        self, **kwargs: Unpack[DescribeReservedNodesOfferingsRequestRequestTypeDef]
    ) -> DescribeReservedNodesOfferingsResponseTypeDef:
        """
        Lists available reserved node offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_reserved_nodes_offerings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_reserved_nodes_offerings)
        """

    async def describe_service_updates(
        self, **kwargs: Unpack[DescribeServiceUpdatesRequestRequestTypeDef]
    ) -> DescribeServiceUpdatesResponseTypeDef:
        """
        Returns details of the service updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_service_updates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_service_updates)
        """

    async def describe_snapshots(
        self, **kwargs: Unpack[DescribeSnapshotsRequestRequestTypeDef]
    ) -> DescribeSnapshotsResponseTypeDef:
        """
        Returns information about cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_snapshots.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_snapshots)
        """

    async def describe_subnet_groups(
        self, **kwargs: Unpack[DescribeSubnetGroupsRequestRequestTypeDef]
    ) -> DescribeSubnetGroupsResponseTypeDef:
        """
        Returns a list of subnet group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_subnet_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_subnet_groups)
        """

    async def describe_users(
        self, **kwargs: Unpack[DescribeUsersRequestRequestTypeDef]
    ) -> DescribeUsersResponseTypeDef:
        """
        Returns a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/describe_users.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_users)
        """

    async def failover_shard(
        self, **kwargs: Unpack[FailoverShardRequestRequestTypeDef]
    ) -> FailoverShardResponseTypeDef:
        """
        Used to failover a shard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/failover_shard.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#failover_shard)
        """

    async def list_allowed_multi_region_cluster_updates(
        self, **kwargs: Unpack[ListAllowedMultiRegionClusterUpdatesRequestRequestTypeDef]
    ) -> ListAllowedMultiRegionClusterUpdatesResponseTypeDef:
        """
        Lists the allowed updates for a multi-Region cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/list_allowed_multi_region_cluster_updates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#list_allowed_multi_region_cluster_updates)
        """

    async def list_allowed_node_type_updates(
        self, **kwargs: Unpack[ListAllowedNodeTypeUpdatesRequestRequestTypeDef]
    ) -> ListAllowedNodeTypeUpdatesResponseTypeDef:
        """
        Lists all available node types that you can scale to from your cluster's
        current node type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/list_allowed_node_type_updates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#list_allowed_node_type_updates)
        """

    async def list_tags(
        self, **kwargs: Unpack[ListTagsRequestRequestTypeDef]
    ) -> ListTagsResponseTypeDef:
        """
        Lists all tags currently on a named resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/list_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#list_tags)
        """

    async def purchase_reserved_nodes_offering(
        self, **kwargs: Unpack[PurchaseReservedNodesOfferingRequestRequestTypeDef]
    ) -> PurchaseReservedNodesOfferingResponseTypeDef:
        """
        Allows you to purchase a reserved node offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/purchase_reserved_nodes_offering.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#purchase_reserved_nodes_offering)
        """

    async def reset_parameter_group(
        self, **kwargs: Unpack[ResetParameterGroupRequestRequestTypeDef]
    ) -> ResetParameterGroupResponseTypeDef:
        """
        Modifies the parameters of a parameter group to the engine or system default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/reset_parameter_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#reset_parameter_group)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> TagResourceResponseTypeDef:
        """
        A tag is a key-value pair where the key and value are case-sensitive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> UntagResourceResponseTypeDef:
        """
        Use this operation to remove tags on a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#untag_resource)
        """

    async def update_acl(
        self, **kwargs: Unpack[UpdateACLRequestRequestTypeDef]
    ) -> UpdateACLResponseTypeDef:
        """
        Changes the list of users that belong to the Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/update_acl.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_acl)
        """

    async def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestRequestTypeDef]
    ) -> UpdateClusterResponseTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/update_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_cluster)
        """

    async def update_multi_region_cluster(
        self, **kwargs: Unpack[UpdateMultiRegionClusterRequestRequestTypeDef]
    ) -> UpdateMultiRegionClusterResponseTypeDef:
        """
        Updates the configuration of an existing multi-Region cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/update_multi_region_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_multi_region_cluster)
        """

    async def update_parameter_group(
        self, **kwargs: Unpack[UpdateParameterGroupRequestRequestTypeDef]
    ) -> UpdateParameterGroupResponseTypeDef:
        """
        Updates the parameters of a parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/update_parameter_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_parameter_group)
        """

    async def update_subnet_group(
        self, **kwargs: Unpack[UpdateSubnetGroupRequestRequestTypeDef]
    ) -> UpdateSubnetGroupResponseTypeDef:
        """
        Updates a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/update_subnet_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_subnet_group)
        """

    async def update_user(
        self, **kwargs: Unpack[UpdateUserRequestRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Changes user password(s) and/or access string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/update_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_user)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_acls"]
    ) -> DescribeACLsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_clusters"]
    ) -> DescribeClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_engine_versions"]
    ) -> DescribeEngineVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_events"]
    ) -> DescribeEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_multi_region_clusters"]
    ) -> DescribeMultiRegionClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_parameter_groups"]
    ) -> DescribeParameterGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_parameters"]
    ) -> DescribeParametersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_reserved_nodes_offerings"]
    ) -> DescribeReservedNodesOfferingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_reserved_nodes"]
    ) -> DescribeReservedNodesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_service_updates"]
    ) -> DescribeServiceUpdatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_snapshots"]
    ) -> DescribeSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_subnet_groups"]
    ) -> DescribeSubnetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_users"]
    ) -> DescribeUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)
        """

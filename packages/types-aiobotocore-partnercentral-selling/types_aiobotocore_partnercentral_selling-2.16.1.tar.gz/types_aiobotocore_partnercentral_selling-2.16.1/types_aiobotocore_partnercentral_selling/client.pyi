"""
Type annotations for partnercentral-selling service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_partnercentral_selling.client import PartnerCentralSellingAPIClient

    session = get_session()
    async with session.create_client("partnercentral-selling") as client:
        client: PartnerCentralSellingAPIClient
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
    ListEngagementByAcceptingInvitationTasksPaginator,
    ListEngagementFromOpportunityTasksPaginator,
    ListEngagementInvitationsPaginator,
    ListEngagementMembersPaginator,
    ListEngagementResourceAssociationsPaginator,
    ListEngagementsPaginator,
    ListOpportunitiesPaginator,
    ListResourceSnapshotJobsPaginator,
    ListResourceSnapshotsPaginator,
    ListSolutionsPaginator,
)
from .type_defs import (
    AcceptEngagementInvitationRequestRequestTypeDef,
    AssignOpportunityRequestRequestTypeDef,
    AssociateOpportunityRequestRequestTypeDef,
    CreateEngagementInvitationRequestRequestTypeDef,
    CreateEngagementInvitationResponseTypeDef,
    CreateEngagementRequestRequestTypeDef,
    CreateEngagementResponseTypeDef,
    CreateOpportunityRequestRequestTypeDef,
    CreateOpportunityResponseTypeDef,
    CreateResourceSnapshotJobRequestRequestTypeDef,
    CreateResourceSnapshotJobResponseTypeDef,
    CreateResourceSnapshotRequestRequestTypeDef,
    CreateResourceSnapshotResponseTypeDef,
    DeleteResourceSnapshotJobRequestRequestTypeDef,
    DisassociateOpportunityRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAwsOpportunitySummaryRequestRequestTypeDef,
    GetAwsOpportunitySummaryResponseTypeDef,
    GetEngagementInvitationRequestRequestTypeDef,
    GetEngagementInvitationResponseTypeDef,
    GetEngagementRequestRequestTypeDef,
    GetEngagementResponseTypeDef,
    GetOpportunityRequestRequestTypeDef,
    GetOpportunityResponseTypeDef,
    GetResourceSnapshotJobRequestRequestTypeDef,
    GetResourceSnapshotJobResponseTypeDef,
    GetResourceSnapshotRequestRequestTypeDef,
    GetResourceSnapshotResponseTypeDef,
    GetSellingSystemSettingsRequestRequestTypeDef,
    GetSellingSystemSettingsResponseTypeDef,
    ListEngagementByAcceptingInvitationTasksRequestRequestTypeDef,
    ListEngagementByAcceptingInvitationTasksResponseTypeDef,
    ListEngagementFromOpportunityTasksRequestRequestTypeDef,
    ListEngagementFromOpportunityTasksResponseTypeDef,
    ListEngagementInvitationsRequestRequestTypeDef,
    ListEngagementInvitationsResponseTypeDef,
    ListEngagementMembersRequestRequestTypeDef,
    ListEngagementMembersResponseTypeDef,
    ListEngagementResourceAssociationsRequestRequestTypeDef,
    ListEngagementResourceAssociationsResponseTypeDef,
    ListEngagementsRequestRequestTypeDef,
    ListEngagementsResponseTypeDef,
    ListOpportunitiesRequestRequestTypeDef,
    ListOpportunitiesResponseTypeDef,
    ListResourceSnapshotJobsRequestRequestTypeDef,
    ListResourceSnapshotJobsResponseTypeDef,
    ListResourceSnapshotsRequestRequestTypeDef,
    ListResourceSnapshotsResponseTypeDef,
    ListSolutionsRequestRequestTypeDef,
    ListSolutionsResponseTypeDef,
    PutSellingSystemSettingsRequestRequestTypeDef,
    PutSellingSystemSettingsResponseTypeDef,
    RejectEngagementInvitationRequestRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef,
    StartEngagementByAcceptingInvitationTaskResponseTypeDef,
    StartEngagementFromOpportunityTaskRequestRequestTypeDef,
    StartEngagementFromOpportunityTaskResponseTypeDef,
    StartResourceSnapshotJobRequestRequestTypeDef,
    StopResourceSnapshotJobRequestRequestTypeDef,
    SubmitOpportunityRequestRequestTypeDef,
    UpdateOpportunityRequestRequestTypeDef,
    UpdateOpportunityResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("PartnerCentralSellingAPIClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class PartnerCentralSellingAPIClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PartnerCentralSellingAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#generate_presigned_url)
        """

    async def accept_engagement_invitation(
        self, **kwargs: Unpack[AcceptEngagementInvitationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use the <code>AcceptEngagementInvitation</code> action to accept an engagement
        invitation shared by AWS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/accept_engagement_invitation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#accept_engagement_invitation)
        """

    async def assign_opportunity(
        self, **kwargs: Unpack[AssignOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to reassign an existing <code>Opportunity</code> to another user
        within your Partner Central account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/assign_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#assign_opportunity)
        """

    async def associate_opportunity(
        self, **kwargs: Unpack[AssociateOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to create a formal association between an <code>Opportunity</code>
        and various related entities, enriching the context and details of the
        opportunity for better collaboration and decision making.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/associate_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#associate_opportunity)
        """

    async def create_engagement(
        self, **kwargs: Unpack[CreateEngagementRequestRequestTypeDef]
    ) -> CreateEngagementResponseTypeDef:
        """
        The <code>CreateEngagement</code> action allows you to create an
        <code>Engagement</code>, which serves as a collaborative space between
        different parties such as AWS Partners and AWS Sellers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#create_engagement)
        """

    async def create_engagement_invitation(
        self, **kwargs: Unpack[CreateEngagementInvitationRequestRequestTypeDef]
    ) -> CreateEngagementInvitationResponseTypeDef:
        """
        This action creates an invitation from a sender to a single receiver to join an
        engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_engagement_invitation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#create_engagement_invitation)
        """

    async def create_opportunity(
        self, **kwargs: Unpack[CreateOpportunityRequestRequestTypeDef]
    ) -> CreateOpportunityResponseTypeDef:
        """
        Creates an <code>Opportunity</code> record in Partner Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#create_opportunity)
        """

    async def create_resource_snapshot(
        self, **kwargs: Unpack[CreateResourceSnapshotRequestRequestTypeDef]
    ) -> CreateResourceSnapshotResponseTypeDef:
        """
        This action allows you to create an immutable snapshot of a specific resource,
        such as an opportunity, within the context of an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_resource_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#create_resource_snapshot)
        """

    async def create_resource_snapshot_job(
        self, **kwargs: Unpack[CreateResourceSnapshotJobRequestRequestTypeDef]
    ) -> CreateResourceSnapshotJobResponseTypeDef:
        """
        Use this action to create a job to generate a snapshot of the specified
        resource within an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/create_resource_snapshot_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#create_resource_snapshot_job)
        """

    async def delete_resource_snapshot_job(
        self, **kwargs: Unpack[DeleteResourceSnapshotJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this action to deletes a previously created resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/delete_resource_snapshot_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#delete_resource_snapshot_job)
        """

    async def disassociate_opportunity(
        self, **kwargs: Unpack[DisassociateOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Allows you to remove an existing association between an
        <code>Opportunity</code> and related entities, such as a Partner Solution,
        Amazon Web Services product, or an Amazon Web Services Marketplace offer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/disassociate_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#disassociate_opportunity)
        """

    async def get_aws_opportunity_summary(
        self, **kwargs: Unpack[GetAwsOpportunitySummaryRequestRequestTypeDef]
    ) -> GetAwsOpportunitySummaryResponseTypeDef:
        """
        Retrieves a summary of an AWS Opportunity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_aws_opportunity_summary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_aws_opportunity_summary)
        """

    async def get_engagement(
        self, **kwargs: Unpack[GetEngagementRequestRequestTypeDef]
    ) -> GetEngagementResponseTypeDef:
        """
        Use this action to retrieve the engagement record for a given
        <code>EngagementIdentifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_engagement.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_engagement)
        """

    async def get_engagement_invitation(
        self, **kwargs: Unpack[GetEngagementInvitationRequestRequestTypeDef]
    ) -> GetEngagementInvitationResponseTypeDef:
        """
        Retrieves the details of an engagement invitation shared by AWS with a partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_engagement_invitation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_engagement_invitation)
        """

    async def get_opportunity(
        self, **kwargs: Unpack[GetOpportunityRequestRequestTypeDef]
    ) -> GetOpportunityResponseTypeDef:
        """
        Fetches the <code>Opportunity</code> record from Partner Central by a given
        <code>Identifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_opportunity)
        """

    async def get_resource_snapshot(
        self, **kwargs: Unpack[GetResourceSnapshotRequestRequestTypeDef]
    ) -> GetResourceSnapshotResponseTypeDef:
        """
        Use this action to retrieve a specific snapshot record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_resource_snapshot.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_resource_snapshot)
        """

    async def get_resource_snapshot_job(
        self, **kwargs: Unpack[GetResourceSnapshotJobRequestRequestTypeDef]
    ) -> GetResourceSnapshotJobResponseTypeDef:
        """
        Use this action to retrieves information about a specific resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_resource_snapshot_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_resource_snapshot_job)
        """

    async def get_selling_system_settings(
        self, **kwargs: Unpack[GetSellingSystemSettingsRequestRequestTypeDef]
    ) -> GetSellingSystemSettingsResponseTypeDef:
        """
        Retrieves the currently set system settings, which include the IAM Role used
        for resource snapshot jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_selling_system_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_selling_system_settings)
        """

    async def list_engagement_by_accepting_invitation_tasks(
        self, **kwargs: Unpack[ListEngagementByAcceptingInvitationTasksRequestRequestTypeDef]
    ) -> ListEngagementByAcceptingInvitationTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed
        StartEngagementByAcceptingInvitationTask tasks that were initiated by the
        caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_by_accepting_invitation_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_engagement_by_accepting_invitation_tasks)
        """

    async def list_engagement_from_opportunity_tasks(
        self, **kwargs: Unpack[ListEngagementFromOpportunityTasksRequestRequestTypeDef]
    ) -> ListEngagementFromOpportunityTasksResponseTypeDef:
        """
        Lists all in-progress, completed, or failed
        <code>EngagementFromOpportunity</code> tasks that were initiated by the
        caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_from_opportunity_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_engagement_from_opportunity_tasks)
        """

    async def list_engagement_invitations(
        self, **kwargs: Unpack[ListEngagementInvitationsRequestRequestTypeDef]
    ) -> ListEngagementInvitationsResponseTypeDef:
        """
        Retrieves a list of engagement invitations sent to the partner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_invitations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_engagement_invitations)
        """

    async def list_engagement_members(
        self, **kwargs: Unpack[ListEngagementMembersRequestRequestTypeDef]
    ) -> ListEngagementMembersResponseTypeDef:
        """
        Retrieves the details of member partners in an engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_members.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_engagement_members)
        """

    async def list_engagement_resource_associations(
        self, **kwargs: Unpack[ListEngagementResourceAssociationsRequestRequestTypeDef]
    ) -> ListEngagementResourceAssociationsResponseTypeDef:
        """
        Lists the associations between resources and engagements where the caller is a
        member and has at least one snapshot in the engagement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagement_resource_associations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_engagement_resource_associations)
        """

    async def list_engagements(
        self, **kwargs: Unpack[ListEngagementsRequestRequestTypeDef]
    ) -> ListEngagementsResponseTypeDef:
        """
        This action allows users to retrieve a list of engagement records from Partner
        Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_engagements.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_engagements)
        """

    async def list_opportunities(
        self, **kwargs: Unpack[ListOpportunitiesRequestRequestTypeDef]
    ) -> ListOpportunitiesResponseTypeDef:
        """
        This request accepts a list of filters that retrieve opportunity subsets as
        well as sort options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_opportunities.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_opportunities)
        """

    async def list_resource_snapshot_jobs(
        self, **kwargs: Unpack[ListResourceSnapshotJobsRequestRequestTypeDef]
    ) -> ListResourceSnapshotJobsResponseTypeDef:
        """
        Lists resource snapshot jobs owned by the customer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_resource_snapshot_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_resource_snapshot_jobs)
        """

    async def list_resource_snapshots(
        self, **kwargs: Unpack[ListResourceSnapshotsRequestRequestTypeDef]
    ) -> ListResourceSnapshotsResponseTypeDef:
        """
        Retrieves a list of resource view snapshots based on specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_resource_snapshots.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_resource_snapshots)
        """

    async def list_solutions(
        self, **kwargs: Unpack[ListSolutionsRequestRequestTypeDef]
    ) -> ListSolutionsResponseTypeDef:
        """
        Retrieves a list of Partner Solutions that the partner registered on Partner
        Central.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/list_solutions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#list_solutions)
        """

    async def put_selling_system_settings(
        self, **kwargs: Unpack[PutSellingSystemSettingsRequestRequestTypeDef]
    ) -> PutSellingSystemSettingsResponseTypeDef:
        """
        Updates the currently set system settings, which include the IAM Role used for
        resource snapshot jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/put_selling_system_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#put_selling_system_settings)
        """

    async def reject_engagement_invitation(
        self, **kwargs: Unpack[RejectEngagementInvitationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        This action rejects an <code>EngagementInvitation</code> that AWS shared.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/reject_engagement_invitation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#reject_engagement_invitation)
        """

    async def start_engagement_by_accepting_invitation_task(
        self, **kwargs: Unpack[StartEngagementByAcceptingInvitationTaskRequestRequestTypeDef]
    ) -> StartEngagementByAcceptingInvitationTaskResponseTypeDef:
        """
        This action starts the engagement by accepting an
        <code>EngagementInvitation</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_engagement_by_accepting_invitation_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#start_engagement_by_accepting_invitation_task)
        """

    async def start_engagement_from_opportunity_task(
        self, **kwargs: Unpack[StartEngagementFromOpportunityTaskRequestRequestTypeDef]
    ) -> StartEngagementFromOpportunityTaskResponseTypeDef:
        """
        This action initiates the engagement process from an existing opportunity by
        accepting the engagement invitation and creating a corresponding opportunity in
        the partner's system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_engagement_from_opportunity_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#start_engagement_from_opportunity_task)
        """

    async def start_resource_snapshot_job(
        self, **kwargs: Unpack[StartResourceSnapshotJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a resource snapshot job that has been previously created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/start_resource_snapshot_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#start_resource_snapshot_job)
        """

    async def stop_resource_snapshot_job(
        self, **kwargs: Unpack[StopResourceSnapshotJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a resource snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/stop_resource_snapshot_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#stop_resource_snapshot_job)
        """

    async def submit_opportunity(
        self, **kwargs: Unpack[SubmitOpportunityRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Use this action to submit an opportunity that was previously created by partner
        for AWS review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/submit_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#submit_opportunity)
        """

    async def update_opportunity(
        self, **kwargs: Unpack[UpdateOpportunityRequestRequestTypeDef]
    ) -> UpdateOpportunityResponseTypeDef:
        """
        Updates the <code>Opportunity</code> record identified by a given
        <code>Identifier</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/update_opportunity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#update_opportunity)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_by_accepting_invitation_tasks"]
    ) -> ListEngagementByAcceptingInvitationTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_from_opportunity_tasks"]
    ) -> ListEngagementFromOpportunityTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_invitations"]
    ) -> ListEngagementInvitationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_members"]
    ) -> ListEngagementMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagement_resource_associations"]
    ) -> ListEngagementResourceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_engagements"]
    ) -> ListEngagementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_opportunities"]
    ) -> ListOpportunitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_snapshot_jobs"]
    ) -> ListResourceSnapshotJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_snapshots"]
    ) -> ListResourceSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_solutions"]
    ) -> ListSolutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-selling.html#PartnerCentralSellingAPI.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_selling/client/)
        """

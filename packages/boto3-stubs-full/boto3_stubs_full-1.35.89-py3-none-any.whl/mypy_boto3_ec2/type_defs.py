"""
Type annotations for ec2 service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ec2/type_defs/)

Usage::

    ```python
    from mypy_boto3_ec2.type_defs import AcceleratorCountRequestTypeDef

    data: AcceleratorCountRequestTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AcceleratorManufacturerType,
    AcceleratorNameType,
    AcceleratorTypeType,
    AccountAttributeNameType,
    ActivityStatusType,
    AddressFamilyType,
    AddressTransferStatusType,
    AffinityType,
    AllocationStateType,
    AllocationStrategyType,
    AllowedImagesSettingsEnabledStateType,
    AllowsMultipleInstanceTypesType,
    AmdSevSnpSpecificationType,
    AnalysisStatusType,
    ApplianceModeSupportValueType,
    ArchitectureTypeType,
    ArchitectureValuesType,
    AsnAssociationStateType,
    AsnStateType,
    AssociationStatusCodeType,
    AttachmentStatusType,
    AutoAcceptSharedAssociationsValueType,
    AutoAcceptSharedAttachmentsValueType,
    AutoPlacementType,
    AvailabilityZoneOptInStatusType,
    AvailabilityZoneStateType,
    BandwidthWeightingTypeType,
    BareMetalType,
    BatchStateType,
    BgpStatusType,
    BlockPublicAccessModeType,
    BootModeTypeType,
    BootModeValuesType,
    BundleTaskStateType,
    BurstablePerformanceType,
    ByoipCidrStateType,
    CallerRoleType,
    CancelBatchErrorCodeType,
    CancelSpotInstanceRequestStateType,
    CapacityBlockExtensionStatusType,
    CapacityReservationBillingRequestStatusType,
    CapacityReservationDeliveryPreferenceType,
    CapacityReservationFleetStateType,
    CapacityReservationInstancePlatformType,
    CapacityReservationPreferenceType,
    CapacityReservationStateType,
    CapacityReservationTenancyType,
    CapacityReservationTypeType,
    CarrierGatewayStateType,
    ClientCertificateRevocationListStatusCodeType,
    ClientVpnAuthenticationTypeType,
    ClientVpnAuthorizationRuleStatusCodeType,
    ClientVpnConnectionStatusCodeType,
    ClientVpnEndpointAttributeStatusCodeType,
    ClientVpnEndpointStatusCodeType,
    ClientVpnRouteStatusCodeType,
    ConnectionNotificationStateType,
    ConnectivityTypeType,
    ConversionTaskStateType,
    CpuManufacturerType,
    DatafeedSubscriptionStateType,
    DefaultInstanceMetadataEndpointStateType,
    DefaultInstanceMetadataTagsStateType,
    DefaultRouteTableAssociationValueType,
    DefaultRouteTablePropagationValueType,
    DefaultTargetCapacityTypeType,
    DeleteFleetErrorCodeType,
    DeleteQueuedReservedInstancesErrorCodeType,
    DestinationFileFormatType,
    DeviceTrustProviderTypeType,
    DeviceTypeType,
    DiskImageFormatType,
    DiskTypeType,
    DnsNameStateType,
    DnsRecordIpTypeType,
    DnsSupportValueType,
    DomainTypeType,
    DynamicRoutingValueType,
    EbsEncryptionSupportType,
    EbsNvmeSupportType,
    EbsOptimizedSupportType,
    Ec2InstanceConnectEndpointStateType,
    EkPubKeyFormatType,
    EkPubKeyTypeType,
    ElasticGpuStatusType,
    EnaSupportType,
    EndDateTypeType,
    EphemeralNvmeSupportType,
    EventCodeType,
    EventTypeType,
    ExcessCapacityTerminationPolicyType,
    ExportEnvironmentType,
    ExportTaskStateType,
    FastLaunchStateCodeType,
    FastSnapshotRestoreStateCodeType,
    FindingsFoundType,
    FleetActivityStatusType,
    FleetEventTypeType,
    FleetExcessCapacityTerminationPolicyType,
    FleetOnDemandAllocationStrategyType,
    FleetReplacementStrategyType,
    FleetStateCodeType,
    FleetTypeType,
    FlowLogsResourceTypeType,
    FpgaImageAttributeNameType,
    FpgaImageStateCodeType,
    GatewayAssociationStateType,
    HostMaintenanceType,
    HostnameTypeType,
    HostRecoveryType,
    HostTenancyType,
    HttpTokensStateType,
    HypervisorTypeType,
    IamInstanceProfileAssociationStateType,
    Igmpv2SupportValueType,
    ImageAttributeNameType,
    ImageStateType,
    ImageTypeValuesType,
    InstanceAttributeNameType,
    InstanceAutoRecoveryStateType,
    InstanceBandwidthWeightingType,
    InstanceBootModeValuesType,
    InstanceEventWindowStateType,
    InstanceGenerationType,
    InstanceHealthStatusType,
    InstanceInterruptionBehaviorType,
    InstanceLifecycleType,
    InstanceLifecycleTypeType,
    InstanceMatchCriteriaType,
    InstanceMetadataEndpointStateType,
    InstanceMetadataOptionsStateType,
    InstanceMetadataProtocolStateType,
    InstanceMetadataTagsStateType,
    InstanceStateNameType,
    InstanceStorageEncryptionSupportType,
    InstanceTypeHypervisorType,
    InstanceTypeType,
    InterfacePermissionTypeType,
    InterfaceProtocolTypeType,
    InternetGatewayBlockModeType,
    InternetGatewayExclusionModeType,
    IpAddressTypeType,
    IpamAddressHistoryResourceTypeType,
    IpamAssociatedResourceDiscoveryStatusType,
    IpamComplianceStatusType,
    IpamDiscoveryFailureCodeType,
    IpamExternalResourceVerificationTokenStateType,
    IpamManagementStateType,
    IpamNetworkInterfaceAttachmentStatusType,
    IpamOverlapStatusType,
    IpamPoolAllocationResourceTypeType,
    IpamPoolCidrFailureCodeType,
    IpamPoolCidrStateType,
    IpamPoolPublicIpSourceType,
    IpamPoolStateType,
    IpamPublicAddressAssociationStatusType,
    IpamPublicAddressAwsServiceType,
    IpamPublicAddressTypeType,
    IpamResourceCidrIpSourceType,
    IpamResourceDiscoveryAssociationStateType,
    IpamResourceDiscoveryStateType,
    IpamResourceTypeType,
    IpamScopeStateType,
    IpamScopeTypeType,
    IpamStateType,
    IpamTierType,
    IpSourceType,
    Ipv6AddressAttributeType,
    Ipv6SupportValueType,
    KeyFormatType,
    KeyTypeType,
    LaunchTemplateAutoRecoveryStateType,
    LaunchTemplateErrorCodeType,
    LaunchTemplateHttpTokensStateType,
    LaunchTemplateInstanceMetadataEndpointStateType,
    LaunchTemplateInstanceMetadataOptionsStateType,
    LaunchTemplateInstanceMetadataProtocolIpv6Type,
    LaunchTemplateInstanceMetadataTagsStateType,
    ListingStateType,
    ListingStatusType,
    LocalGatewayRouteStateType,
    LocalGatewayRouteTableModeType,
    LocalGatewayRouteTypeType,
    LocalStorageType,
    LocalStorageTypeType,
    LocationTypeType,
    LockModeType,
    LockStateType,
    LogDestinationTypeType,
    ManagedByType,
    MarketTypeType,
    MembershipTypeType,
    MetadataDefaultHttpTokensStateType,
    ModifyAvailabilityZoneOptInStatusType,
    MonitoringStateType,
    MoveStatusType,
    MulticastSupportValueType,
    NatGatewayAddressStatusType,
    NatGatewayStateType,
    NetworkInterfaceAttributeType,
    NetworkInterfaceCreationTypeType,
    NetworkInterfacePermissionStateCodeType,
    NetworkInterfaceStatusType,
    NetworkInterfaceTypeType,
    NitroEnclavesSupportType,
    NitroTpmSupportType,
    OfferingClassTypeType,
    OfferingTypeValuesType,
    OnDemandAllocationStrategyType,
    OperationTypeType,
    PartitionLoadFrequencyType,
    PaymentOptionType,
    PeriodTypeType,
    PhcSupportType,
    PlacementGroupStateType,
    PlacementGroupStrategyType,
    PlacementStrategyType,
    PrefixListStateType,
    PrincipalTypeType,
    ProductCodeValuesType,
    ProtocolType,
    ReplacementStrategyType,
    ReplaceRootVolumeTaskStateType,
    ReportInstanceReasonCodesType,
    ReportStateType,
    ReportStatusTypeType,
    ReservationStateType,
    ReservedInstanceStateType,
    ResourceTypeType,
    RIProductDescriptionType,
    RootDeviceTypeType,
    RouteOriginType,
    RouteStateType,
    RouteTableAssociationStateCodeType,
    RuleActionType,
    ScopeType,
    SecurityGroupReferencingSupportValueType,
    SecurityGroupVpcAssociationStateType,
    SelfServicePortalType,
    ServiceConnectivityTypeType,
    ServiceStateType,
    ServiceTypeType,
    ShutdownBehaviorType,
    SnapshotAttributeNameType,
    SnapshotBlockPublicAccessStateType,
    SnapshotLocationEnumType,
    SnapshotStateType,
    SpotAllocationStrategyType,
    SpotInstanceInterruptionBehaviorType,
    SpotInstanceStateType,
    SpotInstanceTypeType,
    SpreadLevelType,
    SSETypeType,
    StateType,
    StaticSourcesSupportValueType,
    StatusType,
    StatusTypeType,
    StorageTierType,
    SubnetCidrBlockStateCodeType,
    SubnetCidrReservationTypeType,
    SubnetStateType,
    SummaryStatusType,
    TargetCapacityUnitTypeType,
    TelemetryStatusType,
    TenancyType,
    TieringOperationStatusType,
    TokenStateType,
    TrafficDirectionType,
    TrafficMirrorFilterRuleFieldType,
    TrafficMirrorRuleActionType,
    TrafficMirrorSessionFieldType,
    TrafficMirrorTargetTypeType,
    TrafficTypeType,
    TransferTypeType,
    TransitGatewayAssociationStateType,
    TransitGatewayAttachmentResourceTypeType,
    TransitGatewayAttachmentStateType,
    TransitGatewayConnectPeerStateType,
    TransitGatewayMulitcastDomainAssociationStateType,
    TransitGatewayMulticastDomainStateType,
    TransitGatewayPolicyTableStateType,
    TransitGatewayPrefixListReferenceStateType,
    TransitGatewayPropagationStateType,
    TransitGatewayRouteStateType,
    TransitGatewayRouteTableAnnouncementDirectionType,
    TransitGatewayRouteTableAnnouncementStateType,
    TransitGatewayRouteTableStateType,
    TransitGatewayRouteTypeType,
    TransitGatewayStateType,
    TransportProtocolType,
    TrustProviderTypeType,
    TunnelInsideIpVersionType,
    UnlimitedSupportedInstanceFamilyType,
    UnsuccessfulInstanceCreditSpecificationErrorCodeType,
    UsageClassTypeType,
    UserTrustProviderTypeType,
    VerificationMethodType,
    VerifiedAccessEndpointProtocolType,
    VerifiedAccessEndpointStatusCodeType,
    VerifiedAccessEndpointTypeType,
    VerifiedAccessLogDeliveryStatusCodeType,
    VirtualizationTypeType,
    VolumeAttachmentStateType,
    VolumeAttributeNameType,
    VolumeModificationStateType,
    VolumeStateType,
    VolumeStatusInfoStatusType,
    VolumeStatusNameType,
    VolumeTypeType,
    VpcAttributeNameType,
    VpcBlockPublicAccessExclusionsAllowedType,
    VpcBlockPublicAccessExclusionStateType,
    VpcBlockPublicAccessStateType,
    VpcCidrBlockStateCodeType,
    VpcEndpointTypeType,
    VpcPeeringConnectionStateReasonCodeType,
    VpcStateType,
    VpnEcmpSupportValueType,
    VpnStateType,
    WeekDayType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceleratorCountRequestTypeDef",
    "AcceleratorCountTypeDef",
    "AcceleratorTotalMemoryMiBRequestTypeDef",
    "AcceleratorTotalMemoryMiBTypeDef",
    "AcceptAddressTransferRequestRequestTypeDef",
    "AcceptAddressTransferResultTypeDef",
    "AcceptCapacityReservationBillingOwnershipRequestRequestTypeDef",
    "AcceptCapacityReservationBillingOwnershipResultTypeDef",
    "AcceptReservedInstancesExchangeQuoteRequestRequestTypeDef",
    "AcceptReservedInstancesExchangeQuoteResultTypeDef",
    "AcceptTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef",
    "AcceptTransitGatewayMulticastDomainAssociationsResultTypeDef",
    "AcceptTransitGatewayPeeringAttachmentRequestRequestTypeDef",
    "AcceptTransitGatewayPeeringAttachmentResultTypeDef",
    "AcceptTransitGatewayVpcAttachmentRequestRequestTypeDef",
    "AcceptTransitGatewayVpcAttachmentResultTypeDef",
    "AcceptVpcEndpointConnectionsRequestRequestTypeDef",
    "AcceptVpcEndpointConnectionsResultTypeDef",
    "AcceptVpcPeeringConnectionRequestRequestTypeDef",
    "AcceptVpcPeeringConnectionRequestVpcPeeringConnectionAcceptTypeDef",
    "AcceptVpcPeeringConnectionResultTypeDef",
    "AccessScopeAnalysisFindingTypeDef",
    "AccessScopePathRequestTypeDef",
    "AccessScopePathTypeDef",
    "AccountAttributeTypeDef",
    "AccountAttributeValueTypeDef",
    "ActiveInstanceTypeDef",
    "AddIpamOperatingRegionTypeDef",
    "AddIpamOrganizationalUnitExclusionTypeDef",
    "AddPrefixListEntryTypeDef",
    "AddedPrincipalTypeDef",
    "AdditionalDetailTypeDef",
    "AddressAttributeTypeDef",
    "AddressTransferTypeDef",
    "AddressTypeDef",
    "AdvertiseByoipCidrRequestRequestTypeDef",
    "AdvertiseByoipCidrResultTypeDef",
    "AllocateAddressRequestRequestTypeDef",
    "AllocateAddressResultTypeDef",
    "AllocateHostsRequestRequestTypeDef",
    "AllocateHostsResultTypeDef",
    "AllocateIpamPoolCidrRequestRequestTypeDef",
    "AllocateIpamPoolCidrResultTypeDef",
    "AllowedPrincipalTypeDef",
    "AlternatePathHintTypeDef",
    "AnalysisAclRuleTypeDef",
    "AnalysisComponentTypeDef",
    "AnalysisLoadBalancerListenerTypeDef",
    "AnalysisLoadBalancerTargetTypeDef",
    "AnalysisPacketHeaderTypeDef",
    "AnalysisRouteTableRouteTypeDef",
    "AnalysisSecurityGroupRuleTypeDef",
    "ApplySecurityGroupsToClientVpnTargetNetworkRequestRequestTypeDef",
    "ApplySecurityGroupsToClientVpnTargetNetworkResultTypeDef",
    "AsnAssociationTypeDef",
    "AsnAuthorizationContextTypeDef",
    "AssignIpv6AddressesRequestRequestTypeDef",
    "AssignIpv6AddressesResultTypeDef",
    "AssignPrivateIpAddressesRequestNetworkInterfaceAssignPrivateIpAddressesTypeDef",
    "AssignPrivateIpAddressesRequestRequestTypeDef",
    "AssignPrivateIpAddressesResultTypeDef",
    "AssignPrivateNatGatewayAddressRequestRequestTypeDef",
    "AssignPrivateNatGatewayAddressResultTypeDef",
    "AssignedPrivateIpAddressTypeDef",
    "AssociateAddressRequestClassicAddressAssociateTypeDef",
    "AssociateAddressRequestRequestTypeDef",
    "AssociateAddressRequestVpcAddressAssociateTypeDef",
    "AssociateAddressResultTypeDef",
    "AssociateCapacityReservationBillingOwnerRequestRequestTypeDef",
    "AssociateCapacityReservationBillingOwnerResultTypeDef",
    "AssociateClientVpnTargetNetworkRequestRequestTypeDef",
    "AssociateClientVpnTargetNetworkResultTypeDef",
    "AssociateDhcpOptionsRequestDhcpOptionsAssociateWithVpcTypeDef",
    "AssociateDhcpOptionsRequestRequestTypeDef",
    "AssociateDhcpOptionsRequestVpcAssociateDhcpOptionsTypeDef",
    "AssociateEnclaveCertificateIamRoleRequestRequestTypeDef",
    "AssociateEnclaveCertificateIamRoleResultTypeDef",
    "AssociateIamInstanceProfileRequestRequestTypeDef",
    "AssociateIamInstanceProfileResultTypeDef",
    "AssociateInstanceEventWindowRequestRequestTypeDef",
    "AssociateInstanceEventWindowResultTypeDef",
    "AssociateIpamByoasnRequestRequestTypeDef",
    "AssociateIpamByoasnResultTypeDef",
    "AssociateIpamResourceDiscoveryRequestRequestTypeDef",
    "AssociateIpamResourceDiscoveryResultTypeDef",
    "AssociateNatGatewayAddressRequestRequestTypeDef",
    "AssociateNatGatewayAddressResultTypeDef",
    "AssociateRouteTableRequestRequestTypeDef",
    "AssociateRouteTableRequestRouteTableAssociateWithSubnetTypeDef",
    "AssociateRouteTableResultTypeDef",
    "AssociateSecurityGroupVpcRequestRequestTypeDef",
    "AssociateSecurityGroupVpcResultTypeDef",
    "AssociateSubnetCidrBlockRequestRequestTypeDef",
    "AssociateSubnetCidrBlockResultTypeDef",
    "AssociateTransitGatewayMulticastDomainRequestRequestTypeDef",
    "AssociateTransitGatewayMulticastDomainResultTypeDef",
    "AssociateTransitGatewayPolicyTableRequestRequestTypeDef",
    "AssociateTransitGatewayPolicyTableResultTypeDef",
    "AssociateTransitGatewayRouteTableRequestRequestTypeDef",
    "AssociateTransitGatewayRouteTableResultTypeDef",
    "AssociateTrunkInterfaceRequestRequestTypeDef",
    "AssociateTrunkInterfaceResultTypeDef",
    "AssociateVpcCidrBlockRequestRequestTypeDef",
    "AssociateVpcCidrBlockResultTypeDef",
    "AssociatedRoleTypeDef",
    "AssociatedTargetNetworkTypeDef",
    "AssociationStatusTypeDef",
    "AthenaIntegrationTypeDef",
    "AttachClassicLinkVpcRequestInstanceAttachClassicLinkVpcTypeDef",
    "AttachClassicLinkVpcRequestRequestTypeDef",
    "AttachClassicLinkVpcRequestVpcAttachClassicLinkInstanceTypeDef",
    "AttachClassicLinkVpcResultTypeDef",
    "AttachInternetGatewayRequestInternetGatewayAttachToVpcTypeDef",
    "AttachInternetGatewayRequestRequestTypeDef",
    "AttachInternetGatewayRequestVpcAttachInternetGatewayTypeDef",
    "AttachNetworkInterfaceRequestNetworkInterfaceAttachTypeDef",
    "AttachNetworkInterfaceRequestRequestTypeDef",
    "AttachNetworkInterfaceResultTypeDef",
    "AttachVerifiedAccessTrustProviderRequestRequestTypeDef",
    "AttachVerifiedAccessTrustProviderResultTypeDef",
    "AttachVolumeRequestInstanceAttachVolumeTypeDef",
    "AttachVolumeRequestRequestTypeDef",
    "AttachVolumeRequestVolumeAttachToInstanceTypeDef",
    "AttachVpnGatewayRequestRequestTypeDef",
    "AttachVpnGatewayResultTypeDef",
    "AttachmentEnaSrdSpecificationTypeDef",
    "AttachmentEnaSrdUdpSpecificationTypeDef",
    "AttributeBooleanValueTypeDef",
    "AttributeSummaryTypeDef",
    "AttributeValueTypeDef",
    "AuthorizationRuleTypeDef",
    "AuthorizeClientVpnIngressRequestRequestTypeDef",
    "AuthorizeClientVpnIngressResultTypeDef",
    "AuthorizeSecurityGroupEgressRequestRequestTypeDef",
    "AuthorizeSecurityGroupEgressRequestSecurityGroupAuthorizeEgressTypeDef",
    "AuthorizeSecurityGroupEgressResultTypeDef",
    "AuthorizeSecurityGroupIngressRequestRequestTypeDef",
    "AuthorizeSecurityGroupIngressRequestSecurityGroupAuthorizeIngressTypeDef",
    "AuthorizeSecurityGroupIngressResultTypeDef",
    "AvailabilityZoneMessageTypeDef",
    "AvailabilityZoneTypeDef",
    "AvailableCapacityTypeDef",
    "BaselineEbsBandwidthMbpsRequestTypeDef",
    "BaselineEbsBandwidthMbpsTypeDef",
    "BaselinePerformanceFactorsOutputTypeDef",
    "BaselinePerformanceFactorsRequestTypeDef",
    "BaselinePerformanceFactorsTypeDef",
    "BaselinePerformanceFactorsUnionTypeDef",
    "BlobAttributeValueTypeDef",
    "BlobTypeDef",
    "BlockDeviceMappingTypeDef",
    "BlockPublicAccessStatesTypeDef",
    "BundleInstanceRequestRequestTypeDef",
    "BundleInstanceResultTypeDef",
    "BundleTaskErrorTypeDef",
    "BundleTaskTypeDef",
    "ByoasnTypeDef",
    "ByoipCidrTypeDef",
    "CancelBundleTaskRequestRequestTypeDef",
    "CancelBundleTaskResultTypeDef",
    "CancelCapacityReservationFleetErrorTypeDef",
    "CancelCapacityReservationFleetsRequestRequestTypeDef",
    "CancelCapacityReservationFleetsResultTypeDef",
    "CancelCapacityReservationRequestRequestTypeDef",
    "CancelCapacityReservationResultTypeDef",
    "CancelConversionRequestRequestTypeDef",
    "CancelDeclarativePoliciesReportRequestRequestTypeDef",
    "CancelDeclarativePoliciesReportResultTypeDef",
    "CancelExportTaskRequestRequestTypeDef",
    "CancelImageLaunchPermissionRequestRequestTypeDef",
    "CancelImageLaunchPermissionResultTypeDef",
    "CancelImportTaskRequestRequestTypeDef",
    "CancelImportTaskResultTypeDef",
    "CancelReservedInstancesListingRequestRequestTypeDef",
    "CancelReservedInstancesListingResultTypeDef",
    "CancelSpotFleetRequestsErrorItemTypeDef",
    "CancelSpotFleetRequestsErrorTypeDef",
    "CancelSpotFleetRequestsRequestRequestTypeDef",
    "CancelSpotFleetRequestsResponseTypeDef",
    "CancelSpotFleetRequestsSuccessItemTypeDef",
    "CancelSpotInstanceRequestsRequestRequestTypeDef",
    "CancelSpotInstanceRequestsResultTypeDef",
    "CancelledSpotInstanceRequestTypeDef",
    "CapacityAllocationTypeDef",
    "CapacityBlockExtensionOfferingTypeDef",
    "CapacityBlockExtensionTypeDef",
    "CapacityBlockOfferingTypeDef",
    "CapacityReservationBillingRequestTypeDef",
    "CapacityReservationCommitmentInfoTypeDef",
    "CapacityReservationFleetCancellationStateTypeDef",
    "CapacityReservationFleetTypeDef",
    "CapacityReservationGroupTypeDef",
    "CapacityReservationInfoTypeDef",
    "CapacityReservationOptionsRequestTypeDef",
    "CapacityReservationOptionsTypeDef",
    "CapacityReservationSpecificationResponseTypeDef",
    "CapacityReservationSpecificationTypeDef",
    "CapacityReservationTargetResponseTypeDef",
    "CapacityReservationTargetTypeDef",
    "CapacityReservationTypeDef",
    "CarrierGatewayTypeDef",
    "CertificateAuthenticationRequestTypeDef",
    "CertificateAuthenticationTypeDef",
    "CidrAuthorizationContextTypeDef",
    "CidrBlockTypeDef",
    "ClassicLinkDnsSupportTypeDef",
    "ClassicLinkInstanceTypeDef",
    "ClassicLoadBalancerTypeDef",
    "ClassicLoadBalancersConfigOutputTypeDef",
    "ClassicLoadBalancersConfigTypeDef",
    "ClassicLoadBalancersConfigUnionTypeDef",
    "ClientCertificateRevocationListStatusTypeDef",
    "ClientConnectOptionsTypeDef",
    "ClientConnectResponseOptionsTypeDef",
    "ClientCreateTagsRequestTypeDef",
    "ClientDataTypeDef",
    "ClientDeleteTagsRequestTypeDef",
    "ClientLoginBannerOptionsTypeDef",
    "ClientLoginBannerResponseOptionsTypeDef",
    "ClientVpnAuthenticationRequestTypeDef",
    "ClientVpnAuthenticationTypeDef",
    "ClientVpnAuthorizationRuleStatusTypeDef",
    "ClientVpnConnectionStatusTypeDef",
    "ClientVpnConnectionTypeDef",
    "ClientVpnEndpointAttributeStatusTypeDef",
    "ClientVpnEndpointStatusTypeDef",
    "ClientVpnEndpointTypeDef",
    "ClientVpnRouteStatusTypeDef",
    "ClientVpnRouteTypeDef",
    "CloudWatchLogOptionsSpecificationTypeDef",
    "CloudWatchLogOptionsTypeDef",
    "CoipAddressUsageTypeDef",
    "CoipCidrTypeDef",
    "CoipPoolTypeDef",
    "ConfirmProductInstanceRequestRequestTypeDef",
    "ConfirmProductInstanceResultTypeDef",
    "ConnectionLogOptionsTypeDef",
    "ConnectionLogResponseOptionsTypeDef",
    "ConnectionNotificationTypeDef",
    "ConnectionTrackingConfigurationTypeDef",
    "ConnectionTrackingSpecificationRequestTypeDef",
    "ConnectionTrackingSpecificationResponseTypeDef",
    "ConnectionTrackingSpecificationTypeDef",
    "ConversionTaskTypeDef",
    "CopyFpgaImageRequestRequestTypeDef",
    "CopyFpgaImageResultTypeDef",
    "CopyImageRequestRequestTypeDef",
    "CopyImageResultTypeDef",
    "CopySnapshotRequestRequestTypeDef",
    "CopySnapshotRequestSnapshotCopyTypeDef",
    "CopySnapshotResultTypeDef",
    "CpuOptionsRequestTypeDef",
    "CpuOptionsTypeDef",
    "CpuPerformanceFactorOutputTypeDef",
    "CpuPerformanceFactorRequestTypeDef",
    "CpuPerformanceFactorTypeDef",
    "CpuPerformanceFactorUnionTypeDef",
    "CreateCapacityReservationBySplittingRequestRequestTypeDef",
    "CreateCapacityReservationBySplittingResultTypeDef",
    "CreateCapacityReservationFleetRequestRequestTypeDef",
    "CreateCapacityReservationFleetResultTypeDef",
    "CreateCapacityReservationRequestRequestTypeDef",
    "CreateCapacityReservationResultTypeDef",
    "CreateCarrierGatewayRequestRequestTypeDef",
    "CreateCarrierGatewayResultTypeDef",
    "CreateClientVpnEndpointRequestRequestTypeDef",
    "CreateClientVpnEndpointResultTypeDef",
    "CreateClientVpnRouteRequestRequestTypeDef",
    "CreateClientVpnRouteResultTypeDef",
    "CreateCoipCidrRequestRequestTypeDef",
    "CreateCoipCidrResultTypeDef",
    "CreateCoipPoolRequestRequestTypeDef",
    "CreateCoipPoolResultTypeDef",
    "CreateCustomerGatewayRequestRequestTypeDef",
    "CreateCustomerGatewayResultTypeDef",
    "CreateDefaultSubnetRequestRequestTypeDef",
    "CreateDefaultSubnetResultTypeDef",
    "CreateDefaultVpcRequestRequestTypeDef",
    "CreateDefaultVpcResultTypeDef",
    "CreateDhcpOptionsRequestRequestTypeDef",
    "CreateDhcpOptionsRequestServiceResourceCreateDhcpOptionsTypeDef",
    "CreateDhcpOptionsResultTypeDef",
    "CreateEgressOnlyInternetGatewayRequestRequestTypeDef",
    "CreateEgressOnlyInternetGatewayResultTypeDef",
    "CreateFleetErrorTypeDef",
    "CreateFleetInstanceTypeDef",
    "CreateFleetRequestRequestTypeDef",
    "CreateFleetResultTypeDef",
    "CreateFlowLogsRequestRequestTypeDef",
    "CreateFlowLogsResultTypeDef",
    "CreateFpgaImageRequestRequestTypeDef",
    "CreateFpgaImageResultTypeDef",
    "CreateImageRequestInstanceCreateImageTypeDef",
    "CreateImageRequestRequestTypeDef",
    "CreateImageResultTypeDef",
    "CreateInstanceConnectEndpointRequestRequestTypeDef",
    "CreateInstanceConnectEndpointResultTypeDef",
    "CreateInstanceEventWindowRequestRequestTypeDef",
    "CreateInstanceEventWindowResultTypeDef",
    "CreateInstanceExportTaskRequestRequestTypeDef",
    "CreateInstanceExportTaskResultTypeDef",
    "CreateInternetGatewayRequestRequestTypeDef",
    "CreateInternetGatewayRequestServiceResourceCreateInternetGatewayTypeDef",
    "CreateInternetGatewayResultTypeDef",
    "CreateIpamExternalResourceVerificationTokenRequestRequestTypeDef",
    "CreateIpamExternalResourceVerificationTokenResultTypeDef",
    "CreateIpamPoolRequestRequestTypeDef",
    "CreateIpamPoolResultTypeDef",
    "CreateIpamRequestRequestTypeDef",
    "CreateIpamResourceDiscoveryRequestRequestTypeDef",
    "CreateIpamResourceDiscoveryResultTypeDef",
    "CreateIpamResultTypeDef",
    "CreateIpamScopeRequestRequestTypeDef",
    "CreateIpamScopeResultTypeDef",
    "CreateKeyPairRequestRequestTypeDef",
    "CreateKeyPairRequestServiceResourceCreateKeyPairTypeDef",
    "CreateLaunchTemplateRequestRequestTypeDef",
    "CreateLaunchTemplateResultTypeDef",
    "CreateLaunchTemplateVersionRequestRequestTypeDef",
    "CreateLaunchTemplateVersionResultTypeDef",
    "CreateLocalGatewayRouteRequestRequestTypeDef",
    "CreateLocalGatewayRouteResultTypeDef",
    "CreateLocalGatewayRouteTableRequestRequestTypeDef",
    "CreateLocalGatewayRouteTableResultTypeDef",
    "CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef",
    "CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef",
    "CreateLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef",
    "CreateLocalGatewayRouteTableVpcAssociationResultTypeDef",
    "CreateManagedPrefixListRequestRequestTypeDef",
    "CreateManagedPrefixListResultTypeDef",
    "CreateNatGatewayRequestRequestTypeDef",
    "CreateNatGatewayResultTypeDef",
    "CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef",
    "CreateNetworkAclEntryRequestRequestTypeDef",
    "CreateNetworkAclRequestRequestTypeDef",
    "CreateNetworkAclRequestServiceResourceCreateNetworkAclTypeDef",
    "CreateNetworkAclRequestVpcCreateNetworkAclTypeDef",
    "CreateNetworkAclResultTypeDef",
    "CreateNetworkInsightsAccessScopeRequestRequestTypeDef",
    "CreateNetworkInsightsAccessScopeResultTypeDef",
    "CreateNetworkInsightsPathRequestRequestTypeDef",
    "CreateNetworkInsightsPathResultTypeDef",
    "CreateNetworkInterfacePermissionRequestRequestTypeDef",
    "CreateNetworkInterfacePermissionResultTypeDef",
    "CreateNetworkInterfaceRequestRequestTypeDef",
    "CreateNetworkInterfaceRequestServiceResourceCreateNetworkInterfaceTypeDef",
    "CreateNetworkInterfaceRequestSubnetCreateNetworkInterfaceTypeDef",
    "CreateNetworkInterfaceResultTypeDef",
    "CreatePlacementGroupRequestRequestTypeDef",
    "CreatePlacementGroupRequestServiceResourceCreatePlacementGroupTypeDef",
    "CreatePlacementGroupResultTypeDef",
    "CreatePublicIpv4PoolRequestRequestTypeDef",
    "CreatePublicIpv4PoolResultTypeDef",
    "CreateReplaceRootVolumeTaskRequestRequestTypeDef",
    "CreateReplaceRootVolumeTaskResultTypeDef",
    "CreateReservedInstancesListingRequestRequestTypeDef",
    "CreateReservedInstancesListingResultTypeDef",
    "CreateRestoreImageTaskRequestRequestTypeDef",
    "CreateRestoreImageTaskResultTypeDef",
    "CreateRouteRequestRequestTypeDef",
    "CreateRouteRequestRouteTableCreateRouteTypeDef",
    "CreateRouteResultTypeDef",
    "CreateRouteTableRequestRequestTypeDef",
    "CreateRouteTableRequestServiceResourceCreateRouteTableTypeDef",
    "CreateRouteTableRequestVpcCreateRouteTableTypeDef",
    "CreateRouteTableResultTypeDef",
    "CreateSecurityGroupRequestRequestTypeDef",
    "CreateSecurityGroupRequestServiceResourceCreateSecurityGroupTypeDef",
    "CreateSecurityGroupRequestVpcCreateSecurityGroupTypeDef",
    "CreateSecurityGroupResultTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateSnapshotRequestServiceResourceCreateSnapshotTypeDef",
    "CreateSnapshotRequestVolumeCreateSnapshotTypeDef",
    "CreateSnapshotsRequestRequestTypeDef",
    "CreateSnapshotsResultTypeDef",
    "CreateSpotDatafeedSubscriptionRequestRequestTypeDef",
    "CreateSpotDatafeedSubscriptionResultTypeDef",
    "CreateStoreImageTaskRequestRequestTypeDef",
    "CreateStoreImageTaskResultTypeDef",
    "CreateSubnetCidrReservationRequestRequestTypeDef",
    "CreateSubnetCidrReservationResultTypeDef",
    "CreateSubnetRequestRequestTypeDef",
    "CreateSubnetRequestServiceResourceCreateSubnetTypeDef",
    "CreateSubnetRequestVpcCreateSubnetTypeDef",
    "CreateSubnetResultTypeDef",
    "CreateTagsRequestServiceResourceCreateTagsTypeDef",
    "CreateTrafficMirrorFilterRequestRequestTypeDef",
    "CreateTrafficMirrorFilterResultTypeDef",
    "CreateTrafficMirrorFilterRuleRequestRequestTypeDef",
    "CreateTrafficMirrorFilterRuleResultTypeDef",
    "CreateTrafficMirrorSessionRequestRequestTypeDef",
    "CreateTrafficMirrorSessionResultTypeDef",
    "CreateTrafficMirrorTargetRequestRequestTypeDef",
    "CreateTrafficMirrorTargetResultTypeDef",
    "CreateTransitGatewayConnectPeerRequestRequestTypeDef",
    "CreateTransitGatewayConnectPeerResultTypeDef",
    "CreateTransitGatewayConnectRequestOptionsTypeDef",
    "CreateTransitGatewayConnectRequestRequestTypeDef",
    "CreateTransitGatewayConnectResultTypeDef",
    "CreateTransitGatewayMulticastDomainRequestOptionsTypeDef",
    "CreateTransitGatewayMulticastDomainRequestRequestTypeDef",
    "CreateTransitGatewayMulticastDomainResultTypeDef",
    "CreateTransitGatewayPeeringAttachmentRequestOptionsTypeDef",
    "CreateTransitGatewayPeeringAttachmentRequestRequestTypeDef",
    "CreateTransitGatewayPeeringAttachmentResultTypeDef",
    "CreateTransitGatewayPolicyTableRequestRequestTypeDef",
    "CreateTransitGatewayPolicyTableResultTypeDef",
    "CreateTransitGatewayPrefixListReferenceRequestRequestTypeDef",
    "CreateTransitGatewayPrefixListReferenceResultTypeDef",
    "CreateTransitGatewayRequestRequestTypeDef",
    "CreateTransitGatewayResultTypeDef",
    "CreateTransitGatewayRouteRequestRequestTypeDef",
    "CreateTransitGatewayRouteResultTypeDef",
    "CreateTransitGatewayRouteTableAnnouncementRequestRequestTypeDef",
    "CreateTransitGatewayRouteTableAnnouncementResultTypeDef",
    "CreateTransitGatewayRouteTableRequestRequestTypeDef",
    "CreateTransitGatewayRouteTableResultTypeDef",
    "CreateTransitGatewayVpcAttachmentRequestOptionsTypeDef",
    "CreateTransitGatewayVpcAttachmentRequestRequestTypeDef",
    "CreateTransitGatewayVpcAttachmentResultTypeDef",
    "CreateVerifiedAccessEndpointCidrOptionsTypeDef",
    "CreateVerifiedAccessEndpointEniOptionsTypeDef",
    "CreateVerifiedAccessEndpointLoadBalancerOptionsTypeDef",
    "CreateVerifiedAccessEndpointPortRangeTypeDef",
    "CreateVerifiedAccessEndpointRdsOptionsTypeDef",
    "CreateVerifiedAccessEndpointRequestRequestTypeDef",
    "CreateVerifiedAccessEndpointResultTypeDef",
    "CreateVerifiedAccessGroupRequestRequestTypeDef",
    "CreateVerifiedAccessGroupResultTypeDef",
    "CreateVerifiedAccessInstanceRequestRequestTypeDef",
    "CreateVerifiedAccessInstanceResultTypeDef",
    "CreateVerifiedAccessNativeApplicationOidcOptionsTypeDef",
    "CreateVerifiedAccessTrustProviderDeviceOptionsTypeDef",
    "CreateVerifiedAccessTrustProviderOidcOptionsTypeDef",
    "CreateVerifiedAccessTrustProviderRequestRequestTypeDef",
    "CreateVerifiedAccessTrustProviderResultTypeDef",
    "CreateVolumePermissionModificationsTypeDef",
    "CreateVolumePermissionTypeDef",
    "CreateVolumeRequestRequestTypeDef",
    "CreateVolumeRequestServiceResourceCreateVolumeTypeDef",
    "CreateVpcBlockPublicAccessExclusionRequestRequestTypeDef",
    "CreateVpcBlockPublicAccessExclusionResultTypeDef",
    "CreateVpcEndpointConnectionNotificationRequestRequestTypeDef",
    "CreateVpcEndpointConnectionNotificationResultTypeDef",
    "CreateVpcEndpointRequestRequestTypeDef",
    "CreateVpcEndpointResultTypeDef",
    "CreateVpcEndpointServiceConfigurationRequestRequestTypeDef",
    "CreateVpcEndpointServiceConfigurationResultTypeDef",
    "CreateVpcPeeringConnectionRequestRequestTypeDef",
    "CreateVpcPeeringConnectionRequestServiceResourceCreateVpcPeeringConnectionTypeDef",
    "CreateVpcPeeringConnectionRequestVpcRequestVpcPeeringConnectionTypeDef",
    "CreateVpcPeeringConnectionResultTypeDef",
    "CreateVpcRequestRequestTypeDef",
    "CreateVpcRequestServiceResourceCreateVpcTypeDef",
    "CreateVpcResultTypeDef",
    "CreateVpnConnectionRequestRequestTypeDef",
    "CreateVpnConnectionResultTypeDef",
    "CreateVpnConnectionRouteRequestRequestTypeDef",
    "CreateVpnGatewayRequestRequestTypeDef",
    "CreateVpnGatewayResultTypeDef",
    "CreditSpecificationRequestTypeDef",
    "CreditSpecificationTypeDef",
    "CustomerGatewayTypeDef",
    "DataQueryTypeDef",
    "DataResponseTypeDef",
    "DeclarativePoliciesReportTypeDef",
    "DeleteCarrierGatewayRequestRequestTypeDef",
    "DeleteCarrierGatewayResultTypeDef",
    "DeleteClientVpnEndpointRequestRequestTypeDef",
    "DeleteClientVpnEndpointResultTypeDef",
    "DeleteClientVpnRouteRequestRequestTypeDef",
    "DeleteClientVpnRouteResultTypeDef",
    "DeleteCoipCidrRequestRequestTypeDef",
    "DeleteCoipCidrResultTypeDef",
    "DeleteCoipPoolRequestRequestTypeDef",
    "DeleteCoipPoolResultTypeDef",
    "DeleteCustomerGatewayRequestRequestTypeDef",
    "DeleteDhcpOptionsRequestDhcpOptionsDeleteTypeDef",
    "DeleteDhcpOptionsRequestRequestTypeDef",
    "DeleteEgressOnlyInternetGatewayRequestRequestTypeDef",
    "DeleteEgressOnlyInternetGatewayResultTypeDef",
    "DeleteFleetErrorItemTypeDef",
    "DeleteFleetErrorTypeDef",
    "DeleteFleetSuccessItemTypeDef",
    "DeleteFleetsRequestRequestTypeDef",
    "DeleteFleetsResultTypeDef",
    "DeleteFlowLogsRequestRequestTypeDef",
    "DeleteFlowLogsResultTypeDef",
    "DeleteFpgaImageRequestRequestTypeDef",
    "DeleteFpgaImageResultTypeDef",
    "DeleteInstanceConnectEndpointRequestRequestTypeDef",
    "DeleteInstanceConnectEndpointResultTypeDef",
    "DeleteInstanceEventWindowRequestRequestTypeDef",
    "DeleteInstanceEventWindowResultTypeDef",
    "DeleteInternetGatewayRequestInternetGatewayDeleteTypeDef",
    "DeleteInternetGatewayRequestRequestTypeDef",
    "DeleteIpamExternalResourceVerificationTokenRequestRequestTypeDef",
    "DeleteIpamExternalResourceVerificationTokenResultTypeDef",
    "DeleteIpamPoolRequestRequestTypeDef",
    "DeleteIpamPoolResultTypeDef",
    "DeleteIpamRequestRequestTypeDef",
    "DeleteIpamResourceDiscoveryRequestRequestTypeDef",
    "DeleteIpamResourceDiscoveryResultTypeDef",
    "DeleteIpamResultTypeDef",
    "DeleteIpamScopeRequestRequestTypeDef",
    "DeleteIpamScopeResultTypeDef",
    "DeleteKeyPairRequestKeyPairDeleteTypeDef",
    "DeleteKeyPairRequestKeyPairInfoDeleteTypeDef",
    "DeleteKeyPairRequestRequestTypeDef",
    "DeleteKeyPairResultTypeDef",
    "DeleteLaunchTemplateRequestRequestTypeDef",
    "DeleteLaunchTemplateResultTypeDef",
    "DeleteLaunchTemplateVersionsRequestRequestTypeDef",
    "DeleteLaunchTemplateVersionsResponseErrorItemTypeDef",
    "DeleteLaunchTemplateVersionsResponseSuccessItemTypeDef",
    "DeleteLaunchTemplateVersionsResultTypeDef",
    "DeleteLocalGatewayRouteRequestRequestTypeDef",
    "DeleteLocalGatewayRouteResultTypeDef",
    "DeleteLocalGatewayRouteTableRequestRequestTypeDef",
    "DeleteLocalGatewayRouteTableResultTypeDef",
    "DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef",
    "DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef",
    "DeleteLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef",
    "DeleteLocalGatewayRouteTableVpcAssociationResultTypeDef",
    "DeleteManagedPrefixListRequestRequestTypeDef",
    "DeleteManagedPrefixListResultTypeDef",
    "DeleteNatGatewayRequestRequestTypeDef",
    "DeleteNatGatewayResultTypeDef",
    "DeleteNetworkAclEntryRequestNetworkAclDeleteEntryTypeDef",
    "DeleteNetworkAclEntryRequestRequestTypeDef",
    "DeleteNetworkAclRequestNetworkAclDeleteTypeDef",
    "DeleteNetworkAclRequestRequestTypeDef",
    "DeleteNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef",
    "DeleteNetworkInsightsAccessScopeAnalysisResultTypeDef",
    "DeleteNetworkInsightsAccessScopeRequestRequestTypeDef",
    "DeleteNetworkInsightsAccessScopeResultTypeDef",
    "DeleteNetworkInsightsAnalysisRequestRequestTypeDef",
    "DeleteNetworkInsightsAnalysisResultTypeDef",
    "DeleteNetworkInsightsPathRequestRequestTypeDef",
    "DeleteNetworkInsightsPathResultTypeDef",
    "DeleteNetworkInterfacePermissionRequestRequestTypeDef",
    "DeleteNetworkInterfacePermissionResultTypeDef",
    "DeleteNetworkInterfaceRequestNetworkInterfaceDeleteTypeDef",
    "DeleteNetworkInterfaceRequestRequestTypeDef",
    "DeletePlacementGroupRequestPlacementGroupDeleteTypeDef",
    "DeletePlacementGroupRequestRequestTypeDef",
    "DeletePublicIpv4PoolRequestRequestTypeDef",
    "DeletePublicIpv4PoolResultTypeDef",
    "DeleteQueuedReservedInstancesErrorTypeDef",
    "DeleteQueuedReservedInstancesRequestRequestTypeDef",
    "DeleteQueuedReservedInstancesResultTypeDef",
    "DeleteRouteRequestRequestTypeDef",
    "DeleteRouteRequestRouteDeleteTypeDef",
    "DeleteRouteTableRequestRequestTypeDef",
    "DeleteRouteTableRequestRouteTableDeleteTypeDef",
    "DeleteSecurityGroupRequestRequestTypeDef",
    "DeleteSecurityGroupRequestSecurityGroupDeleteTypeDef",
    "DeleteSecurityGroupResultTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteSnapshotRequestSnapshotDeleteTypeDef",
    "DeleteSpotDatafeedSubscriptionRequestRequestTypeDef",
    "DeleteSubnetCidrReservationRequestRequestTypeDef",
    "DeleteSubnetCidrReservationResultTypeDef",
    "DeleteSubnetRequestRequestTypeDef",
    "DeleteSubnetRequestSubnetDeleteTypeDef",
    "DeleteTagsRequestTagDeleteTypeDef",
    "DeleteTrafficMirrorFilterRequestRequestTypeDef",
    "DeleteTrafficMirrorFilterResultTypeDef",
    "DeleteTrafficMirrorFilterRuleRequestRequestTypeDef",
    "DeleteTrafficMirrorFilterRuleResultTypeDef",
    "DeleteTrafficMirrorSessionRequestRequestTypeDef",
    "DeleteTrafficMirrorSessionResultTypeDef",
    "DeleteTrafficMirrorTargetRequestRequestTypeDef",
    "DeleteTrafficMirrorTargetResultTypeDef",
    "DeleteTransitGatewayConnectPeerRequestRequestTypeDef",
    "DeleteTransitGatewayConnectPeerResultTypeDef",
    "DeleteTransitGatewayConnectRequestRequestTypeDef",
    "DeleteTransitGatewayConnectResultTypeDef",
    "DeleteTransitGatewayMulticastDomainRequestRequestTypeDef",
    "DeleteTransitGatewayMulticastDomainResultTypeDef",
    "DeleteTransitGatewayPeeringAttachmentRequestRequestTypeDef",
    "DeleteTransitGatewayPeeringAttachmentResultTypeDef",
    "DeleteTransitGatewayPolicyTableRequestRequestTypeDef",
    "DeleteTransitGatewayPolicyTableResultTypeDef",
    "DeleteTransitGatewayPrefixListReferenceRequestRequestTypeDef",
    "DeleteTransitGatewayPrefixListReferenceResultTypeDef",
    "DeleteTransitGatewayRequestRequestTypeDef",
    "DeleteTransitGatewayResultTypeDef",
    "DeleteTransitGatewayRouteRequestRequestTypeDef",
    "DeleteTransitGatewayRouteResultTypeDef",
    "DeleteTransitGatewayRouteTableAnnouncementRequestRequestTypeDef",
    "DeleteTransitGatewayRouteTableAnnouncementResultTypeDef",
    "DeleteTransitGatewayRouteTableRequestRequestTypeDef",
    "DeleteTransitGatewayRouteTableResultTypeDef",
    "DeleteTransitGatewayVpcAttachmentRequestRequestTypeDef",
    "DeleteTransitGatewayVpcAttachmentResultTypeDef",
    "DeleteVerifiedAccessEndpointRequestRequestTypeDef",
    "DeleteVerifiedAccessEndpointResultTypeDef",
    "DeleteVerifiedAccessGroupRequestRequestTypeDef",
    "DeleteVerifiedAccessGroupResultTypeDef",
    "DeleteVerifiedAccessInstanceRequestRequestTypeDef",
    "DeleteVerifiedAccessInstanceResultTypeDef",
    "DeleteVerifiedAccessTrustProviderRequestRequestTypeDef",
    "DeleteVerifiedAccessTrustProviderResultTypeDef",
    "DeleteVolumeRequestRequestTypeDef",
    "DeleteVolumeRequestVolumeDeleteTypeDef",
    "DeleteVpcBlockPublicAccessExclusionRequestRequestTypeDef",
    "DeleteVpcBlockPublicAccessExclusionResultTypeDef",
    "DeleteVpcEndpointConnectionNotificationsRequestRequestTypeDef",
    "DeleteVpcEndpointConnectionNotificationsResultTypeDef",
    "DeleteVpcEndpointServiceConfigurationsRequestRequestTypeDef",
    "DeleteVpcEndpointServiceConfigurationsResultTypeDef",
    "DeleteVpcEndpointsRequestRequestTypeDef",
    "DeleteVpcEndpointsResultTypeDef",
    "DeleteVpcPeeringConnectionRequestRequestTypeDef",
    "DeleteVpcPeeringConnectionRequestVpcPeeringConnectionDeleteTypeDef",
    "DeleteVpcPeeringConnectionResultTypeDef",
    "DeleteVpcRequestRequestTypeDef",
    "DeleteVpcRequestVpcDeleteTypeDef",
    "DeleteVpnConnectionRequestRequestTypeDef",
    "DeleteVpnConnectionRouteRequestRequestTypeDef",
    "DeleteVpnGatewayRequestRequestTypeDef",
    "DeprovisionByoipCidrRequestRequestTypeDef",
    "DeprovisionByoipCidrResultTypeDef",
    "DeprovisionIpamByoasnRequestRequestTypeDef",
    "DeprovisionIpamByoasnResultTypeDef",
    "DeprovisionIpamPoolCidrRequestRequestTypeDef",
    "DeprovisionIpamPoolCidrResultTypeDef",
    "DeprovisionPublicIpv4PoolCidrRequestRequestTypeDef",
    "DeprovisionPublicIpv4PoolCidrResultTypeDef",
    "DeregisterImageRequestImageDeregisterTypeDef",
    "DeregisterImageRequestRequestTypeDef",
    "DeregisterInstanceEventNotificationAttributesRequestRequestTypeDef",
    "DeregisterInstanceEventNotificationAttributesResultTypeDef",
    "DeregisterInstanceTagAttributeRequestTypeDef",
    "DeregisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef",
    "DeregisterTransitGatewayMulticastGroupMembersResultTypeDef",
    "DeregisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef",
    "DeregisterTransitGatewayMulticastGroupSourcesResultTypeDef",
    "DescribeAccountAttributesRequestRequestTypeDef",
    "DescribeAccountAttributesResultTypeDef",
    "DescribeAddressTransfersRequestPaginateTypeDef",
    "DescribeAddressTransfersRequestRequestTypeDef",
    "DescribeAddressTransfersResultTypeDef",
    "DescribeAddressesAttributeRequestPaginateTypeDef",
    "DescribeAddressesAttributeRequestRequestTypeDef",
    "DescribeAddressesAttributeResultTypeDef",
    "DescribeAddressesRequestRequestTypeDef",
    "DescribeAddressesResultTypeDef",
    "DescribeAggregateIdFormatRequestRequestTypeDef",
    "DescribeAggregateIdFormatResultTypeDef",
    "DescribeAvailabilityZonesRequestRequestTypeDef",
    "DescribeAvailabilityZonesResultTypeDef",
    "DescribeAwsNetworkPerformanceMetricSubscriptionsRequestPaginateTypeDef",
    "DescribeAwsNetworkPerformanceMetricSubscriptionsRequestRequestTypeDef",
    "DescribeAwsNetworkPerformanceMetricSubscriptionsResultTypeDef",
    "DescribeBundleTasksRequestRequestTypeDef",
    "DescribeBundleTasksRequestWaitTypeDef",
    "DescribeBundleTasksResultTypeDef",
    "DescribeByoipCidrsRequestPaginateTypeDef",
    "DescribeByoipCidrsRequestRequestTypeDef",
    "DescribeByoipCidrsResultTypeDef",
    "DescribeCapacityBlockExtensionHistoryRequestPaginateTypeDef",
    "DescribeCapacityBlockExtensionHistoryRequestRequestTypeDef",
    "DescribeCapacityBlockExtensionHistoryResultTypeDef",
    "DescribeCapacityBlockExtensionOfferingsRequestPaginateTypeDef",
    "DescribeCapacityBlockExtensionOfferingsRequestRequestTypeDef",
    "DescribeCapacityBlockExtensionOfferingsResultTypeDef",
    "DescribeCapacityBlockOfferingsRequestPaginateTypeDef",
    "DescribeCapacityBlockOfferingsRequestRequestTypeDef",
    "DescribeCapacityBlockOfferingsResultTypeDef",
    "DescribeCapacityReservationBillingRequestsRequestPaginateTypeDef",
    "DescribeCapacityReservationBillingRequestsRequestRequestTypeDef",
    "DescribeCapacityReservationBillingRequestsResultTypeDef",
    "DescribeCapacityReservationFleetsRequestPaginateTypeDef",
    "DescribeCapacityReservationFleetsRequestRequestTypeDef",
    "DescribeCapacityReservationFleetsResultTypeDef",
    "DescribeCapacityReservationsRequestPaginateTypeDef",
    "DescribeCapacityReservationsRequestRequestTypeDef",
    "DescribeCapacityReservationsResultTypeDef",
    "DescribeCarrierGatewaysRequestPaginateTypeDef",
    "DescribeCarrierGatewaysRequestRequestTypeDef",
    "DescribeCarrierGatewaysResultTypeDef",
    "DescribeClassicLinkInstancesRequestPaginateTypeDef",
    "DescribeClassicLinkInstancesRequestRequestTypeDef",
    "DescribeClassicLinkInstancesResultTypeDef",
    "DescribeClientVpnAuthorizationRulesRequestPaginateTypeDef",
    "DescribeClientVpnAuthorizationRulesRequestRequestTypeDef",
    "DescribeClientVpnAuthorizationRulesResultTypeDef",
    "DescribeClientVpnConnectionsRequestPaginateTypeDef",
    "DescribeClientVpnConnectionsRequestRequestTypeDef",
    "DescribeClientVpnConnectionsResultTypeDef",
    "DescribeClientVpnEndpointsRequestPaginateTypeDef",
    "DescribeClientVpnEndpointsRequestRequestTypeDef",
    "DescribeClientVpnEndpointsResultTypeDef",
    "DescribeClientVpnRoutesRequestPaginateTypeDef",
    "DescribeClientVpnRoutesRequestRequestTypeDef",
    "DescribeClientVpnRoutesResultTypeDef",
    "DescribeClientVpnTargetNetworksRequestPaginateTypeDef",
    "DescribeClientVpnTargetNetworksRequestRequestTypeDef",
    "DescribeClientVpnTargetNetworksResultTypeDef",
    "DescribeCoipPoolsRequestPaginateTypeDef",
    "DescribeCoipPoolsRequestRequestTypeDef",
    "DescribeCoipPoolsResultTypeDef",
    "DescribeConversionTasksRequestRequestTypeDef",
    "DescribeConversionTasksRequestWaitTypeDef",
    "DescribeConversionTasksResultTypeDef",
    "DescribeCustomerGatewaysRequestRequestTypeDef",
    "DescribeCustomerGatewaysRequestWaitTypeDef",
    "DescribeCustomerGatewaysResultTypeDef",
    "DescribeDeclarativePoliciesReportsRequestRequestTypeDef",
    "DescribeDeclarativePoliciesReportsResultTypeDef",
    "DescribeDhcpOptionsRequestPaginateTypeDef",
    "DescribeDhcpOptionsRequestRequestTypeDef",
    "DescribeDhcpOptionsResultTypeDef",
    "DescribeEgressOnlyInternetGatewaysRequestPaginateTypeDef",
    "DescribeEgressOnlyInternetGatewaysRequestRequestTypeDef",
    "DescribeEgressOnlyInternetGatewaysResultTypeDef",
    "DescribeElasticGpusRequestRequestTypeDef",
    "DescribeElasticGpusResultTypeDef",
    "DescribeExportImageTasksRequestPaginateTypeDef",
    "DescribeExportImageTasksRequestRequestTypeDef",
    "DescribeExportImageTasksResultTypeDef",
    "DescribeExportTasksRequestRequestTypeDef",
    "DescribeExportTasksRequestWaitTypeDef",
    "DescribeExportTasksResultTypeDef",
    "DescribeFastLaunchImagesRequestPaginateTypeDef",
    "DescribeFastLaunchImagesRequestRequestTypeDef",
    "DescribeFastLaunchImagesResultTypeDef",
    "DescribeFastLaunchImagesSuccessItemTypeDef",
    "DescribeFastSnapshotRestoreSuccessItemTypeDef",
    "DescribeFastSnapshotRestoresRequestPaginateTypeDef",
    "DescribeFastSnapshotRestoresRequestRequestTypeDef",
    "DescribeFastSnapshotRestoresResultTypeDef",
    "DescribeFleetErrorTypeDef",
    "DescribeFleetHistoryRequestRequestTypeDef",
    "DescribeFleetHistoryResultTypeDef",
    "DescribeFleetInstancesRequestRequestTypeDef",
    "DescribeFleetInstancesResultTypeDef",
    "DescribeFleetsInstancesTypeDef",
    "DescribeFleetsRequestPaginateTypeDef",
    "DescribeFleetsRequestRequestTypeDef",
    "DescribeFleetsResultTypeDef",
    "DescribeFlowLogsRequestPaginateTypeDef",
    "DescribeFlowLogsRequestRequestTypeDef",
    "DescribeFlowLogsResultTypeDef",
    "DescribeFpgaImageAttributeRequestRequestTypeDef",
    "DescribeFpgaImageAttributeResultTypeDef",
    "DescribeFpgaImagesRequestPaginateTypeDef",
    "DescribeFpgaImagesRequestRequestTypeDef",
    "DescribeFpgaImagesResultTypeDef",
    "DescribeHostReservationOfferingsRequestPaginateTypeDef",
    "DescribeHostReservationOfferingsRequestRequestTypeDef",
    "DescribeHostReservationOfferingsResultTypeDef",
    "DescribeHostReservationsRequestPaginateTypeDef",
    "DescribeHostReservationsRequestRequestTypeDef",
    "DescribeHostReservationsResultTypeDef",
    "DescribeHostsRequestPaginateTypeDef",
    "DescribeHostsRequestRequestTypeDef",
    "DescribeHostsResultTypeDef",
    "DescribeIamInstanceProfileAssociationsRequestPaginateTypeDef",
    "DescribeIamInstanceProfileAssociationsRequestRequestTypeDef",
    "DescribeIamInstanceProfileAssociationsResultTypeDef",
    "DescribeIdFormatRequestRequestTypeDef",
    "DescribeIdFormatResultTypeDef",
    "DescribeIdentityIdFormatRequestRequestTypeDef",
    "DescribeIdentityIdFormatResultTypeDef",
    "DescribeImageAttributeRequestImageDescribeAttributeTypeDef",
    "DescribeImageAttributeRequestRequestTypeDef",
    "DescribeImagesRequestPaginateTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "DescribeImagesRequestWaitTypeDef",
    "DescribeImagesResultTypeDef",
    "DescribeImportImageTasksRequestPaginateTypeDef",
    "DescribeImportImageTasksRequestRequestTypeDef",
    "DescribeImportImageTasksResultTypeDef",
    "DescribeImportSnapshotTasksRequestPaginateTypeDef",
    "DescribeImportSnapshotTasksRequestRequestTypeDef",
    "DescribeImportSnapshotTasksRequestWaitTypeDef",
    "DescribeImportSnapshotTasksResultTypeDef",
    "DescribeInstanceAttributeRequestInstanceDescribeAttributeTypeDef",
    "DescribeInstanceAttributeRequestRequestTypeDef",
    "DescribeInstanceConnectEndpointsRequestPaginateTypeDef",
    "DescribeInstanceConnectEndpointsRequestRequestTypeDef",
    "DescribeInstanceConnectEndpointsResultTypeDef",
    "DescribeInstanceCreditSpecificationsRequestPaginateTypeDef",
    "DescribeInstanceCreditSpecificationsRequestRequestTypeDef",
    "DescribeInstanceCreditSpecificationsResultTypeDef",
    "DescribeInstanceEventNotificationAttributesRequestRequestTypeDef",
    "DescribeInstanceEventNotificationAttributesResultTypeDef",
    "DescribeInstanceEventWindowsRequestPaginateTypeDef",
    "DescribeInstanceEventWindowsRequestRequestTypeDef",
    "DescribeInstanceEventWindowsResultTypeDef",
    "DescribeInstanceImageMetadataRequestPaginateTypeDef",
    "DescribeInstanceImageMetadataRequestRequestTypeDef",
    "DescribeInstanceImageMetadataResultTypeDef",
    "DescribeInstanceStatusRequestPaginateTypeDef",
    "DescribeInstanceStatusRequestRequestTypeDef",
    "DescribeInstanceStatusRequestWaitTypeDef",
    "DescribeInstanceStatusResultTypeDef",
    "DescribeInstanceTopologyRequestPaginateTypeDef",
    "DescribeInstanceTopologyRequestRequestTypeDef",
    "DescribeInstanceTopologyResultTypeDef",
    "DescribeInstanceTypeOfferingsRequestPaginateTypeDef",
    "DescribeInstanceTypeOfferingsRequestRequestTypeDef",
    "DescribeInstanceTypeOfferingsResultTypeDef",
    "DescribeInstanceTypesRequestPaginateTypeDef",
    "DescribeInstanceTypesRequestRequestTypeDef",
    "DescribeInstanceTypesResultTypeDef",
    "DescribeInstancesRequestPaginateTypeDef",
    "DescribeInstancesRequestRequestTypeDef",
    "DescribeInstancesRequestWaitTypeDef",
    "DescribeInstancesResultTypeDef",
    "DescribeInternetGatewaysRequestPaginateTypeDef",
    "DescribeInternetGatewaysRequestRequestTypeDef",
    "DescribeInternetGatewaysRequestWaitTypeDef",
    "DescribeInternetGatewaysResultTypeDef",
    "DescribeIpamByoasnRequestRequestTypeDef",
    "DescribeIpamByoasnResultTypeDef",
    "DescribeIpamExternalResourceVerificationTokensRequestRequestTypeDef",
    "DescribeIpamExternalResourceVerificationTokensResultTypeDef",
    "DescribeIpamPoolsRequestPaginateTypeDef",
    "DescribeIpamPoolsRequestRequestTypeDef",
    "DescribeIpamPoolsResultTypeDef",
    "DescribeIpamResourceDiscoveriesRequestPaginateTypeDef",
    "DescribeIpamResourceDiscoveriesRequestRequestTypeDef",
    "DescribeIpamResourceDiscoveriesResultTypeDef",
    "DescribeIpamResourceDiscoveryAssociationsRequestPaginateTypeDef",
    "DescribeIpamResourceDiscoveryAssociationsRequestRequestTypeDef",
    "DescribeIpamResourceDiscoveryAssociationsResultTypeDef",
    "DescribeIpamScopesRequestPaginateTypeDef",
    "DescribeIpamScopesRequestRequestTypeDef",
    "DescribeIpamScopesResultTypeDef",
    "DescribeIpamsRequestPaginateTypeDef",
    "DescribeIpamsRequestRequestTypeDef",
    "DescribeIpamsResultTypeDef",
    "DescribeIpv6PoolsRequestPaginateTypeDef",
    "DescribeIpv6PoolsRequestRequestTypeDef",
    "DescribeIpv6PoolsResultTypeDef",
    "DescribeKeyPairsRequestRequestTypeDef",
    "DescribeKeyPairsRequestWaitTypeDef",
    "DescribeKeyPairsResultTypeDef",
    "DescribeLaunchTemplateVersionsRequestPaginateTypeDef",
    "DescribeLaunchTemplateVersionsRequestRequestTypeDef",
    "DescribeLaunchTemplateVersionsResultTypeDef",
    "DescribeLaunchTemplatesRequestPaginateTypeDef",
    "DescribeLaunchTemplatesRequestRequestTypeDef",
    "DescribeLaunchTemplatesResultTypeDef",
    "DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestPaginateTypeDef",
    "DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestRequestTypeDef",
    "DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsResultTypeDef",
    "DescribeLocalGatewayRouteTableVpcAssociationsRequestPaginateTypeDef",
    "DescribeLocalGatewayRouteTableVpcAssociationsRequestRequestTypeDef",
    "DescribeLocalGatewayRouteTableVpcAssociationsResultTypeDef",
    "DescribeLocalGatewayRouteTablesRequestPaginateTypeDef",
    "DescribeLocalGatewayRouteTablesRequestRequestTypeDef",
    "DescribeLocalGatewayRouteTablesResultTypeDef",
    "DescribeLocalGatewayVirtualInterfaceGroupsRequestPaginateTypeDef",
    "DescribeLocalGatewayVirtualInterfaceGroupsRequestRequestTypeDef",
    "DescribeLocalGatewayVirtualInterfaceGroupsResultTypeDef",
    "DescribeLocalGatewayVirtualInterfacesRequestPaginateTypeDef",
    "DescribeLocalGatewayVirtualInterfacesRequestRequestTypeDef",
    "DescribeLocalGatewayVirtualInterfacesResultTypeDef",
    "DescribeLocalGatewaysRequestPaginateTypeDef",
    "DescribeLocalGatewaysRequestRequestTypeDef",
    "DescribeLocalGatewaysResultTypeDef",
    "DescribeLockedSnapshotsRequestRequestTypeDef",
    "DescribeLockedSnapshotsResultTypeDef",
    "DescribeMacHostsRequestPaginateTypeDef",
    "DescribeMacHostsRequestRequestTypeDef",
    "DescribeMacHostsResultTypeDef",
    "DescribeManagedPrefixListsRequestPaginateTypeDef",
    "DescribeManagedPrefixListsRequestRequestTypeDef",
    "DescribeManagedPrefixListsResultTypeDef",
    "DescribeMovingAddressesRequestPaginateTypeDef",
    "DescribeMovingAddressesRequestRequestTypeDef",
    "DescribeMovingAddressesResultTypeDef",
    "DescribeNatGatewaysRequestPaginateTypeDef",
    "DescribeNatGatewaysRequestRequestTypeDef",
    "DescribeNatGatewaysRequestWaitTypeDef",
    "DescribeNatGatewaysResultTypeDef",
    "DescribeNetworkAclsRequestPaginateTypeDef",
    "DescribeNetworkAclsRequestRequestTypeDef",
    "DescribeNetworkAclsResultTypeDef",
    "DescribeNetworkInsightsAccessScopeAnalysesRequestPaginateTypeDef",
    "DescribeNetworkInsightsAccessScopeAnalysesRequestRequestTypeDef",
    "DescribeNetworkInsightsAccessScopeAnalysesResultTypeDef",
    "DescribeNetworkInsightsAccessScopesRequestPaginateTypeDef",
    "DescribeNetworkInsightsAccessScopesRequestRequestTypeDef",
    "DescribeNetworkInsightsAccessScopesResultTypeDef",
    "DescribeNetworkInsightsAnalysesRequestPaginateTypeDef",
    "DescribeNetworkInsightsAnalysesRequestRequestTypeDef",
    "DescribeNetworkInsightsAnalysesResultTypeDef",
    "DescribeNetworkInsightsPathsRequestPaginateTypeDef",
    "DescribeNetworkInsightsPathsRequestRequestTypeDef",
    "DescribeNetworkInsightsPathsResultTypeDef",
    "DescribeNetworkInterfaceAttributeRequestNetworkInterfaceDescribeAttributeTypeDef",
    "DescribeNetworkInterfaceAttributeRequestRequestTypeDef",
    "DescribeNetworkInterfaceAttributeResultTypeDef",
    "DescribeNetworkInterfacePermissionsRequestPaginateTypeDef",
    "DescribeNetworkInterfacePermissionsRequestRequestTypeDef",
    "DescribeNetworkInterfacePermissionsResultTypeDef",
    "DescribeNetworkInterfacesRequestPaginateTypeDef",
    "DescribeNetworkInterfacesRequestRequestTypeDef",
    "DescribeNetworkInterfacesRequestWaitTypeDef",
    "DescribeNetworkInterfacesResultTypeDef",
    "DescribePlacementGroupsRequestRequestTypeDef",
    "DescribePlacementGroupsResultTypeDef",
    "DescribePrefixListsRequestPaginateTypeDef",
    "DescribePrefixListsRequestRequestTypeDef",
    "DescribePrefixListsResultTypeDef",
    "DescribePrincipalIdFormatRequestPaginateTypeDef",
    "DescribePrincipalIdFormatRequestRequestTypeDef",
    "DescribePrincipalIdFormatResultTypeDef",
    "DescribePublicIpv4PoolsRequestPaginateTypeDef",
    "DescribePublicIpv4PoolsRequestRequestTypeDef",
    "DescribePublicIpv4PoolsResultTypeDef",
    "DescribeRegionsRequestRequestTypeDef",
    "DescribeRegionsResultTypeDef",
    "DescribeReplaceRootVolumeTasksRequestPaginateTypeDef",
    "DescribeReplaceRootVolumeTasksRequestRequestTypeDef",
    "DescribeReplaceRootVolumeTasksResultTypeDef",
    "DescribeReservedInstancesListingsRequestRequestTypeDef",
    "DescribeReservedInstancesListingsResultTypeDef",
    "DescribeReservedInstancesModificationsRequestPaginateTypeDef",
    "DescribeReservedInstancesModificationsRequestRequestTypeDef",
    "DescribeReservedInstancesModificationsResultTypeDef",
    "DescribeReservedInstancesOfferingsRequestPaginateTypeDef",
    "DescribeReservedInstancesOfferingsRequestRequestTypeDef",
    "DescribeReservedInstancesOfferingsResultTypeDef",
    "DescribeReservedInstancesRequestRequestTypeDef",
    "DescribeReservedInstancesResultTypeDef",
    "DescribeRouteTablesRequestPaginateTypeDef",
    "DescribeRouteTablesRequestRequestTypeDef",
    "DescribeRouteTablesResultTypeDef",
    "DescribeScheduledInstanceAvailabilityRequestPaginateTypeDef",
    "DescribeScheduledInstanceAvailabilityRequestRequestTypeDef",
    "DescribeScheduledInstanceAvailabilityResultTypeDef",
    "DescribeScheduledInstancesRequestPaginateTypeDef",
    "DescribeScheduledInstancesRequestRequestTypeDef",
    "DescribeScheduledInstancesResultTypeDef",
    "DescribeSecurityGroupReferencesRequestRequestTypeDef",
    "DescribeSecurityGroupReferencesResultTypeDef",
    "DescribeSecurityGroupRulesRequestPaginateTypeDef",
    "DescribeSecurityGroupRulesRequestRequestTypeDef",
    "DescribeSecurityGroupRulesResultTypeDef",
    "DescribeSecurityGroupVpcAssociationsRequestPaginateTypeDef",
    "DescribeSecurityGroupVpcAssociationsRequestRequestTypeDef",
    "DescribeSecurityGroupVpcAssociationsResultTypeDef",
    "DescribeSecurityGroupsRequestPaginateTypeDef",
    "DescribeSecurityGroupsRequestRequestTypeDef",
    "DescribeSecurityGroupsRequestWaitTypeDef",
    "DescribeSecurityGroupsResultTypeDef",
    "DescribeSnapshotAttributeRequestRequestTypeDef",
    "DescribeSnapshotAttributeRequestSnapshotDescribeAttributeTypeDef",
    "DescribeSnapshotAttributeResultTypeDef",
    "DescribeSnapshotTierStatusRequestPaginateTypeDef",
    "DescribeSnapshotTierStatusRequestRequestTypeDef",
    "DescribeSnapshotTierStatusResultTypeDef",
    "DescribeSnapshotsRequestPaginateTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "DescribeSnapshotsRequestWaitTypeDef",
    "DescribeSnapshotsResultTypeDef",
    "DescribeSpotDatafeedSubscriptionRequestRequestTypeDef",
    "DescribeSpotDatafeedSubscriptionResultTypeDef",
    "DescribeSpotFleetInstancesRequestPaginateTypeDef",
    "DescribeSpotFleetInstancesRequestRequestTypeDef",
    "DescribeSpotFleetInstancesResponseTypeDef",
    "DescribeSpotFleetRequestHistoryRequestRequestTypeDef",
    "DescribeSpotFleetRequestHistoryResponseTypeDef",
    "DescribeSpotFleetRequestsRequestPaginateTypeDef",
    "DescribeSpotFleetRequestsRequestRequestTypeDef",
    "DescribeSpotFleetRequestsResponseTypeDef",
    "DescribeSpotInstanceRequestsRequestPaginateTypeDef",
    "DescribeSpotInstanceRequestsRequestRequestTypeDef",
    "DescribeSpotInstanceRequestsRequestWaitTypeDef",
    "DescribeSpotInstanceRequestsResultTypeDef",
    "DescribeSpotPriceHistoryRequestPaginateTypeDef",
    "DescribeSpotPriceHistoryRequestRequestTypeDef",
    "DescribeSpotPriceHistoryResultTypeDef",
    "DescribeStaleSecurityGroupsRequestPaginateTypeDef",
    "DescribeStaleSecurityGroupsRequestRequestTypeDef",
    "DescribeStaleSecurityGroupsResultTypeDef",
    "DescribeStoreImageTasksRequestPaginateTypeDef",
    "DescribeStoreImageTasksRequestRequestTypeDef",
    "DescribeStoreImageTasksRequestWaitTypeDef",
    "DescribeStoreImageTasksResultTypeDef",
    "DescribeSubnetsRequestPaginateTypeDef",
    "DescribeSubnetsRequestRequestTypeDef",
    "DescribeSubnetsRequestWaitTypeDef",
    "DescribeSubnetsResultTypeDef",
    "DescribeTagsRequestPaginateTypeDef",
    "DescribeTagsRequestRequestTypeDef",
    "DescribeTagsResultTypeDef",
    "DescribeTrafficMirrorFilterRulesRequestRequestTypeDef",
    "DescribeTrafficMirrorFilterRulesResultTypeDef",
    "DescribeTrafficMirrorFiltersRequestPaginateTypeDef",
    "DescribeTrafficMirrorFiltersRequestRequestTypeDef",
    "DescribeTrafficMirrorFiltersResultTypeDef",
    "DescribeTrafficMirrorSessionsRequestPaginateTypeDef",
    "DescribeTrafficMirrorSessionsRequestRequestTypeDef",
    "DescribeTrafficMirrorSessionsResultTypeDef",
    "DescribeTrafficMirrorTargetsRequestPaginateTypeDef",
    "DescribeTrafficMirrorTargetsRequestRequestTypeDef",
    "DescribeTrafficMirrorTargetsResultTypeDef",
    "DescribeTransitGatewayAttachmentsRequestPaginateTypeDef",
    "DescribeTransitGatewayAttachmentsRequestRequestTypeDef",
    "DescribeTransitGatewayAttachmentsResultTypeDef",
    "DescribeTransitGatewayConnectPeersRequestPaginateTypeDef",
    "DescribeTransitGatewayConnectPeersRequestRequestTypeDef",
    "DescribeTransitGatewayConnectPeersResultTypeDef",
    "DescribeTransitGatewayConnectsRequestPaginateTypeDef",
    "DescribeTransitGatewayConnectsRequestRequestTypeDef",
    "DescribeTransitGatewayConnectsResultTypeDef",
    "DescribeTransitGatewayMulticastDomainsRequestPaginateTypeDef",
    "DescribeTransitGatewayMulticastDomainsRequestRequestTypeDef",
    "DescribeTransitGatewayMulticastDomainsResultTypeDef",
    "DescribeTransitGatewayPeeringAttachmentsRequestPaginateTypeDef",
    "DescribeTransitGatewayPeeringAttachmentsRequestRequestTypeDef",
    "DescribeTransitGatewayPeeringAttachmentsResultTypeDef",
    "DescribeTransitGatewayPolicyTablesRequestPaginateTypeDef",
    "DescribeTransitGatewayPolicyTablesRequestRequestTypeDef",
    "DescribeTransitGatewayPolicyTablesResultTypeDef",
    "DescribeTransitGatewayRouteTableAnnouncementsRequestPaginateTypeDef",
    "DescribeTransitGatewayRouteTableAnnouncementsRequestRequestTypeDef",
    "DescribeTransitGatewayRouteTableAnnouncementsResultTypeDef",
    "DescribeTransitGatewayRouteTablesRequestPaginateTypeDef",
    "DescribeTransitGatewayRouteTablesRequestRequestTypeDef",
    "DescribeTransitGatewayRouteTablesResultTypeDef",
    "DescribeTransitGatewayVpcAttachmentsRequestPaginateTypeDef",
    "DescribeTransitGatewayVpcAttachmentsRequestRequestTypeDef",
    "DescribeTransitGatewayVpcAttachmentsResultTypeDef",
    "DescribeTransitGatewaysRequestPaginateTypeDef",
    "DescribeTransitGatewaysRequestRequestTypeDef",
    "DescribeTransitGatewaysResultTypeDef",
    "DescribeTrunkInterfaceAssociationsRequestPaginateTypeDef",
    "DescribeTrunkInterfaceAssociationsRequestRequestTypeDef",
    "DescribeTrunkInterfaceAssociationsResultTypeDef",
    "DescribeVerifiedAccessEndpointsRequestPaginateTypeDef",
    "DescribeVerifiedAccessEndpointsRequestRequestTypeDef",
    "DescribeVerifiedAccessEndpointsResultTypeDef",
    "DescribeVerifiedAccessGroupsRequestPaginateTypeDef",
    "DescribeVerifiedAccessGroupsRequestRequestTypeDef",
    "DescribeVerifiedAccessGroupsResultTypeDef",
    "DescribeVerifiedAccessInstanceLoggingConfigurationsRequestPaginateTypeDef",
    "DescribeVerifiedAccessInstanceLoggingConfigurationsRequestRequestTypeDef",
    "DescribeVerifiedAccessInstanceLoggingConfigurationsResultTypeDef",
    "DescribeVerifiedAccessInstancesRequestPaginateTypeDef",
    "DescribeVerifiedAccessInstancesRequestRequestTypeDef",
    "DescribeVerifiedAccessInstancesResultTypeDef",
    "DescribeVerifiedAccessTrustProvidersRequestPaginateTypeDef",
    "DescribeVerifiedAccessTrustProvidersRequestRequestTypeDef",
    "DescribeVerifiedAccessTrustProvidersResultTypeDef",
    "DescribeVolumeAttributeRequestRequestTypeDef",
    "DescribeVolumeAttributeRequestVolumeDescribeAttributeTypeDef",
    "DescribeVolumeAttributeResultTypeDef",
    "DescribeVolumeStatusRequestPaginateTypeDef",
    "DescribeVolumeStatusRequestRequestTypeDef",
    "DescribeVolumeStatusRequestVolumeDescribeStatusTypeDef",
    "DescribeVolumeStatusResultTypeDef",
    "DescribeVolumesModificationsRequestPaginateTypeDef",
    "DescribeVolumesModificationsRequestRequestTypeDef",
    "DescribeVolumesModificationsResultTypeDef",
    "DescribeVolumesRequestPaginateTypeDef",
    "DescribeVolumesRequestRequestTypeDef",
    "DescribeVolumesRequestWaitTypeDef",
    "DescribeVolumesResultTypeDef",
    "DescribeVpcAttributeRequestRequestTypeDef",
    "DescribeVpcAttributeRequestVpcDescribeAttributeTypeDef",
    "DescribeVpcAttributeResultTypeDef",
    "DescribeVpcBlockPublicAccessExclusionsRequestRequestTypeDef",
    "DescribeVpcBlockPublicAccessExclusionsResultTypeDef",
    "DescribeVpcBlockPublicAccessOptionsRequestRequestTypeDef",
    "DescribeVpcBlockPublicAccessOptionsResultTypeDef",
    "DescribeVpcClassicLinkDnsSupportRequestPaginateTypeDef",
    "DescribeVpcClassicLinkDnsSupportRequestRequestTypeDef",
    "DescribeVpcClassicLinkDnsSupportResultTypeDef",
    "DescribeVpcClassicLinkRequestRequestTypeDef",
    "DescribeVpcClassicLinkResultTypeDef",
    "DescribeVpcEndpointAssociationsRequestRequestTypeDef",
    "DescribeVpcEndpointAssociationsResultTypeDef",
    "DescribeVpcEndpointConnectionNotificationsRequestPaginateTypeDef",
    "DescribeVpcEndpointConnectionNotificationsRequestRequestTypeDef",
    "DescribeVpcEndpointConnectionNotificationsResultTypeDef",
    "DescribeVpcEndpointConnectionsRequestPaginateTypeDef",
    "DescribeVpcEndpointConnectionsRequestRequestTypeDef",
    "DescribeVpcEndpointConnectionsResultTypeDef",
    "DescribeVpcEndpointServiceConfigurationsRequestPaginateTypeDef",
    "DescribeVpcEndpointServiceConfigurationsRequestRequestTypeDef",
    "DescribeVpcEndpointServiceConfigurationsResultTypeDef",
    "DescribeVpcEndpointServicePermissionsRequestPaginateTypeDef",
    "DescribeVpcEndpointServicePermissionsRequestRequestTypeDef",
    "DescribeVpcEndpointServicePermissionsResultTypeDef",
    "DescribeVpcEndpointServicesRequestPaginateTypeDef",
    "DescribeVpcEndpointServicesRequestRequestTypeDef",
    "DescribeVpcEndpointServicesResultTypeDef",
    "DescribeVpcEndpointsRequestPaginateTypeDef",
    "DescribeVpcEndpointsRequestRequestTypeDef",
    "DescribeVpcEndpointsResultTypeDef",
    "DescribeVpcPeeringConnectionsRequestPaginateTypeDef",
    "DescribeVpcPeeringConnectionsRequestRequestTypeDef",
    "DescribeVpcPeeringConnectionsRequestWaitTypeDef",
    "DescribeVpcPeeringConnectionsResultTypeDef",
    "DescribeVpcsRequestPaginateTypeDef",
    "DescribeVpcsRequestRequestTypeDef",
    "DescribeVpcsRequestWaitTypeDef",
    "DescribeVpcsResultTypeDef",
    "DescribeVpnConnectionsRequestRequestTypeDef",
    "DescribeVpnConnectionsRequestWaitTypeDef",
    "DescribeVpnConnectionsResultTypeDef",
    "DescribeVpnGatewaysRequestRequestTypeDef",
    "DescribeVpnGatewaysResultTypeDef",
    "DestinationOptionsRequestTypeDef",
    "DestinationOptionsResponseTypeDef",
    "DetachClassicLinkVpcRequestInstanceDetachClassicLinkVpcTypeDef",
    "DetachClassicLinkVpcRequestRequestTypeDef",
    "DetachClassicLinkVpcRequestVpcDetachClassicLinkInstanceTypeDef",
    "DetachClassicLinkVpcResultTypeDef",
    "DetachInternetGatewayRequestInternetGatewayDetachFromVpcTypeDef",
    "DetachInternetGatewayRequestRequestTypeDef",
    "DetachInternetGatewayRequestVpcDetachInternetGatewayTypeDef",
    "DetachNetworkInterfaceRequestNetworkInterfaceDetachTypeDef",
    "DetachNetworkInterfaceRequestRequestTypeDef",
    "DetachVerifiedAccessTrustProviderRequestRequestTypeDef",
    "DetachVerifiedAccessTrustProviderResultTypeDef",
    "DetachVolumeRequestInstanceDetachVolumeTypeDef",
    "DetachVolumeRequestRequestTypeDef",
    "DetachVolumeRequestVolumeDetachFromInstanceTypeDef",
    "DetachVpnGatewayRequestRequestTypeDef",
    "DeviceOptionsTypeDef",
    "DhcpConfigurationTypeDef",
    "DhcpOptionsTypeDef",
    "DirectoryServiceAuthenticationRequestTypeDef",
    "DirectoryServiceAuthenticationTypeDef",
    "DisableAddressTransferRequestRequestTypeDef",
    "DisableAddressTransferResultTypeDef",
    "DisableAllowedImagesSettingsRequestRequestTypeDef",
    "DisableAllowedImagesSettingsResultTypeDef",
    "DisableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef",
    "DisableAwsNetworkPerformanceMetricSubscriptionResultTypeDef",
    "DisableEbsEncryptionByDefaultRequestRequestTypeDef",
    "DisableEbsEncryptionByDefaultResultTypeDef",
    "DisableFastLaunchRequestRequestTypeDef",
    "DisableFastLaunchResultTypeDef",
    "DisableFastSnapshotRestoreErrorItemTypeDef",
    "DisableFastSnapshotRestoreStateErrorItemTypeDef",
    "DisableFastSnapshotRestoreStateErrorTypeDef",
    "DisableFastSnapshotRestoreSuccessItemTypeDef",
    "DisableFastSnapshotRestoresRequestRequestTypeDef",
    "DisableFastSnapshotRestoresResultTypeDef",
    "DisableImageBlockPublicAccessRequestRequestTypeDef",
    "DisableImageBlockPublicAccessResultTypeDef",
    "DisableImageDeprecationRequestRequestTypeDef",
    "DisableImageDeprecationResultTypeDef",
    "DisableImageDeregistrationProtectionRequestRequestTypeDef",
    "DisableImageDeregistrationProtectionResultTypeDef",
    "DisableImageRequestRequestTypeDef",
    "DisableImageResultTypeDef",
    "DisableIpamOrganizationAdminAccountRequestRequestTypeDef",
    "DisableIpamOrganizationAdminAccountResultTypeDef",
    "DisableSerialConsoleAccessRequestRequestTypeDef",
    "DisableSerialConsoleAccessResultTypeDef",
    "DisableSnapshotBlockPublicAccessRequestRequestTypeDef",
    "DisableSnapshotBlockPublicAccessResultTypeDef",
    "DisableTransitGatewayRouteTablePropagationRequestRequestTypeDef",
    "DisableTransitGatewayRouteTablePropagationResultTypeDef",
    "DisableVgwRoutePropagationRequestRequestTypeDef",
    "DisableVpcClassicLinkDnsSupportRequestRequestTypeDef",
    "DisableVpcClassicLinkDnsSupportResultTypeDef",
    "DisableVpcClassicLinkRequestRequestTypeDef",
    "DisableVpcClassicLinkRequestVpcDisableClassicLinkTypeDef",
    "DisableVpcClassicLinkResultTypeDef",
    "DisassociateAddressRequestClassicAddressDisassociateTypeDef",
    "DisassociateAddressRequestNetworkInterfaceAssociationDeleteTypeDef",
    "DisassociateAddressRequestRequestTypeDef",
    "DisassociateCapacityReservationBillingOwnerRequestRequestTypeDef",
    "DisassociateCapacityReservationBillingOwnerResultTypeDef",
    "DisassociateClientVpnTargetNetworkRequestRequestTypeDef",
    "DisassociateClientVpnTargetNetworkResultTypeDef",
    "DisassociateEnclaveCertificateIamRoleRequestRequestTypeDef",
    "DisassociateEnclaveCertificateIamRoleResultTypeDef",
    "DisassociateIamInstanceProfileRequestRequestTypeDef",
    "DisassociateIamInstanceProfileResultTypeDef",
    "DisassociateInstanceEventWindowRequestRequestTypeDef",
    "DisassociateInstanceEventWindowResultTypeDef",
    "DisassociateIpamByoasnRequestRequestTypeDef",
    "DisassociateIpamByoasnResultTypeDef",
    "DisassociateIpamResourceDiscoveryRequestRequestTypeDef",
    "DisassociateIpamResourceDiscoveryResultTypeDef",
    "DisassociateNatGatewayAddressRequestRequestTypeDef",
    "DisassociateNatGatewayAddressResultTypeDef",
    "DisassociateRouteTableRequestRequestTypeDef",
    "DisassociateRouteTableRequestRouteTableAssociationDeleteTypeDef",
    "DisassociateRouteTableRequestServiceResourceDisassociateRouteTableTypeDef",
    "DisassociateSecurityGroupVpcRequestRequestTypeDef",
    "DisassociateSecurityGroupVpcResultTypeDef",
    "DisassociateSubnetCidrBlockRequestRequestTypeDef",
    "DisassociateSubnetCidrBlockResultTypeDef",
    "DisassociateTransitGatewayMulticastDomainRequestRequestTypeDef",
    "DisassociateTransitGatewayMulticastDomainResultTypeDef",
    "DisassociateTransitGatewayPolicyTableRequestRequestTypeDef",
    "DisassociateTransitGatewayPolicyTableResultTypeDef",
    "DisassociateTransitGatewayRouteTableRequestRequestTypeDef",
    "DisassociateTransitGatewayRouteTableResultTypeDef",
    "DisassociateTrunkInterfaceRequestRequestTypeDef",
    "DisassociateTrunkInterfaceResultTypeDef",
    "DisassociateVpcCidrBlockRequestRequestTypeDef",
    "DisassociateVpcCidrBlockResultTypeDef",
    "DiskImageDescriptionTypeDef",
    "DiskImageDetailTypeDef",
    "DiskImageTypeDef",
    "DiskImageVolumeDescriptionTypeDef",
    "DiskInfoTypeDef",
    "DnsEntryTypeDef",
    "DnsOptionsSpecificationTypeDef",
    "DnsOptionsTypeDef",
    "DnsServersOptionsModifyStructureTypeDef",
    "EbsBlockDeviceTypeDef",
    "EbsInfoTypeDef",
    "EbsInstanceBlockDeviceSpecificationTypeDef",
    "EbsInstanceBlockDeviceTypeDef",
    "EbsOptimizedInfoTypeDef",
    "EbsStatusDetailsTypeDef",
    "EbsStatusSummaryTypeDef",
    "Ec2InstanceConnectEndpointTypeDef",
    "EfaInfoTypeDef",
    "EgressOnlyInternetGatewayTypeDef",
    "ElasticGpuAssociationTypeDef",
    "ElasticGpuHealthTypeDef",
    "ElasticGpuSpecificationResponseTypeDef",
    "ElasticGpuSpecificationTypeDef",
    "ElasticGpusTypeDef",
    "ElasticInferenceAcceleratorAssociationTypeDef",
    "ElasticInferenceAcceleratorTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnaSrdSpecificationRequestTypeDef",
    "EnaSrdSpecificationTypeDef",
    "EnaSrdUdpSpecificationRequestTypeDef",
    "EnaSrdUdpSpecificationTypeDef",
    "EnableAddressTransferRequestRequestTypeDef",
    "EnableAddressTransferResultTypeDef",
    "EnableAllowedImagesSettingsRequestRequestTypeDef",
    "EnableAllowedImagesSettingsResultTypeDef",
    "EnableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef",
    "EnableAwsNetworkPerformanceMetricSubscriptionResultTypeDef",
    "EnableEbsEncryptionByDefaultRequestRequestTypeDef",
    "EnableEbsEncryptionByDefaultResultTypeDef",
    "EnableFastLaunchRequestRequestTypeDef",
    "EnableFastLaunchResultTypeDef",
    "EnableFastSnapshotRestoreErrorItemTypeDef",
    "EnableFastSnapshotRestoreStateErrorItemTypeDef",
    "EnableFastSnapshotRestoreStateErrorTypeDef",
    "EnableFastSnapshotRestoreSuccessItemTypeDef",
    "EnableFastSnapshotRestoresRequestRequestTypeDef",
    "EnableFastSnapshotRestoresResultTypeDef",
    "EnableImageBlockPublicAccessRequestRequestTypeDef",
    "EnableImageBlockPublicAccessResultTypeDef",
    "EnableImageDeprecationRequestRequestTypeDef",
    "EnableImageDeprecationResultTypeDef",
    "EnableImageDeregistrationProtectionRequestRequestTypeDef",
    "EnableImageDeregistrationProtectionResultTypeDef",
    "EnableImageRequestRequestTypeDef",
    "EnableImageResultTypeDef",
    "EnableIpamOrganizationAdminAccountRequestRequestTypeDef",
    "EnableIpamOrganizationAdminAccountResultTypeDef",
    "EnableReachabilityAnalyzerOrganizationSharingRequestRequestTypeDef",
    "EnableReachabilityAnalyzerOrganizationSharingResultTypeDef",
    "EnableSerialConsoleAccessRequestRequestTypeDef",
    "EnableSerialConsoleAccessResultTypeDef",
    "EnableSnapshotBlockPublicAccessRequestRequestTypeDef",
    "EnableSnapshotBlockPublicAccessResultTypeDef",
    "EnableTransitGatewayRouteTablePropagationRequestRequestTypeDef",
    "EnableTransitGatewayRouteTablePropagationResultTypeDef",
    "EnableVgwRoutePropagationRequestRequestTypeDef",
    "EnableVolumeIORequestRequestTypeDef",
    "EnableVolumeIORequestVolumeEnableIoTypeDef",
    "EnableVpcClassicLinkDnsSupportRequestRequestTypeDef",
    "EnableVpcClassicLinkDnsSupportResultTypeDef",
    "EnableVpcClassicLinkRequestRequestTypeDef",
    "EnableVpcClassicLinkRequestVpcEnableClassicLinkTypeDef",
    "EnableVpcClassicLinkResultTypeDef",
    "EnclaveOptionsRequestTypeDef",
    "EnclaveOptionsTypeDef",
    "EventInformationTypeDef",
    "ExplanationTypeDef",
    "ExportClientVpnClientCertificateRevocationListRequestRequestTypeDef",
    "ExportClientVpnClientCertificateRevocationListResultTypeDef",
    "ExportClientVpnClientConfigurationRequestRequestTypeDef",
    "ExportClientVpnClientConfigurationResultTypeDef",
    "ExportImageRequestRequestTypeDef",
    "ExportImageResultTypeDef",
    "ExportImageTaskTypeDef",
    "ExportTaskS3LocationRequestTypeDef",
    "ExportTaskS3LocationTypeDef",
    "ExportTaskTypeDef",
    "ExportToS3TaskSpecificationTypeDef",
    "ExportToS3TaskTypeDef",
    "ExportTransitGatewayRoutesRequestRequestTypeDef",
    "ExportTransitGatewayRoutesResultTypeDef",
    "ExportVerifiedAccessInstanceClientConfigurationRequestRequestTypeDef",
    "ExportVerifiedAccessInstanceClientConfigurationResultTypeDef",
    "FailedCapacityReservationFleetCancellationResultTypeDef",
    "FailedQueuedPurchaseDeletionTypeDef",
    "FastLaunchLaunchTemplateSpecificationRequestTypeDef",
    "FastLaunchLaunchTemplateSpecificationResponseTypeDef",
    "FastLaunchSnapshotConfigurationRequestTypeDef",
    "FastLaunchSnapshotConfigurationResponseTypeDef",
    "FederatedAuthenticationRequestTypeDef",
    "FederatedAuthenticationTypeDef",
    "FilterPortRangeTypeDef",
    "FilterTypeDef",
    "FirewallStatefulRuleTypeDef",
    "FirewallStatelessRuleTypeDef",
    "FleetCapacityReservationTypeDef",
    "FleetDataTypeDef",
    "FleetLaunchTemplateConfigRequestTypeDef",
    "FleetLaunchTemplateConfigTypeDef",
    "FleetLaunchTemplateOverridesRequestTypeDef",
    "FleetLaunchTemplateOverridesTypeDef",
    "FleetLaunchTemplateSpecificationRequestTypeDef",
    "FleetLaunchTemplateSpecificationTypeDef",
    "FleetSpotCapacityRebalanceRequestTypeDef",
    "FleetSpotCapacityRebalanceTypeDef",
    "FleetSpotMaintenanceStrategiesRequestTypeDef",
    "FleetSpotMaintenanceStrategiesTypeDef",
    "FlowLogTypeDef",
    "FpgaDeviceInfoTypeDef",
    "FpgaDeviceMemoryInfoTypeDef",
    "FpgaImageAttributeTypeDef",
    "FpgaImageStateTypeDef",
    "FpgaImageTypeDef",
    "FpgaInfoTypeDef",
    "GetAllowedImagesSettingsRequestRequestTypeDef",
    "GetAllowedImagesSettingsResultTypeDef",
    "GetAssociatedEnclaveCertificateIamRolesRequestRequestTypeDef",
    "GetAssociatedEnclaveCertificateIamRolesResultTypeDef",
    "GetAssociatedIpv6PoolCidrsRequestPaginateTypeDef",
    "GetAssociatedIpv6PoolCidrsRequestRequestTypeDef",
    "GetAssociatedIpv6PoolCidrsResultTypeDef",
    "GetAwsNetworkPerformanceDataRequestPaginateTypeDef",
    "GetAwsNetworkPerformanceDataRequestRequestTypeDef",
    "GetAwsNetworkPerformanceDataResultTypeDef",
    "GetCapacityReservationUsageRequestRequestTypeDef",
    "GetCapacityReservationUsageResultTypeDef",
    "GetCoipPoolUsageRequestRequestTypeDef",
    "GetCoipPoolUsageResultTypeDef",
    "GetConsoleOutputRequestInstanceConsoleOutputTypeDef",
    "GetConsoleOutputRequestRequestTypeDef",
    "GetConsoleOutputResultTypeDef",
    "GetConsoleScreenshotRequestRequestTypeDef",
    "GetConsoleScreenshotResultTypeDef",
    "GetDeclarativePoliciesReportSummaryRequestRequestTypeDef",
    "GetDeclarativePoliciesReportSummaryResultTypeDef",
    "GetDefaultCreditSpecificationRequestRequestTypeDef",
    "GetDefaultCreditSpecificationResultTypeDef",
    "GetEbsDefaultKmsKeyIdRequestRequestTypeDef",
    "GetEbsDefaultKmsKeyIdResultTypeDef",
    "GetEbsEncryptionByDefaultRequestRequestTypeDef",
    "GetEbsEncryptionByDefaultResultTypeDef",
    "GetFlowLogsIntegrationTemplateRequestRequestTypeDef",
    "GetFlowLogsIntegrationTemplateResultTypeDef",
    "GetGroupsForCapacityReservationRequestPaginateTypeDef",
    "GetGroupsForCapacityReservationRequestRequestTypeDef",
    "GetGroupsForCapacityReservationResultTypeDef",
    "GetHostReservationPurchasePreviewRequestRequestTypeDef",
    "GetHostReservationPurchasePreviewResultTypeDef",
    "GetImageBlockPublicAccessStateRequestRequestTypeDef",
    "GetImageBlockPublicAccessStateResultTypeDef",
    "GetInstanceMetadataDefaultsRequestRequestTypeDef",
    "GetInstanceMetadataDefaultsResultTypeDef",
    "GetInstanceTpmEkPubRequestRequestTypeDef",
    "GetInstanceTpmEkPubResultTypeDef",
    "GetInstanceTypesFromInstanceRequirementsRequestPaginateTypeDef",
    "GetInstanceTypesFromInstanceRequirementsRequestRequestTypeDef",
    "GetInstanceTypesFromInstanceRequirementsResultTypeDef",
    "GetInstanceUefiDataRequestRequestTypeDef",
    "GetInstanceUefiDataResultTypeDef",
    "GetIpamAddressHistoryRequestPaginateTypeDef",
    "GetIpamAddressHistoryRequestRequestTypeDef",
    "GetIpamAddressHistoryResultTypeDef",
    "GetIpamDiscoveredAccountsRequestPaginateTypeDef",
    "GetIpamDiscoveredAccountsRequestRequestTypeDef",
    "GetIpamDiscoveredAccountsResultTypeDef",
    "GetIpamDiscoveredPublicAddressesRequestRequestTypeDef",
    "GetIpamDiscoveredPublicAddressesResultTypeDef",
    "GetIpamDiscoveredResourceCidrsRequestPaginateTypeDef",
    "GetIpamDiscoveredResourceCidrsRequestRequestTypeDef",
    "GetIpamDiscoveredResourceCidrsResultTypeDef",
    "GetIpamPoolAllocationsRequestPaginateTypeDef",
    "GetIpamPoolAllocationsRequestRequestTypeDef",
    "GetIpamPoolAllocationsResultTypeDef",
    "GetIpamPoolCidrsRequestPaginateTypeDef",
    "GetIpamPoolCidrsRequestRequestTypeDef",
    "GetIpamPoolCidrsResultTypeDef",
    "GetIpamResourceCidrsRequestPaginateTypeDef",
    "GetIpamResourceCidrsRequestRequestTypeDef",
    "GetIpamResourceCidrsResultTypeDef",
    "GetLaunchTemplateDataRequestRequestTypeDef",
    "GetLaunchTemplateDataResultTypeDef",
    "GetManagedPrefixListAssociationsRequestPaginateTypeDef",
    "GetManagedPrefixListAssociationsRequestRequestTypeDef",
    "GetManagedPrefixListAssociationsResultTypeDef",
    "GetManagedPrefixListEntriesRequestPaginateTypeDef",
    "GetManagedPrefixListEntriesRequestRequestTypeDef",
    "GetManagedPrefixListEntriesResultTypeDef",
    "GetNetworkInsightsAccessScopeAnalysisFindingsRequestPaginateTypeDef",
    "GetNetworkInsightsAccessScopeAnalysisFindingsRequestRequestTypeDef",
    "GetNetworkInsightsAccessScopeAnalysisFindingsResultTypeDef",
    "GetNetworkInsightsAccessScopeContentRequestRequestTypeDef",
    "GetNetworkInsightsAccessScopeContentResultTypeDef",
    "GetPasswordDataRequestInstancePasswordDataTypeDef",
    "GetPasswordDataRequestRequestTypeDef",
    "GetPasswordDataRequestWaitTypeDef",
    "GetPasswordDataResultTypeDef",
    "GetReservedInstancesExchangeQuoteRequestRequestTypeDef",
    "GetReservedInstancesExchangeQuoteResultTypeDef",
    "GetSecurityGroupsForVpcRequestPaginateTypeDef",
    "GetSecurityGroupsForVpcRequestRequestTypeDef",
    "GetSecurityGroupsForVpcResultTypeDef",
    "GetSerialConsoleAccessStatusRequestRequestTypeDef",
    "GetSerialConsoleAccessStatusResultTypeDef",
    "GetSnapshotBlockPublicAccessStateRequestRequestTypeDef",
    "GetSnapshotBlockPublicAccessStateResultTypeDef",
    "GetSpotPlacementScoresRequestPaginateTypeDef",
    "GetSpotPlacementScoresRequestRequestTypeDef",
    "GetSpotPlacementScoresResultTypeDef",
    "GetSubnetCidrReservationsRequestRequestTypeDef",
    "GetSubnetCidrReservationsResultTypeDef",
    "GetTransitGatewayAttachmentPropagationsRequestPaginateTypeDef",
    "GetTransitGatewayAttachmentPropagationsRequestRequestTypeDef",
    "GetTransitGatewayAttachmentPropagationsResultTypeDef",
    "GetTransitGatewayMulticastDomainAssociationsRequestPaginateTypeDef",
    "GetTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef",
    "GetTransitGatewayMulticastDomainAssociationsResultTypeDef",
    "GetTransitGatewayPolicyTableAssociationsRequestPaginateTypeDef",
    "GetTransitGatewayPolicyTableAssociationsRequestRequestTypeDef",
    "GetTransitGatewayPolicyTableAssociationsResultTypeDef",
    "GetTransitGatewayPolicyTableEntriesRequestRequestTypeDef",
    "GetTransitGatewayPolicyTableEntriesResultTypeDef",
    "GetTransitGatewayPrefixListReferencesRequestPaginateTypeDef",
    "GetTransitGatewayPrefixListReferencesRequestRequestTypeDef",
    "GetTransitGatewayPrefixListReferencesResultTypeDef",
    "GetTransitGatewayRouteTableAssociationsRequestPaginateTypeDef",
    "GetTransitGatewayRouteTableAssociationsRequestRequestTypeDef",
    "GetTransitGatewayRouteTableAssociationsResultTypeDef",
    "GetTransitGatewayRouteTablePropagationsRequestPaginateTypeDef",
    "GetTransitGatewayRouteTablePropagationsRequestRequestTypeDef",
    "GetTransitGatewayRouteTablePropagationsResultTypeDef",
    "GetVerifiedAccessEndpointPolicyRequestRequestTypeDef",
    "GetVerifiedAccessEndpointPolicyResultTypeDef",
    "GetVerifiedAccessEndpointTargetsRequestRequestTypeDef",
    "GetVerifiedAccessEndpointTargetsResultTypeDef",
    "GetVerifiedAccessGroupPolicyRequestRequestTypeDef",
    "GetVerifiedAccessGroupPolicyResultTypeDef",
    "GetVpnConnectionDeviceSampleConfigurationRequestRequestTypeDef",
    "GetVpnConnectionDeviceSampleConfigurationResultTypeDef",
    "GetVpnConnectionDeviceTypesRequestPaginateTypeDef",
    "GetVpnConnectionDeviceTypesRequestRequestTypeDef",
    "GetVpnConnectionDeviceTypesResultTypeDef",
    "GetVpnTunnelReplacementStatusRequestRequestTypeDef",
    "GetVpnTunnelReplacementStatusResultTypeDef",
    "GpuDeviceInfoTypeDef",
    "GpuDeviceMemoryInfoTypeDef",
    "GpuInfoTypeDef",
    "GroupIdentifierTypeDef",
    "HibernationOptionsRequestTypeDef",
    "HibernationOptionsTypeDef",
    "HistoryRecordEntryTypeDef",
    "HistoryRecordTypeDef",
    "HostInstanceTypeDef",
    "HostOfferingTypeDef",
    "HostPropertiesTypeDef",
    "HostReservationTypeDef",
    "HostTypeDef",
    "IKEVersionsListValueTypeDef",
    "IKEVersionsRequestListValueTypeDef",
    "IamInstanceProfileAssociationTypeDef",
    "IamInstanceProfileSpecificationTypeDef",
    "IamInstanceProfileTypeDef",
    "IcmpTypeCodeTypeDef",
    "IdFormatTypeDef",
    "ImageAttributeTypeDef",
    "ImageCriterionRequestTypeDef",
    "ImageCriterionTypeDef",
    "ImageDiskContainerTypeDef",
    "ImageMetadataTypeDef",
    "ImageRecycleBinInfoTypeDef",
    "ImageTypeDef",
    "ImportClientVpnClientCertificateRevocationListRequestRequestTypeDef",
    "ImportClientVpnClientCertificateRevocationListResultTypeDef",
    "ImportImageLicenseConfigurationRequestTypeDef",
    "ImportImageLicenseConfigurationResponseTypeDef",
    "ImportImageRequestRequestTypeDef",
    "ImportImageResultTypeDef",
    "ImportImageTaskTypeDef",
    "ImportInstanceLaunchSpecificationTypeDef",
    "ImportInstanceRequestRequestTypeDef",
    "ImportInstanceResultTypeDef",
    "ImportInstanceTaskDetailsTypeDef",
    "ImportInstanceVolumeDetailItemTypeDef",
    "ImportKeyPairRequestRequestTypeDef",
    "ImportKeyPairRequestServiceResourceImportKeyPairTypeDef",
    "ImportKeyPairResultTypeDef",
    "ImportSnapshotRequestRequestTypeDef",
    "ImportSnapshotResultTypeDef",
    "ImportSnapshotTaskTypeDef",
    "ImportVolumeRequestRequestTypeDef",
    "ImportVolumeResultTypeDef",
    "ImportVolumeTaskDetailsTypeDef",
    "InferenceAcceleratorInfoTypeDef",
    "InferenceDeviceInfoTypeDef",
    "InferenceDeviceMemoryInfoTypeDef",
    "InstanceAttachmentEnaSrdSpecificationTypeDef",
    "InstanceAttachmentEnaSrdUdpSpecificationTypeDef",
    "InstanceAttributeTypeDef",
    "InstanceBlockDeviceMappingSpecificationTypeDef",
    "InstanceBlockDeviceMappingTypeDef",
    "InstanceCapacityTypeDef",
    "InstanceCountTypeDef",
    "InstanceCreateTagsRequestTypeDef",
    "InstanceCreditSpecificationRequestTypeDef",
    "InstanceCreditSpecificationTypeDef",
    "InstanceDeleteTagsRequestTypeDef",
    "InstanceEventWindowAssociationRequestTypeDef",
    "InstanceEventWindowAssociationTargetTypeDef",
    "InstanceEventWindowDisassociationRequestTypeDef",
    "InstanceEventWindowStateChangeTypeDef",
    "InstanceEventWindowTimeRangeRequestTypeDef",
    "InstanceEventWindowTimeRangeTypeDef",
    "InstanceEventWindowTypeDef",
    "InstanceExportDetailsTypeDef",
    "InstanceFamilyCreditSpecificationTypeDef",
    "InstanceImageMetadataTypeDef",
    "InstanceIpv4PrefixTypeDef",
    "InstanceIpv6AddressRequestTypeDef",
    "InstanceIpv6AddressTypeDef",
    "InstanceIpv6PrefixTypeDef",
    "InstanceMaintenanceOptionsRequestTypeDef",
    "InstanceMaintenanceOptionsTypeDef",
    "InstanceMarketOptionsRequestTypeDef",
    "InstanceMetadataDefaultsResponseTypeDef",
    "InstanceMetadataOptionsRequestTypeDef",
    "InstanceMetadataOptionsResponseTypeDef",
    "InstanceMonitoringTypeDef",
    "InstanceNetworkInterfaceAssociationTypeDef",
    "InstanceNetworkInterfaceAttachmentTypeDef",
    "InstanceNetworkInterfaceSpecificationOutputTypeDef",
    "InstanceNetworkInterfaceSpecificationTypeDef",
    "InstanceNetworkInterfaceSpecificationUnionTypeDef",
    "InstanceNetworkInterfaceTypeDef",
    "InstanceNetworkPerformanceOptionsRequestTypeDef",
    "InstanceNetworkPerformanceOptionsTypeDef",
    "InstancePrivateIpAddressTypeDef",
    "InstanceRequirementsOutputTypeDef",
    "InstanceRequirementsRequestTypeDef",
    "InstanceRequirementsTypeDef",
    "InstanceRequirementsUnionTypeDef",
    "InstanceRequirementsWithMetadataRequestTypeDef",
    "InstanceSpecificationTypeDef",
    "InstanceStateChangeTypeDef",
    "InstanceStateTypeDef",
    "InstanceStatusDetailsTypeDef",
    "InstanceStatusEventTypeDef",
    "InstanceStatusSummaryTypeDef",
    "InstanceStatusTypeDef",
    "InstanceStorageInfoTypeDef",
    "InstanceTagNotificationAttributeTypeDef",
    "InstanceTopologyTypeDef",
    "InstanceTypeDef",
    "InstanceTypeInfoFromInstanceRequirementsTypeDef",
    "InstanceTypeInfoTypeDef",
    "InstanceTypeOfferingTypeDef",
    "InstanceUsageTypeDef",
    "IntegrateServicesTypeDef",
    "InternetGatewayAttachmentTypeDef",
    "InternetGatewayTypeDef",
    "IpPermissionOutputTypeDef",
    "IpPermissionTypeDef",
    "IpPermissionUnionTypeDef",
    "IpRangeTypeDef",
    "IpamAddressHistoryRecordTypeDef",
    "IpamCidrAuthorizationContextTypeDef",
    "IpamDiscoveredAccountTypeDef",
    "IpamDiscoveredPublicAddressTypeDef",
    "IpamDiscoveredResourceCidrTypeDef",
    "IpamDiscoveryFailureReasonTypeDef",
    "IpamExternalResourceVerificationTokenTypeDef",
    "IpamOperatingRegionTypeDef",
    "IpamOrganizationalUnitExclusionTypeDef",
    "IpamPoolAllocationTypeDef",
    "IpamPoolCidrFailureReasonTypeDef",
    "IpamPoolCidrTypeDef",
    "IpamPoolSourceResourceRequestTypeDef",
    "IpamPoolSourceResourceTypeDef",
    "IpamPoolTypeDef",
    "IpamPublicAddressSecurityGroupTypeDef",
    "IpamPublicAddressTagTypeDef",
    "IpamPublicAddressTagsTypeDef",
    "IpamResourceCidrTypeDef",
    "IpamResourceDiscoveryAssociationTypeDef",
    "IpamResourceDiscoveryTypeDef",
    "IpamResourceTagTypeDef",
    "IpamScopeTypeDef",
    "IpamTypeDef",
    "Ipv4PrefixSpecificationRequestTypeDef",
    "Ipv4PrefixSpecificationResponseTypeDef",
    "Ipv4PrefixSpecificationTypeDef",
    "Ipv6CidrAssociationTypeDef",
    "Ipv6CidrBlockTypeDef",
    "Ipv6PoolTypeDef",
    "Ipv6PrefixSpecificationRequestTypeDef",
    "Ipv6PrefixSpecificationResponseTypeDef",
    "Ipv6PrefixSpecificationTypeDef",
    "Ipv6RangeTypeDef",
    "KeyPairInfoTypeDef",
    "KeyPairTypeDef",
    "LastErrorTypeDef",
    "LaunchPermissionModificationsTypeDef",
    "LaunchPermissionTypeDef",
    "LaunchSpecificationTypeDef",
    "LaunchTemplateAndOverridesResponseTypeDef",
    "LaunchTemplateBlockDeviceMappingRequestTypeDef",
    "LaunchTemplateBlockDeviceMappingTypeDef",
    "LaunchTemplateCapacityReservationSpecificationRequestTypeDef",
    "LaunchTemplateCapacityReservationSpecificationResponseTypeDef",
    "LaunchTemplateConfigOutputTypeDef",
    "LaunchTemplateConfigTypeDef",
    "LaunchTemplateConfigUnionTypeDef",
    "LaunchTemplateCpuOptionsRequestTypeDef",
    "LaunchTemplateCpuOptionsTypeDef",
    "LaunchTemplateEbsBlockDeviceRequestTypeDef",
    "LaunchTemplateEbsBlockDeviceTypeDef",
    "LaunchTemplateElasticInferenceAcceleratorResponseTypeDef",
    "LaunchTemplateElasticInferenceAcceleratorTypeDef",
    "LaunchTemplateEnaSrdSpecificationTypeDef",
    "LaunchTemplateEnaSrdUdpSpecificationTypeDef",
    "LaunchTemplateEnclaveOptionsRequestTypeDef",
    "LaunchTemplateEnclaveOptionsTypeDef",
    "LaunchTemplateHibernationOptionsRequestTypeDef",
    "LaunchTemplateHibernationOptionsTypeDef",
    "LaunchTemplateIamInstanceProfileSpecificationRequestTypeDef",
    "LaunchTemplateIamInstanceProfileSpecificationTypeDef",
    "LaunchTemplateInstanceMaintenanceOptionsRequestTypeDef",
    "LaunchTemplateInstanceMaintenanceOptionsTypeDef",
    "LaunchTemplateInstanceMarketOptionsRequestTypeDef",
    "LaunchTemplateInstanceMarketOptionsTypeDef",
    "LaunchTemplateInstanceMetadataOptionsRequestTypeDef",
    "LaunchTemplateInstanceMetadataOptionsTypeDef",
    "LaunchTemplateInstanceNetworkInterfaceSpecificationRequestTypeDef",
    "LaunchTemplateInstanceNetworkInterfaceSpecificationTypeDef",
    "LaunchTemplateLicenseConfigurationRequestTypeDef",
    "LaunchTemplateLicenseConfigurationTypeDef",
    "LaunchTemplateNetworkPerformanceOptionsRequestTypeDef",
    "LaunchTemplateNetworkPerformanceOptionsTypeDef",
    "LaunchTemplateOverridesOutputTypeDef",
    "LaunchTemplateOverridesTypeDef",
    "LaunchTemplateOverridesUnionTypeDef",
    "LaunchTemplatePlacementRequestTypeDef",
    "LaunchTemplatePlacementTypeDef",
    "LaunchTemplatePrivateDnsNameOptionsRequestTypeDef",
    "LaunchTemplatePrivateDnsNameOptionsTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "LaunchTemplateSpotMarketOptionsRequestTypeDef",
    "LaunchTemplateSpotMarketOptionsTypeDef",
    "LaunchTemplateTagSpecificationRequestTypeDef",
    "LaunchTemplateTagSpecificationTypeDef",
    "LaunchTemplateTypeDef",
    "LaunchTemplateVersionTypeDef",
    "LaunchTemplatesMonitoringRequestTypeDef",
    "LaunchTemplatesMonitoringTypeDef",
    "LicenseConfigurationRequestTypeDef",
    "LicenseConfigurationTypeDef",
    "ListImagesInRecycleBinRequestPaginateTypeDef",
    "ListImagesInRecycleBinRequestRequestTypeDef",
    "ListImagesInRecycleBinResultTypeDef",
    "ListSnapshotsInRecycleBinRequestPaginateTypeDef",
    "ListSnapshotsInRecycleBinRequestRequestTypeDef",
    "ListSnapshotsInRecycleBinResultTypeDef",
    "LoadBalancersConfigOutputTypeDef",
    "LoadBalancersConfigTypeDef",
    "LoadBalancersConfigUnionTypeDef",
    "LoadPermissionModificationsTypeDef",
    "LoadPermissionRequestTypeDef",
    "LoadPermissionTypeDef",
    "LocalGatewayRouteTableTypeDef",
    "LocalGatewayRouteTableVirtualInterfaceGroupAssociationTypeDef",
    "LocalGatewayRouteTableVpcAssociationTypeDef",
    "LocalGatewayRouteTypeDef",
    "LocalGatewayTypeDef",
    "LocalGatewayVirtualInterfaceGroupTypeDef",
    "LocalGatewayVirtualInterfaceTypeDef",
    "LockSnapshotRequestRequestTypeDef",
    "LockSnapshotResultTypeDef",
    "LockedSnapshotsInfoTypeDef",
    "MacHostTypeDef",
    "MaintenanceDetailsTypeDef",
    "ManagedPrefixListTypeDef",
    "MediaAcceleratorInfoTypeDef",
    "MediaDeviceInfoTypeDef",
    "MediaDeviceMemoryInfoTypeDef",
    "MemoryGiBPerVCpuRequestTypeDef",
    "MemoryGiBPerVCpuTypeDef",
    "MemoryInfoTypeDef",
    "MemoryMiBRequestTypeDef",
    "MemoryMiBTypeDef",
    "MetricPointTypeDef",
    "ModifyAddressAttributeRequestRequestTypeDef",
    "ModifyAddressAttributeResultTypeDef",
    "ModifyAvailabilityZoneGroupRequestRequestTypeDef",
    "ModifyAvailabilityZoneGroupResultTypeDef",
    "ModifyCapacityReservationFleetRequestRequestTypeDef",
    "ModifyCapacityReservationFleetResultTypeDef",
    "ModifyCapacityReservationRequestRequestTypeDef",
    "ModifyCapacityReservationResultTypeDef",
    "ModifyClientVpnEndpointRequestRequestTypeDef",
    "ModifyClientVpnEndpointResultTypeDef",
    "ModifyDefaultCreditSpecificationRequestRequestTypeDef",
    "ModifyDefaultCreditSpecificationResultTypeDef",
    "ModifyEbsDefaultKmsKeyIdRequestRequestTypeDef",
    "ModifyEbsDefaultKmsKeyIdResultTypeDef",
    "ModifyFleetRequestRequestTypeDef",
    "ModifyFleetResultTypeDef",
    "ModifyFpgaImageAttributeRequestRequestTypeDef",
    "ModifyFpgaImageAttributeResultTypeDef",
    "ModifyHostsRequestRequestTypeDef",
    "ModifyHostsResultTypeDef",
    "ModifyIdFormatRequestRequestTypeDef",
    "ModifyIdentityIdFormatRequestRequestTypeDef",
    "ModifyImageAttributeRequestImageModifyAttributeTypeDef",
    "ModifyImageAttributeRequestRequestTypeDef",
    "ModifyInstanceAttributeRequestInstanceModifyAttributeTypeDef",
    "ModifyInstanceAttributeRequestRequestTypeDef",
    "ModifyInstanceCapacityReservationAttributesRequestRequestTypeDef",
    "ModifyInstanceCapacityReservationAttributesResultTypeDef",
    "ModifyInstanceCpuOptionsRequestRequestTypeDef",
    "ModifyInstanceCpuOptionsResultTypeDef",
    "ModifyInstanceCreditSpecificationRequestRequestTypeDef",
    "ModifyInstanceCreditSpecificationResultTypeDef",
    "ModifyInstanceEventStartTimeRequestRequestTypeDef",
    "ModifyInstanceEventStartTimeResultTypeDef",
    "ModifyInstanceEventWindowRequestRequestTypeDef",
    "ModifyInstanceEventWindowResultTypeDef",
    "ModifyInstanceMaintenanceOptionsRequestRequestTypeDef",
    "ModifyInstanceMaintenanceOptionsResultTypeDef",
    "ModifyInstanceMetadataDefaultsRequestRequestTypeDef",
    "ModifyInstanceMetadataDefaultsResultTypeDef",
    "ModifyInstanceMetadataOptionsRequestRequestTypeDef",
    "ModifyInstanceMetadataOptionsResultTypeDef",
    "ModifyInstanceNetworkPerformanceRequestRequestTypeDef",
    "ModifyInstanceNetworkPerformanceResultTypeDef",
    "ModifyInstancePlacementRequestRequestTypeDef",
    "ModifyInstancePlacementResultTypeDef",
    "ModifyIpamPoolRequestRequestTypeDef",
    "ModifyIpamPoolResultTypeDef",
    "ModifyIpamRequestRequestTypeDef",
    "ModifyIpamResourceCidrRequestRequestTypeDef",
    "ModifyIpamResourceCidrResultTypeDef",
    "ModifyIpamResourceDiscoveryRequestRequestTypeDef",
    "ModifyIpamResourceDiscoveryResultTypeDef",
    "ModifyIpamResultTypeDef",
    "ModifyIpamScopeRequestRequestTypeDef",
    "ModifyIpamScopeResultTypeDef",
    "ModifyLaunchTemplateRequestRequestTypeDef",
    "ModifyLaunchTemplateResultTypeDef",
    "ModifyLocalGatewayRouteRequestRequestTypeDef",
    "ModifyLocalGatewayRouteResultTypeDef",
    "ModifyManagedPrefixListRequestRequestTypeDef",
    "ModifyManagedPrefixListResultTypeDef",
    "ModifyNetworkInterfaceAttributeRequestNetworkInterfaceModifyAttributeTypeDef",
    "ModifyNetworkInterfaceAttributeRequestRequestTypeDef",
    "ModifyPrivateDnsNameOptionsRequestRequestTypeDef",
    "ModifyPrivateDnsNameOptionsResultTypeDef",
    "ModifyReservedInstancesRequestRequestTypeDef",
    "ModifyReservedInstancesResultTypeDef",
    "ModifySecurityGroupRulesRequestRequestTypeDef",
    "ModifySecurityGroupRulesResultTypeDef",
    "ModifySnapshotAttributeRequestRequestTypeDef",
    "ModifySnapshotAttributeRequestSnapshotModifyAttributeTypeDef",
    "ModifySnapshotTierRequestRequestTypeDef",
    "ModifySnapshotTierResultTypeDef",
    "ModifySpotFleetRequestRequestRequestTypeDef",
    "ModifySpotFleetRequestResponseTypeDef",
    "ModifySubnetAttributeRequestRequestTypeDef",
    "ModifyTrafficMirrorFilterNetworkServicesRequestRequestTypeDef",
    "ModifyTrafficMirrorFilterNetworkServicesResultTypeDef",
    "ModifyTrafficMirrorFilterRuleRequestRequestTypeDef",
    "ModifyTrafficMirrorFilterRuleResultTypeDef",
    "ModifyTrafficMirrorSessionRequestRequestTypeDef",
    "ModifyTrafficMirrorSessionResultTypeDef",
    "ModifyTransitGatewayOptionsTypeDef",
    "ModifyTransitGatewayPrefixListReferenceRequestRequestTypeDef",
    "ModifyTransitGatewayPrefixListReferenceResultTypeDef",
    "ModifyTransitGatewayRequestRequestTypeDef",
    "ModifyTransitGatewayResultTypeDef",
    "ModifyTransitGatewayVpcAttachmentRequestOptionsTypeDef",
    "ModifyTransitGatewayVpcAttachmentRequestRequestTypeDef",
    "ModifyTransitGatewayVpcAttachmentResultTypeDef",
    "ModifyVerifiedAccessEndpointCidrOptionsTypeDef",
    "ModifyVerifiedAccessEndpointEniOptionsTypeDef",
    "ModifyVerifiedAccessEndpointLoadBalancerOptionsTypeDef",
    "ModifyVerifiedAccessEndpointPolicyRequestRequestTypeDef",
    "ModifyVerifiedAccessEndpointPolicyResultTypeDef",
    "ModifyVerifiedAccessEndpointPortRangeTypeDef",
    "ModifyVerifiedAccessEndpointRdsOptionsTypeDef",
    "ModifyVerifiedAccessEndpointRequestRequestTypeDef",
    "ModifyVerifiedAccessEndpointResultTypeDef",
    "ModifyVerifiedAccessGroupPolicyRequestRequestTypeDef",
    "ModifyVerifiedAccessGroupPolicyResultTypeDef",
    "ModifyVerifiedAccessGroupRequestRequestTypeDef",
    "ModifyVerifiedAccessGroupResultTypeDef",
    "ModifyVerifiedAccessInstanceLoggingConfigurationRequestRequestTypeDef",
    "ModifyVerifiedAccessInstanceLoggingConfigurationResultTypeDef",
    "ModifyVerifiedAccessInstanceRequestRequestTypeDef",
    "ModifyVerifiedAccessInstanceResultTypeDef",
    "ModifyVerifiedAccessNativeApplicationOidcOptionsTypeDef",
    "ModifyVerifiedAccessTrustProviderDeviceOptionsTypeDef",
    "ModifyVerifiedAccessTrustProviderOidcOptionsTypeDef",
    "ModifyVerifiedAccessTrustProviderRequestRequestTypeDef",
    "ModifyVerifiedAccessTrustProviderResultTypeDef",
    "ModifyVolumeAttributeRequestRequestTypeDef",
    "ModifyVolumeAttributeRequestVolumeModifyAttributeTypeDef",
    "ModifyVolumeRequestRequestTypeDef",
    "ModifyVolumeResultTypeDef",
    "ModifyVpcAttributeRequestRequestTypeDef",
    "ModifyVpcAttributeRequestVpcModifyAttributeTypeDef",
    "ModifyVpcBlockPublicAccessExclusionRequestRequestTypeDef",
    "ModifyVpcBlockPublicAccessExclusionResultTypeDef",
    "ModifyVpcBlockPublicAccessOptionsRequestRequestTypeDef",
    "ModifyVpcBlockPublicAccessOptionsResultTypeDef",
    "ModifyVpcEndpointConnectionNotificationRequestRequestTypeDef",
    "ModifyVpcEndpointConnectionNotificationResultTypeDef",
    "ModifyVpcEndpointRequestRequestTypeDef",
    "ModifyVpcEndpointResultTypeDef",
    "ModifyVpcEndpointServiceConfigurationRequestRequestTypeDef",
    "ModifyVpcEndpointServiceConfigurationResultTypeDef",
    "ModifyVpcEndpointServicePayerResponsibilityRequestRequestTypeDef",
    "ModifyVpcEndpointServicePayerResponsibilityResultTypeDef",
    "ModifyVpcEndpointServicePermissionsRequestRequestTypeDef",
    "ModifyVpcEndpointServicePermissionsResultTypeDef",
    "ModifyVpcPeeringConnectionOptionsRequestRequestTypeDef",
    "ModifyVpcPeeringConnectionOptionsResultTypeDef",
    "ModifyVpcTenancyRequestRequestTypeDef",
    "ModifyVpcTenancyResultTypeDef",
    "ModifyVpnConnectionOptionsRequestRequestTypeDef",
    "ModifyVpnConnectionOptionsResultTypeDef",
    "ModifyVpnConnectionRequestRequestTypeDef",
    "ModifyVpnConnectionResultTypeDef",
    "ModifyVpnTunnelCertificateRequestRequestTypeDef",
    "ModifyVpnTunnelCertificateResultTypeDef",
    "ModifyVpnTunnelOptionsRequestRequestTypeDef",
    "ModifyVpnTunnelOptionsResultTypeDef",
    "ModifyVpnTunnelOptionsSpecificationTypeDef",
    "MonitorInstancesRequestInstanceMonitorTypeDef",
    "MonitorInstancesRequestRequestTypeDef",
    "MonitorInstancesResultTypeDef",
    "MonitoringTypeDef",
    "MoveAddressToVpcRequestRequestTypeDef",
    "MoveAddressToVpcResultTypeDef",
    "MoveByoipCidrToIpamRequestRequestTypeDef",
    "MoveByoipCidrToIpamResultTypeDef",
    "MoveCapacityReservationInstancesRequestRequestTypeDef",
    "MoveCapacityReservationInstancesResultTypeDef",
    "MovingAddressStatusTypeDef",
    "NatGatewayAddressTypeDef",
    "NatGatewayTypeDef",
    "NativeApplicationOidcOptionsTypeDef",
    "NetworkAclAssociationTypeDef",
    "NetworkAclEntryTypeDef",
    "NetworkAclTypeDef",
    "NetworkBandwidthGbpsRequestTypeDef",
    "NetworkBandwidthGbpsTypeDef",
    "NetworkCardInfoTypeDef",
    "NetworkInfoTypeDef",
    "NetworkInsightsAccessScopeAnalysisTypeDef",
    "NetworkInsightsAccessScopeContentTypeDef",
    "NetworkInsightsAccessScopeTypeDef",
    "NetworkInsightsAnalysisTypeDef",
    "NetworkInsightsPathTypeDef",
    "NetworkInterfaceAssociationTypeDef",
    "NetworkInterfaceAttachmentChangesTypeDef",
    "NetworkInterfaceAttachmentTypeDef",
    "NetworkInterfaceCountRequestTypeDef",
    "NetworkInterfaceCountTypeDef",
    "NetworkInterfaceIpv6AddressTypeDef",
    "NetworkInterfacePermissionStateTypeDef",
    "NetworkInterfacePermissionTypeDef",
    "NetworkInterfacePrivateIpAddressTypeDef",
    "NetworkInterfaceTypeDef",
    "NeuronDeviceCoreInfoTypeDef",
    "NeuronDeviceInfoTypeDef",
    "NeuronDeviceMemoryInfoTypeDef",
    "NeuronInfoTypeDef",
    "NewDhcpConfigurationTypeDef",
    "NitroTpmInfoTypeDef",
    "OidcOptionsTypeDef",
    "OnDemandOptionsRequestTypeDef",
    "OnDemandOptionsTypeDef",
    "OperatorRequestTypeDef",
    "OperatorResponseTypeDef",
    "PacketHeaderStatementRequestTypeDef",
    "PacketHeaderStatementTypeDef",
    "PaginatorConfigTypeDef",
    "PathComponentTypeDef",
    "PathFilterTypeDef",
    "PathRequestFilterTypeDef",
    "PathStatementRequestTypeDef",
    "PathStatementTypeDef",
    "PciIdTypeDef",
    "PeeringAttachmentStatusTypeDef",
    "PeeringConnectionOptionsRequestTypeDef",
    "PeeringConnectionOptionsTypeDef",
    "PeeringTgwInfoTypeDef",
    "PerformanceFactorReferenceRequestTypeDef",
    "PerformanceFactorReferenceTypeDef",
    "Phase1DHGroupNumbersListValueTypeDef",
    "Phase1DHGroupNumbersRequestListValueTypeDef",
    "Phase1EncryptionAlgorithmsListValueTypeDef",
    "Phase1EncryptionAlgorithmsRequestListValueTypeDef",
    "Phase1IntegrityAlgorithmsListValueTypeDef",
    "Phase1IntegrityAlgorithmsRequestListValueTypeDef",
    "Phase2DHGroupNumbersListValueTypeDef",
    "Phase2DHGroupNumbersRequestListValueTypeDef",
    "Phase2EncryptionAlgorithmsListValueTypeDef",
    "Phase2EncryptionAlgorithmsRequestListValueTypeDef",
    "Phase2IntegrityAlgorithmsListValueTypeDef",
    "Phase2IntegrityAlgorithmsRequestListValueTypeDef",
    "PlacementGroupInfoTypeDef",
    "PlacementGroupTypeDef",
    "PlacementResponseTypeDef",
    "PlacementTypeDef",
    "PoolCidrBlockTypeDef",
    "PortRangeTypeDef",
    "PrefixListAssociationTypeDef",
    "PrefixListEntryTypeDef",
    "PrefixListIdTypeDef",
    "PrefixListTypeDef",
    "PriceScheduleSpecificationTypeDef",
    "PriceScheduleTypeDef",
    "PricingDetailTypeDef",
    "PrincipalIdFormatTypeDef",
    "PrivateDnsDetailsTypeDef",
    "PrivateDnsNameConfigurationTypeDef",
    "PrivateDnsNameOptionsOnLaunchTypeDef",
    "PrivateDnsNameOptionsRequestTypeDef",
    "PrivateDnsNameOptionsResponseTypeDef",
    "PrivateIpAddressSpecificationTypeDef",
    "ProcessorInfoTypeDef",
    "ProductCodeTypeDef",
    "PropagatingVgwTypeDef",
    "ProvisionByoipCidrRequestRequestTypeDef",
    "ProvisionByoipCidrResultTypeDef",
    "ProvisionIpamByoasnRequestRequestTypeDef",
    "ProvisionIpamByoasnResultTypeDef",
    "ProvisionIpamPoolCidrRequestRequestTypeDef",
    "ProvisionIpamPoolCidrResultTypeDef",
    "ProvisionPublicIpv4PoolCidrRequestRequestTypeDef",
    "ProvisionPublicIpv4PoolCidrResultTypeDef",
    "ProvisionedBandwidthTypeDef",
    "PtrUpdateStatusTypeDef",
    "PublicIpv4PoolRangeTypeDef",
    "PublicIpv4PoolTypeDef",
    "PurchaseCapacityBlockExtensionRequestRequestTypeDef",
    "PurchaseCapacityBlockExtensionResultTypeDef",
    "PurchaseCapacityBlockRequestRequestTypeDef",
    "PurchaseCapacityBlockResultTypeDef",
    "PurchaseHostReservationRequestRequestTypeDef",
    "PurchaseHostReservationResultTypeDef",
    "PurchaseRequestTypeDef",
    "PurchaseReservedInstancesOfferingRequestRequestTypeDef",
    "PurchaseReservedInstancesOfferingResultTypeDef",
    "PurchaseScheduledInstancesRequestRequestTypeDef",
    "PurchaseScheduledInstancesResultTypeDef",
    "PurchaseTypeDef",
    "RebootInstancesRequestInstanceRebootTypeDef",
    "RebootInstancesRequestRequestTypeDef",
    "RecurringChargeTypeDef",
    "ReferencedSecurityGroupTypeDef",
    "RegionTypeDef",
    "RegionalSummaryTypeDef",
    "RegisterImageRequestRequestTypeDef",
    "RegisterImageRequestServiceResourceRegisterImageTypeDef",
    "RegisterImageResultTypeDef",
    "RegisterInstanceEventNotificationAttributesRequestRequestTypeDef",
    "RegisterInstanceEventNotificationAttributesResultTypeDef",
    "RegisterInstanceTagAttributeRequestTypeDef",
    "RegisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef",
    "RegisterTransitGatewayMulticastGroupMembersResultTypeDef",
    "RegisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef",
    "RegisterTransitGatewayMulticastGroupSourcesResultTypeDef",
    "RejectCapacityReservationBillingOwnershipRequestRequestTypeDef",
    "RejectCapacityReservationBillingOwnershipResultTypeDef",
    "RejectTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef",
    "RejectTransitGatewayMulticastDomainAssociationsResultTypeDef",
    "RejectTransitGatewayPeeringAttachmentRequestRequestTypeDef",
    "RejectTransitGatewayPeeringAttachmentResultTypeDef",
    "RejectTransitGatewayVpcAttachmentRequestRequestTypeDef",
    "RejectTransitGatewayVpcAttachmentResultTypeDef",
    "RejectVpcEndpointConnectionsRequestRequestTypeDef",
    "RejectVpcEndpointConnectionsResultTypeDef",
    "RejectVpcPeeringConnectionRequestRequestTypeDef",
    "RejectVpcPeeringConnectionRequestVpcPeeringConnectionRejectTypeDef",
    "RejectVpcPeeringConnectionResultTypeDef",
    "ReleaseAddressRequestClassicAddressReleaseTypeDef",
    "ReleaseAddressRequestRequestTypeDef",
    "ReleaseAddressRequestVpcAddressReleaseTypeDef",
    "ReleaseHostsRequestRequestTypeDef",
    "ReleaseHostsResultTypeDef",
    "ReleaseIpamPoolAllocationRequestRequestTypeDef",
    "ReleaseIpamPoolAllocationResultTypeDef",
    "RemoveIpamOperatingRegionTypeDef",
    "RemoveIpamOrganizationalUnitExclusionTypeDef",
    "RemovePrefixListEntryTypeDef",
    "ReplaceIamInstanceProfileAssociationRequestRequestTypeDef",
    "ReplaceIamInstanceProfileAssociationResultTypeDef",
    "ReplaceImageCriteriaInAllowedImagesSettingsRequestRequestTypeDef",
    "ReplaceImageCriteriaInAllowedImagesSettingsResultTypeDef",
    "ReplaceNetworkAclAssociationRequestNetworkAclReplaceAssociationTypeDef",
    "ReplaceNetworkAclAssociationRequestRequestTypeDef",
    "ReplaceNetworkAclAssociationResultTypeDef",
    "ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef",
    "ReplaceNetworkAclEntryRequestRequestTypeDef",
    "ReplaceRootVolumeTaskTypeDef",
    "ReplaceRouteRequestRequestTypeDef",
    "ReplaceRouteRequestRouteReplaceTypeDef",
    "ReplaceRouteTableAssociationRequestRequestTypeDef",
    "ReplaceRouteTableAssociationRequestRouteTableAssociationReplaceSubnetTypeDef",
    "ReplaceRouteTableAssociationResultTypeDef",
    "ReplaceTransitGatewayRouteRequestRequestTypeDef",
    "ReplaceTransitGatewayRouteResultTypeDef",
    "ReplaceVpnTunnelRequestRequestTypeDef",
    "ReplaceVpnTunnelResultTypeDef",
    "ReportInstanceStatusRequestInstanceReportStatusTypeDef",
    "ReportInstanceStatusRequestRequestTypeDef",
    "RequestFilterPortRangeTypeDef",
    "RequestIpamResourceTagTypeDef",
    "RequestLaunchTemplateDataTypeDef",
    "RequestSpotFleetRequestRequestTypeDef",
    "RequestSpotFleetResponseTypeDef",
    "RequestSpotInstancesRequestRequestTypeDef",
    "RequestSpotInstancesResultTypeDef",
    "RequestSpotLaunchSpecificationTypeDef",
    "ReservationFleetInstanceSpecificationTypeDef",
    "ReservationResponseTypeDef",
    "ReservationTypeDef",
    "ReservationValueTypeDef",
    "ReservedInstanceLimitPriceTypeDef",
    "ReservedInstanceReservationValueTypeDef",
    "ReservedInstancesConfigurationTypeDef",
    "ReservedInstancesIdTypeDef",
    "ReservedInstancesListingTypeDef",
    "ReservedInstancesModificationResultTypeDef",
    "ReservedInstancesModificationTypeDef",
    "ReservedInstancesOfferingTypeDef",
    "ReservedInstancesTypeDef",
    "ResetAddressAttributeRequestRequestTypeDef",
    "ResetAddressAttributeResultTypeDef",
    "ResetEbsDefaultKmsKeyIdRequestRequestTypeDef",
    "ResetEbsDefaultKmsKeyIdResultTypeDef",
    "ResetFpgaImageAttributeRequestRequestTypeDef",
    "ResetFpgaImageAttributeResultTypeDef",
    "ResetImageAttributeRequestImageResetAttributeTypeDef",
    "ResetImageAttributeRequestRequestTypeDef",
    "ResetInstanceAttributeRequestInstanceResetAttributeTypeDef",
    "ResetInstanceAttributeRequestInstanceResetKernelTypeDef",
    "ResetInstanceAttributeRequestInstanceResetRamdiskTypeDef",
    "ResetInstanceAttributeRequestInstanceResetSourceDestCheckTypeDef",
    "ResetInstanceAttributeRequestRequestTypeDef",
    "ResetNetworkInterfaceAttributeRequestNetworkInterfaceResetAttributeTypeDef",
    "ResetNetworkInterfaceAttributeRequestRequestTypeDef",
    "ResetSnapshotAttributeRequestRequestTypeDef",
    "ResetSnapshotAttributeRequestSnapshotResetAttributeTypeDef",
    "ResourceStatementRequestTypeDef",
    "ResourceStatementTypeDef",
    "ResponseErrorTypeDef",
    "ResponseLaunchTemplateDataTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreAddressToClassicRequestRequestTypeDef",
    "RestoreAddressToClassicResultTypeDef",
    "RestoreImageFromRecycleBinRequestRequestTypeDef",
    "RestoreImageFromRecycleBinResultTypeDef",
    "RestoreManagedPrefixListVersionRequestRequestTypeDef",
    "RestoreManagedPrefixListVersionResultTypeDef",
    "RestoreSnapshotFromRecycleBinRequestRequestTypeDef",
    "RestoreSnapshotFromRecycleBinResultTypeDef",
    "RestoreSnapshotTierRequestRequestTypeDef",
    "RestoreSnapshotTierResultTypeDef",
    "RevokeClientVpnIngressRequestRequestTypeDef",
    "RevokeClientVpnIngressResultTypeDef",
    "RevokeSecurityGroupEgressRequestRequestTypeDef",
    "RevokeSecurityGroupEgressRequestSecurityGroupRevokeEgressTypeDef",
    "RevokeSecurityGroupEgressResultTypeDef",
    "RevokeSecurityGroupIngressRequestRequestTypeDef",
    "RevokeSecurityGroupIngressRequestSecurityGroupRevokeIngressTypeDef",
    "RevokeSecurityGroupIngressResultTypeDef",
    "RevokedSecurityGroupRuleTypeDef",
    "RouteTableAssociationStateTypeDef",
    "RouteTableAssociationTypeDef",
    "RouteTableTypeDef",
    "RouteTypeDef",
    "RuleGroupRuleOptionsPairTypeDef",
    "RuleGroupTypePairTypeDef",
    "RuleOptionTypeDef",
    "RunInstancesMonitoringEnabledTypeDef",
    "RunInstancesRequestRequestTypeDef",
    "RunInstancesRequestServiceResourceCreateInstancesTypeDef",
    "RunInstancesRequestSubnetCreateInstancesTypeDef",
    "RunScheduledInstancesRequestRequestTypeDef",
    "RunScheduledInstancesResultTypeDef",
    "S3ObjectTagTypeDef",
    "S3StorageOutputTypeDef",
    "S3StorageTypeDef",
    "S3StorageUnionTypeDef",
    "ScheduledInstanceAvailabilityTypeDef",
    "ScheduledInstanceRecurrenceRequestTypeDef",
    "ScheduledInstanceRecurrenceTypeDef",
    "ScheduledInstanceTypeDef",
    "ScheduledInstancesBlockDeviceMappingTypeDef",
    "ScheduledInstancesEbsTypeDef",
    "ScheduledInstancesIamInstanceProfileTypeDef",
    "ScheduledInstancesIpv6AddressTypeDef",
    "ScheduledInstancesLaunchSpecificationTypeDef",
    "ScheduledInstancesMonitoringTypeDef",
    "ScheduledInstancesNetworkInterfaceTypeDef",
    "ScheduledInstancesPlacementTypeDef",
    "ScheduledInstancesPrivateIpAddressConfigTypeDef",
    "SearchLocalGatewayRoutesRequestPaginateTypeDef",
    "SearchLocalGatewayRoutesRequestRequestTypeDef",
    "SearchLocalGatewayRoutesResultTypeDef",
    "SearchTransitGatewayMulticastGroupsRequestPaginateTypeDef",
    "SearchTransitGatewayMulticastGroupsRequestRequestTypeDef",
    "SearchTransitGatewayMulticastGroupsResultTypeDef",
    "SearchTransitGatewayRoutesRequestRequestTypeDef",
    "SearchTransitGatewayRoutesResultTypeDef",
    "SecurityGroupForVpcTypeDef",
    "SecurityGroupIdentifierTypeDef",
    "SecurityGroupReferenceTypeDef",
    "SecurityGroupRuleDescriptionTypeDef",
    "SecurityGroupRuleRequestTypeDef",
    "SecurityGroupRuleTypeDef",
    "SecurityGroupRuleUpdateTypeDef",
    "SecurityGroupTypeDef",
    "SecurityGroupVpcAssociationTypeDef",
    "SendDiagnosticInterruptRequestRequestTypeDef",
    "ServiceConfigurationTypeDef",
    "ServiceDetailTypeDef",
    "ServiceTypeDetailTypeDef",
    "SlotDateTimeRangeRequestTypeDef",
    "SlotStartTimeRangeRequestTypeDef",
    "SnapshotDetailTypeDef",
    "SnapshotDiskContainerTypeDef",
    "SnapshotInfoTypeDef",
    "SnapshotRecycleBinInfoTypeDef",
    "SnapshotResponseTypeDef",
    "SnapshotTaskDetailTypeDef",
    "SnapshotTierStatusTypeDef",
    "SnapshotTypeDef",
    "SpotCapacityRebalanceTypeDef",
    "SpotDatafeedSubscriptionTypeDef",
    "SpotFleetLaunchSpecificationOutputTypeDef",
    "SpotFleetLaunchSpecificationTypeDef",
    "SpotFleetLaunchSpecificationUnionTypeDef",
    "SpotFleetMonitoringTypeDef",
    "SpotFleetRequestConfigDataOutputTypeDef",
    "SpotFleetRequestConfigDataTypeDef",
    "SpotFleetRequestConfigTypeDef",
    "SpotFleetTagSpecificationOutputTypeDef",
    "SpotFleetTagSpecificationTypeDef",
    "SpotFleetTagSpecificationUnionTypeDef",
    "SpotInstanceRequestTypeDef",
    "SpotInstanceStateFaultTypeDef",
    "SpotInstanceStatusTypeDef",
    "SpotMaintenanceStrategiesTypeDef",
    "SpotMarketOptionsTypeDef",
    "SpotOptionsRequestTypeDef",
    "SpotOptionsTypeDef",
    "SpotPlacementScoreTypeDef",
    "SpotPlacementTypeDef",
    "SpotPriceTypeDef",
    "StaleIpPermissionTypeDef",
    "StaleSecurityGroupTypeDef",
    "StartDeclarativePoliciesReportRequestRequestTypeDef",
    "StartDeclarativePoliciesReportResultTypeDef",
    "StartInstancesRequestInstanceStartTypeDef",
    "StartInstancesRequestRequestTypeDef",
    "StartInstancesResultTypeDef",
    "StartNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef",
    "StartNetworkInsightsAccessScopeAnalysisResultTypeDef",
    "StartNetworkInsightsAnalysisRequestRequestTypeDef",
    "StartNetworkInsightsAnalysisResultTypeDef",
    "StartVpcEndpointServicePrivateDnsVerificationRequestRequestTypeDef",
    "StartVpcEndpointServicePrivateDnsVerificationResultTypeDef",
    "StateReasonTypeDef",
    "StopInstancesRequestInstanceStopTypeDef",
    "StopInstancesRequestRequestTypeDef",
    "StopInstancesResultTypeDef",
    "StorageLocationTypeDef",
    "StorageOutputTypeDef",
    "StorageTypeDef",
    "StoreImageTaskResultTypeDef",
    "SubnetAssociationTypeDef",
    "SubnetCidrBlockStateTypeDef",
    "SubnetCidrReservationTypeDef",
    "SubnetConfigurationTypeDef",
    "SubnetIpPrefixesTypeDef",
    "SubnetIpv6CidrBlockAssociationTypeDef",
    "SubnetTypeDef",
    "SubscriptionTypeDef",
    "SuccessfulInstanceCreditSpecificationItemTypeDef",
    "SuccessfulQueuedPurchaseDeletionTypeDef",
    "SupportedRegionDetailTypeDef",
    "TagDescriptionTypeDef",
    "TagSpecificationOutputTypeDef",
    "TagSpecificationTypeDef",
    "TagSpecificationUnionTypeDef",
    "TagTypeDef",
    "TargetCapacitySpecificationRequestTypeDef",
    "TargetCapacitySpecificationTypeDef",
    "TargetConfigurationRequestTypeDef",
    "TargetConfigurationTypeDef",
    "TargetGroupTypeDef",
    "TargetGroupsConfigOutputTypeDef",
    "TargetGroupsConfigTypeDef",
    "TargetGroupsConfigUnionTypeDef",
    "TargetNetworkTypeDef",
    "TargetReservationValueTypeDef",
    "TerminateClientVpnConnectionsRequestRequestTypeDef",
    "TerminateClientVpnConnectionsResultTypeDef",
    "TerminateConnectionStatusTypeDef",
    "TerminateInstancesRequestInstanceTerminateTypeDef",
    "TerminateInstancesRequestRequestTypeDef",
    "TerminateInstancesResultTypeDef",
    "ThroughResourcesStatementRequestTypeDef",
    "ThroughResourcesStatementTypeDef",
    "TimestampTypeDef",
    "TotalLocalStorageGBRequestTypeDef",
    "TotalLocalStorageGBTypeDef",
    "TrafficMirrorFilterRuleTypeDef",
    "TrafficMirrorFilterTypeDef",
    "TrafficMirrorPortRangeRequestTypeDef",
    "TrafficMirrorPortRangeTypeDef",
    "TrafficMirrorSessionTypeDef",
    "TrafficMirrorTargetTypeDef",
    "TransitGatewayAssociationTypeDef",
    "TransitGatewayAttachmentAssociationTypeDef",
    "TransitGatewayAttachmentBgpConfigurationTypeDef",
    "TransitGatewayAttachmentPropagationTypeDef",
    "TransitGatewayAttachmentTypeDef",
    "TransitGatewayConnectOptionsTypeDef",
    "TransitGatewayConnectPeerConfigurationTypeDef",
    "TransitGatewayConnectPeerTypeDef",
    "TransitGatewayConnectRequestBgpOptionsTypeDef",
    "TransitGatewayConnectTypeDef",
    "TransitGatewayMulticastDeregisteredGroupMembersTypeDef",
    "TransitGatewayMulticastDeregisteredGroupSourcesTypeDef",
    "TransitGatewayMulticastDomainAssociationTypeDef",
    "TransitGatewayMulticastDomainAssociationsTypeDef",
    "TransitGatewayMulticastDomainOptionsTypeDef",
    "TransitGatewayMulticastDomainTypeDef",
    "TransitGatewayMulticastGroupTypeDef",
    "TransitGatewayMulticastRegisteredGroupMembersTypeDef",
    "TransitGatewayMulticastRegisteredGroupSourcesTypeDef",
    "TransitGatewayOptionsTypeDef",
    "TransitGatewayPeeringAttachmentOptionsTypeDef",
    "TransitGatewayPeeringAttachmentTypeDef",
    "TransitGatewayPolicyRuleMetaDataTypeDef",
    "TransitGatewayPolicyRuleTypeDef",
    "TransitGatewayPolicyTableAssociationTypeDef",
    "TransitGatewayPolicyTableEntryTypeDef",
    "TransitGatewayPolicyTableTypeDef",
    "TransitGatewayPrefixListAttachmentTypeDef",
    "TransitGatewayPrefixListReferenceTypeDef",
    "TransitGatewayPropagationTypeDef",
    "TransitGatewayRequestOptionsTypeDef",
    "TransitGatewayRouteAttachmentTypeDef",
    "TransitGatewayRouteTableAnnouncementTypeDef",
    "TransitGatewayRouteTableAssociationTypeDef",
    "TransitGatewayRouteTablePropagationTypeDef",
    "TransitGatewayRouteTableRouteTypeDef",
    "TransitGatewayRouteTableTypeDef",
    "TransitGatewayRouteTypeDef",
    "TransitGatewayTypeDef",
    "TransitGatewayVpcAttachmentOptionsTypeDef",
    "TransitGatewayVpcAttachmentTypeDef",
    "TrunkInterfaceAssociationTypeDef",
    "TunnelOptionTypeDef",
    "UnassignIpv6AddressesRequestRequestTypeDef",
    "UnassignIpv6AddressesResultTypeDef",
    "UnassignPrivateIpAddressesRequestNetworkInterfaceUnassignPrivateIpAddressesTypeDef",
    "UnassignPrivateIpAddressesRequestRequestTypeDef",
    "UnassignPrivateNatGatewayAddressRequestRequestTypeDef",
    "UnassignPrivateNatGatewayAddressResultTypeDef",
    "UnlockSnapshotRequestRequestTypeDef",
    "UnlockSnapshotResultTypeDef",
    "UnmonitorInstancesRequestInstanceUnmonitorTypeDef",
    "UnmonitorInstancesRequestRequestTypeDef",
    "UnmonitorInstancesResultTypeDef",
    "UnsuccessfulInstanceCreditSpecificationItemErrorTypeDef",
    "UnsuccessfulInstanceCreditSpecificationItemTypeDef",
    "UnsuccessfulItemErrorTypeDef",
    "UnsuccessfulItemTypeDef",
    "UpdateSecurityGroupRuleDescriptionsEgressRequestRequestTypeDef",
    "UpdateSecurityGroupRuleDescriptionsEgressResultTypeDef",
    "UpdateSecurityGroupRuleDescriptionsIngressRequestRequestTypeDef",
    "UpdateSecurityGroupRuleDescriptionsIngressResultTypeDef",
    "UserBucketDetailsTypeDef",
    "UserBucketTypeDef",
    "UserDataTypeDef",
    "UserIdGroupPairTypeDef",
    "VCpuCountRangeRequestTypeDef",
    "VCpuCountRangeTypeDef",
    "VCpuInfoTypeDef",
    "ValidationErrorTypeDef",
    "ValidationWarningTypeDef",
    "VerifiedAccessEndpointCidrOptionsTypeDef",
    "VerifiedAccessEndpointEniOptionsTypeDef",
    "VerifiedAccessEndpointLoadBalancerOptionsTypeDef",
    "VerifiedAccessEndpointPortRangeTypeDef",
    "VerifiedAccessEndpointRdsOptionsTypeDef",
    "VerifiedAccessEndpointStatusTypeDef",
    "VerifiedAccessEndpointTargetTypeDef",
    "VerifiedAccessEndpointTypeDef",
    "VerifiedAccessGroupTypeDef",
    "VerifiedAccessInstanceCustomSubDomainTypeDef",
    "VerifiedAccessInstanceLoggingConfigurationTypeDef",
    "VerifiedAccessInstanceOpenVpnClientConfigurationRouteTypeDef",
    "VerifiedAccessInstanceOpenVpnClientConfigurationTypeDef",
    "VerifiedAccessInstanceTypeDef",
    "VerifiedAccessInstanceUserTrustProviderClientConfigurationTypeDef",
    "VerifiedAccessLogCloudWatchLogsDestinationOptionsTypeDef",
    "VerifiedAccessLogCloudWatchLogsDestinationTypeDef",
    "VerifiedAccessLogDeliveryStatusTypeDef",
    "VerifiedAccessLogKinesisDataFirehoseDestinationOptionsTypeDef",
    "VerifiedAccessLogKinesisDataFirehoseDestinationTypeDef",
    "VerifiedAccessLogOptionsTypeDef",
    "VerifiedAccessLogS3DestinationOptionsTypeDef",
    "VerifiedAccessLogS3DestinationTypeDef",
    "VerifiedAccessLogsTypeDef",
    "VerifiedAccessSseSpecificationRequestTypeDef",
    "VerifiedAccessSseSpecificationResponseTypeDef",
    "VerifiedAccessTrustProviderCondensedTypeDef",
    "VerifiedAccessTrustProviderTypeDef",
    "VgwTelemetryTypeDef",
    "VolumeAttachmentResponseTypeDef",
    "VolumeAttachmentTypeDef",
    "VolumeDetailTypeDef",
    "VolumeModificationTypeDef",
    "VolumeResponseTypeDef",
    "VolumeStatusActionTypeDef",
    "VolumeStatusAttachmentStatusTypeDef",
    "VolumeStatusDetailsTypeDef",
    "VolumeStatusEventTypeDef",
    "VolumeStatusInfoTypeDef",
    "VolumeStatusItemTypeDef",
    "VolumeTypeDef",
    "VpcAttachmentTypeDef",
    "VpcBlockPublicAccessExclusionTypeDef",
    "VpcBlockPublicAccessOptionsTypeDef",
    "VpcCidrBlockAssociationTypeDef",
    "VpcCidrBlockStateTypeDef",
    "VpcClassicLinkTypeDef",
    "VpcCreateTagsRequestTypeDef",
    "VpcEndpointAssociationTypeDef",
    "VpcEndpointConnectionTypeDef",
    "VpcEndpointTypeDef",
    "VpcIpv6CidrBlockAssociationTypeDef",
    "VpcPeeringConnectionOptionsDescriptionTypeDef",
    "VpcPeeringConnectionStateReasonTypeDef",
    "VpcPeeringConnectionTypeDef",
    "VpcPeeringConnectionVpcInfoTypeDef",
    "VpcTypeDef",
    "VpnConnectionDeviceTypeTypeDef",
    "VpnConnectionOptionsSpecificationTypeDef",
    "VpnConnectionOptionsTypeDef",
    "VpnConnectionTypeDef",
    "VpnGatewayTypeDef",
    "VpnStaticRouteTypeDef",
    "VpnTunnelLogOptionsSpecificationTypeDef",
    "VpnTunnelLogOptionsTypeDef",
    "VpnTunnelOptionsSpecificationTypeDef",
    "WaiterConfigTypeDef",
    "WithdrawByoipCidrRequestRequestTypeDef",
    "WithdrawByoipCidrResultTypeDef",
)


class AcceleratorCountRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class AcceleratorCountTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class AcceleratorTotalMemoryMiBRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class AcceleratorTotalMemoryMiBTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class AddressTransferTypeDef(TypedDict):
    PublicIp: NotRequired[str]
    AllocationId: NotRequired[str]
    TransferAccountId: NotRequired[str]
    TransferOfferExpirationTimestamp: NotRequired[datetime]
    TransferOfferAcceptedTimestamp: NotRequired[datetime]
    AddressTransferStatus: NotRequired[AddressTransferStatusType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AcceptCapacityReservationBillingOwnershipRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    DryRun: NotRequired[bool]


class TargetConfigurationRequestTypeDef(TypedDict):
    OfferingId: str
    InstanceCount: NotRequired[int]


class AcceptTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class AcceptTransitGatewayPeeringAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class AcceptTransitGatewayVpcAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class AcceptVpcEndpointConnectionsRequestRequestTypeDef(TypedDict):
    ServiceId: str
    VpcEndpointIds: Sequence[str]
    DryRun: NotRequired[bool]


class AcceptVpcPeeringConnectionRequestRequestTypeDef(TypedDict):
    VpcPeeringConnectionId: str
    DryRun: NotRequired[bool]


class AcceptVpcPeeringConnectionRequestVpcPeeringConnectionAcceptTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class AccountAttributeValueTypeDef(TypedDict):
    AttributeValue: NotRequired[str]


class ActiveInstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    SpotInstanceRequestId: NotRequired[str]
    InstanceHealth: NotRequired[InstanceHealthStatusType]


AddIpamOperatingRegionTypeDef = TypedDict(
    "AddIpamOperatingRegionTypeDef",
    {
        "RegionName": NotRequired[str],
    },
)


class AddIpamOrganizationalUnitExclusionTypeDef(TypedDict):
    OrganizationsEntityPath: NotRequired[str]


class AddPrefixListEntryTypeDef(TypedDict):
    Cidr: str
    Description: NotRequired[str]


class AddedPrincipalTypeDef(TypedDict):
    PrincipalType: NotRequired[PrincipalTypeType]
    Principal: NotRequired[str]
    ServicePermissionId: NotRequired[str]
    ServiceId: NotRequired[str]


class AnalysisComponentTypeDef(TypedDict):
    Id: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]


class RuleGroupTypePairTypeDef(TypedDict):
    RuleGroupArn: NotRequired[str]
    RuleGroupType: NotRequired[str]


class RuleOptionTypeDef(TypedDict):
    Keyword: NotRequired[str]
    Settings: NotRequired[list[str]]


class PtrUpdateStatusTypeDef(TypedDict):
    Value: NotRequired[str]
    Status: NotRequired[str]
    Reason: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class AdvertiseByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    Asn: NotRequired[str]
    DryRun: NotRequired[bool]
    NetworkBorderGroup: NotRequired[str]


class AllocateIpamPoolCidrRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Cidr: NotRequired[str]
    NetmaskLength: NotRequired[int]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    PreviewNextCidr: NotRequired[bool]
    AllowedCidrs: NotRequired[Sequence[str]]
    DisallowedCidrs: NotRequired[Sequence[str]]


class IpamPoolAllocationTypeDef(TypedDict):
    Cidr: NotRequired[str]
    IpamPoolAllocationId: NotRequired[str]
    Description: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[IpamPoolAllocationResourceTypeType]
    ResourceRegion: NotRequired[str]
    ResourceOwner: NotRequired[str]


class AlternatePathHintTypeDef(TypedDict):
    ComponentId: NotRequired[str]
    ComponentArn: NotRequired[str]


class PortRangeTypeDef(TypedDict):
    From: NotRequired[int]
    To: NotRequired[int]


class AnalysisLoadBalancerListenerTypeDef(TypedDict):
    LoadBalancerPort: NotRequired[int]
    InstancePort: NotRequired[int]


class AnalysisRouteTableRouteTypeDef(TypedDict):
    DestinationCidr: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    EgressOnlyInternetGatewayId: NotRequired[str]
    GatewayId: NotRequired[str]
    InstanceId: NotRequired[str]
    NatGatewayId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    Origin: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    State: NotRequired[str]
    CarrierGatewayId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    LocalGatewayId: NotRequired[str]


class ApplySecurityGroupsToClientVpnTargetNetworkRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    VpcId: str
    SecurityGroupIds: Sequence[str]
    DryRun: NotRequired[bool]


class AsnAssociationTypeDef(TypedDict):
    Asn: NotRequired[str]
    Cidr: NotRequired[str]
    StatusMessage: NotRequired[str]
    State: NotRequired[AsnAssociationStateType]


class AsnAuthorizationContextTypeDef(TypedDict):
    Message: str
    Signature: str


class AssignIpv6AddressesRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    Ipv6PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[Sequence[str]]
    Ipv6Addresses: NotRequired[Sequence[str]]
    Ipv6AddressCount: NotRequired[int]


class AssignPrivateIpAddressesRequestNetworkInterfaceAssignPrivateIpAddressesTypeDef(TypedDict):
    Ipv4Prefixes: NotRequired[Sequence[str]]
    Ipv4PrefixCount: NotRequired[int]
    PrivateIpAddresses: NotRequired[Sequence[str]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    AllowReassignment: NotRequired[bool]


class AssignPrivateIpAddressesRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    Ipv4Prefixes: NotRequired[Sequence[str]]
    Ipv4PrefixCount: NotRequired[int]
    PrivateIpAddresses: NotRequired[Sequence[str]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    AllowReassignment: NotRequired[bool]


class AssignedPrivateIpAddressTypeDef(TypedDict):
    PrivateIpAddress: NotRequired[str]


class Ipv4PrefixSpecificationTypeDef(TypedDict):
    Ipv4Prefix: NotRequired[str]


class AssignPrivateNatGatewayAddressRequestRequestTypeDef(TypedDict):
    NatGatewayId: str
    PrivateIpAddresses: NotRequired[Sequence[str]]
    PrivateIpAddressCount: NotRequired[int]
    DryRun: NotRequired[bool]


class NatGatewayAddressTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    PrivateIp: NotRequired[str]
    PublicIp: NotRequired[str]
    AssociationId: NotRequired[str]
    IsPrimary: NotRequired[bool]
    FailureMessage: NotRequired[str]
    Status: NotRequired[NatGatewayAddressStatusType]


class AssociateAddressRequestClassicAddressAssociateTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    InstanceId: NotRequired[str]
    DryRun: NotRequired[bool]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    AllowReassociation: NotRequired[bool]


class AssociateAddressRequestRequestTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    InstanceId: NotRequired[str]
    PublicIp: NotRequired[str]
    DryRun: NotRequired[bool]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    AllowReassociation: NotRequired[bool]


class AssociateAddressRequestVpcAddressAssociateTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    PublicIp: NotRequired[str]
    DryRun: NotRequired[bool]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    AllowReassociation: NotRequired[bool]


class AssociateCapacityReservationBillingOwnerRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    UnusedReservationBillingOwnerId: str
    DryRun: NotRequired[bool]


class AssociateClientVpnTargetNetworkRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    SubnetId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class AssociationStatusTypeDef(TypedDict):
    Code: NotRequired[AssociationStatusCodeType]
    Message: NotRequired[str]


class AssociateDhcpOptionsRequestDhcpOptionsAssociateWithVpcTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class AssociateDhcpOptionsRequestRequestTypeDef(TypedDict):
    DhcpOptionsId: str
    VpcId: str
    DryRun: NotRequired[bool]


class AssociateDhcpOptionsRequestVpcAssociateDhcpOptionsTypeDef(TypedDict):
    DhcpOptionsId: str
    DryRun: NotRequired[bool]


class AssociateEnclaveCertificateIamRoleRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    RoleArn: str
    DryRun: NotRequired[bool]


class IamInstanceProfileSpecificationTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class AssociateIpamByoasnRequestRequestTypeDef(TypedDict):
    Asn: str
    Cidr: str
    DryRun: NotRequired[bool]


class AssociateNatGatewayAddressRequestRequestTypeDef(TypedDict):
    NatGatewayId: str
    AllocationIds: Sequence[str]
    PrivateIpAddresses: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class AssociateRouteTableRequestRequestTypeDef(TypedDict):
    RouteTableId: str
    GatewayId: NotRequired[str]
    DryRun: NotRequired[bool]
    SubnetId: NotRequired[str]


class AssociateRouteTableRequestRouteTableAssociateWithSubnetTypeDef(TypedDict):
    GatewayId: NotRequired[str]
    DryRun: NotRequired[bool]
    SubnetId: NotRequired[str]


class RouteTableAssociationStateTypeDef(TypedDict):
    State: NotRequired[RouteTableAssociationStateCodeType]
    StatusMessage: NotRequired[str]


class AssociateSecurityGroupVpcRequestRequestTypeDef(TypedDict):
    GroupId: str
    VpcId: str
    DryRun: NotRequired[bool]


class AssociateSubnetCidrBlockRequestRequestTypeDef(TypedDict):
    SubnetId: str
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    Ipv6CidrBlock: NotRequired[str]


class AssociateTransitGatewayMulticastDomainRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    TransitGatewayAttachmentId: str
    SubnetIds: Sequence[str]
    DryRun: NotRequired[bool]


class AssociateTransitGatewayPolicyTableRequestRequestTypeDef(TypedDict):
    TransitGatewayPolicyTableId: str
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class TransitGatewayPolicyTableAssociationTypeDef(TypedDict):
    TransitGatewayPolicyTableId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    State: NotRequired[TransitGatewayAssociationStateType]


class AssociateTransitGatewayRouteTableRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class TransitGatewayAssociationTypeDef(TypedDict):
    TransitGatewayRouteTableId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    State: NotRequired[TransitGatewayAssociationStateType]


class AssociateTrunkInterfaceRequestRequestTypeDef(TypedDict):
    BranchInterfaceId: str
    TrunkInterfaceId: str
    VlanId: NotRequired[int]
    GreKey: NotRequired[int]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class AssociateVpcCidrBlockRequestRequestTypeDef(TypedDict):
    VpcId: str
    CidrBlock: NotRequired[str]
    Ipv6CidrBlockNetworkBorderGroup: NotRequired[str]
    Ipv6Pool: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    Ipv4IpamPoolId: NotRequired[str]
    Ipv4NetmaskLength: NotRequired[int]
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    AmazonProvidedIpv6CidrBlock: NotRequired[bool]


class AssociatedRoleTypeDef(TypedDict):
    AssociatedRoleArn: NotRequired[str]
    CertificateS3BucketName: NotRequired[str]
    CertificateS3ObjectKey: NotRequired[str]
    EncryptionKmsKeyId: NotRequired[str]


class AssociatedTargetNetworkTypeDef(TypedDict):
    NetworkId: NotRequired[str]
    NetworkType: NotRequired[Literal["vpc"]]


TimestampTypeDef = Union[datetime, str]


class AttachClassicLinkVpcRequestInstanceAttachClassicLinkVpcTypeDef(TypedDict):
    VpcId: str
    Groups: Sequence[str]
    DryRun: NotRequired[bool]


class AttachClassicLinkVpcRequestRequestTypeDef(TypedDict):
    InstanceId: str
    VpcId: str
    Groups: Sequence[str]
    DryRun: NotRequired[bool]


class AttachClassicLinkVpcRequestVpcAttachClassicLinkInstanceTypeDef(TypedDict):
    InstanceId: str
    Groups: Sequence[str]
    DryRun: NotRequired[bool]


class AttachInternetGatewayRequestInternetGatewayAttachToVpcTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class AttachInternetGatewayRequestRequestTypeDef(TypedDict):
    InternetGatewayId: str
    VpcId: str
    DryRun: NotRequired[bool]


class AttachInternetGatewayRequestVpcAttachInternetGatewayTypeDef(TypedDict):
    InternetGatewayId: str
    DryRun: NotRequired[bool]


class AttachVerifiedAccessTrustProviderRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    VerifiedAccessTrustProviderId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class AttachVolumeRequestInstanceAttachVolumeTypeDef(TypedDict):
    Device: str
    VolumeId: str
    DryRun: NotRequired[bool]


class AttachVolumeRequestRequestTypeDef(TypedDict):
    Device: str
    InstanceId: str
    VolumeId: str
    DryRun: NotRequired[bool]


class AttachVolumeRequestVolumeAttachToInstanceTypeDef(TypedDict):
    Device: str
    InstanceId: str
    DryRun: NotRequired[bool]


class AttachVpnGatewayRequestRequestTypeDef(TypedDict):
    VpcId: str
    VpnGatewayId: str
    DryRun: NotRequired[bool]


class VpcAttachmentTypeDef(TypedDict):
    VpcId: NotRequired[str]
    State: NotRequired[AttachmentStatusType]


class AttachmentEnaSrdUdpSpecificationTypeDef(TypedDict):
    EnaSrdUdpEnabled: NotRequired[bool]


class AttributeBooleanValueTypeDef(TypedDict):
    Value: NotRequired[bool]


RegionalSummaryTypeDef = TypedDict(
    "RegionalSummaryTypeDef",
    {
        "RegionName": NotRequired[str],
        "NumberOfMatchedAccounts": NotRequired[int],
        "NumberOfUnmatchedAccounts": NotRequired[int],
    },
)


class AttributeValueTypeDef(TypedDict):
    Value: NotRequired[str]


class ClientVpnAuthorizationRuleStatusTypeDef(TypedDict):
    Code: NotRequired[ClientVpnAuthorizationRuleStatusCodeType]
    Message: NotRequired[str]


class AuthorizeClientVpnIngressRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    TargetNetworkCidr: str
    AccessGroupId: NotRequired[str]
    AuthorizeAllGroups: NotRequired[bool]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class AvailabilityZoneMessageTypeDef(TypedDict):
    Message: NotRequired[str]


class InstanceCapacityTypeDef(TypedDict):
    AvailableCapacity: NotRequired[int]
    InstanceType: NotRequired[str]
    TotalCapacity: NotRequired[int]


class BaselineEbsBandwidthMbpsRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class BaselineEbsBandwidthMbpsTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class EbsBlockDeviceTypeDef(TypedDict):
    DeleteOnTermination: NotRequired[bool]
    Iops: NotRequired[int]
    SnapshotId: NotRequired[str]
    VolumeSize: NotRequired[int]
    VolumeType: NotRequired[VolumeTypeType]
    KmsKeyId: NotRequired[str]
    Throughput: NotRequired[int]
    OutpostArn: NotRequired[str]
    Encrypted: NotRequired[bool]


class BlockPublicAccessStatesTypeDef(TypedDict):
    InternetGatewayBlockMode: NotRequired[BlockPublicAccessModeType]


class BundleTaskErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class ByoasnTypeDef(TypedDict):
    Asn: NotRequired[str]
    IpamId: NotRequired[str]
    StatusMessage: NotRequired[str]
    State: NotRequired[AsnStateType]


class CancelBundleTaskRequestRequestTypeDef(TypedDict):
    BundleId: str
    DryRun: NotRequired[bool]


class CancelCapacityReservationFleetErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class CancelCapacityReservationFleetsRequestRequestTypeDef(TypedDict):
    CapacityReservationFleetIds: Sequence[str]
    DryRun: NotRequired[bool]


class CapacityReservationFleetCancellationStateTypeDef(TypedDict):
    CurrentFleetState: NotRequired[CapacityReservationFleetStateType]
    PreviousFleetState: NotRequired[CapacityReservationFleetStateType]
    CapacityReservationFleetId: NotRequired[str]


class CancelCapacityReservationRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    DryRun: NotRequired[bool]


class CancelConversionRequestRequestTypeDef(TypedDict):
    ConversionTaskId: str
    DryRun: NotRequired[bool]
    ReasonMessage: NotRequired[str]


class CancelDeclarativePoliciesReportRequestRequestTypeDef(TypedDict):
    ReportId: str
    DryRun: NotRequired[bool]


class CancelExportTaskRequestRequestTypeDef(TypedDict):
    ExportTaskId: str


class CancelImageLaunchPermissionRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class CancelImportTaskRequestRequestTypeDef(TypedDict):
    CancelReason: NotRequired[str]
    DryRun: NotRequired[bool]
    ImportTaskId: NotRequired[str]


class CancelReservedInstancesListingRequestRequestTypeDef(TypedDict):
    ReservedInstancesListingId: str


class CancelSpotFleetRequestsErrorTypeDef(TypedDict):
    Code: NotRequired[CancelBatchErrorCodeType]
    Message: NotRequired[str]


class CancelSpotFleetRequestsRequestRequestTypeDef(TypedDict):
    SpotFleetRequestIds: Sequence[str]
    TerminateInstances: bool
    DryRun: NotRequired[bool]


class CancelSpotFleetRequestsSuccessItemTypeDef(TypedDict):
    CurrentSpotFleetRequestState: NotRequired[BatchStateType]
    PreviousSpotFleetRequestState: NotRequired[BatchStateType]
    SpotFleetRequestId: NotRequired[str]


class CancelSpotInstanceRequestsRequestRequestTypeDef(TypedDict):
    SpotInstanceRequestIds: Sequence[str]
    DryRun: NotRequired[bool]


class CancelledSpotInstanceRequestTypeDef(TypedDict):
    SpotInstanceRequestId: NotRequired[str]
    State: NotRequired[CancelSpotInstanceRequestStateType]


class CapacityAllocationTypeDef(TypedDict):
    AllocationType: NotRequired[Literal["used"]]
    Count: NotRequired[int]


class CapacityBlockExtensionOfferingTypeDef(TypedDict):
    CapacityBlockExtensionOfferingId: NotRequired[str]
    InstanceType: NotRequired[str]
    InstanceCount: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    StartDate: NotRequired[datetime]
    CapacityBlockExtensionStartDate: NotRequired[datetime]
    CapacityBlockExtensionEndDate: NotRequired[datetime]
    CapacityBlockExtensionDurationHours: NotRequired[int]
    UpfrontFee: NotRequired[str]
    CurrencyCode: NotRequired[str]
    Tenancy: NotRequired[CapacityReservationTenancyType]


class CapacityBlockExtensionTypeDef(TypedDict):
    CapacityReservationId: NotRequired[str]
    InstanceType: NotRequired[str]
    InstanceCount: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    CapacityBlockExtensionOfferingId: NotRequired[str]
    CapacityBlockExtensionDurationHours: NotRequired[int]
    CapacityBlockExtensionStatus: NotRequired[CapacityBlockExtensionStatusType]
    CapacityBlockExtensionPurchaseDate: NotRequired[datetime]
    CapacityBlockExtensionStartDate: NotRequired[datetime]
    CapacityBlockExtensionEndDate: NotRequired[datetime]
    UpfrontFee: NotRequired[str]
    CurrencyCode: NotRequired[str]


class CapacityBlockOfferingTypeDef(TypedDict):
    CapacityBlockOfferingId: NotRequired[str]
    InstanceType: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    InstanceCount: NotRequired[int]
    StartDate: NotRequired[datetime]
    EndDate: NotRequired[datetime]
    CapacityBlockDurationHours: NotRequired[int]
    UpfrontFee: NotRequired[str]
    CurrencyCode: NotRequired[str]
    Tenancy: NotRequired[CapacityReservationTenancyType]
    CapacityBlockDurationMinutes: NotRequired[int]


class CapacityReservationInfoTypeDef(TypedDict):
    InstanceType: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    Tenancy: NotRequired[CapacityReservationTenancyType]


class CapacityReservationCommitmentInfoTypeDef(TypedDict):
    CommittedInstanceCount: NotRequired[int]
    CommitmentEndDate: NotRequired[datetime]


class FleetCapacityReservationTypeDef(TypedDict):
    CapacityReservationId: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    InstancePlatform: NotRequired[CapacityReservationInstancePlatformType]
    AvailabilityZone: NotRequired[str]
    TotalInstanceCount: NotRequired[int]
    FulfilledCapacity: NotRequired[float]
    EbsOptimized: NotRequired[bool]
    CreateDate: NotRequired[datetime]
    Weight: NotRequired[float]
    Priority: NotRequired[int]


class CapacityReservationGroupTypeDef(TypedDict):
    GroupArn: NotRequired[str]
    OwnerId: NotRequired[str]


class CapacityReservationOptionsRequestTypeDef(TypedDict):
    UsageStrategy: NotRequired[Literal["use-capacity-reservations-first"]]


class CapacityReservationOptionsTypeDef(TypedDict):
    UsageStrategy: NotRequired[Literal["use-capacity-reservations-first"]]


class CapacityReservationTargetResponseTypeDef(TypedDict):
    CapacityReservationId: NotRequired[str]
    CapacityReservationResourceGroupArn: NotRequired[str]


class CapacityReservationTargetTypeDef(TypedDict):
    CapacityReservationId: NotRequired[str]
    CapacityReservationResourceGroupArn: NotRequired[str]


class CertificateAuthenticationRequestTypeDef(TypedDict):
    ClientRootCertificateChainArn: NotRequired[str]


class CertificateAuthenticationTypeDef(TypedDict):
    ClientRootCertificateChain: NotRequired[str]


class CidrAuthorizationContextTypeDef(TypedDict):
    Message: str
    Signature: str


class CidrBlockTypeDef(TypedDict):
    CidrBlock: NotRequired[str]


class ClassicLinkDnsSupportTypeDef(TypedDict):
    ClassicLinkDnsSupported: NotRequired[bool]
    VpcId: NotRequired[str]


class GroupIdentifierTypeDef(TypedDict):
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]


class ClassicLoadBalancerTypeDef(TypedDict):
    Name: NotRequired[str]


class ClientCertificateRevocationListStatusTypeDef(TypedDict):
    Code: NotRequired[ClientCertificateRevocationListStatusCodeType]
    Message: NotRequired[str]


class ClientConnectOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    LambdaFunctionArn: NotRequired[str]


class ClientVpnEndpointAttributeStatusTypeDef(TypedDict):
    Code: NotRequired[ClientVpnEndpointAttributeStatusCodeType]
    Message: NotRequired[str]


class ClientLoginBannerOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    BannerText: NotRequired[str]


class ClientLoginBannerResponseOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    BannerText: NotRequired[str]


class DirectoryServiceAuthenticationRequestTypeDef(TypedDict):
    DirectoryId: NotRequired[str]


class FederatedAuthenticationRequestTypeDef(TypedDict):
    SAMLProviderArn: NotRequired[str]
    SelfServiceSAMLProviderArn: NotRequired[str]


class DirectoryServiceAuthenticationTypeDef(TypedDict):
    DirectoryId: NotRequired[str]


class FederatedAuthenticationTypeDef(TypedDict):
    SamlProviderArn: NotRequired[str]
    SelfServiceSamlProviderArn: NotRequired[str]


class ClientVpnConnectionStatusTypeDef(TypedDict):
    Code: NotRequired[ClientVpnConnectionStatusCodeType]
    Message: NotRequired[str]


class ClientVpnEndpointStatusTypeDef(TypedDict):
    Code: NotRequired[ClientVpnEndpointStatusCodeType]
    Message: NotRequired[str]


class ConnectionLogResponseOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    CloudwatchLogGroup: NotRequired[str]
    CloudwatchLogStream: NotRequired[str]


class ClientVpnRouteStatusTypeDef(TypedDict):
    Code: NotRequired[ClientVpnRouteStatusCodeType]
    Message: NotRequired[str]


class CloudWatchLogOptionsSpecificationTypeDef(TypedDict):
    LogEnabled: NotRequired[bool]
    LogGroupArn: NotRequired[str]
    LogOutputFormat: NotRequired[str]


class CloudWatchLogOptionsTypeDef(TypedDict):
    LogEnabled: NotRequired[bool]
    LogGroupArn: NotRequired[str]
    LogOutputFormat: NotRequired[str]


class CoipAddressUsageTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    AwsAccountId: NotRequired[str]
    AwsService: NotRequired[str]
    CoIp: NotRequired[str]


class CoipCidrTypeDef(TypedDict):
    Cidr: NotRequired[str]
    CoipPoolId: NotRequired[str]
    LocalGatewayRouteTableId: NotRequired[str]


class ConfirmProductInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str
    ProductCode: str
    DryRun: NotRequired[bool]


class ConnectionLogOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    CloudwatchLogGroup: NotRequired[str]
    CloudwatchLogStream: NotRequired[str]


class ConnectionNotificationTypeDef(TypedDict):
    ConnectionNotificationId: NotRequired[str]
    ServiceId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    ConnectionNotificationType: NotRequired[Literal["Topic"]]
    ConnectionNotificationArn: NotRequired[str]
    ConnectionEvents: NotRequired[list[str]]
    ConnectionNotificationState: NotRequired[ConnectionNotificationStateType]
    ServiceRegion: NotRequired[str]


class ConnectionTrackingConfigurationTypeDef(TypedDict):
    TcpEstablishedTimeout: NotRequired[int]
    UdpStreamTimeout: NotRequired[int]
    UdpTimeout: NotRequired[int]


class ConnectionTrackingSpecificationRequestTypeDef(TypedDict):
    TcpEstablishedTimeout: NotRequired[int]
    UdpStreamTimeout: NotRequired[int]
    UdpTimeout: NotRequired[int]


class ConnectionTrackingSpecificationResponseTypeDef(TypedDict):
    TcpEstablishedTimeout: NotRequired[int]
    UdpStreamTimeout: NotRequired[int]
    UdpTimeout: NotRequired[int]


class ConnectionTrackingSpecificationTypeDef(TypedDict):
    TcpEstablishedTimeout: NotRequired[int]
    UdpTimeout: NotRequired[int]
    UdpStreamTimeout: NotRequired[int]


class CopyFpgaImageRequestRequestTypeDef(TypedDict):
    SourceFpgaImageId: str
    SourceRegion: str
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ClientToken: NotRequired[str]


class CpuOptionsRequestTypeDef(TypedDict):
    CoreCount: NotRequired[int]
    ThreadsPerCore: NotRequired[int]
    AmdSevSnp: NotRequired[AmdSevSnpSpecificationType]


class CpuOptionsTypeDef(TypedDict):
    CoreCount: NotRequired[int]
    ThreadsPerCore: NotRequired[int]
    AmdSevSnp: NotRequired[AmdSevSnpSpecificationType]


class PerformanceFactorReferenceTypeDef(TypedDict):
    InstanceFamily: NotRequired[str]


class PerformanceFactorReferenceRequestTypeDef(TypedDict):
    InstanceFamily: NotRequired[str]


class ReservationFleetInstanceSpecificationTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    InstancePlatform: NotRequired[CapacityReservationInstancePlatformType]
    Weight: NotRequired[float]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    EbsOptimized: NotRequired[bool]
    Priority: NotRequired[int]


class CreateClientVpnRouteRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DestinationCidrBlock: str
    TargetVpcSubnetId: str
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateCoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    CoipPoolId: str
    DryRun: NotRequired[bool]


class CreateDefaultSubnetRequestRequestTypeDef(TypedDict):
    AvailabilityZone: str
    DryRun: NotRequired[bool]
    Ipv6Native: NotRequired[bool]


class CreateDefaultVpcRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class NewDhcpConfigurationTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class TargetCapacitySpecificationRequestTypeDef(TypedDict):
    TotalTargetCapacity: int
    OnDemandTargetCapacity: NotRequired[int]
    SpotTargetCapacity: NotRequired[int]
    DefaultTargetCapacityType: NotRequired[DefaultTargetCapacityTypeType]
    TargetCapacityUnitType: NotRequired[TargetCapacityUnitTypeType]


class DestinationOptionsRequestTypeDef(TypedDict):
    FileFormat: NotRequired[DestinationFileFormatType]
    HiveCompatiblePartitions: NotRequired[bool]
    PerHourPartition: NotRequired[bool]


class StorageLocationTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Key: NotRequired[str]


class InstanceEventWindowTimeRangeRequestTypeDef(TypedDict):
    StartWeekDay: NotRequired[WeekDayType]
    StartHour: NotRequired[int]
    EndWeekDay: NotRequired[WeekDayType]
    EndHour: NotRequired[int]


class ExportToS3TaskSpecificationTypeDef(TypedDict):
    DiskImageFormat: NotRequired[DiskImageFormatType]
    ContainerFormat: NotRequired[Literal["ova"]]
    S3Bucket: NotRequired[str]
    S3Prefix: NotRequired[str]


class IpamPoolSourceResourceRequestTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[Literal["vpc"]]
    ResourceRegion: NotRequired[str]
    ResourceOwner: NotRequired[str]


class RequestIpamResourceTagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class OperatorRequestTypeDef(TypedDict):
    Principal: NotRequired[str]


class CreateLocalGatewayRouteRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    DestinationCidrBlock: NotRequired[str]
    LocalGatewayVirtualInterfaceGroupId: NotRequired[str]
    DryRun: NotRequired[bool]
    NetworkInterfaceId: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]


LocalGatewayRouteTypeDef = TypedDict(
    "LocalGatewayRouteTypeDef",
    {
        "DestinationCidrBlock": NotRequired[str],
        "LocalGatewayVirtualInterfaceGroupId": NotRequired[str],
        "Type": NotRequired[LocalGatewayRouteTypeType],
        "State": NotRequired[LocalGatewayRouteStateType],
        "LocalGatewayRouteTableId": NotRequired[str],
        "LocalGatewayRouteTableArn": NotRequired[str],
        "OwnerId": NotRequired[str],
        "SubnetId": NotRequired[str],
        "CoipPoolId": NotRequired[str],
        "NetworkInterfaceId": NotRequired[str],
        "DestinationPrefixListId": NotRequired[str],
    },
)
IcmpTypeCodeTypeDef = TypedDict(
    "IcmpTypeCodeTypeDef",
    {
        "Code": NotRequired[int],
        "Type": NotRequired[int],
    },
)


class CreateNetworkInterfacePermissionRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    Permission: InterfacePermissionTypeType
    AwsAccountId: NotRequired[str]
    AwsService: NotRequired[str]
    DryRun: NotRequired[bool]


class InstanceIpv6AddressTypeDef(TypedDict):
    Ipv6Address: NotRequired[str]
    IsPrimaryIpv6: NotRequired[bool]


class Ipv4PrefixSpecificationRequestTypeDef(TypedDict):
    Ipv4Prefix: NotRequired[str]


class Ipv6PrefixSpecificationRequestTypeDef(TypedDict):
    Ipv6Prefix: NotRequired[str]


class PrivateIpAddressSpecificationTypeDef(TypedDict):
    Primary: NotRequired[bool]
    PrivateIpAddress: NotRequired[str]


class PriceScheduleSpecificationTypeDef(TypedDict):
    Term: NotRequired[int]
    Price: NotRequired[float]
    CurrencyCode: NotRequired[Literal["USD"]]


class CreateRouteRequestRequestTypeDef(TypedDict):
    RouteTableId: str
    DestinationPrefixListId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    CarrierGatewayId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationCidrBlock: NotRequired[str]
    GatewayId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    EgressOnlyInternetGatewayId: NotRequired[str]
    InstanceId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    NatGatewayId: NotRequired[str]


class CreateRouteRequestRouteTableCreateRouteTypeDef(TypedDict):
    DestinationPrefixListId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    CarrierGatewayId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationCidrBlock: NotRequired[str]
    GatewayId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    EgressOnlyInternetGatewayId: NotRequired[str]
    InstanceId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    NatGatewayId: NotRequired[str]


class InstanceSpecificationTypeDef(TypedDict):
    InstanceId: str
    ExcludeBootVolume: NotRequired[bool]
    ExcludeDataVolumeIds: NotRequired[Sequence[str]]


class CreateSpotDatafeedSubscriptionRequestRequestTypeDef(TypedDict):
    Bucket: str
    DryRun: NotRequired[bool]
    Prefix: NotRequired[str]


class S3ObjectTagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class TrafficMirrorPortRangeRequestTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


class TransitGatewayConnectRequestBgpOptionsTypeDef(TypedDict):
    PeerAsn: NotRequired[int]


CreateTransitGatewayConnectRequestOptionsTypeDef = TypedDict(
    "CreateTransitGatewayConnectRequestOptionsTypeDef",
    {
        "Protocol": Literal["gre"],
    },
)


class CreateTransitGatewayMulticastDomainRequestOptionsTypeDef(TypedDict):
    Igmpv2Support: NotRequired[Igmpv2SupportValueType]
    StaticSourcesSupport: NotRequired[StaticSourcesSupportValueType]
    AutoAcceptSharedAssociations: NotRequired[AutoAcceptSharedAssociationsValueType]


class CreateTransitGatewayPeeringAttachmentRequestOptionsTypeDef(TypedDict):
    DynamicRouting: NotRequired[DynamicRoutingValueType]


class CreateTransitGatewayPrefixListReferenceRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    PrefixListId: str
    TransitGatewayAttachmentId: NotRequired[str]
    Blackhole: NotRequired[bool]
    DryRun: NotRequired[bool]


class TransitGatewayRequestOptionsTypeDef(TypedDict):
    AmazonSideAsn: NotRequired[int]
    AutoAcceptSharedAttachments: NotRequired[AutoAcceptSharedAttachmentsValueType]
    DefaultRouteTableAssociation: NotRequired[DefaultRouteTableAssociationValueType]
    DefaultRouteTablePropagation: NotRequired[DefaultRouteTablePropagationValueType]
    VpnEcmpSupport: NotRequired[VpnEcmpSupportValueType]
    DnsSupport: NotRequired[DnsSupportValueType]
    SecurityGroupReferencingSupport: NotRequired[SecurityGroupReferencingSupportValueType]
    MulticastSupport: NotRequired[MulticastSupportValueType]
    TransitGatewayCidrBlocks: NotRequired[Sequence[str]]


class CreateTransitGatewayRouteRequestRequestTypeDef(TypedDict):
    DestinationCidrBlock: str
    TransitGatewayRouteTableId: str
    TransitGatewayAttachmentId: NotRequired[str]
    Blackhole: NotRequired[bool]
    DryRun: NotRequired[bool]


class CreateTransitGatewayVpcAttachmentRequestOptionsTypeDef(TypedDict):
    DnsSupport: NotRequired[DnsSupportValueType]
    SecurityGroupReferencingSupport: NotRequired[SecurityGroupReferencingSupportValueType]
    Ipv6Support: NotRequired[Ipv6SupportValueType]
    ApplianceModeSupport: NotRequired[ApplianceModeSupportValueType]


class CreateVerifiedAccessEndpointPortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


CreateVerifiedAccessEndpointRdsOptionsTypeDef = TypedDict(
    "CreateVerifiedAccessEndpointRdsOptionsTypeDef",
    {
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "RdsDbInstanceArn": NotRequired[str],
        "RdsDbClusterArn": NotRequired[str],
        "RdsDbProxyArn": NotRequired[str],
        "RdsEndpoint": NotRequired[str],
        "SubnetIds": NotRequired[Sequence[str]],
    },
)


class VerifiedAccessSseSpecificationRequestTypeDef(TypedDict):
    CustomerManagedKeyEnabled: NotRequired[bool]
    KmsKeyArn: NotRequired[str]


class CreateVerifiedAccessNativeApplicationOidcOptionsTypeDef(TypedDict):
    PublicSigningKeyEndpoint: NotRequired[str]
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]
    Scope: NotRequired[str]


class CreateVerifiedAccessTrustProviderDeviceOptionsTypeDef(TypedDict):
    TenantId: NotRequired[str]
    PublicSigningKeyUrl: NotRequired[str]


class CreateVerifiedAccessTrustProviderOidcOptionsTypeDef(TypedDict):
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]
    Scope: NotRequired[str]


class CreateVolumePermissionTypeDef(TypedDict):
    UserId: NotRequired[str]
    Group: NotRequired[Literal["all"]]


class CreateVpcEndpointConnectionNotificationRequestRequestTypeDef(TypedDict):
    ConnectionNotificationArn: str
    ConnectionEvents: Sequence[str]
    DryRun: NotRequired[bool]
    ServiceId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    ClientToken: NotRequired[str]


class DnsOptionsSpecificationTypeDef(TypedDict):
    DnsRecordIpType: NotRequired[DnsRecordIpTypeType]
    PrivateDnsOnlyForInboundResolverEndpoint: NotRequired[bool]


class SubnetConfigurationTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    Ipv4: NotRequired[str]
    Ipv6: NotRequired[str]


class CreateVpnConnectionRouteRequestRequestTypeDef(TypedDict):
    DestinationCidrBlock: str
    VpnConnectionId: str


class CreditSpecificationRequestTypeDef(TypedDict):
    CpuCredits: str


class CreditSpecificationTypeDef(TypedDict):
    CpuCredits: NotRequired[str]


class DataQueryTypeDef(TypedDict):
    Id: NotRequired[str]
    Source: NotRequired[str]
    Destination: NotRequired[str]
    Metric: NotRequired[Literal["aggregate-latency"]]
    Statistic: NotRequired[Literal["p50"]]
    Period: NotRequired[PeriodTypeType]


class MetricPointTypeDef(TypedDict):
    StartDate: NotRequired[datetime]
    EndDate: NotRequired[datetime]
    Value: NotRequired[float]
    Status: NotRequired[str]


class DeleteCarrierGatewayRequestRequestTypeDef(TypedDict):
    CarrierGatewayId: str
    DryRun: NotRequired[bool]


class DeleteClientVpnEndpointRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DryRun: NotRequired[bool]


class DeleteClientVpnRouteRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DestinationCidrBlock: str
    TargetVpcSubnetId: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteCoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    CoipPoolId: str
    DryRun: NotRequired[bool]


class DeleteCoipPoolRequestRequestTypeDef(TypedDict):
    CoipPoolId: str
    DryRun: NotRequired[bool]


class DeleteCustomerGatewayRequestRequestTypeDef(TypedDict):
    CustomerGatewayId: str
    DryRun: NotRequired[bool]


class DeleteDhcpOptionsRequestDhcpOptionsDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteDhcpOptionsRequestRequestTypeDef(TypedDict):
    DhcpOptionsId: str
    DryRun: NotRequired[bool]


class DeleteEgressOnlyInternetGatewayRequestRequestTypeDef(TypedDict):
    EgressOnlyInternetGatewayId: str
    DryRun: NotRequired[bool]


class DeleteFleetErrorTypeDef(TypedDict):
    Code: NotRequired[DeleteFleetErrorCodeType]
    Message: NotRequired[str]


class DeleteFleetSuccessItemTypeDef(TypedDict):
    CurrentFleetState: NotRequired[FleetStateCodeType]
    PreviousFleetState: NotRequired[FleetStateCodeType]
    FleetId: NotRequired[str]


class DeleteFleetsRequestRequestTypeDef(TypedDict):
    FleetIds: Sequence[str]
    TerminateInstances: bool
    DryRun: NotRequired[bool]


class DeleteFlowLogsRequestRequestTypeDef(TypedDict):
    FlowLogIds: Sequence[str]
    DryRun: NotRequired[bool]


class DeleteFpgaImageRequestRequestTypeDef(TypedDict):
    FpgaImageId: str
    DryRun: NotRequired[bool]


class DeleteInstanceConnectEndpointRequestRequestTypeDef(TypedDict):
    InstanceConnectEndpointId: str
    DryRun: NotRequired[bool]


class DeleteInstanceEventWindowRequestRequestTypeDef(TypedDict):
    InstanceEventWindowId: str
    DryRun: NotRequired[bool]
    ForceDelete: NotRequired[bool]


class InstanceEventWindowStateChangeTypeDef(TypedDict):
    InstanceEventWindowId: NotRequired[str]
    State: NotRequired[InstanceEventWindowStateType]


class DeleteInternetGatewayRequestInternetGatewayDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteInternetGatewayRequestRequestTypeDef(TypedDict):
    InternetGatewayId: str
    DryRun: NotRequired[bool]


class DeleteIpamExternalResourceVerificationTokenRequestRequestTypeDef(TypedDict):
    IpamExternalResourceVerificationTokenId: str
    DryRun: NotRequired[bool]


class DeleteIpamPoolRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Cascade: NotRequired[bool]


class DeleteIpamRequestRequestTypeDef(TypedDict):
    IpamId: str
    DryRun: NotRequired[bool]
    Cascade: NotRequired[bool]


class DeleteIpamResourceDiscoveryRequestRequestTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    DryRun: NotRequired[bool]


class DeleteIpamScopeRequestRequestTypeDef(TypedDict):
    IpamScopeId: str
    DryRun: NotRequired[bool]


class DeleteKeyPairRequestKeyPairDeleteTypeDef(TypedDict):
    KeyPairId: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteKeyPairRequestKeyPairInfoDeleteTypeDef(TypedDict):
    KeyPairId: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteKeyPairRequestRequestTypeDef(TypedDict):
    KeyName: NotRequired[str]
    KeyPairId: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteLaunchTemplateRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]


class DeleteLaunchTemplateVersionsRequestRequestTypeDef(TypedDict):
    Versions: Sequence[str]
    DryRun: NotRequired[bool]
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]


class ResponseErrorTypeDef(TypedDict):
    Code: NotRequired[LaunchTemplateErrorCodeType]
    Message: NotRequired[str]


class DeleteLaunchTemplateVersionsResponseSuccessItemTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    VersionNumber: NotRequired[int]


class DeleteLocalGatewayRouteRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    DestinationCidrBlock: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationPrefixListId: NotRequired[str]


class DeleteLocalGatewayRouteTableRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    DryRun: NotRequired[bool]


class DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociationId: str
    DryRun: NotRequired[bool]


class DeleteLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociationId: str
    DryRun: NotRequired[bool]


class DeleteManagedPrefixListRequestRequestTypeDef(TypedDict):
    PrefixListId: str
    DryRun: NotRequired[bool]


class DeleteNatGatewayRequestRequestTypeDef(TypedDict):
    NatGatewayId: str
    DryRun: NotRequired[bool]


class DeleteNetworkAclEntryRequestNetworkAclDeleteEntryTypeDef(TypedDict):
    RuleNumber: int
    Egress: bool
    DryRun: NotRequired[bool]


class DeleteNetworkAclEntryRequestRequestTypeDef(TypedDict):
    NetworkAclId: str
    RuleNumber: int
    Egress: bool
    DryRun: NotRequired[bool]


class DeleteNetworkAclRequestNetworkAclDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteNetworkAclRequestRequestTypeDef(TypedDict):
    NetworkAclId: str
    DryRun: NotRequired[bool]


class DeleteNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: str
    DryRun: NotRequired[bool]


class DeleteNetworkInsightsAccessScopeRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeId: str
    DryRun: NotRequired[bool]


class DeleteNetworkInsightsAnalysisRequestRequestTypeDef(TypedDict):
    NetworkInsightsAnalysisId: str
    DryRun: NotRequired[bool]


class DeleteNetworkInsightsPathRequestRequestTypeDef(TypedDict):
    NetworkInsightsPathId: str
    DryRun: NotRequired[bool]


class DeleteNetworkInterfacePermissionRequestRequestTypeDef(TypedDict):
    NetworkInterfacePermissionId: str
    Force: NotRequired[bool]
    DryRun: NotRequired[bool]


class DeleteNetworkInterfaceRequestNetworkInterfaceDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteNetworkInterfaceRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    DryRun: NotRequired[bool]


class DeletePlacementGroupRequestPlacementGroupDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeletePlacementGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    DryRun: NotRequired[bool]


class DeletePublicIpv4PoolRequestRequestTypeDef(TypedDict):
    PoolId: str
    DryRun: NotRequired[bool]
    NetworkBorderGroup: NotRequired[str]


class DeleteQueuedReservedInstancesErrorTypeDef(TypedDict):
    Code: NotRequired[DeleteQueuedReservedInstancesErrorCodeType]
    Message: NotRequired[str]


class DeleteQueuedReservedInstancesRequestRequestTypeDef(TypedDict):
    ReservedInstancesIds: Sequence[str]
    DryRun: NotRequired[bool]


class SuccessfulQueuedPurchaseDeletionTypeDef(TypedDict):
    ReservedInstancesId: NotRequired[str]


class DeleteRouteRequestRequestTypeDef(TypedDict):
    RouteTableId: str
    DestinationPrefixListId: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationCidrBlock: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]


class DeleteRouteRequestRouteDeleteTypeDef(TypedDict):
    DestinationPrefixListId: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationIpv6CidrBlock: NotRequired[str]


class DeleteRouteTableRequestRequestTypeDef(TypedDict):
    RouteTableId: str
    DryRun: NotRequired[bool]


class DeleteRouteTableRequestRouteTableDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteSecurityGroupRequestRequestTypeDef(TypedDict):
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteSecurityGroupRequestSecurityGroupDeleteTypeDef(TypedDict):
    GroupName: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    DryRun: NotRequired[bool]


class DeleteSnapshotRequestSnapshotDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteSpotDatafeedSubscriptionRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteSubnetCidrReservationRequestRequestTypeDef(TypedDict):
    SubnetCidrReservationId: str
    DryRun: NotRequired[bool]


class DeleteSubnetRequestRequestTypeDef(TypedDict):
    SubnetId: str
    DryRun: NotRequired[bool]


class DeleteSubnetRequestSubnetDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteTagsRequestTagDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteTrafficMirrorFilterRequestRequestTypeDef(TypedDict):
    TrafficMirrorFilterId: str
    DryRun: NotRequired[bool]


class DeleteTrafficMirrorFilterRuleRequestRequestTypeDef(TypedDict):
    TrafficMirrorFilterRuleId: str
    DryRun: NotRequired[bool]


class DeleteTrafficMirrorSessionRequestRequestTypeDef(TypedDict):
    TrafficMirrorSessionId: str
    DryRun: NotRequired[bool]


class DeleteTrafficMirrorTargetRequestRequestTypeDef(TypedDict):
    TrafficMirrorTargetId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayConnectPeerRequestRequestTypeDef(TypedDict):
    TransitGatewayConnectPeerId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayConnectRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayMulticastDomainRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayPeeringAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayPolicyTableRequestRequestTypeDef(TypedDict):
    TransitGatewayPolicyTableId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayPrefixListReferenceRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    PrefixListId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayRouteRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    DestinationCidrBlock: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayRouteTableAnnouncementRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncementId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayRouteTableRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    DryRun: NotRequired[bool]


class DeleteTransitGatewayVpcAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class DeleteVerifiedAccessEndpointRequestRequestTypeDef(TypedDict):
    VerifiedAccessEndpointId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteVerifiedAccessGroupRequestRequestTypeDef(TypedDict):
    VerifiedAccessGroupId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DeleteVerifiedAccessInstanceRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class DeleteVerifiedAccessTrustProviderRequestRequestTypeDef(TypedDict):
    VerifiedAccessTrustProviderId: str
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class DeleteVolumeRequestRequestTypeDef(TypedDict):
    VolumeId: str
    DryRun: NotRequired[bool]


class DeleteVolumeRequestVolumeDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteVpcBlockPublicAccessExclusionRequestRequestTypeDef(TypedDict):
    ExclusionId: str
    DryRun: NotRequired[bool]


class DeleteVpcEndpointConnectionNotificationsRequestRequestTypeDef(TypedDict):
    ConnectionNotificationIds: Sequence[str]
    DryRun: NotRequired[bool]


class DeleteVpcEndpointServiceConfigurationsRequestRequestTypeDef(TypedDict):
    ServiceIds: Sequence[str]
    DryRun: NotRequired[bool]


class DeleteVpcEndpointsRequestRequestTypeDef(TypedDict):
    VpcEndpointIds: Sequence[str]
    DryRun: NotRequired[bool]


class DeleteVpcPeeringConnectionRequestRequestTypeDef(TypedDict):
    VpcPeeringConnectionId: str
    DryRun: NotRequired[bool]


class DeleteVpcPeeringConnectionRequestVpcPeeringConnectionDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteVpcRequestRequestTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class DeleteVpcRequestVpcDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeleteVpnConnectionRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    DryRun: NotRequired[bool]


class DeleteVpnConnectionRouteRequestRequestTypeDef(TypedDict):
    DestinationCidrBlock: str
    VpnConnectionId: str


class DeleteVpnGatewayRequestRequestTypeDef(TypedDict):
    VpnGatewayId: str
    DryRun: NotRequired[bool]


class DeprovisionByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    DryRun: NotRequired[bool]


class DeprovisionIpamByoasnRequestRequestTypeDef(TypedDict):
    IpamId: str
    Asn: str
    DryRun: NotRequired[bool]


class DeprovisionIpamPoolCidrRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Cidr: NotRequired[str]


class DeprovisionPublicIpv4PoolCidrRequestRequestTypeDef(TypedDict):
    PoolId: str
    Cidr: str
    DryRun: NotRequired[bool]


class DeregisterImageRequestImageDeregisterTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DeregisterImageRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class DeregisterInstanceTagAttributeRequestTypeDef(TypedDict):
    IncludeAllTagsOfInstance: NotRequired[bool]
    InstanceTagKeys: NotRequired[Sequence[str]]


class InstanceTagNotificationAttributeTypeDef(TypedDict):
    InstanceTagKeys: NotRequired[list[str]]
    IncludeAllTagsOfInstance: NotRequired[bool]


class DeregisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    GroupIpAddress: NotRequired[str]
    NetworkInterfaceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class TransitGatewayMulticastDeregisteredGroupMembersTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    DeregisteredNetworkInterfaceIds: NotRequired[list[str]]
    GroupIpAddress: NotRequired[str]


class DeregisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    GroupIpAddress: NotRequired[str]
    NetworkInterfaceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class TransitGatewayMulticastDeregisteredGroupSourcesTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    DeregisteredNetworkInterfaceIds: NotRequired[list[str]]
    GroupIpAddress: NotRequired[str]


class DescribeAccountAttributesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    AttributeNames: NotRequired[Sequence[AccountAttributeNameType]]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeAddressTransfersRequestRequestTypeDef(TypedDict):
    AllocationIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class DescribeAddressesAttributeRequestRequestTypeDef(TypedDict):
    AllocationIds: NotRequired[Sequence[str]]
    Attribute: NotRequired[Literal["domain-name"]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class FilterTypeDef(TypedDict):
    Name: NotRequired[str]
    Values: NotRequired[Sequence[str]]


class DescribeAggregateIdFormatRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class IdFormatTypeDef(TypedDict):
    Deadline: NotRequired[datetime]
    Resource: NotRequired[str]
    UseLongIds: NotRequired[bool]


class SubscriptionTypeDef(TypedDict):
    Source: NotRequired[str]
    Destination: NotRequired[str]
    Metric: NotRequired[Literal["aggregate-latency"]]
    Statistic: NotRequired[Literal["p50"]]
    Period: NotRequired[PeriodTypeType]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeByoipCidrsRequestRequestTypeDef(TypedDict):
    MaxResults: int
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]


class DescribeCapacityBlockExtensionOfferingsRequestRequestTypeDef(TypedDict):
    CapacityBlockExtensionDurationHours: int
    CapacityReservationId: str
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeConversionTasksRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ConversionTaskIds: NotRequired[Sequence[str]]


class DescribeDeclarativePoliciesReportsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    ReportIds: NotRequired[Sequence[str]]


class FastLaunchLaunchTemplateSpecificationResponseTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Version: NotRequired[str]


class FastLaunchSnapshotConfigurationResponseTypeDef(TypedDict):
    TargetResourceCount: NotRequired[int]


class DescribeFastSnapshotRestoreSuccessItemTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    State: NotRequired[FastSnapshotRestoreStateCodeType]
    StateTransitionReason: NotRequired[str]
    OwnerId: NotRequired[str]
    OwnerAlias: NotRequired[str]
    EnablingTime: NotRequired[datetime]
    OptimizingTime: NotRequired[datetime]
    EnabledTime: NotRequired[datetime]
    DisablingTime: NotRequired[datetime]
    DisabledTime: NotRequired[datetime]


class DescribeFpgaImageAttributeRequestRequestTypeDef(TypedDict):
    FpgaImageId: str
    Attribute: FpgaImageAttributeNameType
    DryRun: NotRequired[bool]


class HostOfferingTypeDef(TypedDict):
    CurrencyCode: NotRequired[Literal["USD"]]
    Duration: NotRequired[int]
    HourlyPrice: NotRequired[str]
    InstanceFamily: NotRequired[str]
    OfferingId: NotRequired[str]
    PaymentOption: NotRequired[PaymentOptionType]
    UpfrontPrice: NotRequired[str]


class DescribeIdFormatRequestRequestTypeDef(TypedDict):
    Resource: NotRequired[str]


class DescribeIdentityIdFormatRequestRequestTypeDef(TypedDict):
    PrincipalArn: str
    Resource: NotRequired[str]


class DescribeImageAttributeRequestImageDescribeAttributeTypeDef(TypedDict):
    Attribute: ImageAttributeNameType
    DryRun: NotRequired[bool]


class DescribeImageAttributeRequestRequestTypeDef(TypedDict):
    Attribute: ImageAttributeNameType
    ImageId: str
    DryRun: NotRequired[bool]


class DescribeInstanceAttributeRequestInstanceDescribeAttributeTypeDef(TypedDict):
    Attribute: InstanceAttributeNameType
    DryRun: NotRequired[bool]


class DescribeInstanceAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Attribute: InstanceAttributeNameType
    DryRun: NotRequired[bool]


class InstanceCreditSpecificationTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    CpuCredits: NotRequired[str]


class DescribeInstanceEventNotificationAttributesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class InstanceTopologyTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    GroupName: NotRequired[str]
    NetworkNodes: NotRequired[list[str]]
    AvailabilityZone: NotRequired[str]
    ZoneId: NotRequired[str]


class InstanceTypeOfferingTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    LocationType: NotRequired[LocationTypeType]
    Location: NotRequired[str]


class DescribeIpamByoasnRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class LockedSnapshotsInfoTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    SnapshotId: NotRequired[str]
    LockState: NotRequired[LockStateType]
    LockDuration: NotRequired[int]
    CoolOffPeriod: NotRequired[int]
    CoolOffPeriodExpiresOn: NotRequired[datetime]
    LockCreatedOn: NotRequired[datetime]
    LockDurationStartTime: NotRequired[datetime]
    LockExpiresOn: NotRequired[datetime]


class MacHostTypeDef(TypedDict):
    HostId: NotRequired[str]
    MacOSLatestSupportedVersions: NotRequired[list[str]]


class MovingAddressStatusTypeDef(TypedDict):
    MoveStatus: NotRequired[MoveStatusType]
    PublicIp: NotRequired[str]


class DescribeNetworkInterfaceAttributeRequestNetworkInterfaceDescribeAttributeTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Attribute: NotRequired[NetworkInterfaceAttributeType]


class DescribeNetworkInterfaceAttributeRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    DryRun: NotRequired[bool]
    Attribute: NotRequired[NetworkInterfaceAttributeType]


class PrefixListTypeDef(TypedDict):
    Cidrs: NotRequired[list[str]]
    PrefixListId: NotRequired[str]
    PrefixListName: NotRequired[str]


class DescribePrincipalIdFormatRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Resources: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


RegionTypeDef = TypedDict(
    "RegionTypeDef",
    {
        "OptInStatus": NotRequired[str],
        "RegionName": NotRequired[str],
        "Endpoint": NotRequired[str],
    },
)


class ScheduledInstanceRecurrenceRequestTypeDef(TypedDict):
    Frequency: NotRequired[str]
    Interval: NotRequired[int]
    OccurrenceDays: NotRequired[Sequence[int]]
    OccurrenceRelativeToEnd: NotRequired[bool]
    OccurrenceUnit: NotRequired[str]


class DescribeSecurityGroupReferencesRequestRequestTypeDef(TypedDict):
    GroupId: Sequence[str]
    DryRun: NotRequired[bool]


class SecurityGroupReferenceTypeDef(TypedDict):
    GroupId: NotRequired[str]
    ReferencingVpcId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    TransitGatewayId: NotRequired[str]


class SecurityGroupVpcAssociationTypeDef(TypedDict):
    GroupId: NotRequired[str]
    VpcId: NotRequired[str]
    VpcOwnerId: NotRequired[str]
    State: NotRequired[SecurityGroupVpcAssociationStateType]
    StateReason: NotRequired[str]


class DescribeSnapshotAttributeRequestRequestTypeDef(TypedDict):
    Attribute: SnapshotAttributeNameType
    SnapshotId: str
    DryRun: NotRequired[bool]


class DescribeSnapshotAttributeRequestSnapshotDescribeAttributeTypeDef(TypedDict):
    Attribute: SnapshotAttributeNameType
    DryRun: NotRequired[bool]


class ProductCodeTypeDef(TypedDict):
    ProductCodeId: NotRequired[str]
    ProductCodeType: NotRequired[ProductCodeValuesType]


class DescribeSpotDatafeedSubscriptionRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DescribeSpotFleetInstancesRequestRequestTypeDef(TypedDict):
    SpotFleetRequestId: str
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeSpotFleetRequestsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    SpotFleetRequestIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SpotPriceTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    ProductDescription: NotRequired[RIProductDescriptionType]
    SpotPrice: NotRequired[str]
    Timestamp: NotRequired[datetime]


class DescribeStaleSecurityGroupsRequestRequestTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class StoreImageTaskResultTypeDef(TypedDict):
    AmiId: NotRequired[str]
    TaskStartTime: NotRequired[datetime]
    Bucket: NotRequired[str]
    S3objectKey: NotRequired[str]
    ProgressPercentage: NotRequired[int]
    StoreTaskState: NotRequired[str]
    StoreTaskFailureReason: NotRequired[str]


class TagDescriptionTypeDef(TypedDict):
    Key: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[ResourceTypeType]
    Value: NotRequired[str]


class DescribeVolumeAttributeRequestRequestTypeDef(TypedDict):
    Attribute: VolumeAttributeNameType
    VolumeId: str
    DryRun: NotRequired[bool]


class DescribeVolumeAttributeRequestVolumeDescribeAttributeTypeDef(TypedDict):
    Attribute: VolumeAttributeNameType
    DryRun: NotRequired[bool]


class VolumeModificationTypeDef(TypedDict):
    VolumeId: NotRequired[str]
    ModificationState: NotRequired[VolumeModificationStateType]
    StatusMessage: NotRequired[str]
    TargetSize: NotRequired[int]
    TargetIops: NotRequired[int]
    TargetVolumeType: NotRequired[VolumeTypeType]
    TargetThroughput: NotRequired[int]
    TargetMultiAttachEnabled: NotRequired[bool]
    OriginalSize: NotRequired[int]
    OriginalIops: NotRequired[int]
    OriginalVolumeType: NotRequired[VolumeTypeType]
    OriginalThroughput: NotRequired[int]
    OriginalMultiAttachEnabled: NotRequired[bool]
    Progress: NotRequired[int]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]


class DescribeVpcAttributeRequestRequestTypeDef(TypedDict):
    Attribute: VpcAttributeNameType
    VpcId: str
    DryRun: NotRequired[bool]


class DescribeVpcAttributeRequestVpcDescribeAttributeTypeDef(TypedDict):
    Attribute: VpcAttributeNameType
    DryRun: NotRequired[bool]


class DescribeVpcBlockPublicAccessOptionsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class VpcBlockPublicAccessOptionsTypeDef(TypedDict):
    AwsAccountId: NotRequired[str]
    AwsRegion: NotRequired[str]
    State: NotRequired[VpcBlockPublicAccessStateType]
    InternetGatewayBlockMode: NotRequired[InternetGatewayBlockModeType]
    Reason: NotRequired[str]
    LastUpdateTimestamp: NotRequired[datetime]
    ManagedBy: NotRequired[ManagedByType]
    ExclusionsAllowed: NotRequired[VpcBlockPublicAccessExclusionsAllowedType]


class DescribeVpcClassicLinkDnsSupportRequestRequestTypeDef(TypedDict):
    VpcIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DestinationOptionsResponseTypeDef(TypedDict):
    FileFormat: NotRequired[DestinationFileFormatType]
    HiveCompatiblePartitions: NotRequired[bool]
    PerHourPartition: NotRequired[bool]


class DetachClassicLinkVpcRequestInstanceDetachClassicLinkVpcTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class DetachClassicLinkVpcRequestRequestTypeDef(TypedDict):
    InstanceId: str
    VpcId: str
    DryRun: NotRequired[bool]


class DetachClassicLinkVpcRequestVpcDetachClassicLinkInstanceTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]


class DetachInternetGatewayRequestInternetGatewayDetachFromVpcTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class DetachInternetGatewayRequestRequestTypeDef(TypedDict):
    InternetGatewayId: str
    VpcId: str
    DryRun: NotRequired[bool]


class DetachInternetGatewayRequestVpcDetachInternetGatewayTypeDef(TypedDict):
    InternetGatewayId: str
    DryRun: NotRequired[bool]


class DetachNetworkInterfaceRequestNetworkInterfaceDetachTypeDef(TypedDict):
    AttachmentId: str
    DryRun: NotRequired[bool]
    Force: NotRequired[bool]


class DetachNetworkInterfaceRequestRequestTypeDef(TypedDict):
    AttachmentId: str
    DryRun: NotRequired[bool]
    Force: NotRequired[bool]


class DetachVerifiedAccessTrustProviderRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    VerifiedAccessTrustProviderId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DetachVolumeRequestInstanceDetachVolumeTypeDef(TypedDict):
    VolumeId: str
    Device: NotRequired[str]
    Force: NotRequired[bool]
    DryRun: NotRequired[bool]


class DetachVolumeRequestRequestTypeDef(TypedDict):
    VolumeId: str
    Device: NotRequired[str]
    Force: NotRequired[bool]
    InstanceId: NotRequired[str]
    DryRun: NotRequired[bool]


class DetachVolumeRequestVolumeDetachFromInstanceTypeDef(TypedDict):
    Device: NotRequired[str]
    Force: NotRequired[bool]
    InstanceId: NotRequired[str]
    DryRun: NotRequired[bool]


class DetachVpnGatewayRequestRequestTypeDef(TypedDict):
    VpcId: str
    VpnGatewayId: str
    DryRun: NotRequired[bool]


class DeviceOptionsTypeDef(TypedDict):
    TenantId: NotRequired[str]
    PublicSigningKeyUrl: NotRequired[str]


class DisableAddressTransferRequestRequestTypeDef(TypedDict):
    AllocationId: str
    DryRun: NotRequired[bool]


class DisableAllowedImagesSettingsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef(TypedDict):
    Source: NotRequired[str]
    Destination: NotRequired[str]
    Metric: NotRequired[Literal["aggregate-latency"]]
    Statistic: NotRequired[Literal["p50"]]
    DryRun: NotRequired[bool]


class DisableEbsEncryptionByDefaultRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisableFastLaunchRequestRequestTypeDef(TypedDict):
    ImageId: str
    Force: NotRequired[bool]
    DryRun: NotRequired[bool]


class DisableFastSnapshotRestoreStateErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class DisableFastSnapshotRestoreSuccessItemTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    State: NotRequired[FastSnapshotRestoreStateCodeType]
    StateTransitionReason: NotRequired[str]
    OwnerId: NotRequired[str]
    OwnerAlias: NotRequired[str]
    EnablingTime: NotRequired[datetime]
    OptimizingTime: NotRequired[datetime]
    EnabledTime: NotRequired[datetime]
    DisablingTime: NotRequired[datetime]
    DisabledTime: NotRequired[datetime]


class DisableFastSnapshotRestoresRequestRequestTypeDef(TypedDict):
    AvailabilityZones: Sequence[str]
    SourceSnapshotIds: Sequence[str]
    DryRun: NotRequired[bool]


class DisableImageBlockPublicAccessRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisableImageDeprecationRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class DisableImageDeregistrationProtectionRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class DisableImageRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class DisableIpamOrganizationAdminAccountRequestRequestTypeDef(TypedDict):
    DelegatedAdminAccountId: str
    DryRun: NotRequired[bool]


class DisableSerialConsoleAccessRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisableSnapshotBlockPublicAccessRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisableTransitGatewayRouteTablePropagationRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    TransitGatewayAttachmentId: NotRequired[str]
    DryRun: NotRequired[bool]
    TransitGatewayRouteTableAnnouncementId: NotRequired[str]


class TransitGatewayPropagationTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    TransitGatewayRouteTableId: NotRequired[str]
    State: NotRequired[TransitGatewayPropagationStateType]
    TransitGatewayRouteTableAnnouncementId: NotRequired[str]


class DisableVgwRoutePropagationRequestRequestTypeDef(TypedDict):
    GatewayId: str
    RouteTableId: str
    DryRun: NotRequired[bool]


class DisableVpcClassicLinkDnsSupportRequestRequestTypeDef(TypedDict):
    VpcId: NotRequired[str]


class DisableVpcClassicLinkRequestRequestTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class DisableVpcClassicLinkRequestVpcDisableClassicLinkTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisassociateAddressRequestClassicAddressDisassociateTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    PublicIp: NotRequired[str]
    DryRun: NotRequired[bool]


class DisassociateAddressRequestNetworkInterfaceAssociationDeleteTypeDef(TypedDict):
    PublicIp: NotRequired[str]
    DryRun: NotRequired[bool]


class DisassociateAddressRequestRequestTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    PublicIp: NotRequired[str]
    DryRun: NotRequired[bool]


class DisassociateCapacityReservationBillingOwnerRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    UnusedReservationBillingOwnerId: str
    DryRun: NotRequired[bool]


class DisassociateClientVpnTargetNetworkRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    AssociationId: str
    DryRun: NotRequired[bool]


class DisassociateEnclaveCertificateIamRoleRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    RoleArn: str
    DryRun: NotRequired[bool]


class DisassociateIamInstanceProfileRequestRequestTypeDef(TypedDict):
    AssociationId: str


class DisassociateIpamByoasnRequestRequestTypeDef(TypedDict):
    Asn: str
    Cidr: str
    DryRun: NotRequired[bool]


class DisassociateIpamResourceDiscoveryRequestRequestTypeDef(TypedDict):
    IpamResourceDiscoveryAssociationId: str
    DryRun: NotRequired[bool]


class DisassociateNatGatewayAddressRequestRequestTypeDef(TypedDict):
    NatGatewayId: str
    AssociationIds: Sequence[str]
    MaxDrainDurationSeconds: NotRequired[int]
    DryRun: NotRequired[bool]


class DisassociateRouteTableRequestRequestTypeDef(TypedDict):
    AssociationId: str
    DryRun: NotRequired[bool]


class DisassociateRouteTableRequestRouteTableAssociationDeleteTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class DisassociateRouteTableRequestServiceResourceDisassociateRouteTableTypeDef(TypedDict):
    AssociationId: str
    DryRun: NotRequired[bool]


class DisassociateSecurityGroupVpcRequestRequestTypeDef(TypedDict):
    GroupId: str
    VpcId: str
    DryRun: NotRequired[bool]


class DisassociateSubnetCidrBlockRequestRequestTypeDef(TypedDict):
    AssociationId: str


class DisassociateTransitGatewayMulticastDomainRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    TransitGatewayAttachmentId: str
    SubnetIds: Sequence[str]
    DryRun: NotRequired[bool]


class DisassociateTransitGatewayPolicyTableRequestRequestTypeDef(TypedDict):
    TransitGatewayPolicyTableId: str
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class DisassociateTransitGatewayRouteTableRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class DisassociateTrunkInterfaceRequestRequestTypeDef(TypedDict):
    AssociationId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DisassociateVpcCidrBlockRequestRequestTypeDef(TypedDict):
    AssociationId: str


class DiskImageDescriptionTypeDef(TypedDict):
    Checksum: NotRequired[str]
    Format: NotRequired[DiskImageFormatType]
    ImportManifestUrl: NotRequired[str]
    Size: NotRequired[int]


class DiskImageDetailTypeDef(TypedDict):
    Format: DiskImageFormatType
    Bytes: int
    ImportManifestUrl: str


class VolumeDetailTypeDef(TypedDict):
    Size: int


class DiskImageVolumeDescriptionTypeDef(TypedDict):
    Id: NotRequired[str]
    Size: NotRequired[int]


DiskInfoTypeDef = TypedDict(
    "DiskInfoTypeDef",
    {
        "SizeInGB": NotRequired[int],
        "Count": NotRequired[int],
        "Type": NotRequired[DiskTypeType],
    },
)


class DnsEntryTypeDef(TypedDict):
    DnsName: NotRequired[str]
    HostedZoneId: NotRequired[str]


class DnsOptionsTypeDef(TypedDict):
    DnsRecordIpType: NotRequired[DnsRecordIpTypeType]
    PrivateDnsOnlyForInboundResolverEndpoint: NotRequired[bool]


class DnsServersOptionsModifyStructureTypeDef(TypedDict):
    CustomDnsServers: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]


class EbsOptimizedInfoTypeDef(TypedDict):
    BaselineBandwidthInMbps: NotRequired[int]
    BaselineThroughputInMBps: NotRequired[float]
    BaselineIops: NotRequired[int]
    MaximumBandwidthInMbps: NotRequired[int]
    MaximumThroughputInMBps: NotRequired[float]
    MaximumIops: NotRequired[int]


class EbsInstanceBlockDeviceSpecificationTypeDef(TypedDict):
    VolumeId: NotRequired[str]
    DeleteOnTermination: NotRequired[bool]


class OperatorResponseTypeDef(TypedDict):
    Managed: NotRequired[bool]
    Principal: NotRequired[str]


class EbsStatusDetailsTypeDef(TypedDict):
    ImpairedSince: NotRequired[datetime]
    Name: NotRequired[Literal["reachability"]]
    Status: NotRequired[StatusTypeType]


class EfaInfoTypeDef(TypedDict):
    MaximumEfaInterfaces: NotRequired[int]


class InternetGatewayAttachmentTypeDef(TypedDict):
    State: NotRequired[AttachmentStatusType]
    VpcId: NotRequired[str]


class ElasticGpuAssociationTypeDef(TypedDict):
    ElasticGpuId: NotRequired[str]
    ElasticGpuAssociationId: NotRequired[str]
    ElasticGpuAssociationState: NotRequired[str]
    ElasticGpuAssociationTime: NotRequired[str]


class ElasticGpuHealthTypeDef(TypedDict):
    Status: NotRequired[ElasticGpuStatusType]


ElasticGpuSpecificationResponseTypeDef = TypedDict(
    "ElasticGpuSpecificationResponseTypeDef",
    {
        "Type": NotRequired[str],
    },
)
ElasticGpuSpecificationTypeDef = TypedDict(
    "ElasticGpuSpecificationTypeDef",
    {
        "Type": str,
    },
)


class ElasticInferenceAcceleratorAssociationTypeDef(TypedDict):
    ElasticInferenceAcceleratorArn: NotRequired[str]
    ElasticInferenceAcceleratorAssociationId: NotRequired[str]
    ElasticInferenceAcceleratorAssociationState: NotRequired[str]
    ElasticInferenceAcceleratorAssociationTime: NotRequired[datetime]


ElasticInferenceAcceleratorTypeDef = TypedDict(
    "ElasticInferenceAcceleratorTypeDef",
    {
        "Type": str,
        "Count": NotRequired[int],
    },
)


class EnaSrdUdpSpecificationRequestTypeDef(TypedDict):
    EnaSrdUdpEnabled: NotRequired[bool]


class EnaSrdUdpSpecificationTypeDef(TypedDict):
    EnaSrdUdpEnabled: NotRequired[bool]


class EnableAddressTransferRequestRequestTypeDef(TypedDict):
    AllocationId: str
    TransferAccountId: str
    DryRun: NotRequired[bool]


class EnableAllowedImagesSettingsRequestRequestTypeDef(TypedDict):
    AllowedImagesSettingsState: AllowedImagesSettingsEnabledStateType
    DryRun: NotRequired[bool]


class EnableAwsNetworkPerformanceMetricSubscriptionRequestRequestTypeDef(TypedDict):
    Source: NotRequired[str]
    Destination: NotRequired[str]
    Metric: NotRequired[Literal["aggregate-latency"]]
    Statistic: NotRequired[Literal["p50"]]
    DryRun: NotRequired[bool]


class EnableEbsEncryptionByDefaultRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class FastLaunchLaunchTemplateSpecificationRequestTypeDef(TypedDict):
    Version: str
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]


class FastLaunchSnapshotConfigurationRequestTypeDef(TypedDict):
    TargetResourceCount: NotRequired[int]


class EnableFastSnapshotRestoreStateErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class EnableFastSnapshotRestoreSuccessItemTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    State: NotRequired[FastSnapshotRestoreStateCodeType]
    StateTransitionReason: NotRequired[str]
    OwnerId: NotRequired[str]
    OwnerAlias: NotRequired[str]
    EnablingTime: NotRequired[datetime]
    OptimizingTime: NotRequired[datetime]
    EnabledTime: NotRequired[datetime]
    DisablingTime: NotRequired[datetime]
    DisabledTime: NotRequired[datetime]


class EnableFastSnapshotRestoresRequestRequestTypeDef(TypedDict):
    AvailabilityZones: Sequence[str]
    SourceSnapshotIds: Sequence[str]
    DryRun: NotRequired[bool]


class EnableImageBlockPublicAccessRequestRequestTypeDef(TypedDict):
    ImageBlockPublicAccessState: Literal["block-new-sharing"]
    DryRun: NotRequired[bool]


class EnableImageDeregistrationProtectionRequestRequestTypeDef(TypedDict):
    ImageId: str
    WithCooldown: NotRequired[bool]
    DryRun: NotRequired[bool]


class EnableImageRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class EnableIpamOrganizationAdminAccountRequestRequestTypeDef(TypedDict):
    DelegatedAdminAccountId: str
    DryRun: NotRequired[bool]


class EnableReachabilityAnalyzerOrganizationSharingRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class EnableSerialConsoleAccessRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class EnableSnapshotBlockPublicAccessRequestRequestTypeDef(TypedDict):
    State: SnapshotBlockPublicAccessStateType
    DryRun: NotRequired[bool]


class EnableTransitGatewayRouteTablePropagationRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    TransitGatewayAttachmentId: NotRequired[str]
    DryRun: NotRequired[bool]
    TransitGatewayRouteTableAnnouncementId: NotRequired[str]


class EnableVgwRoutePropagationRequestRequestTypeDef(TypedDict):
    GatewayId: str
    RouteTableId: str
    DryRun: NotRequired[bool]


class EnableVolumeIORequestRequestTypeDef(TypedDict):
    VolumeId: str
    DryRun: NotRequired[bool]


class EnableVolumeIORequestVolumeEnableIoTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class EnableVpcClassicLinkDnsSupportRequestRequestTypeDef(TypedDict):
    VpcId: NotRequired[str]


class EnableVpcClassicLinkRequestRequestTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]


class EnableVpcClassicLinkRequestVpcEnableClassicLinkTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class EnclaveOptionsRequestTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class EnclaveOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class EventInformationTypeDef(TypedDict):
    EventDescription: NotRequired[str]
    EventSubType: NotRequired[str]
    InstanceId: NotRequired[str]


class TransitGatewayRouteTableRouteTypeDef(TypedDict):
    DestinationCidr: NotRequired[str]
    State: NotRequired[str]
    RouteOrigin: NotRequired[str]
    PrefixListId: NotRequired[str]
    AttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[str]


class ExportClientVpnClientCertificateRevocationListRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DryRun: NotRequired[bool]


class ExportClientVpnClientConfigurationRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DryRun: NotRequired[bool]


class ExportTaskS3LocationRequestTypeDef(TypedDict):
    S3Bucket: str
    S3Prefix: NotRequired[str]


class ExportTaskS3LocationTypeDef(TypedDict):
    S3Bucket: NotRequired[str]
    S3Prefix: NotRequired[str]


class ExportToS3TaskTypeDef(TypedDict):
    ContainerFormat: NotRequired[Literal["ova"]]
    DiskImageFormat: NotRequired[DiskImageFormatType]
    S3Bucket: NotRequired[str]
    S3Key: NotRequired[str]


class InstanceExportDetailsTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    TargetEnvironment: NotRequired[ExportEnvironmentType]


class ExportVerifiedAccessInstanceClientConfigurationRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    DryRun: NotRequired[bool]


VerifiedAccessInstanceUserTrustProviderClientConfigurationTypeDef = TypedDict(
    "VerifiedAccessInstanceUserTrustProviderClientConfigurationTypeDef",
    {
        "Type": NotRequired[UserTrustProviderTypeType],
        "Scopes": NotRequired[str],
        "Issuer": NotRequired[str],
        "AuthorizationEndpoint": NotRequired[str],
        "PublicSigningKeyEndpoint": NotRequired[str],
        "TokenEndpoint": NotRequired[str],
        "UserInfoEndpoint": NotRequired[str],
        "ClientId": NotRequired[str],
        "ClientSecret": NotRequired[str],
        "PkceEnabled": NotRequired[bool],
    },
)


class FilterPortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


class TargetCapacitySpecificationTypeDef(TypedDict):
    TotalTargetCapacity: NotRequired[int]
    OnDemandTargetCapacity: NotRequired[int]
    SpotTargetCapacity: NotRequired[int]
    DefaultTargetCapacityType: NotRequired[DefaultTargetCapacityTypeType]
    TargetCapacityUnitType: NotRequired[TargetCapacityUnitTypeType]


class FleetLaunchTemplateSpecificationRequestTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Version: NotRequired[str]


class FleetLaunchTemplateSpecificationTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Version: NotRequired[str]


class PlacementTypeDef(TypedDict):
    Affinity: NotRequired[str]
    GroupName: NotRequired[str]
    PartitionNumber: NotRequired[int]
    HostId: NotRequired[str]
    Tenancy: NotRequired[TenancyType]
    SpreadDomain: NotRequired[str]
    HostResourceGroupArn: NotRequired[str]
    GroupId: NotRequired[str]
    AvailabilityZone: NotRequired[str]


class PlacementResponseTypeDef(TypedDict):
    GroupName: NotRequired[str]


class FleetSpotCapacityRebalanceRequestTypeDef(TypedDict):
    ReplacementStrategy: NotRequired[FleetReplacementStrategyType]
    TerminationDelay: NotRequired[int]


class FleetSpotCapacityRebalanceTypeDef(TypedDict):
    ReplacementStrategy: NotRequired[FleetReplacementStrategyType]
    TerminationDelay: NotRequired[int]


class FpgaDeviceMemoryInfoTypeDef(TypedDict):
    SizeInMiB: NotRequired[int]


class LoadPermissionTypeDef(TypedDict):
    UserId: NotRequired[str]
    Group: NotRequired[Literal["all"]]


class FpgaImageStateTypeDef(TypedDict):
    Code: NotRequired[FpgaImageStateCodeType]
    Message: NotRequired[str]


class PciIdTypeDef(TypedDict):
    DeviceId: NotRequired[str]
    VendorId: NotRequired[str]
    SubsystemId: NotRequired[str]
    SubsystemVendorId: NotRequired[str]


class GetAllowedImagesSettingsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class ImageCriterionTypeDef(TypedDict):
    ImageProviders: NotRequired[list[str]]


class GetAssociatedEnclaveCertificateIamRolesRequestRequestTypeDef(TypedDict):
    CertificateArn: str
    DryRun: NotRequired[bool]


class GetAssociatedIpv6PoolCidrsRequestRequestTypeDef(TypedDict):
    PoolId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class Ipv6CidrAssociationTypeDef(TypedDict):
    Ipv6Cidr: NotRequired[str]
    AssociatedResource: NotRequired[str]


class GetCapacityReservationUsageRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class InstanceUsageTypeDef(TypedDict):
    AccountId: NotRequired[str]
    UsedInstanceCount: NotRequired[int]


class GetConsoleOutputRequestInstanceConsoleOutputTypeDef(TypedDict):
    Latest: NotRequired[bool]
    DryRun: NotRequired[bool]


class GetConsoleOutputRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Latest: NotRequired[bool]
    DryRun: NotRequired[bool]


class GetConsoleScreenshotRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]
    WakeUp: NotRequired[bool]


class GetDeclarativePoliciesReportSummaryRequestRequestTypeDef(TypedDict):
    ReportId: str
    DryRun: NotRequired[bool]


class GetDefaultCreditSpecificationRequestRequestTypeDef(TypedDict):
    InstanceFamily: UnlimitedSupportedInstanceFamilyType
    DryRun: NotRequired[bool]


class InstanceFamilyCreditSpecificationTypeDef(TypedDict):
    InstanceFamily: NotRequired[UnlimitedSupportedInstanceFamilyType]
    CpuCredits: NotRequired[str]


class GetEbsDefaultKmsKeyIdRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class GetEbsEncryptionByDefaultRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class GetGroupsForCapacityReservationRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class GetHostReservationPurchasePreviewRequestRequestTypeDef(TypedDict):
    HostIdSet: Sequence[str]
    OfferingId: str


class PurchaseTypeDef(TypedDict):
    CurrencyCode: NotRequired[Literal["USD"]]
    Duration: NotRequired[int]
    HostIdSet: NotRequired[list[str]]
    HostReservationId: NotRequired[str]
    HourlyPrice: NotRequired[str]
    InstanceFamily: NotRequired[str]
    PaymentOption: NotRequired[PaymentOptionType]
    UpfrontPrice: NotRequired[str]


class GetImageBlockPublicAccessStateRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class GetInstanceMetadataDefaultsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class InstanceMetadataDefaultsResponseTypeDef(TypedDict):
    HttpTokens: NotRequired[HttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[InstanceMetadataEndpointStateType]
    InstanceMetadataTags: NotRequired[InstanceMetadataTagsStateType]
    ManagedBy: NotRequired[ManagedByType]
    ManagedExceptionMessage: NotRequired[str]


class GetInstanceTpmEkPubRequestRequestTypeDef(TypedDict):
    InstanceId: str
    KeyType: EkPubKeyTypeType
    KeyFormat: EkPubKeyFormatType
    DryRun: NotRequired[bool]


class InstanceTypeInfoFromInstanceRequirementsTypeDef(TypedDict):
    InstanceType: NotRequired[str]


class GetInstanceUefiDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]


class IpamAddressHistoryRecordTypeDef(TypedDict):
    ResourceOwnerId: NotRequired[str]
    ResourceRegion: NotRequired[str]
    ResourceType: NotRequired[IpamAddressHistoryResourceTypeType]
    ResourceId: NotRequired[str]
    ResourceCidr: NotRequired[str]
    ResourceName: NotRequired[str]
    ResourceComplianceStatus: NotRequired[IpamComplianceStatusType]
    ResourceOverlapStatus: NotRequired[IpamOverlapStatusType]
    VpcId: NotRequired[str]
    SampledStartTime: NotRequired[datetime]
    SampledEndTime: NotRequired[datetime]


class GetLaunchTemplateDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]


class GetManagedPrefixListAssociationsRequestRequestTypeDef(TypedDict):
    PrefixListId: str
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class PrefixListAssociationTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ResourceOwner: NotRequired[str]


class GetManagedPrefixListEntriesRequestRequestTypeDef(TypedDict):
    PrefixListId: str
    DryRun: NotRequired[bool]
    TargetVersion: NotRequired[int]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class PrefixListEntryTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Description: NotRequired[str]


class GetNetworkInsightsAccessScopeAnalysisFindingsRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetNetworkInsightsAccessScopeContentRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeId: str
    DryRun: NotRequired[bool]


class GetPasswordDataRequestInstancePasswordDataTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class GetPasswordDataRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]


class ReservationValueTypeDef(TypedDict):
    HourlyPrice: NotRequired[str]
    RemainingTotalValue: NotRequired[str]
    RemainingUpfrontValue: NotRequired[str]


class GetSerialConsoleAccessStatusRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class GetSnapshotBlockPublicAccessStateRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class SpotPlacementScoreTypeDef(TypedDict):
    Region: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    Score: NotRequired[int]


class TransitGatewayAttachmentPropagationTypeDef(TypedDict):
    TransitGatewayRouteTableId: NotRequired[str]
    State: NotRequired[TransitGatewayPropagationStateType]


class TransitGatewayRouteTableAssociationTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    State: NotRequired[TransitGatewayAssociationStateType]


class TransitGatewayRouteTablePropagationTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    State: NotRequired[TransitGatewayPropagationStateType]
    TransitGatewayRouteTableAnnouncementId: NotRequired[str]


class GetVerifiedAccessEndpointPolicyRequestRequestTypeDef(TypedDict):
    VerifiedAccessEndpointId: str
    DryRun: NotRequired[bool]


class GetVerifiedAccessEndpointTargetsRequestRequestTypeDef(TypedDict):
    VerifiedAccessEndpointId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class VerifiedAccessEndpointTargetTypeDef(TypedDict):
    VerifiedAccessEndpointId: NotRequired[str]
    VerifiedAccessEndpointTargetIpAddress: NotRequired[str]
    VerifiedAccessEndpointTargetDns: NotRequired[str]


class GetVerifiedAccessGroupPolicyRequestRequestTypeDef(TypedDict):
    VerifiedAccessGroupId: str
    DryRun: NotRequired[bool]


class GetVpnConnectionDeviceSampleConfigurationRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    VpnConnectionDeviceTypeId: str
    InternetKeyExchangeVersion: NotRequired[str]
    DryRun: NotRequired[bool]


class GetVpnConnectionDeviceTypesRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class VpnConnectionDeviceTypeTypeDef(TypedDict):
    VpnConnectionDeviceTypeId: NotRequired[str]
    Vendor: NotRequired[str]
    Platform: NotRequired[str]
    Software: NotRequired[str]


class GetVpnTunnelReplacementStatusRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    VpnTunnelOutsideIpAddress: str
    DryRun: NotRequired[bool]


class MaintenanceDetailsTypeDef(TypedDict):
    PendingMaintenance: NotRequired[str]
    MaintenanceAutoAppliedAfter: NotRequired[datetime]
    LastMaintenanceApplied: NotRequired[datetime]


class GpuDeviceMemoryInfoTypeDef(TypedDict):
    SizeInMiB: NotRequired[int]


class HibernationOptionsRequestTypeDef(TypedDict):
    Configured: NotRequired[bool]


class HibernationOptionsTypeDef(TypedDict):
    Configured: NotRequired[bool]


class HostInstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[str]
    OwnerId: NotRequired[str]


class HostPropertiesTypeDef(TypedDict):
    Cores: NotRequired[int]
    InstanceType: NotRequired[str]
    InstanceFamily: NotRequired[str]
    Sockets: NotRequired[int]
    TotalVCpus: NotRequired[int]


class IKEVersionsListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class IKEVersionsRequestListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class IamInstanceProfileTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]


class LaunchPermissionTypeDef(TypedDict):
    OrganizationArn: NotRequired[str]
    OrganizationalUnitArn: NotRequired[str]
    UserId: NotRequired[str]
    Group: NotRequired[Literal["all"]]


class ImageCriterionRequestTypeDef(TypedDict):
    ImageProviders: NotRequired[Sequence[str]]


class UserBucketTypeDef(TypedDict):
    S3Bucket: NotRequired[str]
    S3Key: NotRequired[str]


class ImageMetadataTypeDef(TypedDict):
    ImageId: NotRequired[str]
    Name: NotRequired[str]
    OwnerId: NotRequired[str]
    State: NotRequired[ImageStateType]
    ImageOwnerAlias: NotRequired[str]
    CreationDate: NotRequired[str]
    DeprecationTime: NotRequired[str]
    ImageAllowed: NotRequired[bool]
    IsPublic: NotRequired[bool]


class ImageRecycleBinInfoTypeDef(TypedDict):
    ImageId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    RecycleBinEnterTime: NotRequired[datetime]
    RecycleBinExitTime: NotRequired[datetime]


class StateReasonTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class ImportClientVpnClientCertificateRevocationListRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    CertificateRevocationList: str
    DryRun: NotRequired[bool]


class ImportImageLicenseConfigurationRequestTypeDef(TypedDict):
    LicenseConfigurationArn: NotRequired[str]


class ImportImageLicenseConfigurationResponseTypeDef(TypedDict):
    LicenseConfigurationArn: NotRequired[str]


class UserDataTypeDef(TypedDict):
    Data: NotRequired[str]


class InferenceDeviceMemoryInfoTypeDef(TypedDict):
    SizeInMiB: NotRequired[int]


class InstanceAttachmentEnaSrdUdpSpecificationTypeDef(TypedDict):
    EnaSrdUdpEnabled: NotRequired[bool]


class InstanceCountTypeDef(TypedDict):
    InstanceCount: NotRequired[int]
    State: NotRequired[ListingStateType]


class InstanceCreditSpecificationRequestTypeDef(TypedDict):
    InstanceId: str
    CpuCredits: NotRequired[str]


class InstanceEventWindowTimeRangeTypeDef(TypedDict):
    StartWeekDay: NotRequired[WeekDayType]
    StartHour: NotRequired[int]
    EndWeekDay: NotRequired[WeekDayType]
    EndHour: NotRequired[int]


class InstanceStateTypeDef(TypedDict):
    Code: NotRequired[int]
    Name: NotRequired[InstanceStateNameType]


class InstanceIpv4PrefixTypeDef(TypedDict):
    Ipv4Prefix: NotRequired[str]


class InstanceIpv6AddressRequestTypeDef(TypedDict):
    Ipv6Address: NotRequired[str]


class InstanceIpv6PrefixTypeDef(TypedDict):
    Ipv6Prefix: NotRequired[str]


class InstanceMaintenanceOptionsRequestTypeDef(TypedDict):
    AutoRecovery: NotRequired[InstanceAutoRecoveryStateType]


class InstanceMaintenanceOptionsTypeDef(TypedDict):
    AutoRecovery: NotRequired[InstanceAutoRecoveryStateType]


class InstanceMetadataOptionsRequestTypeDef(TypedDict):
    HttpTokens: NotRequired[HttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[InstanceMetadataEndpointStateType]
    HttpProtocolIpv6: NotRequired[InstanceMetadataProtocolStateType]
    InstanceMetadataTags: NotRequired[InstanceMetadataTagsStateType]


class InstanceMetadataOptionsResponseTypeDef(TypedDict):
    State: NotRequired[InstanceMetadataOptionsStateType]
    HttpTokens: NotRequired[HttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[InstanceMetadataEndpointStateType]
    HttpProtocolIpv6: NotRequired[InstanceMetadataProtocolStateType]
    InstanceMetadataTags: NotRequired[InstanceMetadataTagsStateType]


class MonitoringTypeDef(TypedDict):
    State: NotRequired[MonitoringStateType]


class InstanceNetworkInterfaceAssociationTypeDef(TypedDict):
    CarrierIp: NotRequired[str]
    CustomerOwnedIp: NotRequired[str]
    IpOwnerId: NotRequired[str]
    PublicDnsName: NotRequired[str]
    PublicIp: NotRequired[str]


class InstanceNetworkPerformanceOptionsRequestTypeDef(TypedDict):
    BandwidthWeighting: NotRequired[InstanceBandwidthWeightingType]


class InstanceNetworkPerformanceOptionsTypeDef(TypedDict):
    BandwidthWeighting: NotRequired[InstanceBandwidthWeightingType]


class MemoryGiBPerVCpuTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class MemoryMiBTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class NetworkBandwidthGbpsTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class NetworkInterfaceCountTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class TotalLocalStorageGBTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class VCpuCountRangeTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class MemoryGiBPerVCpuRequestTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class MemoryMiBRequestTypeDef(TypedDict):
    Min: int
    Max: NotRequired[int]


class NetworkBandwidthGbpsRequestTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class NetworkInterfaceCountRequestTypeDef(TypedDict):
    Min: NotRequired[int]
    Max: NotRequired[int]


class TotalLocalStorageGBRequestTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class VCpuCountRangeRequestTypeDef(TypedDict):
    Min: int
    Max: NotRequired[int]


class InstanceStatusDetailsTypeDef(TypedDict):
    ImpairedSince: NotRequired[datetime]
    Name: NotRequired[Literal["reachability"]]
    Status: NotRequired[StatusTypeType]


class InstanceStatusEventTypeDef(TypedDict):
    InstanceEventId: NotRequired[str]
    Code: NotRequired[EventCodeType]
    Description: NotRequired[str]
    NotAfter: NotRequired[datetime]
    NotBefore: NotRequired[datetime]
    NotBeforeDeadline: NotRequired[datetime]


class LicenseConfigurationTypeDef(TypedDict):
    LicenseConfigurationArn: NotRequired[str]


class PrivateDnsNameOptionsResponseTypeDef(TypedDict):
    HostnameType: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecord: NotRequired[bool]
    EnableResourceNameDnsAAAARecord: NotRequired[bool]


class MemoryInfoTypeDef(TypedDict):
    SizeInMiB: NotRequired[int]


class NitroTpmInfoTypeDef(TypedDict):
    SupportedVersions: NotRequired[list[str]]


class PlacementGroupInfoTypeDef(TypedDict):
    SupportedStrategies: NotRequired[list[PlacementGroupStrategyType]]


class ProcessorInfoTypeDef(TypedDict):
    SupportedArchitectures: NotRequired[list[ArchitectureTypeType]]
    SustainedClockSpeedInGhz: NotRequired[float]
    SupportedFeatures: NotRequired[list[Literal["amd-sev-snp"]]]
    Manufacturer: NotRequired[str]


class VCpuInfoTypeDef(TypedDict):
    DefaultVCpus: NotRequired[int]
    DefaultCores: NotRequired[int]
    DefaultThreadsPerCore: NotRequired[int]
    ValidCores: NotRequired[list[int]]
    ValidThreadsPerCore: NotRequired[list[int]]


class IpRangeTypeDef(TypedDict):
    Description: NotRequired[str]
    CidrIp: NotRequired[str]


class Ipv6RangeTypeDef(TypedDict):
    Description: NotRequired[str]
    CidrIpv6: NotRequired[str]


class PrefixListIdTypeDef(TypedDict):
    Description: NotRequired[str]
    PrefixListId: NotRequired[str]


class UserIdGroupPairTypeDef(TypedDict):
    Description: NotRequired[str]
    UserId: NotRequired[str]
    GroupName: NotRequired[str]
    GroupId: NotRequired[str]
    VpcId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    PeeringStatus: NotRequired[str]


class IpamCidrAuthorizationContextTypeDef(TypedDict):
    Message: NotRequired[str]
    Signature: NotRequired[str]


class IpamDiscoveryFailureReasonTypeDef(TypedDict):
    Code: NotRequired[IpamDiscoveryFailureCodeType]
    Message: NotRequired[str]


class IpamPublicAddressSecurityGroupTypeDef(TypedDict):
    GroupName: NotRequired[str]
    GroupId: NotRequired[str]


class IpamResourceTagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


IpamOperatingRegionTypeDef = TypedDict(
    "IpamOperatingRegionTypeDef",
    {
        "RegionName": NotRequired[str],
    },
)


class IpamOrganizationalUnitExclusionTypeDef(TypedDict):
    OrganizationsEntityPath: NotRequired[str]


class IpamPoolCidrFailureReasonTypeDef(TypedDict):
    Code: NotRequired[IpamPoolCidrFailureCodeType]
    Message: NotRequired[str]


class IpamPoolSourceResourceTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[Literal["vpc"]]
    ResourceRegion: NotRequired[str]
    ResourceOwner: NotRequired[str]


class IpamPublicAddressTagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class Ipv4PrefixSpecificationResponseTypeDef(TypedDict):
    Ipv4Prefix: NotRequired[str]


class Ipv6CidrBlockTypeDef(TypedDict):
    Ipv6CidrBlock: NotRequired[str]


class PoolCidrBlockTypeDef(TypedDict):
    Cidr: NotRequired[str]


class Ipv6PrefixSpecificationResponseTypeDef(TypedDict):
    Ipv6Prefix: NotRequired[str]


class Ipv6PrefixSpecificationTypeDef(TypedDict):
    Ipv6Prefix: NotRequired[str]


class LastErrorTypeDef(TypedDict):
    Message: NotRequired[str]
    Code: NotRequired[str]


class RunInstancesMonitoringEnabledTypeDef(TypedDict):
    Enabled: bool


class SpotPlacementTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    GroupName: NotRequired[str]
    Tenancy: NotRequired[TenancyType]


class LaunchTemplateEbsBlockDeviceRequestTypeDef(TypedDict):
    Encrypted: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Iops: NotRequired[int]
    KmsKeyId: NotRequired[str]
    SnapshotId: NotRequired[str]
    VolumeSize: NotRequired[int]
    VolumeType: NotRequired[VolumeTypeType]
    Throughput: NotRequired[int]


class LaunchTemplateEbsBlockDeviceTypeDef(TypedDict):
    Encrypted: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Iops: NotRequired[int]
    KmsKeyId: NotRequired[str]
    SnapshotId: NotRequired[str]
    VolumeSize: NotRequired[int]
    VolumeType: NotRequired[VolumeTypeType]
    Throughput: NotRequired[int]


class LaunchTemplateCpuOptionsRequestTypeDef(TypedDict):
    CoreCount: NotRequired[int]
    ThreadsPerCore: NotRequired[int]
    AmdSevSnp: NotRequired[AmdSevSnpSpecificationType]


class LaunchTemplateCpuOptionsTypeDef(TypedDict):
    CoreCount: NotRequired[int]
    ThreadsPerCore: NotRequired[int]
    AmdSevSnp: NotRequired[AmdSevSnpSpecificationType]


LaunchTemplateElasticInferenceAcceleratorResponseTypeDef = TypedDict(
    "LaunchTemplateElasticInferenceAcceleratorResponseTypeDef",
    {
        "Type": NotRequired[str],
        "Count": NotRequired[int],
    },
)
LaunchTemplateElasticInferenceAcceleratorTypeDef = TypedDict(
    "LaunchTemplateElasticInferenceAcceleratorTypeDef",
    {
        "Type": str,
        "Count": NotRequired[int],
    },
)


class LaunchTemplateEnaSrdUdpSpecificationTypeDef(TypedDict):
    EnaSrdUdpEnabled: NotRequired[bool]


class LaunchTemplateEnclaveOptionsRequestTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class LaunchTemplateEnclaveOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class LaunchTemplateHibernationOptionsRequestTypeDef(TypedDict):
    Configured: NotRequired[bool]


class LaunchTemplateHibernationOptionsTypeDef(TypedDict):
    Configured: NotRequired[bool]


class LaunchTemplateIamInstanceProfileSpecificationRequestTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class LaunchTemplateIamInstanceProfileSpecificationTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class LaunchTemplateInstanceMaintenanceOptionsRequestTypeDef(TypedDict):
    AutoRecovery: NotRequired[LaunchTemplateAutoRecoveryStateType]


class LaunchTemplateInstanceMaintenanceOptionsTypeDef(TypedDict):
    AutoRecovery: NotRequired[LaunchTemplateAutoRecoveryStateType]


class LaunchTemplateSpotMarketOptionsTypeDef(TypedDict):
    MaxPrice: NotRequired[str]
    SpotInstanceType: NotRequired[SpotInstanceTypeType]
    BlockDurationMinutes: NotRequired[int]
    ValidUntil: NotRequired[datetime]
    InstanceInterruptionBehavior: NotRequired[InstanceInterruptionBehaviorType]


class LaunchTemplateInstanceMetadataOptionsRequestTypeDef(TypedDict):
    HttpTokens: NotRequired[LaunchTemplateHttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[LaunchTemplateInstanceMetadataEndpointStateType]
    HttpProtocolIpv6: NotRequired[LaunchTemplateInstanceMetadataProtocolIpv6Type]
    InstanceMetadataTags: NotRequired[LaunchTemplateInstanceMetadataTagsStateType]


class LaunchTemplateInstanceMetadataOptionsTypeDef(TypedDict):
    State: NotRequired[LaunchTemplateInstanceMetadataOptionsStateType]
    HttpTokens: NotRequired[LaunchTemplateHttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[LaunchTemplateInstanceMetadataEndpointStateType]
    HttpProtocolIpv6: NotRequired[LaunchTemplateInstanceMetadataProtocolIpv6Type]
    InstanceMetadataTags: NotRequired[LaunchTemplateInstanceMetadataTagsStateType]


class LaunchTemplateLicenseConfigurationRequestTypeDef(TypedDict):
    LicenseConfigurationArn: NotRequired[str]


class LaunchTemplateLicenseConfigurationTypeDef(TypedDict):
    LicenseConfigurationArn: NotRequired[str]


class LaunchTemplateNetworkPerformanceOptionsRequestTypeDef(TypedDict):
    BandwidthWeighting: NotRequired[InstanceBandwidthWeightingType]


class LaunchTemplateNetworkPerformanceOptionsTypeDef(TypedDict):
    BandwidthWeighting: NotRequired[InstanceBandwidthWeightingType]


class LaunchTemplatePlacementRequestTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    Affinity: NotRequired[str]
    GroupName: NotRequired[str]
    HostId: NotRequired[str]
    Tenancy: NotRequired[TenancyType]
    SpreadDomain: NotRequired[str]
    HostResourceGroupArn: NotRequired[str]
    PartitionNumber: NotRequired[int]
    GroupId: NotRequired[str]


class LaunchTemplatePlacementTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    Affinity: NotRequired[str]
    GroupName: NotRequired[str]
    HostId: NotRequired[str]
    Tenancy: NotRequired[TenancyType]
    SpreadDomain: NotRequired[str]
    HostResourceGroupArn: NotRequired[str]
    PartitionNumber: NotRequired[int]
    GroupId: NotRequired[str]


class LaunchTemplatePrivateDnsNameOptionsRequestTypeDef(TypedDict):
    HostnameType: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecord: NotRequired[bool]
    EnableResourceNameDnsAAAARecord: NotRequired[bool]


class LaunchTemplatePrivateDnsNameOptionsTypeDef(TypedDict):
    HostnameType: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecord: NotRequired[bool]
    EnableResourceNameDnsAAAARecord: NotRequired[bool]


class LaunchTemplateSpecificationTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Version: NotRequired[str]


class LaunchTemplatesMonitoringRequestTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class LaunchTemplatesMonitoringTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class LicenseConfigurationRequestTypeDef(TypedDict):
    LicenseConfigurationArn: NotRequired[str]


class ListImagesInRecycleBinRequestRequestTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class ListSnapshotsInRecycleBinRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SnapshotIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class SnapshotRecycleBinInfoTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    RecycleBinEnterTime: NotRequired[datetime]
    RecycleBinExitTime: NotRequired[datetime]
    Description: NotRequired[str]
    VolumeId: NotRequired[str]


class LoadPermissionRequestTypeDef(TypedDict):
    Group: NotRequired[Literal["all"]]
    UserId: NotRequired[str]


class MediaDeviceMemoryInfoTypeDef(TypedDict):
    SizeInMiB: NotRequired[int]


class ModifyAddressAttributeRequestRequestTypeDef(TypedDict):
    AllocationId: str
    DomainName: NotRequired[str]
    DryRun: NotRequired[bool]


class ModifyAvailabilityZoneGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    OptInStatus: ModifyAvailabilityZoneOptInStatusType
    DryRun: NotRequired[bool]


class ModifyDefaultCreditSpecificationRequestRequestTypeDef(TypedDict):
    InstanceFamily: UnlimitedSupportedInstanceFamilyType
    CpuCredits: str
    DryRun: NotRequired[bool]


class ModifyEbsDefaultKmsKeyIdRequestRequestTypeDef(TypedDict):
    KmsKeyId: str
    DryRun: NotRequired[bool]


class ModifyHostsRequestRequestTypeDef(TypedDict):
    HostIds: Sequence[str]
    HostRecovery: NotRequired[HostRecoveryType]
    InstanceType: NotRequired[str]
    InstanceFamily: NotRequired[str]
    HostMaintenance: NotRequired[HostMaintenanceType]
    AutoPlacement: NotRequired[AutoPlacementType]


class ModifyIdFormatRequestRequestTypeDef(TypedDict):
    Resource: str
    UseLongIds: bool


class ModifyIdentityIdFormatRequestRequestTypeDef(TypedDict):
    Resource: str
    UseLongIds: bool
    PrincipalArn: str


class ModifyInstanceCpuOptionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    CoreCount: int
    ThreadsPerCore: int
    DryRun: NotRequired[bool]


class SuccessfulInstanceCreditSpecificationItemTypeDef(TypedDict):
    InstanceId: NotRequired[str]


class ModifyInstanceMaintenanceOptionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    AutoRecovery: NotRequired[InstanceAutoRecoveryStateType]
    DryRun: NotRequired[bool]


class ModifyInstanceMetadataDefaultsRequestRequestTypeDef(TypedDict):
    HttpTokens: NotRequired[MetadataDefaultHttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[DefaultInstanceMetadataEndpointStateType]
    InstanceMetadataTags: NotRequired[DefaultInstanceMetadataTagsStateType]
    DryRun: NotRequired[bool]


class ModifyInstanceMetadataOptionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    HttpTokens: NotRequired[HttpTokensStateType]
    HttpPutResponseHopLimit: NotRequired[int]
    HttpEndpoint: NotRequired[InstanceMetadataEndpointStateType]
    DryRun: NotRequired[bool]
    HttpProtocolIpv6: NotRequired[InstanceMetadataProtocolStateType]
    InstanceMetadataTags: NotRequired[InstanceMetadataTagsStateType]


class ModifyInstanceNetworkPerformanceRequestRequestTypeDef(TypedDict):
    InstanceId: str
    BandwidthWeighting: InstanceBandwidthWeightingType
    DryRun: NotRequired[bool]


class ModifyInstancePlacementRequestRequestTypeDef(TypedDict):
    InstanceId: str
    GroupName: NotRequired[str]
    PartitionNumber: NotRequired[int]
    HostResourceGroupArn: NotRequired[str]
    GroupId: NotRequired[str]
    Tenancy: NotRequired[HostTenancyType]
    Affinity: NotRequired[AffinityType]
    HostId: NotRequired[str]


RemoveIpamOperatingRegionTypeDef = TypedDict(
    "RemoveIpamOperatingRegionTypeDef",
    {
        "RegionName": NotRequired[str],
    },
)


class ModifyIpamResourceCidrRequestRequestTypeDef(TypedDict):
    ResourceId: str
    ResourceCidr: str
    ResourceRegion: str
    CurrentIpamScopeId: str
    Monitored: bool
    DryRun: NotRequired[bool]
    DestinationIpamScopeId: NotRequired[str]


class RemoveIpamOrganizationalUnitExclusionTypeDef(TypedDict):
    OrganizationsEntityPath: NotRequired[str]


class ModifyIpamScopeRequestRequestTypeDef(TypedDict):
    IpamScopeId: str
    DryRun: NotRequired[bool]
    Description: NotRequired[str]


class ModifyLaunchTemplateRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    DefaultVersion: NotRequired[str]


class ModifyLocalGatewayRouteRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    DestinationCidrBlock: NotRequired[str]
    LocalGatewayVirtualInterfaceGroupId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationPrefixListId: NotRequired[str]


class RemovePrefixListEntryTypeDef(TypedDict):
    Cidr: str


class NetworkInterfaceAttachmentChangesTypeDef(TypedDict):
    AttachmentId: NotRequired[str]
    DeleteOnTermination: NotRequired[bool]


class ModifyPrivateDnsNameOptionsRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]
    PrivateDnsHostnameType: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecord: NotRequired[bool]
    EnableResourceNameDnsAAAARecord: NotRequired[bool]


class ReservedInstancesConfigurationTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    InstanceCount: NotRequired[int]
    InstanceType: NotRequired[InstanceTypeType]
    Platform: NotRequired[str]
    Scope: NotRequired[ScopeType]


class ModifySnapshotTierRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    StorageTier: NotRequired[Literal["archive"]]
    DryRun: NotRequired[bool]


class ModifyTrafficMirrorFilterNetworkServicesRequestRequestTypeDef(TypedDict):
    TrafficMirrorFilterId: str
    AddNetworkServices: NotRequired[Sequence[Literal["amazon-dns"]]]
    RemoveNetworkServices: NotRequired[Sequence[Literal["amazon-dns"]]]
    DryRun: NotRequired[bool]


class ModifyTrafficMirrorSessionRequestRequestTypeDef(TypedDict):
    TrafficMirrorSessionId: str
    TrafficMirrorTargetId: NotRequired[str]
    TrafficMirrorFilterId: NotRequired[str]
    PacketLength: NotRequired[int]
    SessionNumber: NotRequired[int]
    VirtualNetworkId: NotRequired[int]
    Description: NotRequired[str]
    RemoveFields: NotRequired[Sequence[TrafficMirrorSessionFieldType]]
    DryRun: NotRequired[bool]


class ModifyTransitGatewayOptionsTypeDef(TypedDict):
    AddTransitGatewayCidrBlocks: NotRequired[Sequence[str]]
    RemoveTransitGatewayCidrBlocks: NotRequired[Sequence[str]]
    VpnEcmpSupport: NotRequired[VpnEcmpSupportValueType]
    DnsSupport: NotRequired[DnsSupportValueType]
    SecurityGroupReferencingSupport: NotRequired[SecurityGroupReferencingSupportValueType]
    AutoAcceptSharedAttachments: NotRequired[AutoAcceptSharedAttachmentsValueType]
    DefaultRouteTableAssociation: NotRequired[DefaultRouteTableAssociationValueType]
    AssociationDefaultRouteTableId: NotRequired[str]
    DefaultRouteTablePropagation: NotRequired[DefaultRouteTablePropagationValueType]
    PropagationDefaultRouteTableId: NotRequired[str]
    AmazonSideAsn: NotRequired[int]


class ModifyTransitGatewayPrefixListReferenceRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    PrefixListId: str
    TransitGatewayAttachmentId: NotRequired[str]
    Blackhole: NotRequired[bool]
    DryRun: NotRequired[bool]


class ModifyTransitGatewayVpcAttachmentRequestOptionsTypeDef(TypedDict):
    DnsSupport: NotRequired[DnsSupportValueType]
    SecurityGroupReferencingSupport: NotRequired[SecurityGroupReferencingSupportValueType]
    Ipv6Support: NotRequired[Ipv6SupportValueType]
    ApplianceModeSupport: NotRequired[ApplianceModeSupportValueType]


class ModifyVerifiedAccessEndpointPortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


class VerifiedAccessSseSpecificationResponseTypeDef(TypedDict):
    CustomerManagedKeyEnabled: NotRequired[bool]
    KmsKeyArn: NotRequired[str]


class ModifyVerifiedAccessEndpointRdsOptionsTypeDef(TypedDict):
    SubnetIds: NotRequired[Sequence[str]]
    Port: NotRequired[int]
    RdsEndpoint: NotRequired[str]


class ModifyVerifiedAccessGroupRequestRequestTypeDef(TypedDict):
    VerifiedAccessGroupId: str
    VerifiedAccessInstanceId: NotRequired[str]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class ModifyVerifiedAccessInstanceRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    CidrEndpointsCustomSubDomain: NotRequired[str]


class ModifyVerifiedAccessNativeApplicationOidcOptionsTypeDef(TypedDict):
    PublicSigningKeyEndpoint: NotRequired[str]
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]
    Scope: NotRequired[str]


class ModifyVerifiedAccessTrustProviderDeviceOptionsTypeDef(TypedDict):
    PublicSigningKeyUrl: NotRequired[str]


class ModifyVerifiedAccessTrustProviderOidcOptionsTypeDef(TypedDict):
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]
    Scope: NotRequired[str]


class ModifyVolumeRequestRequestTypeDef(TypedDict):
    VolumeId: str
    DryRun: NotRequired[bool]
    Size: NotRequired[int]
    VolumeType: NotRequired[VolumeTypeType]
    Iops: NotRequired[int]
    Throughput: NotRequired[int]
    MultiAttachEnabled: NotRequired[bool]


class ModifyVpcBlockPublicAccessExclusionRequestRequestTypeDef(TypedDict):
    ExclusionId: str
    InternetGatewayExclusionMode: InternetGatewayExclusionModeType
    DryRun: NotRequired[bool]


class ModifyVpcBlockPublicAccessOptionsRequestRequestTypeDef(TypedDict):
    InternetGatewayBlockMode: InternetGatewayBlockModeType
    DryRun: NotRequired[bool]


class ModifyVpcEndpointConnectionNotificationRequestRequestTypeDef(TypedDict):
    ConnectionNotificationId: str
    DryRun: NotRequired[bool]
    ConnectionNotificationArn: NotRequired[str]
    ConnectionEvents: NotRequired[Sequence[str]]


class ModifyVpcEndpointServiceConfigurationRequestRequestTypeDef(TypedDict):
    ServiceId: str
    DryRun: NotRequired[bool]
    PrivateDnsName: NotRequired[str]
    RemovePrivateDnsName: NotRequired[bool]
    AcceptanceRequired: NotRequired[bool]
    AddNetworkLoadBalancerArns: NotRequired[Sequence[str]]
    RemoveNetworkLoadBalancerArns: NotRequired[Sequence[str]]
    AddGatewayLoadBalancerArns: NotRequired[Sequence[str]]
    RemoveGatewayLoadBalancerArns: NotRequired[Sequence[str]]
    AddSupportedIpAddressTypes: NotRequired[Sequence[str]]
    RemoveSupportedIpAddressTypes: NotRequired[Sequence[str]]
    AddSupportedRegions: NotRequired[Sequence[str]]
    RemoveSupportedRegions: NotRequired[Sequence[str]]


class ModifyVpcEndpointServicePayerResponsibilityRequestRequestTypeDef(TypedDict):
    ServiceId: str
    PayerResponsibility: Literal["ServiceOwner"]
    DryRun: NotRequired[bool]


class ModifyVpcEndpointServicePermissionsRequestRequestTypeDef(TypedDict):
    ServiceId: str
    DryRun: NotRequired[bool]
    AddAllowedPrincipals: NotRequired[Sequence[str]]
    RemoveAllowedPrincipals: NotRequired[Sequence[str]]


class PeeringConnectionOptionsRequestTypeDef(TypedDict):
    AllowDnsResolutionFromRemoteVpc: NotRequired[bool]
    AllowEgressFromLocalClassicLinkToRemoteVpc: NotRequired[bool]
    AllowEgressFromLocalVpcToRemoteClassicLink: NotRequired[bool]


class PeeringConnectionOptionsTypeDef(TypedDict):
    AllowDnsResolutionFromRemoteVpc: NotRequired[bool]
    AllowEgressFromLocalClassicLinkToRemoteVpc: NotRequired[bool]
    AllowEgressFromLocalVpcToRemoteClassicLink: NotRequired[bool]


class ModifyVpcTenancyRequestRequestTypeDef(TypedDict):
    VpcId: str
    InstanceTenancy: Literal["default"]
    DryRun: NotRequired[bool]


class ModifyVpnConnectionOptionsRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    LocalIpv4NetworkCidr: NotRequired[str]
    RemoteIpv4NetworkCidr: NotRequired[str]
    LocalIpv6NetworkCidr: NotRequired[str]
    RemoteIpv6NetworkCidr: NotRequired[str]
    DryRun: NotRequired[bool]


class ModifyVpnConnectionRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    TransitGatewayId: NotRequired[str]
    CustomerGatewayId: NotRequired[str]
    VpnGatewayId: NotRequired[str]
    DryRun: NotRequired[bool]


class ModifyVpnTunnelCertificateRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    VpnTunnelOutsideIpAddress: str
    DryRun: NotRequired[bool]


class Phase1DHGroupNumbersRequestListValueTypeDef(TypedDict):
    Value: NotRequired[int]


class Phase1EncryptionAlgorithmsRequestListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class Phase1IntegrityAlgorithmsRequestListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class Phase2DHGroupNumbersRequestListValueTypeDef(TypedDict):
    Value: NotRequired[int]


class Phase2EncryptionAlgorithmsRequestListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class Phase2IntegrityAlgorithmsRequestListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class MonitorInstancesRequestInstanceMonitorTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class MonitorInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    DryRun: NotRequired[bool]


class MoveAddressToVpcRequestRequestTypeDef(TypedDict):
    PublicIp: str
    DryRun: NotRequired[bool]


class MoveByoipCidrToIpamRequestRequestTypeDef(TypedDict):
    Cidr: str
    IpamPoolId: str
    IpamPoolOwner: str
    DryRun: NotRequired[bool]


class MoveCapacityReservationInstancesRequestRequestTypeDef(TypedDict):
    SourceCapacityReservationId: str
    DestinationCapacityReservationId: str
    InstanceCount: int
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class ProvisionedBandwidthTypeDef(TypedDict):
    ProvisionTime: NotRequired[datetime]
    Provisioned: NotRequired[str]
    RequestTime: NotRequired[datetime]
    Requested: NotRequired[str]
    Status: NotRequired[str]


class NativeApplicationOidcOptionsTypeDef(TypedDict):
    PublicSigningKeyEndpoint: NotRequired[str]
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    ClientId: NotRequired[str]
    Scope: NotRequired[str]


class NetworkAclAssociationTypeDef(TypedDict):
    NetworkAclAssociationId: NotRequired[str]
    NetworkAclId: NotRequired[str]
    SubnetId: NotRequired[str]


class NetworkCardInfoTypeDef(TypedDict):
    NetworkCardIndex: NotRequired[int]
    NetworkPerformance: NotRequired[str]
    MaximumNetworkInterfaces: NotRequired[int]
    BaselineBandwidthInGbps: NotRequired[float]
    PeakBandwidthInGbps: NotRequired[float]


class NetworkInterfaceAssociationTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    AssociationId: NotRequired[str]
    IpOwnerId: NotRequired[str]
    PublicDnsName: NotRequired[str]
    PublicIp: NotRequired[str]
    CustomerOwnedIp: NotRequired[str]
    CarrierIp: NotRequired[str]


class NetworkInterfaceIpv6AddressTypeDef(TypedDict):
    Ipv6Address: NotRequired[str]
    IsPrimaryIpv6: NotRequired[bool]


class NetworkInterfacePermissionStateTypeDef(TypedDict):
    State: NotRequired[NetworkInterfacePermissionStateCodeType]
    StatusMessage: NotRequired[str]


class NeuronDeviceCoreInfoTypeDef(TypedDict):
    Count: NotRequired[int]
    Version: NotRequired[int]


class NeuronDeviceMemoryInfoTypeDef(TypedDict):
    SizeInMiB: NotRequired[int]


class OidcOptionsTypeDef(TypedDict):
    Issuer: NotRequired[str]
    AuthorizationEndpoint: NotRequired[str]
    TokenEndpoint: NotRequired[str]
    UserInfoEndpoint: NotRequired[str]
    ClientId: NotRequired[str]
    ClientSecret: NotRequired[str]
    Scope: NotRequired[str]


class PacketHeaderStatementRequestTypeDef(TypedDict):
    SourceAddresses: NotRequired[Sequence[str]]
    DestinationAddresses: NotRequired[Sequence[str]]
    SourcePorts: NotRequired[Sequence[str]]
    DestinationPorts: NotRequired[Sequence[str]]
    SourcePrefixLists: NotRequired[Sequence[str]]
    DestinationPrefixLists: NotRequired[Sequence[str]]
    Protocols: NotRequired[Sequence[ProtocolType]]


class PacketHeaderStatementTypeDef(TypedDict):
    SourceAddresses: NotRequired[list[str]]
    DestinationAddresses: NotRequired[list[str]]
    SourcePorts: NotRequired[list[str]]
    DestinationPorts: NotRequired[list[str]]
    SourcePrefixLists: NotRequired[list[str]]
    DestinationPrefixLists: NotRequired[list[str]]
    Protocols: NotRequired[list[ProtocolType]]


class RequestFilterPortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


class ResourceStatementRequestTypeDef(TypedDict):
    Resources: NotRequired[Sequence[str]]
    ResourceTypes: NotRequired[Sequence[str]]


class ResourceStatementTypeDef(TypedDict):
    Resources: NotRequired[list[str]]
    ResourceTypes: NotRequired[list[str]]


class PeeringAttachmentStatusTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class PeeringTgwInfoTypeDef(TypedDict):
    TransitGatewayId: NotRequired[str]
    CoreNetworkId: NotRequired[str]
    OwnerId: NotRequired[str]
    Region: NotRequired[str]


class Phase1DHGroupNumbersListValueTypeDef(TypedDict):
    Value: NotRequired[int]


class Phase1EncryptionAlgorithmsListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class Phase1IntegrityAlgorithmsListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class Phase2DHGroupNumbersListValueTypeDef(TypedDict):
    Value: NotRequired[int]


class Phase2EncryptionAlgorithmsListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class Phase2IntegrityAlgorithmsListValueTypeDef(TypedDict):
    Value: NotRequired[str]


class PriceScheduleTypeDef(TypedDict):
    Active: NotRequired[bool]
    CurrencyCode: NotRequired[Literal["USD"]]
    Price: NotRequired[float]
    Term: NotRequired[int]


class PricingDetailTypeDef(TypedDict):
    Count: NotRequired[int]
    Price: NotRequired[float]


class PrivateDnsDetailsTypeDef(TypedDict):
    PrivateDnsName: NotRequired[str]


PrivateDnsNameConfigurationTypeDef = TypedDict(
    "PrivateDnsNameConfigurationTypeDef",
    {
        "State": NotRequired[DnsNameStateType],
        "Type": NotRequired[str],
        "Value": NotRequired[str],
        "Name": NotRequired[str],
    },
)


class PrivateDnsNameOptionsOnLaunchTypeDef(TypedDict):
    HostnameType: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecord: NotRequired[bool]
    EnableResourceNameDnsAAAARecord: NotRequired[bool]


class PrivateDnsNameOptionsRequestTypeDef(TypedDict):
    HostnameType: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecord: NotRequired[bool]
    EnableResourceNameDnsAAAARecord: NotRequired[bool]


class PropagatingVgwTypeDef(TypedDict):
    GatewayId: NotRequired[str]


class ProvisionPublicIpv4PoolCidrRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    PoolId: str
    NetmaskLength: int
    DryRun: NotRequired[bool]
    NetworkBorderGroup: NotRequired[str]


class PublicIpv4PoolRangeTypeDef(TypedDict):
    FirstAddress: NotRequired[str]
    LastAddress: NotRequired[str]
    AddressCount: NotRequired[int]
    AvailableAddressCount: NotRequired[int]


class PurchaseCapacityBlockExtensionRequestRequestTypeDef(TypedDict):
    CapacityBlockExtensionOfferingId: str
    CapacityReservationId: str
    DryRun: NotRequired[bool]


class PurchaseRequestTypeDef(TypedDict):
    InstanceCount: int
    PurchaseToken: str


class ReservedInstanceLimitPriceTypeDef(TypedDict):
    Amount: NotRequired[float]
    CurrencyCode: NotRequired[Literal["USD"]]


class RebootInstancesRequestInstanceRebootTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class RebootInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    DryRun: NotRequired[bool]


class RecurringChargeTypeDef(TypedDict):
    Amount: NotRequired[float]
    Frequency: NotRequired[Literal["Hourly"]]


class ReferencedSecurityGroupTypeDef(TypedDict):
    GroupId: NotRequired[str]
    PeeringStatus: NotRequired[str]
    UserId: NotRequired[str]
    VpcId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]


class RegisterInstanceTagAttributeRequestTypeDef(TypedDict):
    IncludeAllTagsOfInstance: NotRequired[bool]
    InstanceTagKeys: NotRequired[Sequence[str]]


class RegisterTransitGatewayMulticastGroupMembersRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    NetworkInterfaceIds: Sequence[str]
    GroupIpAddress: NotRequired[str]
    DryRun: NotRequired[bool]


class TransitGatewayMulticastRegisteredGroupMembersTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    RegisteredNetworkInterfaceIds: NotRequired[list[str]]
    GroupIpAddress: NotRequired[str]


class RegisterTransitGatewayMulticastGroupSourcesRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    NetworkInterfaceIds: Sequence[str]
    GroupIpAddress: NotRequired[str]
    DryRun: NotRequired[bool]


class TransitGatewayMulticastRegisteredGroupSourcesTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    RegisteredNetworkInterfaceIds: NotRequired[list[str]]
    GroupIpAddress: NotRequired[str]


class RejectCapacityReservationBillingOwnershipRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    DryRun: NotRequired[bool]


class RejectTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class RejectTransitGatewayPeeringAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class RejectTransitGatewayVpcAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    DryRun: NotRequired[bool]


class RejectVpcEndpointConnectionsRequestRequestTypeDef(TypedDict):
    ServiceId: str
    VpcEndpointIds: Sequence[str]
    DryRun: NotRequired[bool]


class RejectVpcPeeringConnectionRequestRequestTypeDef(TypedDict):
    VpcPeeringConnectionId: str
    DryRun: NotRequired[bool]


class RejectVpcPeeringConnectionRequestVpcPeeringConnectionRejectTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class ReleaseAddressRequestClassicAddressReleaseTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    PublicIp: NotRequired[str]
    NetworkBorderGroup: NotRequired[str]
    DryRun: NotRequired[bool]


class ReleaseAddressRequestRequestTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    PublicIp: NotRequired[str]
    NetworkBorderGroup: NotRequired[str]
    DryRun: NotRequired[bool]


class ReleaseAddressRequestVpcAddressReleaseTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    PublicIp: NotRequired[str]
    NetworkBorderGroup: NotRequired[str]
    DryRun: NotRequired[bool]


class ReleaseHostsRequestRequestTypeDef(TypedDict):
    HostIds: Sequence[str]


class ReleaseIpamPoolAllocationRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    Cidr: str
    IpamPoolAllocationId: str
    DryRun: NotRequired[bool]


class ReplaceNetworkAclAssociationRequestNetworkAclReplaceAssociationTypeDef(TypedDict):
    AssociationId: str
    DryRun: NotRequired[bool]


class ReplaceNetworkAclAssociationRequestRequestTypeDef(TypedDict):
    AssociationId: str
    NetworkAclId: str
    DryRun: NotRequired[bool]


class ReplaceRouteRequestRequestTypeDef(TypedDict):
    RouteTableId: str
    DestinationPrefixListId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    LocalTarget: NotRequired[bool]
    TransitGatewayId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    CarrierGatewayId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    DryRun: NotRequired[bool]
    DestinationCidrBlock: NotRequired[str]
    GatewayId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    EgressOnlyInternetGatewayId: NotRequired[str]
    InstanceId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    NatGatewayId: NotRequired[str]


class ReplaceRouteRequestRouteReplaceTypeDef(TypedDict):
    DestinationPrefixListId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    LocalTarget: NotRequired[bool]
    TransitGatewayId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    CarrierGatewayId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]
    DryRun: NotRequired[bool]
    GatewayId: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    EgressOnlyInternetGatewayId: NotRequired[str]
    InstanceId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    VpcPeeringConnectionId: NotRequired[str]
    NatGatewayId: NotRequired[str]


class ReplaceRouteTableAssociationRequestRequestTypeDef(TypedDict):
    AssociationId: str
    RouteTableId: str
    DryRun: NotRequired[bool]


class ReplaceRouteTableAssociationRequestRouteTableAssociationReplaceSubnetTypeDef(TypedDict):
    RouteTableId: str
    DryRun: NotRequired[bool]


class ReplaceTransitGatewayRouteRequestRequestTypeDef(TypedDict):
    DestinationCidrBlock: str
    TransitGatewayRouteTableId: str
    TransitGatewayAttachmentId: NotRequired[str]
    Blackhole: NotRequired[bool]
    DryRun: NotRequired[bool]


class ReplaceVpnTunnelRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    VpnTunnelOutsideIpAddress: str
    ApplyPendingMaintenance: NotRequired[bool]
    DryRun: NotRequired[bool]


class ReservedInstancesIdTypeDef(TypedDict):
    ReservedInstancesId: NotRequired[str]


class ResetAddressAttributeRequestRequestTypeDef(TypedDict):
    AllocationId: str
    Attribute: Literal["domain-name"]
    DryRun: NotRequired[bool]


class ResetEbsDefaultKmsKeyIdRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class ResetFpgaImageAttributeRequestRequestTypeDef(TypedDict):
    FpgaImageId: str
    DryRun: NotRequired[bool]
    Attribute: NotRequired[Literal["loadPermission"]]


class ResetImageAttributeRequestImageResetAttributeTypeDef(TypedDict):
    Attribute: Literal["launchPermission"]
    DryRun: NotRequired[bool]


class ResetImageAttributeRequestRequestTypeDef(TypedDict):
    Attribute: Literal["launchPermission"]
    ImageId: str
    DryRun: NotRequired[bool]


class ResetInstanceAttributeRequestInstanceResetAttributeTypeDef(TypedDict):
    Attribute: InstanceAttributeNameType
    DryRun: NotRequired[bool]


class ResetInstanceAttributeRequestInstanceResetKernelTypeDef(TypedDict):
    Attribute: NotRequired[InstanceAttributeNameType]
    DryRun: NotRequired[bool]


class ResetInstanceAttributeRequestInstanceResetRamdiskTypeDef(TypedDict):
    Attribute: NotRequired[InstanceAttributeNameType]
    DryRun: NotRequired[bool]


class ResetInstanceAttributeRequestInstanceResetSourceDestCheckTypeDef(TypedDict):
    Attribute: NotRequired[InstanceAttributeNameType]
    DryRun: NotRequired[bool]


class ResetInstanceAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Attribute: InstanceAttributeNameType
    DryRun: NotRequired[bool]


class ResetNetworkInterfaceAttributeRequestNetworkInterfaceResetAttributeTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    SourceDestCheck: NotRequired[str]


class ResetNetworkInterfaceAttributeRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    DryRun: NotRequired[bool]
    SourceDestCheck: NotRequired[str]


class ResetSnapshotAttributeRequestRequestTypeDef(TypedDict):
    Attribute: SnapshotAttributeNameType
    SnapshotId: str
    DryRun: NotRequired[bool]


class ResetSnapshotAttributeRequestSnapshotResetAttributeTypeDef(TypedDict):
    Attribute: SnapshotAttributeNameType
    DryRun: NotRequired[bool]


class RestoreAddressToClassicRequestRequestTypeDef(TypedDict):
    PublicIp: str
    DryRun: NotRequired[bool]


class RestoreImageFromRecycleBinRequestRequestTypeDef(TypedDict):
    ImageId: str
    DryRun: NotRequired[bool]


class RestoreManagedPrefixListVersionRequestRequestTypeDef(TypedDict):
    PrefixListId: str
    PreviousVersion: int
    CurrentVersion: int
    DryRun: NotRequired[bool]


class RestoreSnapshotFromRecycleBinRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    DryRun: NotRequired[bool]


class RestoreSnapshotTierRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    TemporaryRestoreDays: NotRequired[int]
    PermanentRestore: NotRequired[bool]
    DryRun: NotRequired[bool]


class RevokeClientVpnIngressRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    TargetNetworkCidr: str
    AccessGroupId: NotRequired[str]
    RevokeAllGroups: NotRequired[bool]
    DryRun: NotRequired[bool]


class RevokedSecurityGroupRuleTypeDef(TypedDict):
    SecurityGroupRuleId: NotRequired[str]
    GroupId: NotRequired[str]
    IsEgress: NotRequired[bool]
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIpv4: NotRequired[str]
    CidrIpv6: NotRequired[str]
    PrefixListId: NotRequired[str]
    ReferencedGroupId: NotRequired[str]
    Description: NotRequired[str]


class RouteTypeDef(TypedDict):
    DestinationCidrBlock: NotRequired[str]
    DestinationIpv6CidrBlock: NotRequired[str]
    DestinationPrefixListId: NotRequired[str]
    EgressOnlyInternetGatewayId: NotRequired[str]
    GatewayId: NotRequired[str]
    InstanceId: NotRequired[str]
    InstanceOwnerId: NotRequired[str]
    NatGatewayId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    CarrierGatewayId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    Origin: NotRequired[RouteOriginType]
    State: NotRequired[RouteStateType]
    VpcPeeringConnectionId: NotRequired[str]
    CoreNetworkArn: NotRequired[str]


class S3StorageOutputTypeDef(TypedDict):
    AWSAccessKeyId: NotRequired[str]
    Bucket: NotRequired[str]
    Prefix: NotRequired[str]
    UploadPolicy: NotRequired[bytes]
    UploadPolicySignature: NotRequired[str]


class ScheduledInstanceRecurrenceTypeDef(TypedDict):
    Frequency: NotRequired[str]
    Interval: NotRequired[int]
    OccurrenceDaySet: NotRequired[list[int]]
    OccurrenceRelativeToEnd: NotRequired[bool]
    OccurrenceUnit: NotRequired[str]


class ScheduledInstancesEbsTypeDef(TypedDict):
    DeleteOnTermination: NotRequired[bool]
    Encrypted: NotRequired[bool]
    Iops: NotRequired[int]
    SnapshotId: NotRequired[str]
    VolumeSize: NotRequired[int]
    VolumeType: NotRequired[str]


class ScheduledInstancesIamInstanceProfileTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]


class ScheduledInstancesIpv6AddressTypeDef(TypedDict):
    Ipv6Address: NotRequired[str]


class ScheduledInstancesMonitoringTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class ScheduledInstancesPlacementTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    GroupName: NotRequired[str]


class ScheduledInstancesPrivateIpAddressConfigTypeDef(TypedDict):
    Primary: NotRequired[bool]
    PrivateIpAddress: NotRequired[str]


class TransitGatewayMulticastGroupTypeDef(TypedDict):
    GroupIpAddress: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    SubnetId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    ResourceOwnerId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    GroupMember: NotRequired[bool]
    GroupSource: NotRequired[bool]
    MemberType: NotRequired[MembershipTypeType]
    SourceType: NotRequired[MembershipTypeType]


class SecurityGroupIdentifierTypeDef(TypedDict):
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]


class SecurityGroupRuleDescriptionTypeDef(TypedDict):
    SecurityGroupRuleId: NotRequired[str]
    Description: NotRequired[str]


class SecurityGroupRuleRequestTypeDef(TypedDict):
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIpv4: NotRequired[str]
    CidrIpv6: NotRequired[str]
    PrefixListId: NotRequired[str]
    ReferencedGroupId: NotRequired[str]
    Description: NotRequired[str]


class SendDiagnosticInterruptRequestRequestTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]


class ServiceTypeDetailTypeDef(TypedDict):
    ServiceType: NotRequired[ServiceTypeType]


class SupportedRegionDetailTypeDef(TypedDict):
    Region: NotRequired[str]
    ServiceState: NotRequired[str]


class UserBucketDetailsTypeDef(TypedDict):
    S3Bucket: NotRequired[str]
    S3Key: NotRequired[str]


class SpotCapacityRebalanceTypeDef(TypedDict):
    ReplacementStrategy: NotRequired[ReplacementStrategyType]
    TerminationDelay: NotRequired[int]


class SpotInstanceStateFaultTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class SpotFleetMonitoringTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class SpotInstanceStatusTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]
    UpdateTime: NotRequired[datetime]


class StartInstancesRequestInstanceStartTypeDef(TypedDict):
    AdditionalInfo: NotRequired[str]
    DryRun: NotRequired[bool]


class StartInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    AdditionalInfo: NotRequired[str]
    DryRun: NotRequired[bool]


class StartVpcEndpointServicePrivateDnsVerificationRequestRequestTypeDef(TypedDict):
    ServiceId: str
    DryRun: NotRequired[bool]


class StopInstancesRequestInstanceStopTypeDef(TypedDict):
    Hibernate: NotRequired[bool]
    DryRun: NotRequired[bool]
    Force: NotRequired[bool]


class StopInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    Hibernate: NotRequired[bool]
    DryRun: NotRequired[bool]
    Force: NotRequired[bool]


class SubnetAssociationTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    State: NotRequired[TransitGatewayMulitcastDomainAssociationStateType]


class SubnetCidrBlockStateTypeDef(TypedDict):
    State: NotRequired[SubnetCidrBlockStateCodeType]
    StatusMessage: NotRequired[str]


class SubnetIpPrefixesTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    IpPrefixes: NotRequired[list[str]]


class TargetConfigurationTypeDef(TypedDict):
    InstanceCount: NotRequired[int]
    OfferingId: NotRequired[str]


class TargetGroupTypeDef(TypedDict):
    Arn: NotRequired[str]


class TerminateClientVpnConnectionsRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    ConnectionId: NotRequired[str]
    Username: NotRequired[str]
    DryRun: NotRequired[bool]


class TerminateInstancesRequestInstanceTerminateTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class TerminateInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    DryRun: NotRequired[bool]


class TrafficMirrorPortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


class TransitGatewayAttachmentAssociationTypeDef(TypedDict):
    TransitGatewayRouteTableId: NotRequired[str]
    State: NotRequired[TransitGatewayAssociationStateType]


class TransitGatewayAttachmentBgpConfigurationTypeDef(TypedDict):
    TransitGatewayAsn: NotRequired[int]
    PeerAsn: NotRequired[int]
    TransitGatewayAddress: NotRequired[str]
    PeerAddress: NotRequired[str]
    BgpStatus: NotRequired[BgpStatusType]


TransitGatewayConnectOptionsTypeDef = TypedDict(
    "TransitGatewayConnectOptionsTypeDef",
    {
        "Protocol": NotRequired[Literal["gre"]],
    },
)


class TransitGatewayMulticastDomainOptionsTypeDef(TypedDict):
    Igmpv2Support: NotRequired[Igmpv2SupportValueType]
    StaticSourcesSupport: NotRequired[StaticSourcesSupportValueType]
    AutoAcceptSharedAssociations: NotRequired[AutoAcceptSharedAssociationsValueType]


class TransitGatewayOptionsTypeDef(TypedDict):
    AmazonSideAsn: NotRequired[int]
    TransitGatewayCidrBlocks: NotRequired[list[str]]
    AutoAcceptSharedAttachments: NotRequired[AutoAcceptSharedAttachmentsValueType]
    DefaultRouteTableAssociation: NotRequired[DefaultRouteTableAssociationValueType]
    AssociationDefaultRouteTableId: NotRequired[str]
    DefaultRouteTablePropagation: NotRequired[DefaultRouteTablePropagationValueType]
    PropagationDefaultRouteTableId: NotRequired[str]
    VpnEcmpSupport: NotRequired[VpnEcmpSupportValueType]
    DnsSupport: NotRequired[DnsSupportValueType]
    SecurityGroupReferencingSupport: NotRequired[SecurityGroupReferencingSupportValueType]
    MulticastSupport: NotRequired[MulticastSupportValueType]


class TransitGatewayPeeringAttachmentOptionsTypeDef(TypedDict):
    DynamicRouting: NotRequired[DynamicRoutingValueType]


class TransitGatewayPolicyRuleMetaDataTypeDef(TypedDict):
    MetaDataKey: NotRequired[str]
    MetaDataValue: NotRequired[str]


class TransitGatewayPrefixListAttachmentTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    ResourceId: NotRequired[str]


class TransitGatewayRouteAttachmentTypeDef(TypedDict):
    ResourceId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]


class TransitGatewayVpcAttachmentOptionsTypeDef(TypedDict):
    DnsSupport: NotRequired[DnsSupportValueType]
    SecurityGroupReferencingSupport: NotRequired[SecurityGroupReferencingSupportValueType]
    Ipv6Support: NotRequired[Ipv6SupportValueType]
    ApplianceModeSupport: NotRequired[ApplianceModeSupportValueType]


class UnassignIpv6AddressesRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    Ipv6Prefixes: NotRequired[Sequence[str]]
    Ipv6Addresses: NotRequired[Sequence[str]]


class UnassignPrivateIpAddressesRequestNetworkInterfaceUnassignPrivateIpAddressesTypeDef(TypedDict):
    Ipv4Prefixes: NotRequired[Sequence[str]]
    PrivateIpAddresses: NotRequired[Sequence[str]]


class UnassignPrivateIpAddressesRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    Ipv4Prefixes: NotRequired[Sequence[str]]
    PrivateIpAddresses: NotRequired[Sequence[str]]


class UnassignPrivateNatGatewayAddressRequestRequestTypeDef(TypedDict):
    NatGatewayId: str
    PrivateIpAddresses: Sequence[str]
    MaxDrainDurationSeconds: NotRequired[int]
    DryRun: NotRequired[bool]


class UnlockSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    DryRun: NotRequired[bool]


class UnmonitorInstancesRequestInstanceUnmonitorTypeDef(TypedDict):
    DryRun: NotRequired[bool]


class UnmonitorInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: Sequence[str]
    DryRun: NotRequired[bool]


class UnsuccessfulInstanceCreditSpecificationItemErrorTypeDef(TypedDict):
    Code: NotRequired[UnsuccessfulInstanceCreditSpecificationErrorCodeType]
    Message: NotRequired[str]


class UnsuccessfulItemErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class ValidationErrorTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class VerifiedAccessEndpointPortRangeTypeDef(TypedDict):
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]


VerifiedAccessEndpointRdsOptionsTypeDef = TypedDict(
    "VerifiedAccessEndpointRdsOptionsTypeDef",
    {
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "RdsDbInstanceArn": NotRequired[str],
        "RdsDbClusterArn": NotRequired[str],
        "RdsDbProxyArn": NotRequired[str],
        "RdsEndpoint": NotRequired[str],
        "SubnetIds": NotRequired[list[str]],
    },
)


class VerifiedAccessEndpointStatusTypeDef(TypedDict):
    Code: NotRequired[VerifiedAccessEndpointStatusCodeType]
    Message: NotRequired[str]


class VerifiedAccessInstanceCustomSubDomainTypeDef(TypedDict):
    SubDomain: NotRequired[str]
    Nameservers: NotRequired[list[str]]


class VerifiedAccessInstanceOpenVpnClientConfigurationRouteTypeDef(TypedDict):
    Cidr: NotRequired[str]


class VerifiedAccessTrustProviderCondensedTypeDef(TypedDict):
    VerifiedAccessTrustProviderId: NotRequired[str]
    Description: NotRequired[str]
    TrustProviderType: NotRequired[TrustProviderTypeType]
    UserTrustProviderType: NotRequired[UserTrustProviderTypeType]
    DeviceTrustProviderType: NotRequired[DeviceTrustProviderTypeType]


class VerifiedAccessLogCloudWatchLogsDestinationOptionsTypeDef(TypedDict):
    Enabled: bool
    LogGroup: NotRequired[str]


class VerifiedAccessLogDeliveryStatusTypeDef(TypedDict):
    Code: NotRequired[VerifiedAccessLogDeliveryStatusCodeType]
    Message: NotRequired[str]


class VerifiedAccessLogKinesisDataFirehoseDestinationOptionsTypeDef(TypedDict):
    Enabled: bool
    DeliveryStream: NotRequired[str]


class VerifiedAccessLogS3DestinationOptionsTypeDef(TypedDict):
    Enabled: bool
    BucketName: NotRequired[str]
    Prefix: NotRequired[str]
    BucketOwner: NotRequired[str]


class VgwTelemetryTypeDef(TypedDict):
    AcceptedRouteCount: NotRequired[int]
    LastStatusChange: NotRequired[datetime]
    OutsideIpAddress: NotRequired[str]
    Status: NotRequired[TelemetryStatusType]
    StatusMessage: NotRequired[str]
    CertificateArn: NotRequired[str]


class VolumeAttachmentTypeDef(TypedDict):
    DeleteOnTermination: NotRequired[bool]
    AssociatedResource: NotRequired[str]
    InstanceOwningService: NotRequired[str]
    VolumeId: NotRequired[str]
    InstanceId: NotRequired[str]
    Device: NotRequired[str]
    State: NotRequired[VolumeAttachmentStateType]
    AttachTime: NotRequired[datetime]


class VolumeStatusActionTypeDef(TypedDict):
    Code: NotRequired[str]
    Description: NotRequired[str]
    EventId: NotRequired[str]
    EventType: NotRequired[str]


class VolumeStatusAttachmentStatusTypeDef(TypedDict):
    IoPerformance: NotRequired[str]
    InstanceId: NotRequired[str]


class VolumeStatusDetailsTypeDef(TypedDict):
    Name: NotRequired[VolumeStatusNameType]
    Status: NotRequired[str]


class VolumeStatusEventTypeDef(TypedDict):
    Description: NotRequired[str]
    EventId: NotRequired[str]
    EventType: NotRequired[str]
    NotAfter: NotRequired[datetime]
    NotBefore: NotRequired[datetime]
    InstanceId: NotRequired[str]


class VpcCidrBlockStateTypeDef(TypedDict):
    State: NotRequired[VpcCidrBlockStateCodeType]
    StatusMessage: NotRequired[str]


class VpcPeeringConnectionOptionsDescriptionTypeDef(TypedDict):
    AllowDnsResolutionFromRemoteVpc: NotRequired[bool]
    AllowEgressFromLocalClassicLinkToRemoteVpc: NotRequired[bool]
    AllowEgressFromLocalVpcToRemoteClassicLink: NotRequired[bool]


class VpcPeeringConnectionStateReasonTypeDef(TypedDict):
    Code: NotRequired[VpcPeeringConnectionStateReasonCodeType]
    Message: NotRequired[str]


class VpnStaticRouteTypeDef(TypedDict):
    DestinationCidrBlock: NotRequired[str]
    Source: NotRequired[Literal["Static"]]
    State: NotRequired[VpnStateType]


class WithdrawByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    DryRun: NotRequired[bool]


class AcceptAddressTransferResultTypeDef(TypedDict):
    AddressTransfer: AddressTransferTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptCapacityReservationBillingOwnershipResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptReservedInstancesExchangeQuoteResultTypeDef(TypedDict):
    ExchangeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AllocateAddressResultTypeDef(TypedDict):
    AllocationId: str
    PublicIpv4Pool: str
    NetworkBorderGroup: str
    Domain: DomainTypeType
    CustomerOwnedIp: str
    CustomerOwnedIpv4Pool: str
    CarrierIp: str
    PublicIp: str
    ResponseMetadata: ResponseMetadataTypeDef


class AllocateHostsResultTypeDef(TypedDict):
    HostIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ApplySecurityGroupsToClientVpnTargetNetworkResultTypeDef(TypedDict):
    SecurityGroupIds: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class AssignIpv6AddressesResultTypeDef(TypedDict):
    AssignedIpv6Addresses: list[str]
    AssignedIpv6Prefixes: list[str]
    NetworkInterfaceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateAddressResultTypeDef(TypedDict):
    AssociationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateCapacityReservationBillingOwnerResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateEnclaveCertificateIamRoleResultTypeDef(TypedDict):
    CertificateS3BucketName: str
    CertificateS3ObjectKey: str
    EncryptionKmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateSecurityGroupVpcResultTypeDef(TypedDict):
    State: SecurityGroupVpcAssociationStateType
    ResponseMetadata: ResponseMetadataTypeDef


class AttachClassicLinkVpcResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class AttachNetworkInterfaceResultTypeDef(TypedDict):
    AttachmentId: str
    NetworkCardIndex: int
    ResponseMetadata: ResponseMetadataTypeDef


class CancelCapacityReservationResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CancelDeclarativePoliciesReportResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CancelImageLaunchPermissionResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CancelImportTaskResultTypeDef(TypedDict):
    ImportTaskId: str
    PreviousState: str
    State: str
    ResponseMetadata: ResponseMetadataTypeDef


class ConfirmProductInstanceResultTypeDef(TypedDict):
    Return: bool
    OwnerId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CopyFpgaImageResultTypeDef(TypedDict):
    FpgaImageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CopyImageResultTypeDef(TypedDict):
    ImageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFpgaImageResultTypeDef(TypedDict):
    FpgaImageId: str
    FpgaImageGlobalId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateImageResultTypeDef(TypedDict):
    ImageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePublicIpv4PoolResultTypeDef(TypedDict):
    PoolId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRestoreImageTaskResultTypeDef(TypedDict):
    ImageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRouteResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStoreImageTaskResultTypeDef(TypedDict):
    ObjectKey: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEgressOnlyInternetGatewayResultTypeDef(TypedDict):
    ReturnCode: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFpgaImageResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteKeyPairResultTypeDef(TypedDict):
    Return: bool
    KeyPairId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNatGatewayResultTypeDef(TypedDict):
    NatGatewayId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNetworkInsightsAccessScopeAnalysisResultTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNetworkInsightsAccessScopeResultTypeDef(TypedDict):
    NetworkInsightsAccessScopeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNetworkInsightsAnalysisResultTypeDef(TypedDict):
    NetworkInsightsAnalysisId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNetworkInsightsPathResultTypeDef(TypedDict):
    NetworkInsightsPathId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNetworkInterfacePermissionResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DeletePublicIpv4PoolResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSecurityGroupResultTypeDef(TypedDict):
    Return: bool
    GroupId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrafficMirrorFilterResultTypeDef(TypedDict):
    TrafficMirrorFilterId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrafficMirrorFilterRuleResultTypeDef(TypedDict):
    TrafficMirrorFilterRuleId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrafficMirrorSessionResultTypeDef(TypedDict):
    TrafficMirrorSessionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTrafficMirrorTargetResultTypeDef(TypedDict):
    TrafficMirrorTargetId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcPeeringConnectionResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DeprovisionPublicIpv4PoolCidrResultTypeDef(TypedDict):
    PoolId: str
    DeprovisionedAddresses: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAddressTransfersResultTypeDef(TypedDict):
    AddressTransfers: list[AddressTransferTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DetachClassicLinkVpcResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableAddressTransferResultTypeDef(TypedDict):
    AddressTransfer: AddressTransferTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisableAllowedImagesSettingsResultTypeDef(TypedDict):
    AllowedImagesSettingsState: Literal["disabled"]
    ResponseMetadata: ResponseMetadataTypeDef


class DisableAwsNetworkPerformanceMetricSubscriptionResultTypeDef(TypedDict):
    Output: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableEbsEncryptionByDefaultResultTypeDef(TypedDict):
    EbsEncryptionByDefault: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableImageBlockPublicAccessResultTypeDef(TypedDict):
    ImageBlockPublicAccessState: Literal["unblocked"]
    ResponseMetadata: ResponseMetadataTypeDef


class DisableImageDeprecationResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableImageDeregistrationProtectionResultTypeDef(TypedDict):
    Return: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisableImageResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableIpamOrganizationAdminAccountResultTypeDef(TypedDict):
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableSerialConsoleAccessResultTypeDef(TypedDict):
    SerialConsoleAccessEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableSnapshotBlockPublicAccessResultTypeDef(TypedDict):
    State: SnapshotBlockPublicAccessStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DisableVpcClassicLinkDnsSupportResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisableVpcClassicLinkResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateCapacityReservationBillingOwnerResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateEnclaveCertificateIamRoleResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateSecurityGroupVpcResultTypeDef(TypedDict):
    State: SecurityGroupVpcAssociationStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTrunkInterfaceResultTypeDef(TypedDict):
    Return: bool
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class EnableAddressTransferResultTypeDef(TypedDict):
    AddressTransfer: AddressTransferTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EnableAllowedImagesSettingsResultTypeDef(TypedDict):
    AllowedImagesSettingsState: AllowedImagesSettingsEnabledStateType
    ResponseMetadata: ResponseMetadataTypeDef


class EnableAwsNetworkPerformanceMetricSubscriptionResultTypeDef(TypedDict):
    Output: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableEbsEncryptionByDefaultResultTypeDef(TypedDict):
    EbsEncryptionByDefault: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableImageBlockPublicAccessResultTypeDef(TypedDict):
    ImageBlockPublicAccessState: Literal["block-new-sharing"]
    ResponseMetadata: ResponseMetadataTypeDef


class EnableImageDeprecationResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableImageDeregistrationProtectionResultTypeDef(TypedDict):
    Return: str
    ResponseMetadata: ResponseMetadataTypeDef


class EnableImageResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableIpamOrganizationAdminAccountResultTypeDef(TypedDict):
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableReachabilityAnalyzerOrganizationSharingResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableSerialConsoleAccessResultTypeDef(TypedDict):
    SerialConsoleAccessEnabled: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableSnapshotBlockPublicAccessResultTypeDef(TypedDict):
    State: SnapshotBlockPublicAccessStateType
    ResponseMetadata: ResponseMetadataTypeDef


class EnableVpcClassicLinkDnsSupportResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class EnableVpcClassicLinkResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ExportClientVpnClientConfigurationResultTypeDef(TypedDict):
    ClientConfiguration: str
    ResponseMetadata: ResponseMetadataTypeDef


class ExportTransitGatewayRoutesResultTypeDef(TypedDict):
    S3Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetConsoleOutputResultTypeDef(TypedDict):
    InstanceId: str
    Timestamp: datetime
    Output: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetConsoleScreenshotResultTypeDef(TypedDict):
    ImageData: str
    InstanceId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetEbsDefaultKmsKeyIdResultTypeDef(TypedDict):
    KmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetEbsEncryptionByDefaultResultTypeDef(TypedDict):
    EbsEncryptionByDefault: bool
    SseType: SSETypeType
    ResponseMetadata: ResponseMetadataTypeDef


class GetFlowLogsIntegrationTemplateResultTypeDef(TypedDict):
    Result: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetImageBlockPublicAccessStateResultTypeDef(TypedDict):
    ImageBlockPublicAccessState: str
    ManagedBy: ManagedByType
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceTpmEkPubResultTypeDef(TypedDict):
    InstanceId: str
    KeyType: EkPubKeyTypeType
    KeyFormat: EkPubKeyFormatType
    KeyValue: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceUefiDataResultTypeDef(TypedDict):
    InstanceId: str
    UefiData: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPasswordDataResultTypeDef(TypedDict):
    InstanceId: str
    Timestamp: datetime
    PasswordData: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSerialConsoleAccessStatusResultTypeDef(TypedDict):
    SerialConsoleAccessEnabled: bool
    ManagedBy: ManagedByType
    ResponseMetadata: ResponseMetadataTypeDef


class GetSnapshotBlockPublicAccessStateResultTypeDef(TypedDict):
    State: SnapshotBlockPublicAccessStateType
    ManagedBy: ManagedByType
    ResponseMetadata: ResponseMetadataTypeDef


class GetVerifiedAccessEndpointPolicyResultTypeDef(TypedDict):
    PolicyEnabled: bool
    PolicyDocument: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetVerifiedAccessGroupPolicyResultTypeDef(TypedDict):
    PolicyEnabled: bool
    PolicyDocument: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetVpnConnectionDeviceSampleConfigurationResultTypeDef(TypedDict):
    VpnConnectionDeviceSampleConfiguration: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportClientVpnClientCertificateRevocationListResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class LockSnapshotResultTypeDef(TypedDict):
    SnapshotId: str
    LockState: LockStateType
    LockDuration: int
    CoolOffPeriod: int
    CoolOffPeriodExpiresOn: datetime
    LockCreatedOn: datetime
    LockExpiresOn: datetime
    LockDurationStartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyAvailabilityZoneGroupResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyCapacityReservationFleetResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyCapacityReservationResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyClientVpnEndpointResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyEbsDefaultKmsKeyIdResultTypeDef(TypedDict):
    KmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyFleetResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceCapacityReservationAttributesResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceCpuOptionsResultTypeDef(TypedDict):
    InstanceId: str
    CoreCount: int
    ThreadsPerCore: int
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceMaintenanceOptionsResultTypeDef(TypedDict):
    InstanceId: str
    AutoRecovery: InstanceAutoRecoveryStateType
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceMetadataDefaultsResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceNetworkPerformanceResultTypeDef(TypedDict):
    InstanceId: str
    BandwidthWeighting: InstanceBandwidthWeightingType
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstancePlacementResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyPrivateDnsNameOptionsResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReservedInstancesResultTypeDef(TypedDict):
    ReservedInstancesModificationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifySecurityGroupRulesResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifySnapshotTierResultTypeDef(TypedDict):
    SnapshotId: str
    TieringStartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ModifySpotFleetRequestResponseTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpcEndpointConnectionNotificationResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpcEndpointResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpcEndpointServiceConfigurationResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpcEndpointServicePayerResponsibilityResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpcTenancyResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class MoveAddressToVpcResultTypeDef(TypedDict):
    AllocationId: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef


class PurchaseReservedInstancesOfferingResultTypeDef(TypedDict):
    ReservedInstancesId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterImageResultTypeDef(TypedDict):
    ImageId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RejectCapacityReservationBillingOwnershipResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RejectVpcPeeringConnectionResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReleaseIpamPoolAllocationResultTypeDef(TypedDict):
    Success: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReplaceImageCriteriaInAllowedImagesSettingsResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ReplaceNetworkAclAssociationResultTypeDef(TypedDict):
    NewAssociationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReplaceVpnTunnelResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RequestSpotFleetResponseTypeDef(TypedDict):
    SpotFleetRequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResetEbsDefaultKmsKeyIdResultTypeDef(TypedDict):
    KmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResetFpgaImageAttributeResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreAddressToClassicResultTypeDef(TypedDict):
    PublicIp: str
    Status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreImageFromRecycleBinResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreSnapshotFromRecycleBinResultTypeDef(TypedDict):
    SnapshotId: str
    OutpostArn: str
    Description: str
    Encrypted: bool
    OwnerId: str
    Progress: str
    StartTime: datetime
    State: SnapshotStateType
    VolumeId: str
    VolumeSize: int
    SseType: SSETypeType
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreSnapshotTierResultTypeDef(TypedDict):
    SnapshotId: str
    RestoreStartTime: datetime
    RestoreDuration: int
    IsPermanentRestore: bool
    ResponseMetadata: ResponseMetadataTypeDef


class RunScheduledInstancesResultTypeDef(TypedDict):
    InstanceIdSet: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class StartDeclarativePoliciesReportResultTypeDef(TypedDict):
    ReportId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartVpcEndpointServicePrivateDnsVerificationResultTypeDef(TypedDict):
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UnassignIpv6AddressesResultTypeDef(TypedDict):
    NetworkInterfaceId: str
    UnassignedIpv6Addresses: list[str]
    UnassignedIpv6Prefixes: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UnlockSnapshotResultTypeDef(TypedDict):
    SnapshotId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSecurityGroupRuleDescriptionsEgressResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSecurityGroupRuleDescriptionsIngressResultTypeDef(TypedDict):
    Return: bool
    ResponseMetadata: ResponseMetadataTypeDef


class VolumeAttachmentResponseTypeDef(TypedDict):
    DeleteOnTermination: bool
    AssociatedResource: str
    InstanceOwningService: str
    VolumeId: str
    InstanceId: str
    Device: str
    State: VolumeAttachmentStateType
    AttachTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptReservedInstancesExchangeQuoteRequestRequestTypeDef(TypedDict):
    ReservedInstanceIds: Sequence[str]
    DryRun: NotRequired[bool]
    TargetConfigurations: NotRequired[Sequence[TargetConfigurationRequestTypeDef]]


class GetReservedInstancesExchangeQuoteRequestRequestTypeDef(TypedDict):
    ReservedInstanceIds: Sequence[str]
    DryRun: NotRequired[bool]
    TargetConfigurations: NotRequired[Sequence[TargetConfigurationRequestTypeDef]]


class AccountAttributeTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValues: NotRequired[list[AccountAttributeValueTypeDef]]


class DescribeFleetInstancesResultTypeDef(TypedDict):
    ActiveInstances: list[ActiveInstanceTypeDef]
    FleetId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSpotFleetInstancesResponseTypeDef(TypedDict):
    ActiveInstances: list[ActiveInstanceTypeDef]
    SpotFleetRequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVpcEndpointServicePermissionsResultTypeDef(TypedDict):
    AddedPrincipals: list[AddedPrincipalTypeDef]
    ReturnValue: bool
    ResponseMetadata: ResponseMetadataTypeDef


class AnalysisLoadBalancerTargetTypeDef(TypedDict):
    Address: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    Instance: NotRequired[AnalysisComponentTypeDef]
    Port: NotRequired[int]


class RuleGroupRuleOptionsPairTypeDef(TypedDict):
    RuleGroupArn: NotRequired[str]
    RuleOptions: NotRequired[list[RuleOptionTypeDef]]


class AddressAttributeTypeDef(TypedDict):
    PublicIp: NotRequired[str]
    AllocationId: NotRequired[str]
    PtrRecord: NotRequired[str]
    PtrRecordUpdate: NotRequired[PtrUpdateStatusTypeDef]


class AddressTypeDef(TypedDict):
    AllocationId: NotRequired[str]
    AssociationId: NotRequired[str]
    Domain: NotRequired[DomainTypeType]
    NetworkInterfaceId: NotRequired[str]
    NetworkInterfaceOwnerId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    PublicIpv4Pool: NotRequired[str]
    NetworkBorderGroup: NotRequired[str]
    CustomerOwnedIp: NotRequired[str]
    CustomerOwnedIpv4Pool: NotRequired[str]
    CarrierIp: NotRequired[str]
    InstanceId: NotRequired[str]
    PublicIp: NotRequired[str]


class AllowedPrincipalTypeDef(TypedDict):
    PrincipalType: NotRequired[PrincipalTypeType]
    Principal: NotRequired[str]
    ServicePermissionId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    ServiceId: NotRequired[str]


class CarrierGatewayTypeDef(TypedDict):
    CarrierGatewayId: NotRequired[str]
    VpcId: NotRequired[str]
    State: NotRequired[CarrierGatewayStateType]
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ClientCreateTagsRequestTypeDef(TypedDict):
    Resources: Sequence[str]
    Tags: Sequence[TagTypeDef]
    DryRun: NotRequired[bool]


class ClientDeleteTagsRequestTypeDef(TypedDict):
    Resources: Sequence[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DryRun: NotRequired[bool]


class CoipPoolTypeDef(TypedDict):
    PoolId: NotRequired[str]
    PoolCidrs: NotRequired[list[str]]
    LocalGatewayRouteTableId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    PoolArn: NotRequired[str]


class CopySnapshotResultTypeDef(TypedDict):
    Tags: list[TagTypeDef]
    SnapshotId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSecurityGroupResultTypeDef(TypedDict):
    GroupId: str
    Tags: list[TagTypeDef]
    SecurityGroupArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTagsRequestServiceResourceCreateTagsTypeDef(TypedDict):
    Resources: Sequence[str]
    Tags: Sequence[TagTypeDef]
    DryRun: NotRequired[bool]


CustomerGatewayTypeDef = TypedDict(
    "CustomerGatewayTypeDef",
    {
        "CertificateArn": NotRequired[str],
        "DeviceName": NotRequired[str],
        "Tags": NotRequired[list[TagTypeDef]],
        "BgpAsnExtended": NotRequired[str],
        "CustomerGatewayId": NotRequired[str],
        "State": NotRequired[str],
        "Type": NotRequired[str],
        "IpAddress": NotRequired[str],
        "BgpAsn": NotRequired[str],
    },
)


class DeclarativePoliciesReportTypeDef(TypedDict):
    ReportId: NotRequired[str]
    S3Bucket: NotRequired[str]
    S3Prefix: NotRequired[str]
    TargetId: NotRequired[str]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    Status: NotRequired[ReportStateType]
    Tags: NotRequired[list[TagTypeDef]]


class Ec2InstanceConnectEndpointTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    InstanceConnectEndpointId: NotRequired[str]
    InstanceConnectEndpointArn: NotRequired[str]
    State: NotRequired[Ec2InstanceConnectEndpointStateType]
    StateMessage: NotRequired[str]
    DnsName: NotRequired[str]
    FipsDnsName: NotRequired[str]
    NetworkInterfaceIds: NotRequired[list[str]]
    VpcId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    CreatedAt: NotRequired[datetime]
    SubnetId: NotRequired[str]
    PreserveClientIp: NotRequired[bool]
    SecurityGroupIds: NotRequired[list[str]]
    Tags: NotRequired[list[TagTypeDef]]


class HostReservationTypeDef(TypedDict):
    Count: NotRequired[int]
    CurrencyCode: NotRequired[Literal["USD"]]
    Duration: NotRequired[int]
    End: NotRequired[datetime]
    HostIdSet: NotRequired[list[str]]
    HostReservationId: NotRequired[str]
    HourlyPrice: NotRequired[str]
    InstanceFamily: NotRequired[str]
    OfferingId: NotRequired[str]
    PaymentOption: NotRequired[PaymentOptionType]
    Start: NotRequired[datetime]
    State: NotRequired[ReservationStateType]
    UpfrontPrice: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ImportKeyPairResultTypeDef(TypedDict):
    KeyFingerprint: str
    KeyName: str
    KeyPairId: str
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class InstanceCreateTagsRequestTypeDef(TypedDict):
    Tags: Sequence[TagTypeDef]
    DryRun: NotRequired[bool]


class InstanceDeleteTagsRequestTypeDef(TypedDict):
    Tags: NotRequired[Sequence[TagTypeDef]]
    DryRun: NotRequired[bool]


class InstanceEventWindowAssociationRequestTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    InstanceTags: NotRequired[Sequence[TagTypeDef]]
    DedicatedHostIds: NotRequired[Sequence[str]]


class InstanceEventWindowAssociationTargetTypeDef(TypedDict):
    InstanceIds: NotRequired[list[str]]
    Tags: NotRequired[list[TagTypeDef]]
    DedicatedHostIds: NotRequired[list[str]]


class InstanceEventWindowDisassociationRequestTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    InstanceTags: NotRequired[Sequence[TagTypeDef]]
    DedicatedHostIds: NotRequired[Sequence[str]]


class IpamExternalResourceVerificationTokenTypeDef(TypedDict):
    IpamExternalResourceVerificationTokenId: NotRequired[str]
    IpamExternalResourceVerificationTokenArn: NotRequired[str]
    IpamId: NotRequired[str]
    IpamArn: NotRequired[str]
    IpamRegion: NotRequired[str]
    TokenValue: NotRequired[str]
    TokenName: NotRequired[str]
    NotAfter: NotRequired[datetime]
    Status: NotRequired[TokenStateType]
    Tags: NotRequired[list[TagTypeDef]]
    State: NotRequired[IpamExternalResourceVerificationTokenStateType]


class IpamResourceDiscoveryAssociationTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    IpamResourceDiscoveryAssociationId: NotRequired[str]
    IpamResourceDiscoveryAssociationArn: NotRequired[str]
    IpamResourceDiscoveryId: NotRequired[str]
    IpamId: NotRequired[str]
    IpamArn: NotRequired[str]
    IpamRegion: NotRequired[str]
    IsDefault: NotRequired[bool]
    ResourceDiscoveryStatus: NotRequired[IpamAssociatedResourceDiscoveryStatusType]
    State: NotRequired[IpamResourceDiscoveryAssociationStateType]
    Tags: NotRequired[list[TagTypeDef]]


class IpamScopeTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    IpamScopeId: NotRequired[str]
    IpamScopeArn: NotRequired[str]
    IpamArn: NotRequired[str]
    IpamRegion: NotRequired[str]
    IpamScopeType: NotRequired[IpamScopeTypeType]
    IsDefault: NotRequired[bool]
    Description: NotRequired[str]
    PoolCount: NotRequired[int]
    State: NotRequired[IpamScopeStateType]
    Tags: NotRequired[list[TagTypeDef]]


class KeyPairInfoTypeDef(TypedDict):
    KeyPairId: NotRequired[str]
    KeyType: NotRequired[KeyTypeType]
    Tags: NotRequired[list[TagTypeDef]]
    PublicKey: NotRequired[str]
    CreateTime: NotRequired[datetime]
    KeyName: NotRequired[str]
    KeyFingerprint: NotRequired[str]


class KeyPairTypeDef(TypedDict):
    KeyPairId: str
    Tags: list[TagTypeDef]
    KeyName: str
    KeyFingerprint: str
    KeyMaterial: str
    ResponseMetadata: ResponseMetadataTypeDef


class LaunchTemplateTagSpecificationRequestTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class LaunchTemplateTagSpecificationTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    Tags: NotRequired[list[TagTypeDef]]


class LocalGatewayRouteTableVirtualInterfaceGroupAssociationTypeDef(TypedDict):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociationId: NotRequired[str]
    LocalGatewayVirtualInterfaceGroupId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    LocalGatewayRouteTableId: NotRequired[str]
    LocalGatewayRouteTableArn: NotRequired[str]
    OwnerId: NotRequired[str]
    State: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class LocalGatewayRouteTableVpcAssociationTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociationId: NotRequired[str]
    LocalGatewayRouteTableId: NotRequired[str]
    LocalGatewayRouteTableArn: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    VpcId: NotRequired[str]
    OwnerId: NotRequired[str]
    State: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class LocalGatewayTypeDef(TypedDict):
    LocalGatewayId: NotRequired[str]
    OutpostArn: NotRequired[str]
    OwnerId: NotRequired[str]
    State: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class LocalGatewayVirtualInterfaceGroupTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceGroupId: NotRequired[str]
    LocalGatewayVirtualInterfaceIds: NotRequired[list[str]]
    LocalGatewayId: NotRequired[str]
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class LocalGatewayVirtualInterfaceTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceId: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    Vlan: NotRequired[int]
    LocalAddress: NotRequired[str]
    PeerAddress: NotRequired[str]
    LocalBgpAsn: NotRequired[int]
    PeerBgpAsn: NotRequired[int]
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ManagedPrefixListTypeDef(TypedDict):
    PrefixListId: NotRequired[str]
    AddressFamily: NotRequired[str]
    State: NotRequired[PrefixListStateType]
    StateMessage: NotRequired[str]
    PrefixListArn: NotRequired[str]
    PrefixListName: NotRequired[str]
    MaxEntries: NotRequired[int]
    Version: NotRequired[int]
    Tags: NotRequired[list[TagTypeDef]]
    OwnerId: NotRequired[str]


class NetworkInsightsAccessScopeAnalysisTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: NotRequired[str]
    NetworkInsightsAccessScopeAnalysisArn: NotRequired[str]
    NetworkInsightsAccessScopeId: NotRequired[str]
    Status: NotRequired[AnalysisStatusType]
    StatusMessage: NotRequired[str]
    WarningMessage: NotRequired[str]
    StartDate: NotRequired[datetime]
    EndDate: NotRequired[datetime]
    FindingsFound: NotRequired[FindingsFoundType]
    AnalyzedEniCount: NotRequired[int]
    Tags: NotRequired[list[TagTypeDef]]


class NetworkInsightsAccessScopeTypeDef(TypedDict):
    NetworkInsightsAccessScopeId: NotRequired[str]
    NetworkInsightsAccessScopeArn: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    UpdatedDate: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


class PlacementGroupTypeDef(TypedDict):
    GroupName: NotRequired[str]
    State: NotRequired[PlacementGroupStateType]
    Strategy: NotRequired[PlacementStrategyType]
    PartitionCount: NotRequired[int]
    GroupId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    GroupArn: NotRequired[str]
    SpreadLevel: NotRequired[SpreadLevelType]


class ReplaceRootVolumeTaskTypeDef(TypedDict):
    ReplaceRootVolumeTaskId: NotRequired[str]
    InstanceId: NotRequired[str]
    TaskState: NotRequired[ReplaceRootVolumeTaskStateType]
    StartTime: NotRequired[str]
    CompleteTime: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    ImageId: NotRequired[str]
    SnapshotId: NotRequired[str]
    DeleteReplacedRootVolume: NotRequired[bool]


class SecurityGroupForVpcTypeDef(TypedDict):
    Description: NotRequired[str]
    GroupName: NotRequired[str]
    OwnerId: NotRequired[str]
    GroupId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    PrimaryVpcId: NotRequired[str]


class SnapshotInfoTypeDef(TypedDict):
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    Encrypted: NotRequired[bool]
    VolumeId: NotRequired[str]
    State: NotRequired[SnapshotStateType]
    VolumeSize: NotRequired[int]
    StartTime: NotRequired[datetime]
    Progress: NotRequired[str]
    OwnerId: NotRequired[str]
    SnapshotId: NotRequired[str]
    OutpostArn: NotRequired[str]
    SseType: NotRequired[SSETypeType]
    AvailabilityZone: NotRequired[str]


class SnapshotResponseTypeDef(TypedDict):
    OwnerAlias: str
    OutpostArn: str
    Tags: list[TagTypeDef]
    StorageTier: StorageTierType
    RestoreExpiryTime: datetime
    SseType: SSETypeType
    AvailabilityZone: str
    TransferType: TransferTypeType
    CompletionDurationMinutes: int
    CompletionTime: datetime
    SnapshotId: str
    VolumeId: str
    State: SnapshotStateType
    StateMessage: str
    StartTime: datetime
    Progress: str
    OwnerId: str
    Description: str
    VolumeSize: int
    Encrypted: bool
    KmsKeyId: str
    DataEncryptionKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SnapshotTierStatusTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    VolumeId: NotRequired[str]
    Status: NotRequired[SnapshotStateType]
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    StorageTier: NotRequired[StorageTierType]
    LastTieringStartTime: NotRequired[datetime]
    LastTieringProgress: NotRequired[int]
    LastTieringOperationStatus: NotRequired[TieringOperationStatusType]
    LastTieringOperationStatusDetail: NotRequired[str]
    ArchivalCompleteTime: NotRequired[datetime]
    RestoreExpiryTime: NotRequired[datetime]


class SnapshotTypeDef(TypedDict):
    OwnerAlias: NotRequired[str]
    OutpostArn: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    StorageTier: NotRequired[StorageTierType]
    RestoreExpiryTime: NotRequired[datetime]
    SseType: NotRequired[SSETypeType]
    AvailabilityZone: NotRequired[str]
    TransferType: NotRequired[TransferTypeType]
    CompletionDurationMinutes: NotRequired[int]
    CompletionTime: NotRequired[datetime]
    SnapshotId: NotRequired[str]
    VolumeId: NotRequired[str]
    State: NotRequired[SnapshotStateType]
    StateMessage: NotRequired[str]
    StartTime: NotRequired[datetime]
    Progress: NotRequired[str]
    OwnerId: NotRequired[str]
    Description: NotRequired[str]
    VolumeSize: NotRequired[int]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    DataEncryptionKeyId: NotRequired[str]


class SpotFleetTagSpecificationOutputTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    Tags: NotRequired[list[TagTypeDef]]


class SpotFleetTagSpecificationTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class SubnetCidrReservationTypeDef(TypedDict):
    SubnetCidrReservationId: NotRequired[str]
    SubnetId: NotRequired[str]
    Cidr: NotRequired[str]
    ReservationType: NotRequired[SubnetCidrReservationTypeType]
    OwnerId: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class TagSpecificationOutputTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    Tags: NotRequired[list[TagTypeDef]]


class TagSpecificationTypeDef(TypedDict):
    ResourceType: NotRequired[ResourceTypeType]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TrafficMirrorSessionTypeDef(TypedDict):
    TrafficMirrorSessionId: NotRequired[str]
    TrafficMirrorTargetId: NotRequired[str]
    TrafficMirrorFilterId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    OwnerId: NotRequired[str]
    PacketLength: NotRequired[int]
    SessionNumber: NotRequired[int]
    VirtualNetworkId: NotRequired[int]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


TrafficMirrorTargetTypeDef = TypedDict(
    "TrafficMirrorTargetTypeDef",
    {
        "TrafficMirrorTargetId": NotRequired[str],
        "NetworkInterfaceId": NotRequired[str],
        "NetworkLoadBalancerArn": NotRequired[str],
        "Type": NotRequired[TrafficMirrorTargetTypeType],
        "Description": NotRequired[str],
        "OwnerId": NotRequired[str],
        "Tags": NotRequired[list[TagTypeDef]],
        "GatewayLoadBalancerEndpointId": NotRequired[str],
    },
)


class TransitGatewayPolicyTableTypeDef(TypedDict):
    TransitGatewayPolicyTableId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    State: NotRequired[TransitGatewayPolicyTableStateType]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


class TransitGatewayRouteTableAnnouncementTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncementId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    CoreNetworkId: NotRequired[str]
    PeerTransitGatewayId: NotRequired[str]
    PeerCoreNetworkId: NotRequired[str]
    PeeringAttachmentId: NotRequired[str]
    AnnouncementDirection: NotRequired[TransitGatewayRouteTableAnnouncementDirectionType]
    TransitGatewayRouteTableId: NotRequired[str]
    State: NotRequired[TransitGatewayRouteTableAnnouncementStateType]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


class TransitGatewayRouteTableTypeDef(TypedDict):
    TransitGatewayRouteTableId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    State: NotRequired[TransitGatewayRouteTableStateType]
    DefaultAssociationRouteTable: NotRequired[bool]
    DefaultPropagationRouteTable: NotRequired[bool]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


class TrunkInterfaceAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    BranchInterfaceId: NotRequired[str]
    TrunkInterfaceId: NotRequired[str]
    InterfaceProtocol: NotRequired[InterfaceProtocolTypeType]
    VlanId: NotRequired[int]
    GreKey: NotRequired[int]
    Tags: NotRequired[list[TagTypeDef]]


class VpcBlockPublicAccessExclusionTypeDef(TypedDict):
    ExclusionId: NotRequired[str]
    InternetGatewayExclusionMode: NotRequired[InternetGatewayExclusionModeType]
    ResourceArn: NotRequired[str]
    State: NotRequired[VpcBlockPublicAccessExclusionStateType]
    Reason: NotRequired[str]
    CreationTimestamp: NotRequired[datetime]
    LastUpdateTimestamp: NotRequired[datetime]
    DeletionTimestamp: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


class VpcClassicLinkTypeDef(TypedDict):
    ClassicLinkEnabled: NotRequired[bool]
    Tags: NotRequired[list[TagTypeDef]]
    VpcId: NotRequired[str]


class VpcCreateTagsRequestTypeDef(TypedDict):
    Tags: Sequence[TagTypeDef]
    DryRun: NotRequired[bool]


class AllocateIpamPoolCidrResultTypeDef(TypedDict):
    IpamPoolAllocation: IpamPoolAllocationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIpamPoolAllocationsResultTypeDef(TypedDict):
    IpamPoolAllocations: list[IpamPoolAllocationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


AnalysisAclRuleTypeDef = TypedDict(
    "AnalysisAclRuleTypeDef",
    {
        "Cidr": NotRequired[str],
        "Egress": NotRequired[bool],
        "PortRange": NotRequired[PortRangeTypeDef],
        "Protocol": NotRequired[str],
        "RuleAction": NotRequired[str],
        "RuleNumber": NotRequired[int],
    },
)
AnalysisPacketHeaderTypeDef = TypedDict(
    "AnalysisPacketHeaderTypeDef",
    {
        "DestinationAddresses": NotRequired[list[str]],
        "DestinationPortRanges": NotRequired[list[PortRangeTypeDef]],
        "Protocol": NotRequired[str],
        "SourceAddresses": NotRequired[list[str]],
        "SourcePortRanges": NotRequired[list[PortRangeTypeDef]],
    },
)
AnalysisSecurityGroupRuleTypeDef = TypedDict(
    "AnalysisSecurityGroupRuleTypeDef",
    {
        "Cidr": NotRequired[str],
        "Direction": NotRequired[str],
        "SecurityGroupId": NotRequired[str],
        "PortRange": NotRequired[PortRangeTypeDef],
        "PrefixListId": NotRequired[str],
        "Protocol": NotRequired[str],
    },
)
FirewallStatefulRuleTypeDef = TypedDict(
    "FirewallStatefulRuleTypeDef",
    {
        "RuleGroupArn": NotRequired[str],
        "Sources": NotRequired[list[str]],
        "Destinations": NotRequired[list[str]],
        "SourcePorts": NotRequired[list[PortRangeTypeDef]],
        "DestinationPorts": NotRequired[list[PortRangeTypeDef]],
        "Protocol": NotRequired[str],
        "RuleAction": NotRequired[str],
        "Direction": NotRequired[str],
    },
)


class FirewallStatelessRuleTypeDef(TypedDict):
    RuleGroupArn: NotRequired[str]
    Sources: NotRequired[list[str]]
    Destinations: NotRequired[list[str]]
    SourcePorts: NotRequired[list[PortRangeTypeDef]]
    DestinationPorts: NotRequired[list[PortRangeTypeDef]]
    Protocols: NotRequired[list[int]]
    RuleAction: NotRequired[str]
    Priority: NotRequired[int]


class AssociateIpamByoasnResultTypeDef(TypedDict):
    AsnAssociation: AsnAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ByoipCidrTypeDef(TypedDict):
    Cidr: NotRequired[str]
    Description: NotRequired[str]
    AsnAssociations: NotRequired[list[AsnAssociationTypeDef]]
    StatusMessage: NotRequired[str]
    State: NotRequired[ByoipCidrStateType]
    NetworkBorderGroup: NotRequired[str]


class DisassociateIpamByoasnResultTypeDef(TypedDict):
    AsnAssociation: AsnAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ProvisionIpamByoasnRequestRequestTypeDef(TypedDict):
    IpamId: str
    Asn: str
    AsnAuthorizationContext: AsnAuthorizationContextTypeDef
    DryRun: NotRequired[bool]


class AssignPrivateIpAddressesResultTypeDef(TypedDict):
    NetworkInterfaceId: str
    AssignedPrivateIpAddresses: list[AssignedPrivateIpAddressTypeDef]
    AssignedIpv4Prefixes: list[Ipv4PrefixSpecificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AssignPrivateNatGatewayAddressResultTypeDef(TypedDict):
    NatGatewayId: str
    NatGatewayAddresses: list[NatGatewayAddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateNatGatewayAddressResultTypeDef(TypedDict):
    NatGatewayId: str
    NatGatewayAddresses: list[NatGatewayAddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateNatGatewayAddressResultTypeDef(TypedDict):
    NatGatewayId: str
    NatGatewayAddresses: list[NatGatewayAddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UnassignPrivateNatGatewayAddressResultTypeDef(TypedDict):
    NatGatewayId: str
    NatGatewayAddresses: list[NatGatewayAddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateClientVpnTargetNetworkResultTypeDef(TypedDict):
    AssociationId: str
    Status: AssociationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateClientVpnTargetNetworkResultTypeDef(TypedDict):
    AssociationId: str
    Status: AssociationStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TargetNetworkTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    VpcId: NotRequired[str]
    TargetNetworkId: NotRequired[str]
    ClientVpnEndpointId: NotRequired[str]
    Status: NotRequired[AssociationStatusTypeDef]
    SecurityGroups: NotRequired[list[str]]


class AssociateIamInstanceProfileRequestRequestTypeDef(TypedDict):
    IamInstanceProfile: IamInstanceProfileSpecificationTypeDef
    InstanceId: str


class ReplaceIamInstanceProfileAssociationRequestRequestTypeDef(TypedDict):
    IamInstanceProfile: IamInstanceProfileSpecificationTypeDef
    AssociationId: str


class AssociateRouteTableResultTypeDef(TypedDict):
    AssociationId: str
    AssociationState: RouteTableAssociationStateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReplaceRouteTableAssociationResultTypeDef(TypedDict):
    NewAssociationId: str
    AssociationState: RouteTableAssociationStateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RouteTableAssociationTypeDef(TypedDict):
    Main: NotRequired[bool]
    RouteTableAssociationId: NotRequired[str]
    RouteTableId: NotRequired[str]
    SubnetId: NotRequired[str]
    GatewayId: NotRequired[str]
    AssociationState: NotRequired[RouteTableAssociationStateTypeDef]


class AssociateTransitGatewayPolicyTableResultTypeDef(TypedDict):
    Association: TransitGatewayPolicyTableAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTransitGatewayPolicyTableResultTypeDef(TypedDict):
    Association: TransitGatewayPolicyTableAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayPolicyTableAssociationsResultTypeDef(TypedDict):
    Associations: list[TransitGatewayPolicyTableAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateTransitGatewayRouteTableResultTypeDef(TypedDict):
    Association: TransitGatewayAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTransitGatewayRouteTableResultTypeDef(TypedDict):
    Association: TransitGatewayAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssociatedEnclaveCertificateIamRolesResultTypeDef(TypedDict):
    AssociatedRoles: list[AssociatedRoleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AthenaIntegrationTypeDef(TypedDict):
    IntegrationResultS3DestinationArn: str
    PartitionLoadFrequency: PartitionLoadFrequencyType
    PartitionStartDate: NotRequired[TimestampTypeDef]
    PartitionEndDate: NotRequired[TimestampTypeDef]


class ClientDataTypeDef(TypedDict):
    Comment: NotRequired[str]
    UploadEnd: NotRequired[TimestampTypeDef]
    UploadSize: NotRequired[float]
    UploadStart: NotRequired[TimestampTypeDef]


class DescribeCapacityBlockOfferingsRequestRequestTypeDef(TypedDict):
    CapacityDurationHours: int
    DryRun: NotRequired[bool]
    InstanceType: NotRequired[str]
    InstanceCount: NotRequired[int]
    StartDateRange: NotRequired[TimestampTypeDef]
    EndDateRange: NotRequired[TimestampTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeFleetHistoryRequestRequestTypeDef(TypedDict):
    FleetId: str
    StartTime: TimestampTypeDef
    DryRun: NotRequired[bool]
    EventType: NotRequired[FleetEventTypeType]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeSpotFleetRequestHistoryRequestRequestTypeDef(TypedDict):
    SpotFleetRequestId: str
    StartTime: TimestampTypeDef
    DryRun: NotRequired[bool]
    EventType: NotRequired[EventTypeType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class EnableImageDeprecationRequestRequestTypeDef(TypedDict):
    ImageId: str
    DeprecateAt: TimestampTypeDef
    DryRun: NotRequired[bool]


class GetIpamAddressHistoryRequestRequestTypeDef(TypedDict):
    Cidr: str
    IpamScopeId: str
    DryRun: NotRequired[bool]
    VpcId: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class LaunchTemplateSpotMarketOptionsRequestTypeDef(TypedDict):
    MaxPrice: NotRequired[str]
    SpotInstanceType: NotRequired[SpotInstanceTypeType]
    BlockDurationMinutes: NotRequired[int]
    ValidUntil: NotRequired[TimestampTypeDef]
    InstanceInterruptionBehavior: NotRequired[InstanceInterruptionBehaviorType]


class LockSnapshotRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    LockMode: LockModeType
    DryRun: NotRequired[bool]
    CoolOffPeriod: NotRequired[int]
    LockDuration: NotRequired[int]
    ExpirationDate: NotRequired[TimestampTypeDef]


class ModifyCapacityReservationFleetRequestRequestTypeDef(TypedDict):
    CapacityReservationFleetId: str
    TotalTargetCapacity: NotRequired[int]
    EndDate: NotRequired[TimestampTypeDef]
    DryRun: NotRequired[bool]
    RemoveEndDate: NotRequired[bool]


class ModifyCapacityReservationRequestRequestTypeDef(TypedDict):
    CapacityReservationId: str
    InstanceCount: NotRequired[int]
    EndDate: NotRequired[TimestampTypeDef]
    EndDateType: NotRequired[EndDateTypeType]
    Accept: NotRequired[bool]
    DryRun: NotRequired[bool]
    AdditionalInfo: NotRequired[str]
    InstanceMatchCriteria: NotRequired[InstanceMatchCriteriaType]


class ModifyInstanceEventStartTimeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    InstanceEventId: str
    NotBefore: TimestampTypeDef
    DryRun: NotRequired[bool]


class ReportInstanceStatusRequestInstanceReportStatusTypeDef(TypedDict):
    Status: ReportStatusTypeType
    ReasonCodes: Sequence[ReportInstanceReasonCodesType]
    DryRun: NotRequired[bool]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Description: NotRequired[str]


class ReportInstanceStatusRequestRequestTypeDef(TypedDict):
    Instances: Sequence[str]
    Status: ReportStatusTypeType
    ReasonCodes: Sequence[ReportInstanceReasonCodesType]
    DryRun: NotRequired[bool]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Description: NotRequired[str]


class SlotDateTimeRangeRequestTypeDef(TypedDict):
    EarliestTime: TimestampTypeDef
    LatestTime: TimestampTypeDef


class SlotStartTimeRangeRequestTypeDef(TypedDict):
    EarliestTime: NotRequired[TimestampTypeDef]
    LatestTime: NotRequired[TimestampTypeDef]


class SpotMarketOptionsTypeDef(TypedDict):
    MaxPrice: NotRequired[str]
    SpotInstanceType: NotRequired[SpotInstanceTypeType]
    BlockDurationMinutes: NotRequired[int]
    ValidUntil: NotRequired[TimestampTypeDef]
    InstanceInterruptionBehavior: NotRequired[InstanceInterruptionBehaviorType]


class AttachVpnGatewayResultTypeDef(TypedDict):
    VpcAttachment: VpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


VpnGatewayTypeDef = TypedDict(
    "VpnGatewayTypeDef",
    {
        "AmazonSideAsn": NotRequired[int],
        "Tags": NotRequired[list[TagTypeDef]],
        "VpnGatewayId": NotRequired[str],
        "State": NotRequired[VpnStateType],
        "Type": NotRequired[Literal["ipsec.1"]],
        "AvailabilityZone": NotRequired[str],
        "VpcAttachments": NotRequired[list[VpcAttachmentTypeDef]],
    },
)


class AttachmentEnaSrdSpecificationTypeDef(TypedDict):
    EnaSrdEnabled: NotRequired[bool]
    EnaSrdUdpSpecification: NotRequired[AttachmentEnaSrdUdpSpecificationTypeDef]


class DescribeVpcAttributeResultTypeDef(TypedDict):
    EnableDnsHostnames: AttributeBooleanValueTypeDef
    EnableDnsSupport: AttributeBooleanValueTypeDef
    EnableNetworkAddressUsageMetrics: AttributeBooleanValueTypeDef
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifySubnetAttributeRequestRequestTypeDef(TypedDict):
    SubnetId: str
    AssignIpv6AddressOnCreation: NotRequired[AttributeBooleanValueTypeDef]
    MapPublicIpOnLaunch: NotRequired[AttributeBooleanValueTypeDef]
    MapCustomerOwnedIpOnLaunch: NotRequired[AttributeBooleanValueTypeDef]
    CustomerOwnedIpv4Pool: NotRequired[str]
    EnableDns64: NotRequired[AttributeBooleanValueTypeDef]
    PrivateDnsHostnameTypeOnLaunch: NotRequired[HostnameTypeType]
    EnableResourceNameDnsARecordOnLaunch: NotRequired[AttributeBooleanValueTypeDef]
    EnableResourceNameDnsAAAARecordOnLaunch: NotRequired[AttributeBooleanValueTypeDef]
    EnableLniAtDeviceIndex: NotRequired[int]
    DisableLniAtDeviceIndex: NotRequired[AttributeBooleanValueTypeDef]


class ModifyVolumeAttributeRequestRequestTypeDef(TypedDict):
    VolumeId: str
    AutoEnableIO: NotRequired[AttributeBooleanValueTypeDef]
    DryRun: NotRequired[bool]


class ModifyVolumeAttributeRequestVolumeModifyAttributeTypeDef(TypedDict):
    AutoEnableIO: NotRequired[AttributeBooleanValueTypeDef]
    DryRun: NotRequired[bool]


class ModifyVpcAttributeRequestRequestTypeDef(TypedDict):
    VpcId: str
    EnableDnsHostnames: NotRequired[AttributeBooleanValueTypeDef]
    EnableDnsSupport: NotRequired[AttributeBooleanValueTypeDef]
    EnableNetworkAddressUsageMetrics: NotRequired[AttributeBooleanValueTypeDef]


class ModifyVpcAttributeRequestVpcModifyAttributeTypeDef(TypedDict):
    EnableDnsHostnames: NotRequired[AttributeBooleanValueTypeDef]
    EnableDnsSupport: NotRequired[AttributeBooleanValueTypeDef]
    EnableNetworkAddressUsageMetrics: NotRequired[AttributeBooleanValueTypeDef]


class AttributeSummaryTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    MostFrequentValue: NotRequired[str]
    NumberOfMatchedAccounts: NotRequired[int]
    NumberOfUnmatchedAccounts: NotRequired[int]
    RegionalSummaries: NotRequired[list[RegionalSummaryTypeDef]]


class DhcpConfigurationTypeDef(TypedDict):
    Key: NotRequired[str]
    Values: NotRequired[list[AttributeValueTypeDef]]


class AuthorizationRuleTypeDef(TypedDict):
    ClientVpnEndpointId: NotRequired[str]
    Description: NotRequired[str]
    GroupId: NotRequired[str]
    AccessAll: NotRequired[bool]
    DestinationCidr: NotRequired[str]
    Status: NotRequired[ClientVpnAuthorizationRuleStatusTypeDef]


class AuthorizeClientVpnIngressResultTypeDef(TypedDict):
    Status: ClientVpnAuthorizationRuleStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeClientVpnIngressResultTypeDef(TypedDict):
    Status: ClientVpnAuthorizationRuleStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "OptInStatus": NotRequired[AvailabilityZoneOptInStatusType],
        "Messages": NotRequired[list[AvailabilityZoneMessageTypeDef]],
        "RegionName": NotRequired[str],
        "ZoneName": NotRequired[str],
        "ZoneId": NotRequired[str],
        "GroupName": NotRequired[str],
        "NetworkBorderGroup": NotRequired[str],
        "ZoneType": NotRequired[str],
        "ParentZoneName": NotRequired[str],
        "ParentZoneId": NotRequired[str],
        "State": NotRequired[AvailabilityZoneStateType],
    },
)


class AvailableCapacityTypeDef(TypedDict):
    AvailableInstanceCapacity: NotRequired[list[InstanceCapacityTypeDef]]
    AvailableVCpus: NotRequired[int]


class BlobAttributeValueTypeDef(TypedDict):
    Value: NotRequired[BlobTypeDef]


class S3StorageTypeDef(TypedDict):
    AWSAccessKeyId: NotRequired[str]
    Bucket: NotRequired[str]
    Prefix: NotRequired[str]
    UploadPolicy: NotRequired[BlobTypeDef]
    UploadPolicySignature: NotRequired[str]


class BlockDeviceMappingTypeDef(TypedDict):
    Ebs: NotRequired[EbsBlockDeviceTypeDef]
    NoDevice: NotRequired[str]
    DeviceName: NotRequired[str]
    VirtualName: NotRequired[str]


class DeprovisionIpamByoasnResultTypeDef(TypedDict):
    Byoasn: ByoasnTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamByoasnResultTypeDef(TypedDict):
    Byoasns: list[ByoasnTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ProvisionIpamByoasnResultTypeDef(TypedDict):
    Byoasn: ByoasnTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FailedCapacityReservationFleetCancellationResultTypeDef(TypedDict):
    CapacityReservationFleetId: NotRequired[str]
    CancelCapacityReservationFleetError: NotRequired[CancelCapacityReservationFleetErrorTypeDef]


class CancelSpotFleetRequestsErrorItemTypeDef(TypedDict):
    Error: NotRequired[CancelSpotFleetRequestsErrorTypeDef]
    SpotFleetRequestId: NotRequired[str]


class CancelSpotInstanceRequestsResultTypeDef(TypedDict):
    CancelledSpotInstanceRequests: list[CancelledSpotInstanceRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCapacityBlockExtensionOfferingsResultTypeDef(TypedDict):
    CapacityBlockExtensionOfferings: list[CapacityBlockExtensionOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeCapacityBlockExtensionHistoryResultTypeDef(TypedDict):
    CapacityBlockExtensions: list[CapacityBlockExtensionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PurchaseCapacityBlockExtensionResultTypeDef(TypedDict):
    CapacityBlockExtensions: list[CapacityBlockExtensionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCapacityBlockOfferingsResultTypeDef(TypedDict):
    CapacityBlockOfferings: list[CapacityBlockOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CapacityReservationBillingRequestTypeDef(TypedDict):
    CapacityReservationId: NotRequired[str]
    RequestedBy: NotRequired[str]
    UnusedReservationBillingOwnerId: NotRequired[str]
    LastUpdateTime: NotRequired[datetime]
    Status: NotRequired[CapacityReservationBillingRequestStatusType]
    StatusMessage: NotRequired[str]
    CapacityReservationInfo: NotRequired[CapacityReservationInfoTypeDef]


class CapacityReservationTypeDef(TypedDict):
    CapacityReservationId: NotRequired[str]
    OwnerId: NotRequired[str]
    CapacityReservationArn: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    InstanceType: NotRequired[str]
    InstancePlatform: NotRequired[CapacityReservationInstancePlatformType]
    AvailabilityZone: NotRequired[str]
    Tenancy: NotRequired[CapacityReservationTenancyType]
    TotalInstanceCount: NotRequired[int]
    AvailableInstanceCount: NotRequired[int]
    EbsOptimized: NotRequired[bool]
    EphemeralStorage: NotRequired[bool]
    State: NotRequired[CapacityReservationStateType]
    StartDate: NotRequired[datetime]
    EndDate: NotRequired[datetime]
    EndDateType: NotRequired[EndDateTypeType]
    InstanceMatchCriteria: NotRequired[InstanceMatchCriteriaType]
    CreateDate: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]
    OutpostArn: NotRequired[str]
    CapacityReservationFleetId: NotRequired[str]
    PlacementGroupArn: NotRequired[str]
    CapacityAllocations: NotRequired[list[CapacityAllocationTypeDef]]
    ReservationType: NotRequired[CapacityReservationTypeType]
    UnusedReservationBillingOwnerId: NotRequired[str]
    CommitmentInfo: NotRequired[CapacityReservationCommitmentInfoTypeDef]
    DeliveryPreference: NotRequired[CapacityReservationDeliveryPreferenceType]


class CapacityReservationFleetTypeDef(TypedDict):
    CapacityReservationFleetId: NotRequired[str]
    CapacityReservationFleetArn: NotRequired[str]
    State: NotRequired[CapacityReservationFleetStateType]
    TotalTargetCapacity: NotRequired[int]
    TotalFulfilledCapacity: NotRequired[float]
    Tenancy: NotRequired[Literal["default"]]
    EndDate: NotRequired[datetime]
    CreateTime: NotRequired[datetime]
    InstanceMatchCriteria: NotRequired[Literal["open"]]
    AllocationStrategy: NotRequired[str]
    InstanceTypeSpecifications: NotRequired[list[FleetCapacityReservationTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]


class CreateCapacityReservationFleetResultTypeDef(TypedDict):
    CapacityReservationFleetId: str
    State: CapacityReservationFleetStateType
    TotalTargetCapacity: int
    TotalFulfilledCapacity: float
    InstanceMatchCriteria: Literal["open"]
    AllocationStrategy: str
    CreateTime: datetime
    EndDate: datetime
    Tenancy: Literal["default"]
    FleetCapacityReservations: list[FleetCapacityReservationTypeDef]
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetGroupsForCapacityReservationResultTypeDef(TypedDict):
    CapacityReservationGroups: list[CapacityReservationGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class OnDemandOptionsRequestTypeDef(TypedDict):
    AllocationStrategy: NotRequired[FleetOnDemandAllocationStrategyType]
    CapacityReservationOptions: NotRequired[CapacityReservationOptionsRequestTypeDef]
    SingleInstanceType: NotRequired[bool]
    SingleAvailabilityZone: NotRequired[bool]
    MinTargetCapacity: NotRequired[int]
    MaxTotalPrice: NotRequired[str]


class OnDemandOptionsTypeDef(TypedDict):
    AllocationStrategy: NotRequired[FleetOnDemandAllocationStrategyType]
    CapacityReservationOptions: NotRequired[CapacityReservationOptionsTypeDef]
    SingleInstanceType: NotRequired[bool]
    SingleAvailabilityZone: NotRequired[bool]
    MinTargetCapacity: NotRequired[int]
    MaxTotalPrice: NotRequired[str]


class CapacityReservationSpecificationResponseTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[CapacityReservationPreferenceType]
    CapacityReservationTarget: NotRequired[CapacityReservationTargetResponseTypeDef]


class LaunchTemplateCapacityReservationSpecificationResponseTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[CapacityReservationPreferenceType]
    CapacityReservationTarget: NotRequired[CapacityReservationTargetResponseTypeDef]


class CapacityReservationSpecificationTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[CapacityReservationPreferenceType]
    CapacityReservationTarget: NotRequired[CapacityReservationTargetTypeDef]


class LaunchTemplateCapacityReservationSpecificationRequestTypeDef(TypedDict):
    CapacityReservationPreference: NotRequired[CapacityReservationPreferenceType]
    CapacityReservationTarget: NotRequired[CapacityReservationTargetTypeDef]


class DescribeVpcClassicLinkDnsSupportResultTypeDef(TypedDict):
    Vpcs: list[ClassicLinkDnsSupportTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClassicLinkInstanceTypeDef(TypedDict):
    Groups: NotRequired[list[GroupIdentifierTypeDef]]
    InstanceId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    VpcId: NotRequired[str]


class ClassicLoadBalancersConfigOutputTypeDef(TypedDict):
    ClassicLoadBalancers: NotRequired[list[ClassicLoadBalancerTypeDef]]


class ClassicLoadBalancersConfigTypeDef(TypedDict):
    ClassicLoadBalancers: NotRequired[Sequence[ClassicLoadBalancerTypeDef]]


class ExportClientVpnClientCertificateRevocationListResultTypeDef(TypedDict):
    CertificateRevocationList: str
    Status: ClientCertificateRevocationListStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ClientConnectResponseOptionsTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    LambdaFunctionArn: NotRequired[str]
    Status: NotRequired[ClientVpnEndpointAttributeStatusTypeDef]


ClientVpnAuthenticationRequestTypeDef = TypedDict(
    "ClientVpnAuthenticationRequestTypeDef",
    {
        "Type": NotRequired[ClientVpnAuthenticationTypeType],
        "ActiveDirectory": NotRequired[DirectoryServiceAuthenticationRequestTypeDef],
        "MutualAuthentication": NotRequired[CertificateAuthenticationRequestTypeDef],
        "FederatedAuthentication": NotRequired[FederatedAuthenticationRequestTypeDef],
    },
)
ClientVpnAuthenticationTypeDef = TypedDict(
    "ClientVpnAuthenticationTypeDef",
    {
        "Type": NotRequired[ClientVpnAuthenticationTypeType],
        "ActiveDirectory": NotRequired[DirectoryServiceAuthenticationTypeDef],
        "MutualAuthentication": NotRequired[CertificateAuthenticationTypeDef],
        "FederatedAuthentication": NotRequired[FederatedAuthenticationTypeDef],
    },
)


class ClientVpnConnectionTypeDef(TypedDict):
    ClientVpnEndpointId: NotRequired[str]
    Timestamp: NotRequired[str]
    ConnectionId: NotRequired[str]
    Username: NotRequired[str]
    ConnectionEstablishedTime: NotRequired[str]
    IngressBytes: NotRequired[str]
    EgressBytes: NotRequired[str]
    IngressPackets: NotRequired[str]
    EgressPackets: NotRequired[str]
    ClientIp: NotRequired[str]
    CommonName: NotRequired[str]
    Status: NotRequired[ClientVpnConnectionStatusTypeDef]
    ConnectionEndTime: NotRequired[str]
    PostureComplianceStatuses: NotRequired[list[str]]


class TerminateConnectionStatusTypeDef(TypedDict):
    ConnectionId: NotRequired[str]
    PreviousStatus: NotRequired[ClientVpnConnectionStatusTypeDef]
    CurrentStatus: NotRequired[ClientVpnConnectionStatusTypeDef]


class CreateClientVpnEndpointResultTypeDef(TypedDict):
    ClientVpnEndpointId: str
    Status: ClientVpnEndpointStatusTypeDef
    DnsName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClientVpnEndpointResultTypeDef(TypedDict):
    Status: ClientVpnEndpointStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ClientVpnRouteTypeDef = TypedDict(
    "ClientVpnRouteTypeDef",
    {
        "ClientVpnEndpointId": NotRequired[str],
        "DestinationCidr": NotRequired[str],
        "TargetSubnet": NotRequired[str],
        "Type": NotRequired[str],
        "Origin": NotRequired[str],
        "Status": NotRequired[ClientVpnRouteStatusTypeDef],
        "Description": NotRequired[str],
    },
)


class CreateClientVpnRouteResultTypeDef(TypedDict):
    Status: ClientVpnRouteStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClientVpnRouteResultTypeDef(TypedDict):
    Status: ClientVpnRouteStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VpnTunnelLogOptionsSpecificationTypeDef(TypedDict):
    CloudWatchLogOptions: NotRequired[CloudWatchLogOptionsSpecificationTypeDef]


class VpnTunnelLogOptionsTypeDef(TypedDict):
    CloudWatchLogOptions: NotRequired[CloudWatchLogOptionsTypeDef]


class GetCoipPoolUsageResultTypeDef(TypedDict):
    CoipPoolId: str
    CoipAddressUsages: list[CoipAddressUsageTypeDef]
    LocalGatewayRouteTableId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCoipCidrResultTypeDef(TypedDict):
    CoipCidr: CoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCoipCidrResultTypeDef(TypedDict):
    CoipCidr: CoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcEndpointConnectionNotificationResultTypeDef(TypedDict):
    ConnectionNotification: ConnectionNotificationTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcEndpointConnectionNotificationsResultTypeDef(TypedDict):
    ConnectionNotificationSet: list[ConnectionNotificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CpuPerformanceFactorOutputTypeDef(TypedDict):
    References: NotRequired[list[PerformanceFactorReferenceTypeDef]]


class CpuPerformanceFactorTypeDef(TypedDict):
    References: NotRequired[Sequence[PerformanceFactorReferenceTypeDef]]


class CpuPerformanceFactorRequestTypeDef(TypedDict):
    References: NotRequired[Sequence[PerformanceFactorReferenceRequestTypeDef]]


class ModifyInstanceEventWindowRequestRequestTypeDef(TypedDict):
    InstanceEventWindowId: str
    DryRun: NotRequired[bool]
    Name: NotRequired[str]
    TimeRanges: NotRequired[Sequence[InstanceEventWindowTimeRangeRequestTypeDef]]
    CronExpression: NotRequired[str]


class ModifyIpamPoolRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    AutoImport: NotRequired[bool]
    AllocationMinNetmaskLength: NotRequired[int]
    AllocationMaxNetmaskLength: NotRequired[int]
    AllocationDefaultNetmaskLength: NotRequired[int]
    ClearAllocationDefaultNetmaskLength: NotRequired[bool]
    AddAllocationResourceTags: NotRequired[Sequence[RequestIpamResourceTagTypeDef]]
    RemoveAllocationResourceTags: NotRequired[Sequence[RequestIpamResourceTagTypeDef]]


class CreateLocalGatewayRouteResultTypeDef(TypedDict):
    Route: LocalGatewayRouteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLocalGatewayRouteResultTypeDef(TypedDict):
    Route: LocalGatewayRouteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyLocalGatewayRouteResultTypeDef(TypedDict):
    Route: LocalGatewayRouteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchLocalGatewayRoutesResultTypeDef(TypedDict):
    Routes: list[LocalGatewayRouteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef = TypedDict(
    "CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef",
    {
        "RuleNumber": int,
        "Protocol": str,
        "RuleAction": RuleActionType,
        "Egress": bool,
        "DryRun": NotRequired[bool],
        "CidrBlock": NotRequired[str],
        "Ipv6CidrBlock": NotRequired[str],
        "IcmpTypeCode": NotRequired[IcmpTypeCodeTypeDef],
        "PortRange": NotRequired[PortRangeTypeDef],
    },
)
CreateNetworkAclEntryRequestRequestTypeDef = TypedDict(
    "CreateNetworkAclEntryRequestRequestTypeDef",
    {
        "NetworkAclId": str,
        "RuleNumber": int,
        "Protocol": str,
        "RuleAction": RuleActionType,
        "Egress": bool,
        "DryRun": NotRequired[bool],
        "CidrBlock": NotRequired[str],
        "Ipv6CidrBlock": NotRequired[str],
        "IcmpTypeCode": NotRequired[IcmpTypeCodeTypeDef],
        "PortRange": NotRequired[PortRangeTypeDef],
    },
)
NetworkAclEntryTypeDef = TypedDict(
    "NetworkAclEntryTypeDef",
    {
        "CidrBlock": NotRequired[str],
        "Egress": NotRequired[bool],
        "IcmpTypeCode": NotRequired[IcmpTypeCodeTypeDef],
        "Ipv6CidrBlock": NotRequired[str],
        "PortRange": NotRequired[PortRangeTypeDef],
        "Protocol": NotRequired[str],
        "RuleAction": NotRequired[RuleActionType],
        "RuleNumber": NotRequired[int],
    },
)
ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef = TypedDict(
    "ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef",
    {
        "RuleNumber": int,
        "Protocol": str,
        "RuleAction": RuleActionType,
        "Egress": bool,
        "DryRun": NotRequired[bool],
        "CidrBlock": NotRequired[str],
        "Ipv6CidrBlock": NotRequired[str],
        "IcmpTypeCode": NotRequired[IcmpTypeCodeTypeDef],
        "PortRange": NotRequired[PortRangeTypeDef],
    },
)
ReplaceNetworkAclEntryRequestRequestTypeDef = TypedDict(
    "ReplaceNetworkAclEntryRequestRequestTypeDef",
    {
        "NetworkAclId": str,
        "RuleNumber": int,
        "Protocol": str,
        "RuleAction": RuleActionType,
        "Egress": bool,
        "DryRun": NotRequired[bool],
        "CidrBlock": NotRequired[str],
        "Ipv6CidrBlock": NotRequired[str],
        "IcmpTypeCode": NotRequired[IcmpTypeCodeTypeDef],
        "PortRange": NotRequired[PortRangeTypeDef],
    },
)


class CreateReservedInstancesListingRequestRequestTypeDef(TypedDict):
    ReservedInstancesId: str
    InstanceCount: int
    PriceSchedules: Sequence[PriceScheduleSpecificationTypeDef]
    ClientToken: str


class CreateStoreImageTaskRequestRequestTypeDef(TypedDict):
    ImageId: str
    Bucket: str
    S3ObjectTags: NotRequired[Sequence[S3ObjectTagTypeDef]]
    DryRun: NotRequired[bool]


ModifyTrafficMirrorFilterRuleRequestRequestTypeDef = TypedDict(
    "ModifyTrafficMirrorFilterRuleRequestRequestTypeDef",
    {
        "TrafficMirrorFilterRuleId": str,
        "TrafficDirection": NotRequired[TrafficDirectionType],
        "RuleNumber": NotRequired[int],
        "RuleAction": NotRequired[TrafficMirrorRuleActionType],
        "DestinationPortRange": NotRequired[TrafficMirrorPortRangeRequestTypeDef],
        "SourcePortRange": NotRequired[TrafficMirrorPortRangeRequestTypeDef],
        "Protocol": NotRequired[int],
        "DestinationCidrBlock": NotRequired[str],
        "SourceCidrBlock": NotRequired[str],
        "Description": NotRequired[str],
        "RemoveFields": NotRequired[Sequence[TrafficMirrorFilterRuleFieldType]],
        "DryRun": NotRequired[bool],
    },
)
CreateVerifiedAccessEndpointCidrOptionsTypeDef = TypedDict(
    "CreateVerifiedAccessEndpointCidrOptionsTypeDef",
    {
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "SubnetIds": NotRequired[Sequence[str]],
        "Cidr": NotRequired[str],
        "PortRanges": NotRequired[Sequence[CreateVerifiedAccessEndpointPortRangeTypeDef]],
    },
)
CreateVerifiedAccessEndpointEniOptionsTypeDef = TypedDict(
    "CreateVerifiedAccessEndpointEniOptionsTypeDef",
    {
        "NetworkInterfaceId": NotRequired[str],
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "PortRanges": NotRequired[Sequence[CreateVerifiedAccessEndpointPortRangeTypeDef]],
    },
)
CreateVerifiedAccessEndpointLoadBalancerOptionsTypeDef = TypedDict(
    "CreateVerifiedAccessEndpointLoadBalancerOptionsTypeDef",
    {
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "LoadBalancerArn": NotRequired[str],
        "SubnetIds": NotRequired[Sequence[str]],
        "PortRanges": NotRequired[Sequence[CreateVerifiedAccessEndpointPortRangeTypeDef]],
    },
)


class ModifyVerifiedAccessEndpointPolicyRequestRequestTypeDef(TypedDict):
    VerifiedAccessEndpointId: str
    PolicyEnabled: NotRequired[bool]
    PolicyDocument: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationRequestTypeDef]


class ModifyVerifiedAccessGroupPolicyRequestRequestTypeDef(TypedDict):
    VerifiedAccessGroupId: str
    PolicyEnabled: NotRequired[bool]
    PolicyDocument: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationRequestTypeDef]


class CreateVolumePermissionModificationsTypeDef(TypedDict):
    Add: NotRequired[Sequence[CreateVolumePermissionTypeDef]]
    Remove: NotRequired[Sequence[CreateVolumePermissionTypeDef]]


class ModifyVpcEndpointRequestRequestTypeDef(TypedDict):
    VpcEndpointId: str
    DryRun: NotRequired[bool]
    ResetPolicy: NotRequired[bool]
    PolicyDocument: NotRequired[str]
    AddRouteTableIds: NotRequired[Sequence[str]]
    RemoveRouteTableIds: NotRequired[Sequence[str]]
    AddSubnetIds: NotRequired[Sequence[str]]
    RemoveSubnetIds: NotRequired[Sequence[str]]
    AddSecurityGroupIds: NotRequired[Sequence[str]]
    RemoveSecurityGroupIds: NotRequired[Sequence[str]]
    IpAddressType: NotRequired[IpAddressTypeType]
    DnsOptions: NotRequired[DnsOptionsSpecificationTypeDef]
    PrivateDnsEnabled: NotRequired[bool]
    SubnetConfigurations: NotRequired[Sequence[SubnetConfigurationTypeDef]]


class GetAwsNetworkPerformanceDataRequestRequestTypeDef(TypedDict):
    DataQueries: NotRequired[Sequence[DataQueryTypeDef]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DataResponseTypeDef(TypedDict):
    Id: NotRequired[str]
    Source: NotRequired[str]
    Destination: NotRequired[str]
    Metric: NotRequired[Literal["aggregate-latency"]]
    Statistic: NotRequired[Literal["p50"]]
    Period: NotRequired[PeriodTypeType]
    MetricPoints: NotRequired[list[MetricPointTypeDef]]


class DeleteFleetErrorItemTypeDef(TypedDict):
    Error: NotRequired[DeleteFleetErrorTypeDef]
    FleetId: NotRequired[str]


class DeleteInstanceEventWindowResultTypeDef(TypedDict):
    InstanceEventWindowState: InstanceEventWindowStateChangeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLaunchTemplateVersionsResponseErrorItemTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    VersionNumber: NotRequired[int]
    ResponseError: NotRequired[ResponseErrorTypeDef]


class FailedQueuedPurchaseDeletionTypeDef(TypedDict):
    Error: NotRequired[DeleteQueuedReservedInstancesErrorTypeDef]
    ReservedInstancesId: NotRequired[str]


class DeregisterInstanceEventNotificationAttributesRequestRequestTypeDef(TypedDict):
    InstanceTagAttribute: DeregisterInstanceTagAttributeRequestTypeDef
    DryRun: NotRequired[bool]


class DeregisterInstanceEventNotificationAttributesResultTypeDef(TypedDict):
    InstanceTagAttribute: InstanceTagNotificationAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInstanceEventNotificationAttributesResultTypeDef(TypedDict):
    InstanceTagAttribute: InstanceTagNotificationAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterInstanceEventNotificationAttributesResultTypeDef(TypedDict):
    InstanceTagAttribute: InstanceTagNotificationAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterTransitGatewayMulticastGroupMembersResultTypeDef(TypedDict):
    DeregisteredMulticastGroupMembers: TransitGatewayMulticastDeregisteredGroupMembersTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeregisterTransitGatewayMulticastGroupSourcesResultTypeDef(TypedDict):
    DeregisteredMulticastGroupSources: TransitGatewayMulticastDeregisteredGroupSourcesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAddressTransfersRequestPaginateTypeDef(TypedDict):
    AllocationIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAddressesAttributeRequestPaginateTypeDef(TypedDict):
    AllocationIds: NotRequired[Sequence[str]]
    Attribute: NotRequired[Literal["domain-name"]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeByoipCidrsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCapacityBlockExtensionOfferingsRequestPaginateTypeDef(TypedDict):
    CapacityBlockExtensionDurationHours: int
    CapacityReservationId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCapacityBlockOfferingsRequestPaginateTypeDef(TypedDict):
    CapacityDurationHours: int
    DryRun: NotRequired[bool]
    InstanceType: NotRequired[str]
    InstanceCount: NotRequired[int]
    StartDateRange: NotRequired[TimestampTypeDef]
    EndDateRange: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePrincipalIdFormatRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Resources: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSpotFleetInstancesRequestPaginateTypeDef(TypedDict):
    SpotFleetRequestId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSpotFleetRequestsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    SpotFleetRequestIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeStaleSecurityGroupsRequestPaginateTypeDef(TypedDict):
    VpcId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcClassicLinkDnsSupportRequestPaginateTypeDef(TypedDict):
    VpcIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAssociatedIpv6PoolCidrsRequestPaginateTypeDef(TypedDict):
    PoolId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetAwsNetworkPerformanceDataRequestPaginateTypeDef(TypedDict):
    DataQueries: NotRequired[Sequence[DataQueryTypeDef]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetGroupsForCapacityReservationRequestPaginateTypeDef(TypedDict):
    CapacityReservationId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetIpamAddressHistoryRequestPaginateTypeDef(TypedDict):
    Cidr: str
    IpamScopeId: str
    DryRun: NotRequired[bool]
    VpcId: NotRequired[str]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetManagedPrefixListAssociationsRequestPaginateTypeDef(TypedDict):
    PrefixListId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetManagedPrefixListEntriesRequestPaginateTypeDef(TypedDict):
    PrefixListId: str
    DryRun: NotRequired[bool]
    TargetVersion: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetNetworkInsightsAccessScopeAnalysisFindingsRequestPaginateTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: str
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetVpnConnectionDeviceTypesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListImagesInRecycleBinRequestPaginateTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSnapshotsInRecycleBinRequestPaginateTypeDef(TypedDict):
    SnapshotIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAddressesRequestRequestTypeDef(TypedDict):
    PublicIps: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    AllocationIds: NotRequired[Sequence[str]]


class DescribeAvailabilityZonesRequestRequestTypeDef(TypedDict):
    ZoneNames: NotRequired[Sequence[str]]
    ZoneIds: NotRequired[Sequence[str]]
    AllAvailabilityZones: NotRequired[bool]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeAwsNetworkPerformanceMetricSubscriptionsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAwsNetworkPerformanceMetricSubscriptionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeBundleTasksRequestRequestTypeDef(TypedDict):
    BundleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeCapacityBlockExtensionHistoryRequestPaginateTypeDef(TypedDict):
    CapacityReservationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCapacityBlockExtensionHistoryRequestRequestTypeDef(TypedDict):
    CapacityReservationIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeCapacityReservationBillingRequestsRequestPaginateTypeDef(TypedDict):
    Role: CallerRoleType
    CapacityReservationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCapacityReservationBillingRequestsRequestRequestTypeDef(TypedDict):
    Role: CallerRoleType
    CapacityReservationIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeCapacityReservationFleetsRequestPaginateTypeDef(TypedDict):
    CapacityReservationFleetIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCapacityReservationFleetsRequestRequestTypeDef(TypedDict):
    CapacityReservationFleetIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeCapacityReservationsRequestPaginateTypeDef(TypedDict):
    CapacityReservationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCapacityReservationsRequestRequestTypeDef(TypedDict):
    CapacityReservationIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeCarrierGatewaysRequestPaginateTypeDef(TypedDict):
    CarrierGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCarrierGatewaysRequestRequestTypeDef(TypedDict):
    CarrierGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeClassicLinkInstancesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClassicLinkInstancesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeClientVpnAuthorizationRulesRequestPaginateTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClientVpnAuthorizationRulesRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]


class DescribeClientVpnConnectionsRequestPaginateTypeDef(TypedDict):
    ClientVpnEndpointId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClientVpnConnectionsRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class DescribeClientVpnEndpointsRequestPaginateTypeDef(TypedDict):
    ClientVpnEndpointIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClientVpnEndpointsRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeClientVpnRoutesRequestPaginateTypeDef(TypedDict):
    ClientVpnEndpointId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClientVpnRoutesRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeClientVpnTargetNetworksRequestPaginateTypeDef(TypedDict):
    ClientVpnEndpointId: str
    AssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeClientVpnTargetNetworksRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    AssociationIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeCoipPoolsRequestPaginateTypeDef(TypedDict):
    PoolIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeCoipPoolsRequestRequestTypeDef(TypedDict):
    PoolIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeCustomerGatewaysRequestRequestTypeDef(TypedDict):
    CustomerGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeDhcpOptionsRequestPaginateTypeDef(TypedDict):
    DhcpOptionsIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDhcpOptionsRequestRequestTypeDef(TypedDict):
    DhcpOptionsIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeEgressOnlyInternetGatewaysRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    EgressOnlyInternetGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEgressOnlyInternetGatewaysRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    EgressOnlyInternetGatewayIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeElasticGpusRequestRequestTypeDef(TypedDict):
    ElasticGpuIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeExportImageTasksRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ExportImageTaskIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeExportImageTasksRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ExportImageTaskIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeExportTasksRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ExportTaskIds: NotRequired[Sequence[str]]


class DescribeFastLaunchImagesRequestPaginateTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFastLaunchImagesRequestRequestTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeFastSnapshotRestoresRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFastSnapshotRestoresRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeFleetInstancesRequestRequestTypeDef(TypedDict):
    FleetId: str
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeFleetsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    FleetIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFleetsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    FleetIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeFlowLogsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    FlowLogIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFlowLogsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    FlowLogIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeFpgaImagesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    FpgaImageIds: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFpgaImagesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    FpgaImageIds: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeHostReservationOfferingsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxDuration: NotRequired[int]
    MinDuration: NotRequired[int]
    OfferingId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeHostReservationOfferingsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxDuration: NotRequired[int]
    MaxResults: NotRequired[int]
    MinDuration: NotRequired[int]
    NextToken: NotRequired[str]
    OfferingId: NotRequired[str]


class DescribeHostReservationsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    HostReservationIdSet: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeHostReservationsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    HostReservationIdSet: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeHostsRequestPaginateTypeDef(TypedDict):
    HostIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeHostsRequestRequestTypeDef(TypedDict):
    HostIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeIamInstanceProfileAssociationsRequestPaginateTypeDef(TypedDict):
    AssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIamInstanceProfileAssociationsRequestRequestTypeDef(TypedDict):
    AssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeImagesRequestPaginateTypeDef(TypedDict):
    ExecutableUsers: NotRequired[Sequence[str]]
    ImageIds: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    IncludeDeprecated: NotRequired[bool]
    IncludeDisabled: NotRequired[bool]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeImagesRequestRequestTypeDef(TypedDict):
    ExecutableUsers: NotRequired[Sequence[str]]
    ImageIds: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    IncludeDeprecated: NotRequired[bool]
    IncludeDisabled: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeImportImageTasksRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ImportTaskIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeImportImageTasksRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ImportTaskIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeImportSnapshotTasksRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ImportTaskIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeImportSnapshotTasksRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ImportTaskIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceConnectEndpointsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceConnectEndpointIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceConnectEndpointsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceConnectEndpointIds: NotRequired[Sequence[str]]


class DescribeInstanceCreditSpecificationsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceCreditSpecificationsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceEventWindowsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceEventWindowIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceEventWindowsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceEventWindowIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceImageMetadataRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceImageMetadataRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeInstanceStatusRequestPaginateTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IncludeAllInstances: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceStatusRequestRequestTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IncludeAllInstances: NotRequired[bool]


class DescribeInstanceTopologyRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceIds: NotRequired[Sequence[str]]
    GroupNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceTopologyRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    InstanceIds: NotRequired[Sequence[str]]
    GroupNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeInstanceTypeOfferingsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LocationType: NotRequired[LocationTypeType]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceTypeOfferingsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LocationType: NotRequired[LocationTypeType]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceTypesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceTypes: NotRequired[Sequence[InstanceTypeType]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstanceTypesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InstanceTypes: NotRequired[Sequence[InstanceTypeType]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstancesRequestPaginateTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInstancesRequestRequestTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeInternetGatewaysRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    InternetGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeInternetGatewaysRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    InternetGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeIpamExternalResourceVerificationTokensRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    IpamExternalResourceVerificationTokenIds: NotRequired[Sequence[str]]


class DescribeIpamPoolsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IpamPoolIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIpamPoolsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IpamPoolIds: NotRequired[Sequence[str]]


class DescribeIpamResourceDiscoveriesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    IpamResourceDiscoveryIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIpamResourceDiscoveriesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    IpamResourceDiscoveryIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeIpamResourceDiscoveryAssociationsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    IpamResourceDiscoveryAssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIpamResourceDiscoveryAssociationsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    IpamResourceDiscoveryAssociationIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeIpamScopesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IpamScopeIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIpamScopesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IpamScopeIds: NotRequired[Sequence[str]]


class DescribeIpamsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IpamIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIpamsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IpamIds: NotRequired[Sequence[str]]


class DescribeIpv6PoolsRequestPaginateTypeDef(TypedDict):
    PoolIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeIpv6PoolsRequestRequestTypeDef(TypedDict):
    PoolIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeKeyPairsRequestRequestTypeDef(TypedDict):
    KeyNames: NotRequired[Sequence[str]]
    KeyPairIds: NotRequired[Sequence[str]]
    IncludePublicKey: NotRequired[bool]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeLaunchTemplateVersionsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Versions: NotRequired[Sequence[str]]
    MinVersion: NotRequired[str]
    MaxVersion: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ResolveAlias: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLaunchTemplateVersionsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    Versions: NotRequired[Sequence[str]]
    MinVersion: NotRequired[str]
    MaxVersion: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ResolveAlias: NotRequired[bool]


class DescribeLaunchTemplatesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LaunchTemplateIds: NotRequired[Sequence[str]]
    LaunchTemplateNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLaunchTemplatesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    LaunchTemplateIds: NotRequired[Sequence[str]]
    LaunchTemplateNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestPaginateTypeDef(
    TypedDict
):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsRequestRequestTypeDef(
    TypedDict
):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeLocalGatewayRouteTableVpcAssociationsRequestPaginateTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLocalGatewayRouteTableVpcAssociationsRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeLocalGatewayRouteTablesRequestPaginateTypeDef(TypedDict):
    LocalGatewayRouteTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLocalGatewayRouteTablesRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeLocalGatewayVirtualInterfaceGroupsRequestPaginateTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceGroupIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLocalGatewayVirtualInterfaceGroupsRequestRequestTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceGroupIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeLocalGatewayVirtualInterfacesRequestPaginateTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLocalGatewayVirtualInterfacesRequestRequestTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeLocalGatewaysRequestPaginateTypeDef(TypedDict):
    LocalGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeLocalGatewaysRequestRequestTypeDef(TypedDict):
    LocalGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeLockedSnapshotsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    SnapshotIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class DescribeMacHostsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    HostIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMacHostsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    HostIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeManagedPrefixListsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PrefixListIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeManagedPrefixListsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PrefixListIds: NotRequired[Sequence[str]]


class DescribeMovingAddressesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    PublicIps: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeMovingAddressesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    PublicIps: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]


class DescribeNatGatewaysRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NatGatewayIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNatGatewaysRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NatGatewayIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]


class DescribeNetworkAclsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    NetworkAclIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkAclsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NetworkAclIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeNetworkInsightsAccessScopeAnalysesRequestPaginateTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisIds: NotRequired[Sequence[str]]
    NetworkInsightsAccessScopeId: NotRequired[str]
    AnalysisStartTimeBegin: NotRequired[TimestampTypeDef]
    AnalysisStartTimeEnd: NotRequired[TimestampTypeDef]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkInsightsAccessScopeAnalysesRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisIds: NotRequired[Sequence[str]]
    NetworkInsightsAccessScopeId: NotRequired[str]
    AnalysisStartTimeBegin: NotRequired[TimestampTypeDef]
    AnalysisStartTimeEnd: NotRequired[TimestampTypeDef]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]


class DescribeNetworkInsightsAccessScopesRequestPaginateTypeDef(TypedDict):
    NetworkInsightsAccessScopeIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkInsightsAccessScopesRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]


class DescribeNetworkInsightsAnalysesRequestPaginateTypeDef(TypedDict):
    NetworkInsightsAnalysisIds: NotRequired[Sequence[str]]
    NetworkInsightsPathId: NotRequired[str]
    AnalysisStartTime: NotRequired[TimestampTypeDef]
    AnalysisEndTime: NotRequired[TimestampTypeDef]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkInsightsAnalysesRequestRequestTypeDef(TypedDict):
    NetworkInsightsAnalysisIds: NotRequired[Sequence[str]]
    NetworkInsightsPathId: NotRequired[str]
    AnalysisStartTime: NotRequired[TimestampTypeDef]
    AnalysisEndTime: NotRequired[TimestampTypeDef]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]


class DescribeNetworkInsightsPathsRequestPaginateTypeDef(TypedDict):
    NetworkInsightsPathIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkInsightsPathsRequestRequestTypeDef(TypedDict):
    NetworkInsightsPathIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]


class DescribeNetworkInterfacePermissionsRequestPaginateTypeDef(TypedDict):
    NetworkInterfacePermissionIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkInterfacePermissionsRequestRequestTypeDef(TypedDict):
    NetworkInterfacePermissionIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeNetworkInterfacesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    NetworkInterfaceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeNetworkInterfacesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NetworkInterfaceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribePlacementGroupsRequestRequestTypeDef(TypedDict):
    GroupIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    GroupNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribePrefixListsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PrefixListIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePrefixListsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    PrefixListIds: NotRequired[Sequence[str]]


class DescribePublicIpv4PoolsRequestPaginateTypeDef(TypedDict):
    PoolIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribePublicIpv4PoolsRequestRequestTypeDef(TypedDict):
    PoolIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeRegionsRequestRequestTypeDef(TypedDict):
    RegionNames: NotRequired[Sequence[str]]
    AllRegions: NotRequired[bool]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeReplaceRootVolumeTasksRequestPaginateTypeDef(TypedDict):
    ReplaceRootVolumeTaskIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplaceRootVolumeTasksRequestRequestTypeDef(TypedDict):
    ReplaceRootVolumeTaskIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeReservedInstancesListingsRequestRequestTypeDef(TypedDict):
    ReservedInstancesId: NotRequired[str]
    ReservedInstancesListingId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeReservedInstancesModificationsRequestPaginateTypeDef(TypedDict):
    ReservedInstancesModificationIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedInstancesModificationsRequestRequestTypeDef(TypedDict):
    ReservedInstancesModificationIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeReservedInstancesOfferingsRequestPaginateTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    IncludeMarketplace: NotRequired[bool]
    InstanceType: NotRequired[InstanceTypeType]
    MaxDuration: NotRequired[int]
    MaxInstanceCount: NotRequired[int]
    MinDuration: NotRequired[int]
    OfferingClass: NotRequired[OfferingClassTypeType]
    ProductDescription: NotRequired[RIProductDescriptionType]
    ReservedInstancesOfferingIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceTenancy: NotRequired[TenancyType]
    OfferingType: NotRequired[OfferingTypeValuesType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReservedInstancesOfferingsRequestRequestTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    IncludeMarketplace: NotRequired[bool]
    InstanceType: NotRequired[InstanceTypeType]
    MaxDuration: NotRequired[int]
    MaxInstanceCount: NotRequired[int]
    MinDuration: NotRequired[int]
    OfferingClass: NotRequired[OfferingClassTypeType]
    ProductDescription: NotRequired[RIProductDescriptionType]
    ReservedInstancesOfferingIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    InstanceTenancy: NotRequired[TenancyType]
    OfferingType: NotRequired[OfferingTypeValuesType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeReservedInstancesRequestRequestTypeDef(TypedDict):
    OfferingClass: NotRequired[OfferingClassTypeType]
    ReservedInstancesIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    OfferingType: NotRequired[OfferingTypeValuesType]


class DescribeRouteTablesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    RouteTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeRouteTablesRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    RouteTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeSecurityGroupRulesRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SecurityGroupRuleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSecurityGroupRulesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SecurityGroupRuleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeSecurityGroupVpcAssociationsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSecurityGroupVpcAssociationsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class DescribeSecurityGroupsRequestPaginateTypeDef(TypedDict):
    GroupIds: NotRequired[Sequence[str]]
    GroupNames: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSecurityGroupsRequestRequestTypeDef(TypedDict):
    GroupIds: NotRequired[Sequence[str]]
    GroupNames: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeSnapshotTierStatusRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSnapshotTierStatusRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeSnapshotsRequestPaginateTypeDef(TypedDict):
    OwnerIds: NotRequired[Sequence[str]]
    RestorableByUserIds: NotRequired[Sequence[str]]
    SnapshotIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSnapshotsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    OwnerIds: NotRequired[Sequence[str]]
    RestorableByUserIds: NotRequired[Sequence[str]]
    SnapshotIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeSpotInstanceRequestsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    SpotInstanceRequestIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSpotInstanceRequestsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    SpotInstanceRequestIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeSpotPriceHistoryRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    InstanceTypes: NotRequired[Sequence[InstanceTypeType]]
    ProductDescriptions: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    AvailabilityZone: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSpotPriceHistoryRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    InstanceTypes: NotRequired[Sequence[InstanceTypeType]]
    ProductDescriptions: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    AvailabilityZone: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeStoreImageTasksRequestPaginateTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeStoreImageTasksRequestRequestTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeSubnetsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SubnetIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSubnetsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SubnetIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class DescribeTagsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTagsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeTrafficMirrorFilterRulesRequestRequestTypeDef(TypedDict):
    TrafficMirrorFilterRuleIds: NotRequired[Sequence[str]]
    TrafficMirrorFilterId: NotRequired[str]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeTrafficMirrorFiltersRequestPaginateTypeDef(TypedDict):
    TrafficMirrorFilterIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTrafficMirrorFiltersRequestRequestTypeDef(TypedDict):
    TrafficMirrorFilterIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeTrafficMirrorSessionsRequestPaginateTypeDef(TypedDict):
    TrafficMirrorSessionIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTrafficMirrorSessionsRequestRequestTypeDef(TypedDict):
    TrafficMirrorSessionIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeTrafficMirrorTargetsRequestPaginateTypeDef(TypedDict):
    TrafficMirrorTargetIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTrafficMirrorTargetsRequestRequestTypeDef(TypedDict):
    TrafficMirrorTargetIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeTransitGatewayAttachmentsRequestPaginateTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayAttachmentsRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayConnectPeersRequestPaginateTypeDef(TypedDict):
    TransitGatewayConnectPeerIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayConnectPeersRequestRequestTypeDef(TypedDict):
    TransitGatewayConnectPeerIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayConnectsRequestPaginateTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayConnectsRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayMulticastDomainsRequestPaginateTypeDef(TypedDict):
    TransitGatewayMulticastDomainIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayMulticastDomainsRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayPeeringAttachmentsRequestPaginateTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayPeeringAttachmentsRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayPolicyTablesRequestPaginateTypeDef(TypedDict):
    TransitGatewayPolicyTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayPolicyTablesRequestRequestTypeDef(TypedDict):
    TransitGatewayPolicyTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayRouteTableAnnouncementsRequestPaginateTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncementIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayRouteTableAnnouncementsRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncementIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayRouteTablesRequestPaginateTypeDef(TypedDict):
    TransitGatewayRouteTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayRouteTablesRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewayVpcAttachmentsRequestPaginateTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewayVpcAttachmentsRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTransitGatewaysRequestPaginateTypeDef(TypedDict):
    TransitGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTransitGatewaysRequestRequestTypeDef(TypedDict):
    TransitGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class DescribeTrunkInterfaceAssociationsRequestPaginateTypeDef(TypedDict):
    AssociationIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTrunkInterfaceAssociationsRequestRequestTypeDef(TypedDict):
    AssociationIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeVerifiedAccessEndpointsRequestPaginateTypeDef(TypedDict):
    VerifiedAccessEndpointIds: NotRequired[Sequence[str]]
    VerifiedAccessInstanceId: NotRequired[str]
    VerifiedAccessGroupId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVerifiedAccessEndpointsRequestRequestTypeDef(TypedDict):
    VerifiedAccessEndpointIds: NotRequired[Sequence[str]]
    VerifiedAccessInstanceId: NotRequired[str]
    VerifiedAccessGroupId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeVerifiedAccessGroupsRequestPaginateTypeDef(TypedDict):
    VerifiedAccessGroupIds: NotRequired[Sequence[str]]
    VerifiedAccessInstanceId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVerifiedAccessGroupsRequestRequestTypeDef(TypedDict):
    VerifiedAccessGroupIds: NotRequired[Sequence[str]]
    VerifiedAccessInstanceId: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeVerifiedAccessInstanceLoggingConfigurationsRequestPaginateTypeDef(TypedDict):
    VerifiedAccessInstanceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVerifiedAccessInstanceLoggingConfigurationsRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeVerifiedAccessInstancesRequestPaginateTypeDef(TypedDict):
    VerifiedAccessInstanceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVerifiedAccessInstancesRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeVerifiedAccessTrustProvidersRequestPaginateTypeDef(TypedDict):
    VerifiedAccessTrustProviderIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVerifiedAccessTrustProvidersRequestRequestTypeDef(TypedDict):
    VerifiedAccessTrustProviderIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class DescribeVolumeStatusRequestPaginateTypeDef(TypedDict):
    VolumeIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVolumeStatusRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    VolumeIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeVolumeStatusRequestVolumeDescribeStatusTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeVolumesModificationsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VolumeIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVolumesModificationsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VolumeIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeVolumesRequestPaginateTypeDef(TypedDict):
    VolumeIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVolumesRequestRequestTypeDef(TypedDict):
    VolumeIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeVpcBlockPublicAccessExclusionsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ExclusionIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class DescribeVpcClassicLinkRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VpcIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeVpcEndpointAssociationsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VpcEndpointIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeVpcEndpointConnectionNotificationsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ConnectionNotificationId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcEndpointConnectionNotificationsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ConnectionNotificationId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeVpcEndpointConnectionsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcEndpointConnectionsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeVpcEndpointServiceConfigurationsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ServiceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcEndpointServiceConfigurationsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ServiceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeVpcEndpointServicePermissionsRequestPaginateTypeDef(TypedDict):
    ServiceId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcEndpointServicePermissionsRequestRequestTypeDef(TypedDict):
    ServiceId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeVpcEndpointServicesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ServiceNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ServiceRegions: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcEndpointServicesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ServiceNames: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ServiceRegions: NotRequired[Sequence[str]]


class DescribeVpcEndpointsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VpcEndpointIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcEndpointsRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VpcEndpointIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeVpcPeeringConnectionsRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    VpcPeeringConnectionIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcPeeringConnectionsRequestRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    VpcPeeringConnectionIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeVpcsRequestPaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    VpcIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeVpcsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    VpcIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class DescribeVpnConnectionsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    VpnConnectionIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class DescribeVpnGatewaysRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    VpnGatewayIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class ExportTransitGatewayRoutesRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    S3Bucket: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class GetCoipPoolUsageRequestRequestTypeDef(TypedDict):
    PoolId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetIpamDiscoveredAccountsRequestPaginateTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    DiscoveryRegion: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetIpamDiscoveredAccountsRequestRequestTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    DiscoveryRegion: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetIpamDiscoveredPublicAddressesRequestRequestTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    AddressRegion: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetIpamDiscoveredResourceCidrsRequestPaginateTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    ResourceRegion: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetIpamDiscoveredResourceCidrsRequestRequestTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    ResourceRegion: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetIpamPoolAllocationsRequestPaginateTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    IpamPoolAllocationId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetIpamPoolAllocationsRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    IpamPoolAllocationId: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetIpamPoolCidrsRequestPaginateTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetIpamPoolCidrsRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class GetIpamResourceCidrsRequestPaginateTypeDef(TypedDict):
    IpamScopeId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IpamPoolId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[IpamResourceTypeType]
    ResourceTag: NotRequired[RequestIpamResourceTagTypeDef]
    ResourceOwner: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetIpamResourceCidrsRequestRequestTypeDef(TypedDict):
    IpamScopeId: str
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    IpamPoolId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[IpamResourceTypeType]
    ResourceTag: NotRequired[RequestIpamResourceTagTypeDef]
    ResourceOwner: NotRequired[str]


class GetSecurityGroupsForVpcRequestPaginateTypeDef(TypedDict):
    VpcId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetSecurityGroupsForVpcRequestRequestTypeDef(TypedDict):
    VpcId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]


class GetSubnetCidrReservationsRequestRequestTypeDef(TypedDict):
    SubnetId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class GetTransitGatewayAttachmentPropagationsRequestPaginateTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayAttachmentPropagationsRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetTransitGatewayMulticastDomainAssociationsRequestPaginateTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayMulticastDomainAssociationsRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetTransitGatewayPolicyTableAssociationsRequestPaginateTypeDef(TypedDict):
    TransitGatewayPolicyTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayPolicyTableAssociationsRequestRequestTypeDef(TypedDict):
    TransitGatewayPolicyTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetTransitGatewayPolicyTableEntriesRequestRequestTypeDef(TypedDict):
    TransitGatewayPolicyTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetTransitGatewayPrefixListReferencesRequestPaginateTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayPrefixListReferencesRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetTransitGatewayRouteTableAssociationsRequestPaginateTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayRouteTableAssociationsRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class GetTransitGatewayRouteTablePropagationsRequestPaginateTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetTransitGatewayRouteTablePropagationsRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class SearchLocalGatewayRoutesRequestPaginateTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchLocalGatewayRoutesRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class SearchTransitGatewayMulticastGroupsRequestPaginateTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchTransitGatewayMulticastGroupsRequestRequestTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]


class SearchTransitGatewayRoutesRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    Filters: Sequence[FilterTypeDef]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]


class DescribeAggregateIdFormatResultTypeDef(TypedDict):
    UseLongIdsAggregated: bool
    Statuses: list[IdFormatTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIdFormatResultTypeDef(TypedDict):
    Statuses: list[IdFormatTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIdentityIdFormatResultTypeDef(TypedDict):
    Statuses: list[IdFormatTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PrincipalIdFormatTypeDef(TypedDict):
    Arn: NotRequired[str]
    Statuses: NotRequired[list[IdFormatTypeDef]]


class DescribeAwsNetworkPerformanceMetricSubscriptionsResultTypeDef(TypedDict):
    Subscriptions: list[SubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeBundleTasksRequestWaitTypeDef(TypedDict):
    BundleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeConversionTasksRequestWaitTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    ConversionTaskIds: NotRequired[Sequence[str]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeCustomerGatewaysRequestWaitTypeDef(TypedDict):
    CustomerGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    DryRun: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeExportTasksRequestWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ExportTaskIds: NotRequired[Sequence[str]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImagesRequestWaitTypeDef(TypedDict):
    ExecutableUsers: NotRequired[Sequence[str]]
    ImageIds: NotRequired[Sequence[str]]
    Owners: NotRequired[Sequence[str]]
    IncludeDeprecated: NotRequired[bool]
    IncludeDisabled: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeImportSnapshotTasksRequestWaitTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ImportTaskIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeInstanceStatusRequestWaitTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    IncludeAllInstances: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeInstancesRequestWaitTypeDef(TypedDict):
    InstanceIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeInternetGatewaysRequestWaitTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    InternetGatewayIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeKeyPairsRequestWaitTypeDef(TypedDict):
    KeyNames: NotRequired[Sequence[str]]
    KeyPairIds: NotRequired[Sequence[str]]
    IncludePublicKey: NotRequired[bool]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNatGatewaysRequestWaitTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NatGatewayIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeNetworkInterfacesRequestWaitTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    NetworkInterfaceIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeSecurityGroupsRequestWaitTypeDef(TypedDict):
    GroupIds: NotRequired[Sequence[str]]
    GroupNames: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeSnapshotsRequestWaitTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    OwnerIds: NotRequired[Sequence[str]]
    RestorableByUserIds: NotRequired[Sequence[str]]
    SnapshotIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeSpotInstanceRequestsRequestWaitTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    SpotInstanceRequestIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeStoreImageTasksRequestWaitTypeDef(TypedDict):
    ImageIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeSubnetsRequestWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    SubnetIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeVolumesRequestWaitTypeDef(TypedDict):
    VolumeIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeVpcPeeringConnectionsRequestWaitTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    VpcPeeringConnectionIds: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeVpcsRequestWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    VpcIds: NotRequired[Sequence[str]]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]
    DryRun: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeVpnConnectionsRequestWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    VpnConnectionIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetPasswordDataRequestWaitTypeDef(TypedDict):
    InstanceId: str
    DryRun: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeFastLaunchImagesSuccessItemTypeDef(TypedDict):
    ImageId: NotRequired[str]
    ResourceType: NotRequired[Literal["snapshot"]]
    SnapshotConfiguration: NotRequired[FastLaunchSnapshotConfigurationResponseTypeDef]
    LaunchTemplate: NotRequired[FastLaunchLaunchTemplateSpecificationResponseTypeDef]
    MaxParallelLaunches: NotRequired[int]
    OwnerId: NotRequired[str]
    State: NotRequired[FastLaunchStateCodeType]
    StateTransitionReason: NotRequired[str]
    StateTransitionTime: NotRequired[datetime]


class DisableFastLaunchResultTypeDef(TypedDict):
    ImageId: str
    ResourceType: Literal["snapshot"]
    SnapshotConfiguration: FastLaunchSnapshotConfigurationResponseTypeDef
    LaunchTemplate: FastLaunchLaunchTemplateSpecificationResponseTypeDef
    MaxParallelLaunches: int
    OwnerId: str
    State: FastLaunchStateCodeType
    StateTransitionReason: str
    StateTransitionTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class EnableFastLaunchResultTypeDef(TypedDict):
    ImageId: str
    ResourceType: Literal["snapshot"]
    SnapshotConfiguration: FastLaunchSnapshotConfigurationResponseTypeDef
    LaunchTemplate: FastLaunchLaunchTemplateSpecificationResponseTypeDef
    MaxParallelLaunches: int
    OwnerId: str
    State: FastLaunchStateCodeType
    StateTransitionReason: str
    StateTransitionTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFastSnapshotRestoresResultTypeDef(TypedDict):
    FastSnapshotRestores: list[DescribeFastSnapshotRestoreSuccessItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeHostReservationOfferingsResultTypeDef(TypedDict):
    OfferingSet: list[HostOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstanceCreditSpecificationsResultTypeDef(TypedDict):
    InstanceCreditSpecifications: list[InstanceCreditSpecificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstanceTopologyResultTypeDef(TypedDict):
    Instances: list[InstanceTopologyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeInstanceTypeOfferingsResultTypeDef(TypedDict):
    InstanceTypeOfferings: list[InstanceTypeOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeLockedSnapshotsResultTypeDef(TypedDict):
    Snapshots: list[LockedSnapshotsInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMacHostsResultTypeDef(TypedDict):
    MacHosts: list[MacHostTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeMovingAddressesResultTypeDef(TypedDict):
    MovingAddressStatuses: list[MovingAddressStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribePrefixListsResultTypeDef(TypedDict):
    PrefixLists: list[PrefixListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeRegionsResultTypeDef(TypedDict):
    Regions: list[RegionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSecurityGroupReferencesResultTypeDef(TypedDict):
    SecurityGroupReferenceSet: list[SecurityGroupReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSecurityGroupVpcAssociationsResultTypeDef(TypedDict):
    SecurityGroupVpcAssociations: list[SecurityGroupVpcAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSnapshotAttributeResultTypeDef(TypedDict):
    ProductCodes: list[ProductCodeTypeDef]
    SnapshotId: str
    CreateVolumePermissions: list[CreateVolumePermissionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVolumeAttributeResultTypeDef(TypedDict):
    AutoEnableIO: AttributeBooleanValueTypeDef
    ProductCodes: list[ProductCodeTypeDef]
    VolumeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSpotPriceHistoryResultTypeDef(TypedDict):
    SpotPriceHistory: list[SpotPriceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeStoreImageTasksResultTypeDef(TypedDict):
    StoreImageTaskResults: list[StoreImageTaskResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeTagsResultTypeDef(TypedDict):
    Tags: list[TagDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeVolumesModificationsResultTypeDef(TypedDict):
    VolumesModifications: list[VolumeModificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVolumeResultTypeDef(TypedDict):
    VolumeModification: VolumeModificationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcBlockPublicAccessOptionsResultTypeDef(TypedDict):
    VpcBlockPublicAccessOptions: VpcBlockPublicAccessOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpcBlockPublicAccessOptionsResultTypeDef(TypedDict):
    VpcBlockPublicAccessOptions: VpcBlockPublicAccessOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FlowLogTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    DeliverLogsErrorMessage: NotRequired[str]
    DeliverLogsPermissionArn: NotRequired[str]
    DeliverCrossAccountRole: NotRequired[str]
    DeliverLogsStatus: NotRequired[str]
    FlowLogId: NotRequired[str]
    FlowLogStatus: NotRequired[str]
    LogGroupName: NotRequired[str]
    ResourceId: NotRequired[str]
    TrafficType: NotRequired[TrafficTypeType]
    LogDestinationType: NotRequired[LogDestinationTypeType]
    LogDestination: NotRequired[str]
    LogFormat: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    MaxAggregationInterval: NotRequired[int]
    DestinationOptions: NotRequired[DestinationOptionsResponseTypeDef]


class DisableFastSnapshotRestoreStateErrorItemTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    Error: NotRequired[DisableFastSnapshotRestoreStateErrorTypeDef]


class DisableTransitGatewayRouteTablePropagationResultTypeDef(TypedDict):
    Propagation: TransitGatewayPropagationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EnableTransitGatewayRouteTablePropagationResultTypeDef(TypedDict):
    Propagation: TransitGatewayPropagationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DiskImageTypeDef(TypedDict):
    Description: NotRequired[str]
    Image: NotRequired[DiskImageDetailTypeDef]
    Volume: NotRequired[VolumeDetailTypeDef]


class ImportVolumeRequestRequestTypeDef(TypedDict):
    AvailabilityZone: str
    Image: DiskImageDetailTypeDef
    Volume: VolumeDetailTypeDef
    DryRun: NotRequired[bool]
    Description: NotRequired[str]


class ImportInstanceVolumeDetailItemTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    BytesConverted: NotRequired[int]
    Description: NotRequired[str]
    Image: NotRequired[DiskImageDescriptionTypeDef]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    Volume: NotRequired[DiskImageVolumeDescriptionTypeDef]


class ImportVolumeTaskDetailsTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    BytesConverted: NotRequired[int]
    Description: NotRequired[str]
    Image: NotRequired[DiskImageDescriptionTypeDef]
    Volume: NotRequired[DiskImageVolumeDescriptionTypeDef]


class InstanceStorageInfoTypeDef(TypedDict):
    TotalSizeInGB: NotRequired[int]
    Disks: NotRequired[list[DiskInfoTypeDef]]
    NvmeSupport: NotRequired[EphemeralNvmeSupportType]
    EncryptionSupport: NotRequired[InstanceStorageEncryptionSupportType]


class VpcEndpointAssociationTypeDef(TypedDict):
    Id: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    ServiceNetworkArn: NotRequired[str]
    ServiceNetworkName: NotRequired[str]
    AssociatedResourceAccessibility: NotRequired[str]
    FailureReason: NotRequired[str]
    FailureCode: NotRequired[str]
    DnsEntry: NotRequired[DnsEntryTypeDef]
    PrivateDnsEntry: NotRequired[DnsEntryTypeDef]
    AssociatedResourceArn: NotRequired[str]
    ResourceConfigurationGroupArn: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class VpcEndpointConnectionTypeDef(TypedDict):
    ServiceId: NotRequired[str]
    VpcEndpointId: NotRequired[str]
    VpcEndpointOwner: NotRequired[str]
    VpcEndpointState: NotRequired[StateType]
    CreationTimestamp: NotRequired[datetime]
    DnsEntries: NotRequired[list[DnsEntryTypeDef]]
    NetworkLoadBalancerArns: NotRequired[list[str]]
    GatewayLoadBalancerArns: NotRequired[list[str]]
    IpAddressType: NotRequired[IpAddressTypeType]
    VpcEndpointConnectionId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    VpcEndpointRegion: NotRequired[str]


class ModifyClientVpnEndpointRequestRequestTypeDef(TypedDict):
    ClientVpnEndpointId: str
    ServerCertificateArn: NotRequired[str]
    ConnectionLogOptions: NotRequired[ConnectionLogOptionsTypeDef]
    DnsServers: NotRequired[DnsServersOptionsModifyStructureTypeDef]
    VpnPort: NotRequired[int]
    Description: NotRequired[str]
    SplitTunnel: NotRequired[bool]
    DryRun: NotRequired[bool]
    SecurityGroupIds: NotRequired[Sequence[str]]
    VpcId: NotRequired[str]
    SelfServicePortal: NotRequired[SelfServicePortalType]
    ClientConnectOptions: NotRequired[ClientConnectOptionsTypeDef]
    SessionTimeoutHours: NotRequired[int]
    ClientLoginBannerOptions: NotRequired[ClientLoginBannerOptionsTypeDef]


class EbsInfoTypeDef(TypedDict):
    EbsOptimizedSupport: NotRequired[EbsOptimizedSupportType]
    EncryptionSupport: NotRequired[EbsEncryptionSupportType]
    EbsOptimizedInfo: NotRequired[EbsOptimizedInfoTypeDef]
    NvmeSupport: NotRequired[EbsNvmeSupportType]


class InstanceBlockDeviceMappingSpecificationTypeDef(TypedDict):
    DeviceName: NotRequired[str]
    Ebs: NotRequired[EbsInstanceBlockDeviceSpecificationTypeDef]
    VirtualName: NotRequired[str]
    NoDevice: NotRequired[str]


class EbsInstanceBlockDeviceTypeDef(TypedDict):
    AttachTime: NotRequired[datetime]
    DeleteOnTermination: NotRequired[bool]
    Status: NotRequired[AttachmentStatusType]
    VolumeId: NotRequired[str]
    AssociatedResource: NotRequired[str]
    VolumeOwnerId: NotRequired[str]
    Operator: NotRequired[OperatorResponseTypeDef]


class LaunchTemplateTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    CreateTime: NotRequired[datetime]
    CreatedBy: NotRequired[str]
    DefaultVersionNumber: NotRequired[int]
    LatestVersionNumber: NotRequired[int]
    Tags: NotRequired[list[TagTypeDef]]
    Operator: NotRequired[OperatorResponseTypeDef]


class EbsStatusSummaryTypeDef(TypedDict):
    Details: NotRequired[list[EbsStatusDetailsTypeDef]]
    Status: NotRequired[SummaryStatusType]


class EgressOnlyInternetGatewayTypeDef(TypedDict):
    Attachments: NotRequired[list[InternetGatewayAttachmentTypeDef]]
    EgressOnlyInternetGatewayId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class InternetGatewayTypeDef(TypedDict):
    Attachments: NotRequired[list[InternetGatewayAttachmentTypeDef]]
    InternetGatewayId: NotRequired[str]
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ElasticGpusTypeDef(TypedDict):
    ElasticGpuId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    ElasticGpuType: NotRequired[str]
    ElasticGpuHealth: NotRequired[ElasticGpuHealthTypeDef]
    ElasticGpuState: NotRequired[Literal["ATTACHED"]]
    InstanceId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class EnaSrdSpecificationRequestTypeDef(TypedDict):
    EnaSrdEnabled: NotRequired[bool]
    EnaSrdUdpSpecification: NotRequired[EnaSrdUdpSpecificationRequestTypeDef]


class EnaSrdSpecificationTypeDef(TypedDict):
    EnaSrdEnabled: NotRequired[bool]
    EnaSrdUdpSpecification: NotRequired[EnaSrdUdpSpecificationTypeDef]


class EnableFastLaunchRequestRequestTypeDef(TypedDict):
    ImageId: str
    ResourceType: NotRequired[str]
    SnapshotConfiguration: NotRequired[FastLaunchSnapshotConfigurationRequestTypeDef]
    LaunchTemplate: NotRequired[FastLaunchLaunchTemplateSpecificationRequestTypeDef]
    MaxParallelLaunches: NotRequired[int]
    DryRun: NotRequired[bool]


class EnableFastSnapshotRestoreStateErrorItemTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    Error: NotRequired[EnableFastSnapshotRestoreStateErrorTypeDef]


class HistoryRecordEntryTypeDef(TypedDict):
    EventInformation: NotRequired[EventInformationTypeDef]
    EventType: NotRequired[FleetEventTypeType]
    Timestamp: NotRequired[datetime]


class HistoryRecordTypeDef(TypedDict):
    EventInformation: NotRequired[EventInformationTypeDef]
    EventType: NotRequired[EventTypeType]
    Timestamp: NotRequired[datetime]


class ExportImageResultTypeDef(TypedDict):
    Description: str
    DiskImageFormat: DiskImageFormatType
    ExportImageTaskId: str
    ImageId: str
    RoleName: str
    Progress: str
    S3ExportLocation: ExportTaskS3LocationTypeDef
    Status: str
    StatusMessage: str
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExportImageTaskTypeDef(TypedDict):
    Description: NotRequired[str]
    ExportImageTaskId: NotRequired[str]
    ImageId: NotRequired[str]
    Progress: NotRequired[str]
    S3ExportLocation: NotRequired[ExportTaskS3LocationTypeDef]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ExportTaskTypeDef(TypedDict):
    Description: NotRequired[str]
    ExportTaskId: NotRequired[str]
    ExportToS3Task: NotRequired[ExportToS3TaskTypeDef]
    InstanceExportDetails: NotRequired[InstanceExportDetailsTypeDef]
    State: NotRequired[ExportTaskStateType]
    StatusMessage: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class PathFilterTypeDef(TypedDict):
    SourceAddress: NotRequired[str]
    SourcePortRange: NotRequired[FilterPortRangeTypeDef]
    DestinationAddress: NotRequired[str]
    DestinationPortRange: NotRequired[FilterPortRangeTypeDef]


class FleetSpotMaintenanceStrategiesRequestTypeDef(TypedDict):
    CapacityRebalance: NotRequired[FleetSpotCapacityRebalanceRequestTypeDef]


class FleetSpotMaintenanceStrategiesTypeDef(TypedDict):
    CapacityRebalance: NotRequired[FleetSpotCapacityRebalanceTypeDef]


class FpgaDeviceInfoTypeDef(TypedDict):
    Name: NotRequired[str]
    Manufacturer: NotRequired[str]
    Count: NotRequired[int]
    MemoryInfo: NotRequired[FpgaDeviceMemoryInfoTypeDef]


class FpgaImageAttributeTypeDef(TypedDict):
    FpgaImageId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    LoadPermissions: NotRequired[list[LoadPermissionTypeDef]]
    ProductCodes: NotRequired[list[ProductCodeTypeDef]]


class FpgaImageTypeDef(TypedDict):
    FpgaImageId: NotRequired[str]
    FpgaImageGlobalId: NotRequired[str]
    Name: NotRequired[str]
    Description: NotRequired[str]
    ShellVersion: NotRequired[str]
    PciId: NotRequired[PciIdTypeDef]
    State: NotRequired[FpgaImageStateTypeDef]
    CreateTime: NotRequired[datetime]
    UpdateTime: NotRequired[datetime]
    OwnerId: NotRequired[str]
    OwnerAlias: NotRequired[str]
    ProductCodes: NotRequired[list[ProductCodeTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    Public: NotRequired[bool]
    DataRetentionSupport: NotRequired[bool]
    InstanceTypes: NotRequired[list[str]]


class GetAllowedImagesSettingsResultTypeDef(TypedDict):
    State: str
    ImageCriteria: list[ImageCriterionTypeDef]
    ManagedBy: ManagedByType
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssociatedIpv6PoolCidrsResultTypeDef(TypedDict):
    Ipv6CidrAssociations: list[Ipv6CidrAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetCapacityReservationUsageResultTypeDef(TypedDict):
    CapacityReservationId: str
    InstanceType: str
    TotalInstanceCount: int
    AvailableInstanceCount: int
    State: CapacityReservationStateType
    InstanceUsages: list[InstanceUsageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetDefaultCreditSpecificationResultTypeDef(TypedDict):
    InstanceFamilyCreditSpecification: InstanceFamilyCreditSpecificationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDefaultCreditSpecificationResultTypeDef(TypedDict):
    InstanceFamilyCreditSpecification: InstanceFamilyCreditSpecificationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetHostReservationPurchasePreviewResultTypeDef(TypedDict):
    CurrencyCode: Literal["USD"]
    Purchase: list[PurchaseTypeDef]
    TotalHourlyPrice: str
    TotalUpfrontPrice: str
    ResponseMetadata: ResponseMetadataTypeDef


class PurchaseHostReservationResultTypeDef(TypedDict):
    ClientToken: str
    CurrencyCode: Literal["USD"]
    Purchase: list[PurchaseTypeDef]
    TotalHourlyPrice: str
    TotalUpfrontPrice: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceMetadataDefaultsResultTypeDef(TypedDict):
    AccountLevel: InstanceMetadataDefaultsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetInstanceTypesFromInstanceRequirementsResultTypeDef(TypedDict):
    InstanceTypes: list[InstanceTypeInfoFromInstanceRequirementsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetIpamAddressHistoryResultTypeDef(TypedDict):
    HistoryRecords: list[IpamAddressHistoryRecordTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetManagedPrefixListAssociationsResultTypeDef(TypedDict):
    PrefixListAssociations: list[PrefixListAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetManagedPrefixListEntriesResultTypeDef(TypedDict):
    Entries: list[PrefixListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ReservedInstanceReservationValueTypeDef(TypedDict):
    ReservationValue: NotRequired[ReservationValueTypeDef]
    ReservedInstanceId: NotRequired[str]


class GetSpotPlacementScoresResultTypeDef(TypedDict):
    SpotPlacementScores: list[SpotPlacementScoreTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetTransitGatewayAttachmentPropagationsResultTypeDef(TypedDict):
    TransitGatewayAttachmentPropagations: list[TransitGatewayAttachmentPropagationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetTransitGatewayRouteTableAssociationsResultTypeDef(TypedDict):
    Associations: list[TransitGatewayRouteTableAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetTransitGatewayRouteTablePropagationsResultTypeDef(TypedDict):
    TransitGatewayRouteTablePropagations: list[TransitGatewayRouteTablePropagationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetVerifiedAccessEndpointTargetsResultTypeDef(TypedDict):
    VerifiedAccessEndpointTargets: list[VerifiedAccessEndpointTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetVpnConnectionDeviceTypesResultTypeDef(TypedDict):
    VpnConnectionDeviceTypes: list[VpnConnectionDeviceTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetVpnTunnelReplacementStatusResultTypeDef(TypedDict):
    VpnConnectionId: str
    TransitGatewayId: str
    CustomerGatewayId: str
    VpnGatewayId: str
    VpnTunnelOutsideIpAddress: str
    MaintenanceDetails: MaintenanceDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GpuDeviceInfoTypeDef(TypedDict):
    Name: NotRequired[str]
    Manufacturer: NotRequired[str]
    Count: NotRequired[int]
    MemoryInfo: NotRequired[GpuDeviceMemoryInfoTypeDef]


class IamInstanceProfileAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    InstanceId: NotRequired[str]
    IamInstanceProfile: NotRequired[IamInstanceProfileTypeDef]
    State: NotRequired[IamInstanceProfileAssociationStateType]
    Timestamp: NotRequired[datetime]


class LaunchPermissionModificationsTypeDef(TypedDict):
    Add: NotRequired[Sequence[LaunchPermissionTypeDef]]
    Remove: NotRequired[Sequence[LaunchPermissionTypeDef]]


class ReplaceImageCriteriaInAllowedImagesSettingsRequestRequestTypeDef(TypedDict):
    ImageCriteria: NotRequired[Sequence[ImageCriterionRequestTypeDef]]
    DryRun: NotRequired[bool]


class ImageDiskContainerTypeDef(TypedDict):
    Description: NotRequired[str]
    DeviceName: NotRequired[str]
    Format: NotRequired[str]
    SnapshotId: NotRequired[str]
    Url: NotRequired[str]
    UserBucket: NotRequired[UserBucketTypeDef]


class SnapshotDiskContainerTypeDef(TypedDict):
    Description: NotRequired[str]
    Format: NotRequired[str]
    Url: NotRequired[str]
    UserBucket: NotRequired[UserBucketTypeDef]


class ListImagesInRecycleBinResultTypeDef(TypedDict):
    Images: list[ImageRecycleBinInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LocalGatewayRouteTableTypeDef(TypedDict):
    LocalGatewayRouteTableId: NotRequired[str]
    LocalGatewayRouteTableArn: NotRequired[str]
    LocalGatewayId: NotRequired[str]
    OutpostArn: NotRequired[str]
    OwnerId: NotRequired[str]
    State: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    Mode: NotRequired[LocalGatewayRouteTableModeType]
    StateReason: NotRequired[StateReasonTypeDef]


class ImportInstanceLaunchSpecificationTypeDef(TypedDict):
    Architecture: NotRequired[ArchitectureValuesType]
    GroupNames: NotRequired[Sequence[str]]
    GroupIds: NotRequired[Sequence[str]]
    AdditionalInfo: NotRequired[str]
    UserData: NotRequired[UserDataTypeDef]
    InstanceType: NotRequired[InstanceTypeType]
    Placement: NotRequired[PlacementTypeDef]
    Monitoring: NotRequired[bool]
    SubnetId: NotRequired[str]
    InstanceInitiatedShutdownBehavior: NotRequired[ShutdownBehaviorType]
    PrivateIpAddress: NotRequired[str]


class InferenceDeviceInfoTypeDef(TypedDict):
    Count: NotRequired[int]
    Name: NotRequired[str]
    Manufacturer: NotRequired[str]
    MemoryInfo: NotRequired[InferenceDeviceMemoryInfoTypeDef]


class InstanceAttachmentEnaSrdSpecificationTypeDef(TypedDict):
    EnaSrdEnabled: NotRequired[bool]
    EnaSrdUdpSpecification: NotRequired[InstanceAttachmentEnaSrdUdpSpecificationTypeDef]


class ModifyInstanceCreditSpecificationRequestRequestTypeDef(TypedDict):
    InstanceCreditSpecifications: Sequence[InstanceCreditSpecificationRequestTypeDef]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class InstanceImageMetadataTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    LaunchTime: NotRequired[datetime]
    AvailabilityZone: NotRequired[str]
    ZoneId: NotRequired[str]
    State: NotRequired[InstanceStateTypeDef]
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    ImageMetadata: NotRequired[ImageMetadataTypeDef]
    Operator: NotRequired[OperatorResponseTypeDef]


class InstanceStateChangeTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    CurrentState: NotRequired[InstanceStateTypeDef]
    PreviousState: NotRequired[InstanceStateTypeDef]


class ModifyInstanceMetadataOptionsResultTypeDef(TypedDict):
    InstanceId: str
    InstanceMetadataOptions: InstanceMetadataOptionsResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class InstanceMonitoringTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    Monitoring: NotRequired[MonitoringTypeDef]


class InstancePrivateIpAddressTypeDef(TypedDict):
    Association: NotRequired[InstanceNetworkInterfaceAssociationTypeDef]
    Primary: NotRequired[bool]
    PrivateDnsName: NotRequired[str]
    PrivateIpAddress: NotRequired[str]


class InstanceStatusSummaryTypeDef(TypedDict):
    Details: NotRequired[list[InstanceStatusDetailsTypeDef]]
    Status: NotRequired[SummaryStatusType]


class ModifyInstanceEventStartTimeResultTypeDef(TypedDict):
    Event: InstanceStatusEventTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IpPermissionOutputTypeDef(TypedDict):
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    UserIdGroupPairs: NotRequired[list[UserIdGroupPairTypeDef]]
    IpRanges: NotRequired[list[IpRangeTypeDef]]
    Ipv6Ranges: NotRequired[list[Ipv6RangeTypeDef]]
    PrefixListIds: NotRequired[list[PrefixListIdTypeDef]]


class IpPermissionTypeDef(TypedDict):
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    UserIdGroupPairs: NotRequired[Sequence[UserIdGroupPairTypeDef]]
    IpRanges: NotRequired[Sequence[IpRangeTypeDef]]
    Ipv6Ranges: NotRequired[Sequence[Ipv6RangeTypeDef]]
    PrefixListIds: NotRequired[Sequence[PrefixListIdTypeDef]]


class StaleIpPermissionTypeDef(TypedDict):
    FromPort: NotRequired[int]
    IpProtocol: NotRequired[str]
    IpRanges: NotRequired[list[str]]
    PrefixListIds: NotRequired[list[str]]
    ToPort: NotRequired[int]
    UserIdGroupPairs: NotRequired[list[UserIdGroupPairTypeDef]]


class ProvisionIpamPoolCidrRequestRequestTypeDef(TypedDict):
    IpamPoolId: str
    DryRun: NotRequired[bool]
    Cidr: NotRequired[str]
    CidrAuthorizationContext: NotRequired[IpamCidrAuthorizationContextTypeDef]
    NetmaskLength: NotRequired[int]
    ClientToken: NotRequired[str]
    VerificationMethod: NotRequired[VerificationMethodType]
    IpamExternalResourceVerificationTokenId: NotRequired[str]


class IpamDiscoveredAccountTypeDef(TypedDict):
    AccountId: NotRequired[str]
    DiscoveryRegion: NotRequired[str]
    FailureReason: NotRequired[IpamDiscoveryFailureReasonTypeDef]
    LastAttemptedDiscoveryTime: NotRequired[datetime]
    LastSuccessfulDiscoveryTime: NotRequired[datetime]
    OrganizationalUnitId: NotRequired[str]


class IpamDiscoveredResourceCidrTypeDef(TypedDict):
    IpamResourceDiscoveryId: NotRequired[str]
    ResourceRegion: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceOwnerId: NotRequired[str]
    ResourceCidr: NotRequired[str]
    IpSource: NotRequired[IpamResourceCidrIpSourceType]
    ResourceType: NotRequired[IpamResourceTypeType]
    ResourceTags: NotRequired[list[IpamResourceTagTypeDef]]
    IpUsage: NotRequired[float]
    VpcId: NotRequired[str]
    SubnetId: NotRequired[str]
    NetworkInterfaceAttachmentStatus: NotRequired[IpamNetworkInterfaceAttachmentStatusType]
    SampleTime: NotRequired[datetime]
    AvailabilityZoneId: NotRequired[str]


class IpamResourceCidrTypeDef(TypedDict):
    IpamId: NotRequired[str]
    IpamScopeId: NotRequired[str]
    IpamPoolId: NotRequired[str]
    ResourceRegion: NotRequired[str]
    ResourceOwnerId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceName: NotRequired[str]
    ResourceCidr: NotRequired[str]
    ResourceType: NotRequired[IpamResourceTypeType]
    ResourceTags: NotRequired[list[IpamResourceTagTypeDef]]
    IpUsage: NotRequired[float]
    ComplianceStatus: NotRequired[IpamComplianceStatusType]
    ManagementState: NotRequired[IpamManagementStateType]
    OverlapStatus: NotRequired[IpamOverlapStatusType]
    VpcId: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]


class IpamTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    IpamId: NotRequired[str]
    IpamArn: NotRequired[str]
    IpamRegion: NotRequired[str]
    PublicDefaultScopeId: NotRequired[str]
    PrivateDefaultScopeId: NotRequired[str]
    ScopeCount: NotRequired[int]
    Description: NotRequired[str]
    OperatingRegions: NotRequired[list[IpamOperatingRegionTypeDef]]
    State: NotRequired[IpamStateType]
    Tags: NotRequired[list[TagTypeDef]]
    DefaultResourceDiscoveryId: NotRequired[str]
    DefaultResourceDiscoveryAssociationId: NotRequired[str]
    ResourceDiscoveryAssociationCount: NotRequired[int]
    StateMessage: NotRequired[str]
    Tier: NotRequired[IpamTierType]
    EnablePrivateGua: NotRequired[bool]


class IpamResourceDiscoveryTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    IpamResourceDiscoveryId: NotRequired[str]
    IpamResourceDiscoveryArn: NotRequired[str]
    IpamResourceDiscoveryRegion: NotRequired[str]
    Description: NotRequired[str]
    OperatingRegions: NotRequired[list[IpamOperatingRegionTypeDef]]
    IsDefault: NotRequired[bool]
    State: NotRequired[IpamResourceDiscoveryStateType]
    Tags: NotRequired[list[TagTypeDef]]
    OrganizationalUnitExclusions: NotRequired[list[IpamOrganizationalUnitExclusionTypeDef]]


class IpamPoolCidrTypeDef(TypedDict):
    Cidr: NotRequired[str]
    State: NotRequired[IpamPoolCidrStateType]
    FailureReason: NotRequired[IpamPoolCidrFailureReasonTypeDef]
    IpamPoolCidrId: NotRequired[str]
    NetmaskLength: NotRequired[int]


class IpamPoolTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    IpamPoolId: NotRequired[str]
    SourceIpamPoolId: NotRequired[str]
    IpamPoolArn: NotRequired[str]
    IpamScopeArn: NotRequired[str]
    IpamScopeType: NotRequired[IpamScopeTypeType]
    IpamArn: NotRequired[str]
    IpamRegion: NotRequired[str]
    Locale: NotRequired[str]
    PoolDepth: NotRequired[int]
    State: NotRequired[IpamPoolStateType]
    StateMessage: NotRequired[str]
    Description: NotRequired[str]
    AutoImport: NotRequired[bool]
    PubliclyAdvertisable: NotRequired[bool]
    AddressFamily: NotRequired[AddressFamilyType]
    AllocationMinNetmaskLength: NotRequired[int]
    AllocationMaxNetmaskLength: NotRequired[int]
    AllocationDefaultNetmaskLength: NotRequired[int]
    AllocationResourceTags: NotRequired[list[IpamResourceTagTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    AwsService: NotRequired[Literal["ec2"]]
    PublicIpSource: NotRequired[IpamPoolPublicIpSourceType]
    SourceResource: NotRequired[IpamPoolSourceResourceTypeDef]


class IpamPublicAddressTagsTypeDef(TypedDict):
    EipTags: NotRequired[list[IpamPublicAddressTagTypeDef]]


class Ipv6PoolTypeDef(TypedDict):
    PoolId: NotRequired[str]
    Description: NotRequired[str]
    PoolCidrBlocks: NotRequired[list[PoolCidrBlockTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]


class LaunchTemplateBlockDeviceMappingRequestTypeDef(TypedDict):
    DeviceName: NotRequired[str]
    VirtualName: NotRequired[str]
    Ebs: NotRequired[LaunchTemplateEbsBlockDeviceRequestTypeDef]
    NoDevice: NotRequired[str]


class LaunchTemplateBlockDeviceMappingTypeDef(TypedDict):
    DeviceName: NotRequired[str]
    VirtualName: NotRequired[str]
    Ebs: NotRequired[LaunchTemplateEbsBlockDeviceTypeDef]
    NoDevice: NotRequired[str]


class LaunchTemplateEnaSrdSpecificationTypeDef(TypedDict):
    EnaSrdEnabled: NotRequired[bool]
    EnaSrdUdpSpecification: NotRequired[LaunchTemplateEnaSrdUdpSpecificationTypeDef]


class LaunchTemplateInstanceMarketOptionsTypeDef(TypedDict):
    MarketType: NotRequired[MarketTypeType]
    SpotOptions: NotRequired[LaunchTemplateSpotMarketOptionsTypeDef]


class ListSnapshotsInRecycleBinResultTypeDef(TypedDict):
    Snapshots: list[SnapshotRecycleBinInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LoadPermissionModificationsTypeDef(TypedDict):
    Add: NotRequired[Sequence[LoadPermissionRequestTypeDef]]
    Remove: NotRequired[Sequence[LoadPermissionRequestTypeDef]]


class MediaDeviceInfoTypeDef(TypedDict):
    Count: NotRequired[int]
    Name: NotRequired[str]
    Manufacturer: NotRequired[str]
    MemoryInfo: NotRequired[MediaDeviceMemoryInfoTypeDef]


class ModifyIpamRequestRequestTypeDef(TypedDict):
    IpamId: str
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    AddOperatingRegions: NotRequired[Sequence[AddIpamOperatingRegionTypeDef]]
    RemoveOperatingRegions: NotRequired[Sequence[RemoveIpamOperatingRegionTypeDef]]
    Tier: NotRequired[IpamTierType]
    EnablePrivateGua: NotRequired[bool]


class ModifyIpamResourceDiscoveryRequestRequestTypeDef(TypedDict):
    IpamResourceDiscoveryId: str
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    AddOperatingRegions: NotRequired[Sequence[AddIpamOperatingRegionTypeDef]]
    RemoveOperatingRegions: NotRequired[Sequence[RemoveIpamOperatingRegionTypeDef]]
    AddOrganizationalUnitExclusions: NotRequired[
        Sequence[AddIpamOrganizationalUnitExclusionTypeDef]
    ]
    RemoveOrganizationalUnitExclusions: NotRequired[
        Sequence[RemoveIpamOrganizationalUnitExclusionTypeDef]
    ]


class ModifyManagedPrefixListRequestRequestTypeDef(TypedDict):
    PrefixListId: str
    DryRun: NotRequired[bool]
    CurrentVersion: NotRequired[int]
    PrefixListName: NotRequired[str]
    AddEntries: NotRequired[Sequence[AddPrefixListEntryTypeDef]]
    RemoveEntries: NotRequired[Sequence[RemovePrefixListEntryTypeDef]]
    MaxEntries: NotRequired[int]


class ModifyReservedInstancesRequestRequestTypeDef(TypedDict):
    ReservedInstancesIds: Sequence[str]
    TargetConfigurations: Sequence[ReservedInstancesConfigurationTypeDef]
    ClientToken: NotRequired[str]


class ReservedInstancesModificationResultTypeDef(TypedDict):
    ReservedInstancesId: NotRequired[str]
    TargetConfiguration: NotRequired[ReservedInstancesConfigurationTypeDef]


class ModifyTransitGatewayRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    Description: NotRequired[str]
    Options: NotRequired[ModifyTransitGatewayOptionsTypeDef]
    DryRun: NotRequired[bool]


class ModifyTransitGatewayVpcAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    AddSubnetIds: NotRequired[Sequence[str]]
    RemoveSubnetIds: NotRequired[Sequence[str]]
    Options: NotRequired[ModifyTransitGatewayVpcAttachmentRequestOptionsTypeDef]
    DryRun: NotRequired[bool]


class ModifyVerifiedAccessEndpointCidrOptionsTypeDef(TypedDict):
    PortRanges: NotRequired[Sequence[ModifyVerifiedAccessEndpointPortRangeTypeDef]]


ModifyVerifiedAccessEndpointEniOptionsTypeDef = TypedDict(
    "ModifyVerifiedAccessEndpointEniOptionsTypeDef",
    {
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "PortRanges": NotRequired[Sequence[ModifyVerifiedAccessEndpointPortRangeTypeDef]],
    },
)
ModifyVerifiedAccessEndpointLoadBalancerOptionsTypeDef = TypedDict(
    "ModifyVerifiedAccessEndpointLoadBalancerOptionsTypeDef",
    {
        "SubnetIds": NotRequired[Sequence[str]],
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "PortRanges": NotRequired[Sequence[ModifyVerifiedAccessEndpointPortRangeTypeDef]],
    },
)


class ModifyVerifiedAccessEndpointPolicyResultTypeDef(TypedDict):
    PolicyEnabled: bool
    PolicyDocument: str
    SseSpecification: VerifiedAccessSseSpecificationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVerifiedAccessGroupPolicyResultTypeDef(TypedDict):
    PolicyEnabled: bool
    PolicyDocument: str
    SseSpecification: VerifiedAccessSseSpecificationResponseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VerifiedAccessGroupTypeDef(TypedDict):
    VerifiedAccessGroupId: NotRequired[str]
    VerifiedAccessInstanceId: NotRequired[str]
    Description: NotRequired[str]
    Owner: NotRequired[str]
    VerifiedAccessGroupArn: NotRequired[str]
    CreationTime: NotRequired[str]
    LastUpdatedTime: NotRequired[str]
    DeletionTime: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationResponseTypeDef]


class ModifyVerifiedAccessTrustProviderRequestRequestTypeDef(TypedDict):
    VerifiedAccessTrustProviderId: str
    OidcOptions: NotRequired[ModifyVerifiedAccessTrustProviderOidcOptionsTypeDef]
    DeviceOptions: NotRequired[ModifyVerifiedAccessTrustProviderDeviceOptionsTypeDef]
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationRequestTypeDef]
    NativeApplicationOidcOptions: NotRequired[
        ModifyVerifiedAccessNativeApplicationOidcOptionsTypeDef
    ]


class ModifyVpcPeeringConnectionOptionsRequestRequestTypeDef(TypedDict):
    VpcPeeringConnectionId: str
    AccepterPeeringConnectionOptions: NotRequired[PeeringConnectionOptionsRequestTypeDef]
    DryRun: NotRequired[bool]
    RequesterPeeringConnectionOptions: NotRequired[PeeringConnectionOptionsRequestTypeDef]


class ModifyVpcPeeringConnectionOptionsResultTypeDef(TypedDict):
    AccepterPeeringConnectionOptions: PeeringConnectionOptionsTypeDef
    RequesterPeeringConnectionOptions: PeeringConnectionOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class NatGatewayTypeDef(TypedDict):
    CreateTime: NotRequired[datetime]
    DeleteTime: NotRequired[datetime]
    FailureCode: NotRequired[str]
    FailureMessage: NotRequired[str]
    NatGatewayAddresses: NotRequired[list[NatGatewayAddressTypeDef]]
    NatGatewayId: NotRequired[str]
    ProvisionedBandwidth: NotRequired[ProvisionedBandwidthTypeDef]
    State: NotRequired[NatGatewayStateType]
    SubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    ConnectivityType: NotRequired[ConnectivityTypeType]


class NetworkInfoTypeDef(TypedDict):
    NetworkPerformance: NotRequired[str]
    MaximumNetworkInterfaces: NotRequired[int]
    MaximumNetworkCards: NotRequired[int]
    DefaultNetworkCardIndex: NotRequired[int]
    NetworkCards: NotRequired[list[NetworkCardInfoTypeDef]]
    Ipv4AddressesPerInterface: NotRequired[int]
    Ipv6AddressesPerInterface: NotRequired[int]
    Ipv6Supported: NotRequired[bool]
    EnaSupport: NotRequired[EnaSupportType]
    EfaSupported: NotRequired[bool]
    EfaInfo: NotRequired[EfaInfoTypeDef]
    EncryptionInTransitSupported: NotRequired[bool]
    EnaSrdSupported: NotRequired[bool]
    BandwidthWeightings: NotRequired[list[BandwidthWeightingTypeType]]


class NetworkInterfacePrivateIpAddressTypeDef(TypedDict):
    Association: NotRequired[NetworkInterfaceAssociationTypeDef]
    Primary: NotRequired[bool]
    PrivateDnsName: NotRequired[str]
    PrivateIpAddress: NotRequired[str]


class NetworkInterfacePermissionTypeDef(TypedDict):
    NetworkInterfacePermissionId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    AwsAccountId: NotRequired[str]
    AwsService: NotRequired[str]
    Permission: NotRequired[InterfacePermissionTypeType]
    PermissionState: NotRequired[NetworkInterfacePermissionStateTypeDef]


class NeuronDeviceInfoTypeDef(TypedDict):
    Count: NotRequired[int]
    Name: NotRequired[str]
    CoreInfo: NotRequired[NeuronDeviceCoreInfoTypeDef]
    MemoryInfo: NotRequired[NeuronDeviceMemoryInfoTypeDef]


class VerifiedAccessTrustProviderTypeDef(TypedDict):
    VerifiedAccessTrustProviderId: NotRequired[str]
    Description: NotRequired[str]
    TrustProviderType: NotRequired[TrustProviderTypeType]
    UserTrustProviderType: NotRequired[UserTrustProviderTypeType]
    DeviceTrustProviderType: NotRequired[DeviceTrustProviderTypeType]
    OidcOptions: NotRequired[OidcOptionsTypeDef]
    DeviceOptions: NotRequired[DeviceOptionsTypeDef]
    PolicyReferenceName: NotRequired[str]
    CreationTime: NotRequired[str]
    LastUpdatedTime: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationResponseTypeDef]
    NativeApplicationOidcOptions: NotRequired[NativeApplicationOidcOptionsTypeDef]


class PathRequestFilterTypeDef(TypedDict):
    SourceAddress: NotRequired[str]
    SourcePortRange: NotRequired[RequestFilterPortRangeTypeDef]
    DestinationAddress: NotRequired[str]
    DestinationPortRange: NotRequired[RequestFilterPortRangeTypeDef]


class PathStatementRequestTypeDef(TypedDict):
    PacketHeaderStatement: NotRequired[PacketHeaderStatementRequestTypeDef]
    ResourceStatement: NotRequired[ResourceStatementRequestTypeDef]


class ThroughResourcesStatementRequestTypeDef(TypedDict):
    ResourceStatement: NotRequired[ResourceStatementRequestTypeDef]


class PathStatementTypeDef(TypedDict):
    PacketHeaderStatement: NotRequired[PacketHeaderStatementTypeDef]
    ResourceStatement: NotRequired[ResourceStatementTypeDef]


class ThroughResourcesStatementTypeDef(TypedDict):
    ResourceStatement: NotRequired[ResourceStatementTypeDef]


class ReservedInstancesListingTypeDef(TypedDict):
    ClientToken: NotRequired[str]
    CreateDate: NotRequired[datetime]
    InstanceCounts: NotRequired[list[InstanceCountTypeDef]]
    PriceSchedules: NotRequired[list[PriceScheduleTypeDef]]
    ReservedInstancesId: NotRequired[str]
    ReservedInstancesListingId: NotRequired[str]
    Status: NotRequired[ListingStatusType]
    StatusMessage: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    UpdateDate: NotRequired[datetime]


class ProvisionPublicIpv4PoolCidrResultTypeDef(TypedDict):
    PoolId: str
    PoolAddressRange: PublicIpv4PoolRangeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PublicIpv4PoolTypeDef(TypedDict):
    PoolId: NotRequired[str]
    Description: NotRequired[str]
    PoolAddressRanges: NotRequired[list[PublicIpv4PoolRangeTypeDef]]
    TotalAddressCount: NotRequired[int]
    TotalAvailableAddressCount: NotRequired[int]
    NetworkBorderGroup: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class PurchaseScheduledInstancesRequestRequestTypeDef(TypedDict):
    PurchaseRequests: Sequence[PurchaseRequestTypeDef]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class PurchaseReservedInstancesOfferingRequestRequestTypeDef(TypedDict):
    InstanceCount: int
    ReservedInstancesOfferingId: str
    PurchaseTime: NotRequired[TimestampTypeDef]
    DryRun: NotRequired[bool]
    LimitPrice: NotRequired[ReservedInstanceLimitPriceTypeDef]


class ReservedInstancesOfferingTypeDef(TypedDict):
    CurrencyCode: NotRequired[Literal["USD"]]
    InstanceTenancy: NotRequired[TenancyType]
    Marketplace: NotRequired[bool]
    OfferingClass: NotRequired[OfferingClassTypeType]
    OfferingType: NotRequired[OfferingTypeValuesType]
    PricingDetails: NotRequired[list[PricingDetailTypeDef]]
    RecurringCharges: NotRequired[list[RecurringChargeTypeDef]]
    Scope: NotRequired[ScopeType]
    ReservedInstancesOfferingId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    AvailabilityZone: NotRequired[str]
    Duration: NotRequired[int]
    UsagePrice: NotRequired[float]
    FixedPrice: NotRequired[float]
    ProductDescription: NotRequired[RIProductDescriptionType]


class ReservedInstancesTypeDef(TypedDict):
    CurrencyCode: NotRequired[Literal["USD"]]
    InstanceTenancy: NotRequired[TenancyType]
    OfferingClass: NotRequired[OfferingClassTypeType]
    OfferingType: NotRequired[OfferingTypeValuesType]
    RecurringCharges: NotRequired[list[RecurringChargeTypeDef]]
    Scope: NotRequired[ScopeType]
    Tags: NotRequired[list[TagTypeDef]]
    ReservedInstancesId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    AvailabilityZone: NotRequired[str]
    Start: NotRequired[datetime]
    End: NotRequired[datetime]
    Duration: NotRequired[int]
    UsagePrice: NotRequired[float]
    FixedPrice: NotRequired[float]
    InstanceCount: NotRequired[int]
    ProductDescription: NotRequired[RIProductDescriptionType]
    State: NotRequired[ReservedInstanceStateType]


class SecurityGroupRuleTypeDef(TypedDict):
    SecurityGroupRuleId: NotRequired[str]
    GroupId: NotRequired[str]
    GroupOwnerId: NotRequired[str]
    IsEgress: NotRequired[bool]
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIpv4: NotRequired[str]
    CidrIpv6: NotRequired[str]
    PrefixListId: NotRequired[str]
    ReferencedGroupInfo: NotRequired[ReferencedSecurityGroupTypeDef]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    SecurityGroupRuleArn: NotRequired[str]


class RegisterInstanceEventNotificationAttributesRequestRequestTypeDef(TypedDict):
    InstanceTagAttribute: RegisterInstanceTagAttributeRequestTypeDef
    DryRun: NotRequired[bool]


class RegisterTransitGatewayMulticastGroupMembersResultTypeDef(TypedDict):
    RegisteredMulticastGroupMembers: TransitGatewayMulticastRegisteredGroupMembersTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterTransitGatewayMulticastGroupSourcesResultTypeDef(TypedDict):
    RegisteredMulticastGroupSources: TransitGatewayMulticastRegisteredGroupSourcesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StorageOutputTypeDef(TypedDict):
    S3: NotRequired[S3StorageOutputTypeDef]


class ScheduledInstanceAvailabilityTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    AvailableInstanceCount: NotRequired[int]
    FirstSlotStartTime: NotRequired[datetime]
    HourlyPrice: NotRequired[str]
    InstanceType: NotRequired[str]
    MaxTermDurationInDays: NotRequired[int]
    MinTermDurationInDays: NotRequired[int]
    NetworkPlatform: NotRequired[str]
    Platform: NotRequired[str]
    PurchaseToken: NotRequired[str]
    Recurrence: NotRequired[ScheduledInstanceRecurrenceTypeDef]
    SlotDurationInHours: NotRequired[int]
    TotalScheduledInstanceHours: NotRequired[int]


class ScheduledInstanceTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    CreateDate: NotRequired[datetime]
    HourlyPrice: NotRequired[str]
    InstanceCount: NotRequired[int]
    InstanceType: NotRequired[str]
    NetworkPlatform: NotRequired[str]
    NextSlotStartTime: NotRequired[datetime]
    Platform: NotRequired[str]
    PreviousSlotEndTime: NotRequired[datetime]
    Recurrence: NotRequired[ScheduledInstanceRecurrenceTypeDef]
    ScheduledInstanceId: NotRequired[str]
    SlotDurationInHours: NotRequired[int]
    TermEndDate: NotRequired[datetime]
    TermStartDate: NotRequired[datetime]
    TotalScheduledInstanceHours: NotRequired[int]


class ScheduledInstancesBlockDeviceMappingTypeDef(TypedDict):
    DeviceName: NotRequired[str]
    Ebs: NotRequired[ScheduledInstancesEbsTypeDef]
    NoDevice: NotRequired[str]
    VirtualName: NotRequired[str]


class ScheduledInstancesNetworkInterfaceTypeDef(TypedDict):
    AssociatePublicIpAddress: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Description: NotRequired[str]
    DeviceIndex: NotRequired[int]
    Groups: NotRequired[Sequence[str]]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[ScheduledInstancesIpv6AddressTypeDef]]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddressConfigs: NotRequired[Sequence[ScheduledInstancesPrivateIpAddressConfigTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    SubnetId: NotRequired[str]


class SearchTransitGatewayMulticastGroupsResultTypeDef(TypedDict):
    MulticastGroups: list[TransitGatewayMulticastGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SecurityGroupRuleUpdateTypeDef(TypedDict):
    SecurityGroupRuleId: str
    SecurityGroupRule: NotRequired[SecurityGroupRuleRequestTypeDef]


ServiceDetailTypeDef = TypedDict(
    "ServiceDetailTypeDef",
    {
        "ServiceName": NotRequired[str],
        "ServiceId": NotRequired[str],
        "ServiceType": NotRequired[list[ServiceTypeDetailTypeDef]],
        "ServiceRegion": NotRequired[str],
        "AvailabilityZones": NotRequired[list[str]],
        "Owner": NotRequired[str],
        "BaseEndpointDnsNames": NotRequired[list[str]],
        "PrivateDnsName": NotRequired[str],
        "PrivateDnsNames": NotRequired[list[PrivateDnsDetailsTypeDef]],
        "VpcEndpointPolicySupported": NotRequired[bool],
        "AcceptanceRequired": NotRequired[bool],
        "ManagesVpcEndpoints": NotRequired[bool],
        "PayerResponsibility": NotRequired[Literal["ServiceOwner"]],
        "Tags": NotRequired[list[TagTypeDef]],
        "PrivateDnsNameVerificationState": NotRequired[DnsNameStateType],
        "SupportedIpAddressTypes": NotRequired[list[ServiceConnectivityTypeType]],
    },
)
ServiceConfigurationTypeDef = TypedDict(
    "ServiceConfigurationTypeDef",
    {
        "ServiceType": NotRequired[list[ServiceTypeDetailTypeDef]],
        "ServiceId": NotRequired[str],
        "ServiceName": NotRequired[str],
        "ServiceState": NotRequired[ServiceStateType],
        "AvailabilityZones": NotRequired[list[str]],
        "AcceptanceRequired": NotRequired[bool],
        "ManagesVpcEndpoints": NotRequired[bool],
        "NetworkLoadBalancerArns": NotRequired[list[str]],
        "GatewayLoadBalancerArns": NotRequired[list[str]],
        "SupportedIpAddressTypes": NotRequired[list[ServiceConnectivityTypeType]],
        "BaseEndpointDnsNames": NotRequired[list[str]],
        "PrivateDnsName": NotRequired[str],
        "PrivateDnsNameConfiguration": NotRequired[PrivateDnsNameConfigurationTypeDef],
        "PayerResponsibility": NotRequired[Literal["ServiceOwner"]],
        "Tags": NotRequired[list[TagTypeDef]],
        "SupportedRegions": NotRequired[list[SupportedRegionDetailTypeDef]],
        "RemoteAccessEnabled": NotRequired[bool],
    },
)


class SnapshotDetailTypeDef(TypedDict):
    Description: NotRequired[str]
    DeviceName: NotRequired[str]
    DiskImageSize: NotRequired[float]
    Format: NotRequired[str]
    Progress: NotRequired[str]
    SnapshotId: NotRequired[str]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    Url: NotRequired[str]
    UserBucket: NotRequired[UserBucketDetailsTypeDef]


class SnapshotTaskDetailTypeDef(TypedDict):
    Description: NotRequired[str]
    DiskImageSize: NotRequired[float]
    Encrypted: NotRequired[bool]
    Format: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Progress: NotRequired[str]
    SnapshotId: NotRequired[str]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    Url: NotRequired[str]
    UserBucket: NotRequired[UserBucketDetailsTypeDef]


class SpotMaintenanceStrategiesTypeDef(TypedDict):
    CapacityRebalance: NotRequired[SpotCapacityRebalanceTypeDef]


class SpotDatafeedSubscriptionTypeDef(TypedDict):
    Bucket: NotRequired[str]
    Fault: NotRequired[SpotInstanceStateFaultTypeDef]
    OwnerId: NotRequired[str]
    Prefix: NotRequired[str]
    State: NotRequired[DatafeedSubscriptionStateType]


class TransitGatewayMulticastDomainAssociationTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    ResourceOwnerId: NotRequired[str]
    Subnet: NotRequired[SubnetAssociationTypeDef]


class TransitGatewayMulticastDomainAssociationsTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    TransitGatewayAttachmentId: NotRequired[str]
    ResourceId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    ResourceOwnerId: NotRequired[str]
    Subnets: NotRequired[list[SubnetAssociationTypeDef]]


class SubnetIpv6CidrBlockAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    Ipv6CidrBlockState: NotRequired[SubnetCidrBlockStateTypeDef]
    Ipv6AddressAttribute: NotRequired[Ipv6AddressAttributeType]
    IpSource: NotRequired[IpSourceType]


VpcEndpointTypeDef = TypedDict(
    "VpcEndpointTypeDef",
    {
        "VpcEndpointId": NotRequired[str],
        "VpcEndpointType": NotRequired[VpcEndpointTypeType],
        "VpcId": NotRequired[str],
        "ServiceName": NotRequired[str],
        "State": NotRequired[StateType],
        "PolicyDocument": NotRequired[str],
        "RouteTableIds": NotRequired[list[str]],
        "SubnetIds": NotRequired[list[str]],
        "Groups": NotRequired[list[SecurityGroupIdentifierTypeDef]],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "DnsOptions": NotRequired[DnsOptionsTypeDef],
        "PrivateDnsEnabled": NotRequired[bool],
        "RequesterManaged": NotRequired[bool],
        "NetworkInterfaceIds": NotRequired[list[str]],
        "DnsEntries": NotRequired[list[DnsEntryTypeDef]],
        "CreationTimestamp": NotRequired[datetime],
        "Tags": NotRequired[list[TagTypeDef]],
        "OwnerId": NotRequired[str],
        "LastError": NotRequired[LastErrorTypeDef],
        "Ipv4Prefixes": NotRequired[list[SubnetIpPrefixesTypeDef]],
        "Ipv6Prefixes": NotRequired[list[SubnetIpPrefixesTypeDef]],
        "FailureReason": NotRequired[str],
        "ServiceNetworkArn": NotRequired[str],
        "ResourceConfigurationArn": NotRequired[str],
        "ServiceRegion": NotRequired[str],
    },
)


class TargetReservationValueTypeDef(TypedDict):
    ReservationValue: NotRequired[ReservationValueTypeDef]
    TargetConfiguration: NotRequired[TargetConfigurationTypeDef]


class TargetGroupsConfigOutputTypeDef(TypedDict):
    TargetGroups: NotRequired[list[TargetGroupTypeDef]]


class TargetGroupsConfigTypeDef(TypedDict):
    TargetGroups: NotRequired[Sequence[TargetGroupTypeDef]]


TrafficMirrorFilterRuleTypeDef = TypedDict(
    "TrafficMirrorFilterRuleTypeDef",
    {
        "TrafficMirrorFilterRuleId": NotRequired[str],
        "TrafficMirrorFilterId": NotRequired[str],
        "TrafficDirection": NotRequired[TrafficDirectionType],
        "RuleNumber": NotRequired[int],
        "RuleAction": NotRequired[TrafficMirrorRuleActionType],
        "Protocol": NotRequired[int],
        "DestinationPortRange": NotRequired[TrafficMirrorPortRangeTypeDef],
        "SourcePortRange": NotRequired[TrafficMirrorPortRangeTypeDef],
        "DestinationCidrBlock": NotRequired[str],
        "SourceCidrBlock": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[list[TagTypeDef]],
    },
)


class TransitGatewayAttachmentTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    TransitGatewayOwnerId: NotRequired[str]
    ResourceOwnerId: NotRequired[str]
    ResourceType: NotRequired[TransitGatewayAttachmentResourceTypeType]
    ResourceId: NotRequired[str]
    State: NotRequired[TransitGatewayAttachmentStateType]
    Association: NotRequired[TransitGatewayAttachmentAssociationTypeDef]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


TransitGatewayConnectPeerConfigurationTypeDef = TypedDict(
    "TransitGatewayConnectPeerConfigurationTypeDef",
    {
        "TransitGatewayAddress": NotRequired[str],
        "PeerAddress": NotRequired[str],
        "InsideCidrBlocks": NotRequired[list[str]],
        "Protocol": NotRequired[Literal["gre"]],
        "BgpConfigurations": NotRequired[list[TransitGatewayAttachmentBgpConfigurationTypeDef]],
    },
)


class TransitGatewayConnectTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    TransportTransitGatewayAttachmentId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    State: NotRequired[TransitGatewayAttachmentStateType]
    CreationTime: NotRequired[datetime]
    Options: NotRequired[TransitGatewayConnectOptionsTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class TransitGatewayMulticastDomainTypeDef(TypedDict):
    TransitGatewayMulticastDomainId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    TransitGatewayMulticastDomainArn: NotRequired[str]
    OwnerId: NotRequired[str]
    Options: NotRequired[TransitGatewayMulticastDomainOptionsTypeDef]
    State: NotRequired[TransitGatewayMulticastDomainStateType]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


class TransitGatewayTypeDef(TypedDict):
    TransitGatewayId: NotRequired[str]
    TransitGatewayArn: NotRequired[str]
    State: NotRequired[TransitGatewayStateType]
    OwnerId: NotRequired[str]
    Description: NotRequired[str]
    CreationTime: NotRequired[datetime]
    Options: NotRequired[TransitGatewayOptionsTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class TransitGatewayPeeringAttachmentTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    AccepterTransitGatewayAttachmentId: NotRequired[str]
    RequesterTgwInfo: NotRequired[PeeringTgwInfoTypeDef]
    AccepterTgwInfo: NotRequired[PeeringTgwInfoTypeDef]
    Options: NotRequired[TransitGatewayPeeringAttachmentOptionsTypeDef]
    Status: NotRequired[PeeringAttachmentStatusTypeDef]
    State: NotRequired[TransitGatewayAttachmentStateType]
    CreationTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]


TransitGatewayPolicyRuleTypeDef = TypedDict(
    "TransitGatewayPolicyRuleTypeDef",
    {
        "SourceCidrBlock": NotRequired[str],
        "SourcePortRange": NotRequired[str],
        "DestinationCidrBlock": NotRequired[str],
        "DestinationPortRange": NotRequired[str],
        "Protocol": NotRequired[str],
        "MetaData": NotRequired[TransitGatewayPolicyRuleMetaDataTypeDef],
    },
)


class TransitGatewayPrefixListReferenceTypeDef(TypedDict):
    TransitGatewayRouteTableId: NotRequired[str]
    PrefixListId: NotRequired[str]
    PrefixListOwnerId: NotRequired[str]
    State: NotRequired[TransitGatewayPrefixListReferenceStateType]
    Blackhole: NotRequired[bool]
    TransitGatewayAttachment: NotRequired[TransitGatewayPrefixListAttachmentTypeDef]


TransitGatewayRouteTypeDef = TypedDict(
    "TransitGatewayRouteTypeDef",
    {
        "DestinationCidrBlock": NotRequired[str],
        "PrefixListId": NotRequired[str],
        "TransitGatewayRouteTableAnnouncementId": NotRequired[str],
        "TransitGatewayAttachments": NotRequired[list[TransitGatewayRouteAttachmentTypeDef]],
        "Type": NotRequired[TransitGatewayRouteTypeType],
        "State": NotRequired[TransitGatewayRouteStateType],
    },
)


class TransitGatewayVpcAttachmentTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    TransitGatewayId: NotRequired[str]
    VpcId: NotRequired[str]
    VpcOwnerId: NotRequired[str]
    State: NotRequired[TransitGatewayAttachmentStateType]
    SubnetIds: NotRequired[list[str]]
    CreationTime: NotRequired[datetime]
    Options: NotRequired[TransitGatewayVpcAttachmentOptionsTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class UnsuccessfulInstanceCreditSpecificationItemTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    Error: NotRequired[UnsuccessfulInstanceCreditSpecificationItemErrorTypeDef]


class UnsuccessfulItemTypeDef(TypedDict):
    Error: NotRequired[UnsuccessfulItemErrorTypeDef]
    ResourceId: NotRequired[str]


class ValidationWarningTypeDef(TypedDict):
    Errors: NotRequired[list[ValidationErrorTypeDef]]


VerifiedAccessEndpointCidrOptionsTypeDef = TypedDict(
    "VerifiedAccessEndpointCidrOptionsTypeDef",
    {
        "Cidr": NotRequired[str],
        "PortRanges": NotRequired[list[VerifiedAccessEndpointPortRangeTypeDef]],
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "SubnetIds": NotRequired[list[str]],
    },
)
VerifiedAccessEndpointEniOptionsTypeDef = TypedDict(
    "VerifiedAccessEndpointEniOptionsTypeDef",
    {
        "NetworkInterfaceId": NotRequired[str],
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "PortRanges": NotRequired[list[VerifiedAccessEndpointPortRangeTypeDef]],
    },
)
VerifiedAccessEndpointLoadBalancerOptionsTypeDef = TypedDict(
    "VerifiedAccessEndpointLoadBalancerOptionsTypeDef",
    {
        "Protocol": NotRequired[VerifiedAccessEndpointProtocolType],
        "Port": NotRequired[int],
        "LoadBalancerArn": NotRequired[str],
        "SubnetIds": NotRequired[list[str]],
        "PortRanges": NotRequired[list[VerifiedAccessEndpointPortRangeTypeDef]],
    },
)


class VerifiedAccessInstanceOpenVpnClientConfigurationTypeDef(TypedDict):
    Config: NotRequired[str]
    Routes: NotRequired[list[VerifiedAccessInstanceOpenVpnClientConfigurationRouteTypeDef]]


class VerifiedAccessInstanceTypeDef(TypedDict):
    VerifiedAccessInstanceId: NotRequired[str]
    Description: NotRequired[str]
    VerifiedAccessTrustProviders: NotRequired[list[VerifiedAccessTrustProviderCondensedTypeDef]]
    CreationTime: NotRequired[str]
    LastUpdatedTime: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    FipsEnabled: NotRequired[bool]
    CidrEndpointsCustomSubDomain: NotRequired[VerifiedAccessInstanceCustomSubDomainTypeDef]


class VerifiedAccessLogCloudWatchLogsDestinationTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    DeliveryStatus: NotRequired[VerifiedAccessLogDeliveryStatusTypeDef]
    LogGroup: NotRequired[str]


class VerifiedAccessLogKinesisDataFirehoseDestinationTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    DeliveryStatus: NotRequired[VerifiedAccessLogDeliveryStatusTypeDef]
    DeliveryStream: NotRequired[str]


class VerifiedAccessLogS3DestinationTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    DeliveryStatus: NotRequired[VerifiedAccessLogDeliveryStatusTypeDef]
    BucketName: NotRequired[str]
    Prefix: NotRequired[str]
    BucketOwner: NotRequired[str]


class VerifiedAccessLogOptionsTypeDef(TypedDict):
    S3: NotRequired[VerifiedAccessLogS3DestinationOptionsTypeDef]
    CloudWatchLogs: NotRequired[VerifiedAccessLogCloudWatchLogsDestinationOptionsTypeDef]
    KinesisDataFirehose: NotRequired[VerifiedAccessLogKinesisDataFirehoseDestinationOptionsTypeDef]
    LogVersion: NotRequired[str]
    IncludeTrustContext: NotRequired[bool]


class VolumeResponseTypeDef(TypedDict):
    OutpostArn: str
    Iops: int
    Tags: list[TagTypeDef]
    VolumeType: VolumeTypeType
    FastRestored: bool
    MultiAttachEnabled: bool
    Throughput: int
    SseType: SSETypeType
    Operator: OperatorResponseTypeDef
    VolumeId: str
    Size: int
    SnapshotId: str
    AvailabilityZone: str
    State: VolumeStateType
    CreateTime: datetime
    Attachments: list[VolumeAttachmentTypeDef]
    Encrypted: bool
    KmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef


class VolumeTypeDef(TypedDict):
    OutpostArn: NotRequired[str]
    Iops: NotRequired[int]
    Tags: NotRequired[list[TagTypeDef]]
    VolumeType: NotRequired[VolumeTypeType]
    FastRestored: NotRequired[bool]
    MultiAttachEnabled: NotRequired[bool]
    Throughput: NotRequired[int]
    SseType: NotRequired[SSETypeType]
    Operator: NotRequired[OperatorResponseTypeDef]
    VolumeId: NotRequired[str]
    Size: NotRequired[int]
    SnapshotId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    State: NotRequired[VolumeStateType]
    CreateTime: NotRequired[datetime]
    Attachments: NotRequired[list[VolumeAttachmentTypeDef]]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]


class VolumeStatusInfoTypeDef(TypedDict):
    Details: NotRequired[list[VolumeStatusDetailsTypeDef]]
    Status: NotRequired[VolumeStatusInfoStatusType]


class VpcCidrBlockAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    CidrBlock: NotRequired[str]
    CidrBlockState: NotRequired[VpcCidrBlockStateTypeDef]


class VpcIpv6CidrBlockAssociationTypeDef(TypedDict):
    AssociationId: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    Ipv6CidrBlockState: NotRequired[VpcCidrBlockStateTypeDef]
    NetworkBorderGroup: NotRequired[str]
    Ipv6Pool: NotRequired[str]
    Ipv6AddressAttribute: NotRequired[Ipv6AddressAttributeType]
    IpSource: NotRequired[IpSourceType]


class VpcPeeringConnectionVpcInfoTypeDef(TypedDict):
    CidrBlock: NotRequired[str]
    Ipv6CidrBlockSet: NotRequired[list[Ipv6CidrBlockTypeDef]]
    CidrBlockSet: NotRequired[list[CidrBlockTypeDef]]
    OwnerId: NotRequired[str]
    PeeringOptions: NotRequired[VpcPeeringConnectionOptionsDescriptionTypeDef]
    VpcId: NotRequired[str]
    Region: NotRequired[str]


class DescribeAccountAttributesResultTypeDef(TypedDict):
    AccountAttributes: list[AccountAttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


AdditionalDetailTypeDef = TypedDict(
    "AdditionalDetailTypeDef",
    {
        "AdditionalDetailType": NotRequired[str],
        "Component": NotRequired[AnalysisComponentTypeDef],
        "VpcEndpointService": NotRequired[AnalysisComponentTypeDef],
        "RuleOptions": NotRequired[list[RuleOptionTypeDef]],
        "RuleGroupTypePairs": NotRequired[list[RuleGroupTypePairTypeDef]],
        "RuleGroupRuleOptionsPairs": NotRequired[list[RuleGroupRuleOptionsPairTypeDef]],
        "ServiceName": NotRequired[str],
        "LoadBalancers": NotRequired[list[AnalysisComponentTypeDef]],
    },
)


class DescribeAddressesAttributeResultTypeDef(TypedDict):
    Addresses: list[AddressAttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyAddressAttributeResultTypeDef(TypedDict):
    Address: AddressAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ResetAddressAttributeResultTypeDef(TypedDict):
    Address: AddressAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAddressesResultTypeDef(TypedDict):
    Addresses: list[AddressTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcEndpointServicePermissionsResultTypeDef(TypedDict):
    AllowedPrincipals: list[AllowedPrincipalTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCarrierGatewayResultTypeDef(TypedDict):
    CarrierGateway: CarrierGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCarrierGatewayResultTypeDef(TypedDict):
    CarrierGateway: CarrierGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCarrierGatewaysResultTypeDef(TypedDict):
    CarrierGateways: list[CarrierGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCoipPoolResultTypeDef(TypedDict):
    CoipPool: CoipPoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCoipPoolResultTypeDef(TypedDict):
    CoipPool: CoipPoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCoipPoolsResultTypeDef(TypedDict):
    CoipPools: list[CoipPoolTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCustomerGatewayResultTypeDef(TypedDict):
    CustomerGateway: CustomerGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCustomerGatewaysResultTypeDef(TypedDict):
    CustomerGateways: list[CustomerGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDeclarativePoliciesReportsResultTypeDef(TypedDict):
    Reports: list[DeclarativePoliciesReportTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateInstanceConnectEndpointResultTypeDef(TypedDict):
    InstanceConnectEndpoint: Ec2InstanceConnectEndpointTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInstanceConnectEndpointResultTypeDef(TypedDict):
    InstanceConnectEndpoint: Ec2InstanceConnectEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInstanceConnectEndpointsResultTypeDef(TypedDict):
    InstanceConnectEndpoints: list[Ec2InstanceConnectEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeHostReservationsResultTypeDef(TypedDict):
    HostReservationSet: list[HostReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateInstanceEventWindowRequestRequestTypeDef(TypedDict):
    InstanceEventWindowId: str
    AssociationTarget: InstanceEventWindowAssociationRequestTypeDef
    DryRun: NotRequired[bool]


class InstanceEventWindowTypeDef(TypedDict):
    InstanceEventWindowId: NotRequired[str]
    TimeRanges: NotRequired[list[InstanceEventWindowTimeRangeTypeDef]]
    Name: NotRequired[str]
    CronExpression: NotRequired[str]
    AssociationTarget: NotRequired[InstanceEventWindowAssociationTargetTypeDef]
    State: NotRequired[InstanceEventWindowStateType]
    Tags: NotRequired[list[TagTypeDef]]


class DisassociateInstanceEventWindowRequestRequestTypeDef(TypedDict):
    InstanceEventWindowId: str
    AssociationTarget: InstanceEventWindowDisassociationRequestTypeDef
    DryRun: NotRequired[bool]


class CreateIpamExternalResourceVerificationTokenResultTypeDef(TypedDict):
    IpamExternalResourceVerificationToken: IpamExternalResourceVerificationTokenTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIpamExternalResourceVerificationTokenResultTypeDef(TypedDict):
    IpamExternalResourceVerificationToken: IpamExternalResourceVerificationTokenTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamExternalResourceVerificationTokensResultTypeDef(TypedDict):
    IpamExternalResourceVerificationTokens: list[IpamExternalResourceVerificationTokenTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateIpamResourceDiscoveryResultTypeDef(TypedDict):
    IpamResourceDiscoveryAssociation: IpamResourceDiscoveryAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamResourceDiscoveryAssociationsResultTypeDef(TypedDict):
    IpamResourceDiscoveryAssociations: list[IpamResourceDiscoveryAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DisassociateIpamResourceDiscoveryResultTypeDef(TypedDict):
    IpamResourceDiscoveryAssociation: IpamResourceDiscoveryAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIpamScopeResultTypeDef(TypedDict):
    IpamScope: IpamScopeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIpamScopeResultTypeDef(TypedDict):
    IpamScope: IpamScopeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamScopesResultTypeDef(TypedDict):
    IpamScopes: list[IpamScopeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyIpamScopeResultTypeDef(TypedDict):
    IpamScope: IpamScopeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeKeyPairsResultTypeDef(TypedDict):
    KeyPairs: list[KeyPairInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef(TypedDict):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociation: (
        LocalGatewayRouteTableVirtualInterfaceGroupAssociationTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLocalGatewayRouteTableVirtualInterfaceGroupAssociationResultTypeDef(TypedDict):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociation: (
        LocalGatewayRouteTableVirtualInterfaceGroupAssociationTypeDef
    )
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocalGatewayRouteTableVirtualInterfaceGroupAssociationsResultTypeDef(TypedDict):
    LocalGatewayRouteTableVirtualInterfaceGroupAssociations: list[
        LocalGatewayRouteTableVirtualInterfaceGroupAssociationTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateLocalGatewayRouteTableVpcAssociationResultTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociation: LocalGatewayRouteTableVpcAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLocalGatewayRouteTableVpcAssociationResultTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociation: LocalGatewayRouteTableVpcAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocalGatewayRouteTableVpcAssociationsResultTypeDef(TypedDict):
    LocalGatewayRouteTableVpcAssociations: list[LocalGatewayRouteTableVpcAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeLocalGatewaysResultTypeDef(TypedDict):
    LocalGateways: list[LocalGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeLocalGatewayVirtualInterfaceGroupsResultTypeDef(TypedDict):
    LocalGatewayVirtualInterfaceGroups: list[LocalGatewayVirtualInterfaceGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeLocalGatewayVirtualInterfacesResultTypeDef(TypedDict):
    LocalGatewayVirtualInterfaces: list[LocalGatewayVirtualInterfaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateManagedPrefixListResultTypeDef(TypedDict):
    PrefixList: ManagedPrefixListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteManagedPrefixListResultTypeDef(TypedDict):
    PrefixList: ManagedPrefixListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeManagedPrefixListsResultTypeDef(TypedDict):
    PrefixLists: list[ManagedPrefixListTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyManagedPrefixListResultTypeDef(TypedDict):
    PrefixList: ManagedPrefixListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreManagedPrefixListVersionResultTypeDef(TypedDict):
    PrefixList: ManagedPrefixListTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNetworkInsightsAccessScopeAnalysesResultTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalyses: list[NetworkInsightsAccessScopeAnalysisTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartNetworkInsightsAccessScopeAnalysisResultTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysis: NetworkInsightsAccessScopeAnalysisTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNetworkInsightsAccessScopesResultTypeDef(TypedDict):
    NetworkInsightsAccessScopes: list[NetworkInsightsAccessScopeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreatePlacementGroupResultTypeDef(TypedDict):
    PlacementGroup: PlacementGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePlacementGroupsResultTypeDef(TypedDict):
    PlacementGroups: list[PlacementGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReplaceRootVolumeTaskResultTypeDef(TypedDict):
    ReplaceRootVolumeTask: ReplaceRootVolumeTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplaceRootVolumeTasksResultTypeDef(TypedDict):
    ReplaceRootVolumeTasks: list[ReplaceRootVolumeTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetSecurityGroupsForVpcResultTypeDef(TypedDict):
    SecurityGroupForVpcs: list[SecurityGroupForVpcTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateSnapshotsResultTypeDef(TypedDict):
    Snapshots: list[SnapshotInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSnapshotTierStatusResultTypeDef(TypedDict):
    SnapshotTierStatuses: list[SnapshotTierStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSnapshotsResultTypeDef(TypedDict):
    Snapshots: list[SnapshotTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


SpotFleetTagSpecificationUnionTypeDef = Union[
    SpotFleetTagSpecificationTypeDef, SpotFleetTagSpecificationOutputTypeDef
]


class CreateSubnetCidrReservationResultTypeDef(TypedDict):
    SubnetCidrReservation: SubnetCidrReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteSubnetCidrReservationResultTypeDef(TypedDict):
    DeletedSubnetCidrReservation: SubnetCidrReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSubnetCidrReservationsResultTypeDef(TypedDict):
    SubnetIpv4CidrReservations: list[SubnetCidrReservationTypeDef]
    SubnetIpv6CidrReservations: list[SubnetCidrReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AllocateAddressRequestRequestTypeDef(TypedDict):
    Domain: NotRequired[DomainTypeType]
    Address: NotRequired[str]
    PublicIpv4Pool: NotRequired[str]
    NetworkBorderGroup: NotRequired[str]
    CustomerOwnedIpv4Pool: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    IpamPoolId: NotRequired[str]
    DryRun: NotRequired[bool]


class AllocateHostsRequestRequestTypeDef(TypedDict):
    AvailabilityZone: str
    InstanceFamily: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    HostRecovery: NotRequired[HostRecoveryType]
    OutpostArn: NotRequired[str]
    HostMaintenance: NotRequired[HostMaintenanceType]
    AssetIds: NotRequired[Sequence[str]]
    AutoPlacement: NotRequired[AutoPlacementType]
    ClientToken: NotRequired[str]
    InstanceType: NotRequired[str]
    Quantity: NotRequired[int]


class AssociateIpamResourceDiscoveryRequestRequestTypeDef(TypedDict):
    IpamId: str
    IpamResourceDiscoveryId: str
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]


class CopyImageRequestRequestTypeDef(TypedDict):
    Name: str
    SourceImageId: str
    SourceRegion: str
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    DestinationOutpostArn: NotRequired[str]
    CopyImageTags: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CopySnapshotRequestRequestTypeDef(TypedDict):
    SourceRegion: str
    SourceSnapshotId: str
    Description: NotRequired[str]
    DestinationOutpostArn: NotRequired[str]
    DestinationRegion: NotRequired[str]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    PresignedUrl: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    CompletionDurationMinutes: NotRequired[int]
    DryRun: NotRequired[bool]


class CopySnapshotRequestSnapshotCopyTypeDef(TypedDict):
    SourceRegion: str
    Description: NotRequired[str]
    DestinationOutpostArn: NotRequired[str]
    DestinationRegion: NotRequired[str]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    PresignedUrl: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    CompletionDurationMinutes: NotRequired[int]
    DryRun: NotRequired[bool]


class CreateCapacityReservationBySplittingRequestRequestTypeDef(TypedDict):
    SourceCapacityReservationId: str
    InstanceCount: int
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateCapacityReservationFleetRequestRequestTypeDef(TypedDict):
    InstanceTypeSpecifications: Sequence[ReservationFleetInstanceSpecificationTypeDef]
    TotalTargetCapacity: int
    AllocationStrategy: NotRequired[str]
    ClientToken: NotRequired[str]
    Tenancy: NotRequired[Literal["default"]]
    EndDate: NotRequired[TimestampTypeDef]
    InstanceMatchCriteria: NotRequired[Literal["open"]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateCapacityReservationRequestRequestTypeDef(TypedDict):
    InstanceType: str
    InstancePlatform: CapacityReservationInstancePlatformType
    InstanceCount: int
    ClientToken: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    Tenancy: NotRequired[CapacityReservationTenancyType]
    EbsOptimized: NotRequired[bool]
    EphemeralStorage: NotRequired[bool]
    EndDate: NotRequired[TimestampTypeDef]
    EndDateType: NotRequired[EndDateTypeType]
    InstanceMatchCriteria: NotRequired[InstanceMatchCriteriaType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    OutpostArn: NotRequired[str]
    PlacementGroupArn: NotRequired[str]
    StartDate: NotRequired[TimestampTypeDef]
    CommitmentDuration: NotRequired[int]
    DeliveryPreference: NotRequired[CapacityReservationDeliveryPreferenceType]


class CreateCarrierGatewayRequestRequestTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class CreateCoipPoolRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


CreateCustomerGatewayRequestRequestTypeDef = TypedDict(
    "CreateCustomerGatewayRequestRequestTypeDef",
    {
        "Type": Literal["ipsec.1"],
        "BgpAsn": NotRequired[int],
        "PublicIp": NotRequired[str],
        "CertificateArn": NotRequired[str],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "DeviceName": NotRequired[str],
        "IpAddress": NotRequired[str],
        "BgpAsnExtended": NotRequired[int],
        "DryRun": NotRequired[bool],
    },
)


class CreateDhcpOptionsRequestRequestTypeDef(TypedDict):
    DhcpConfigurations: Sequence[NewDhcpConfigurationTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateDhcpOptionsRequestServiceResourceCreateDhcpOptionsTypeDef(TypedDict):
    DhcpConfigurations: Sequence[NewDhcpConfigurationTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateEgressOnlyInternetGatewayRequestRequestTypeDef(TypedDict):
    VpcId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateFlowLogsRequestRequestTypeDef(TypedDict):
    ResourceIds: Sequence[str]
    ResourceType: FlowLogsResourceTypeType
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    DeliverLogsPermissionArn: NotRequired[str]
    DeliverCrossAccountRole: NotRequired[str]
    LogGroupName: NotRequired[str]
    TrafficType: NotRequired[TrafficTypeType]
    LogDestinationType: NotRequired[LogDestinationTypeType]
    LogDestination: NotRequired[str]
    LogFormat: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    MaxAggregationInterval: NotRequired[int]
    DestinationOptions: NotRequired[DestinationOptionsRequestTypeDef]


class CreateFpgaImageRequestRequestTypeDef(TypedDict):
    InputStorageLocation: StorageLocationTypeDef
    DryRun: NotRequired[bool]
    LogsStorageLocation: NotRequired[StorageLocationTypeDef]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ClientToken: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateInstanceConnectEndpointRequestRequestTypeDef(TypedDict):
    SubnetId: str
    DryRun: NotRequired[bool]
    SecurityGroupIds: NotRequired[Sequence[str]]
    PreserveClientIp: NotRequired[bool]
    ClientToken: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateInstanceEventWindowRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Name: NotRequired[str]
    TimeRanges: NotRequired[Sequence[InstanceEventWindowTimeRangeRequestTypeDef]]
    CronExpression: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateInstanceExportTaskRequestRequestTypeDef(TypedDict):
    InstanceId: str
    TargetEnvironment: ExportEnvironmentType
    ExportToS3Task: ExportToS3TaskSpecificationTypeDef
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    Description: NotRequired[str]


class CreateInternetGatewayRequestRequestTypeDef(TypedDict):
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateInternetGatewayRequestServiceResourceCreateInternetGatewayTypeDef(TypedDict):
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateIpamExternalResourceVerificationTokenRequestRequestTypeDef(TypedDict):
    IpamId: str
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]


class CreateIpamPoolRequestRequestTypeDef(TypedDict):
    IpamScopeId: str
    AddressFamily: AddressFamilyType
    DryRun: NotRequired[bool]
    Locale: NotRequired[str]
    SourceIpamPoolId: NotRequired[str]
    Description: NotRequired[str]
    AutoImport: NotRequired[bool]
    PubliclyAdvertisable: NotRequired[bool]
    AllocationMinNetmaskLength: NotRequired[int]
    AllocationMaxNetmaskLength: NotRequired[int]
    AllocationDefaultNetmaskLength: NotRequired[int]
    AllocationResourceTags: NotRequired[Sequence[RequestIpamResourceTagTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    AwsService: NotRequired[Literal["ec2"]]
    PublicIpSource: NotRequired[IpamPoolPublicIpSourceType]
    SourceResource: NotRequired[IpamPoolSourceResourceRequestTypeDef]


class CreateIpamRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    OperatingRegions: NotRequired[Sequence[AddIpamOperatingRegionTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    Tier: NotRequired[IpamTierType]
    EnablePrivateGua: NotRequired[bool]


class CreateIpamResourceDiscoveryRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    OperatingRegions: NotRequired[Sequence[AddIpamOperatingRegionTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]


class CreateIpamScopeRequestRequestTypeDef(TypedDict):
    IpamId: str
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]


class CreateKeyPairRequestRequestTypeDef(TypedDict):
    KeyName: str
    KeyType: NotRequired[KeyTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    KeyFormat: NotRequired[KeyFormatType]
    DryRun: NotRequired[bool]


class CreateKeyPairRequestServiceResourceCreateKeyPairTypeDef(TypedDict):
    KeyName: str
    KeyType: NotRequired[KeyTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    KeyFormat: NotRequired[KeyFormatType]
    DryRun: NotRequired[bool]


class CreateLocalGatewayRouteTableRequestRequestTypeDef(TypedDict):
    LocalGatewayId: str
    Mode: NotRequired[LocalGatewayRouteTableModeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateLocalGatewayRouteTableVirtualInterfaceGroupAssociationRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    LocalGatewayVirtualInterfaceGroupId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateLocalGatewayRouteTableVpcAssociationRequestRequestTypeDef(TypedDict):
    LocalGatewayRouteTableId: str
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateManagedPrefixListRequestRequestTypeDef(TypedDict):
    PrefixListName: str
    MaxEntries: int
    AddressFamily: str
    DryRun: NotRequired[bool]
    Entries: NotRequired[Sequence[AddPrefixListEntryTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]


class CreateNatGatewayRequestRequestTypeDef(TypedDict):
    SubnetId: str
    AllocationId: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ConnectivityType: NotRequired[ConnectivityTypeType]
    PrivateIpAddress: NotRequired[str]
    SecondaryAllocationIds: NotRequired[Sequence[str]]
    SecondaryPrivateIpAddresses: NotRequired[Sequence[str]]
    SecondaryPrivateIpAddressCount: NotRequired[int]


class CreateNetworkAclRequestRequestTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateNetworkAclRequestServiceResourceCreateNetworkAclTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateNetworkAclRequestVpcCreateNetworkAclTypeDef(TypedDict):
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateNetworkInterfaceRequestRequestTypeDef(TypedDict):
    SubnetId: str
    Ipv4Prefixes: NotRequired[Sequence[Ipv4PrefixSpecificationRequestTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[Sequence[Ipv6PrefixSpecificationRequestTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    InterfaceType: NotRequired[NetworkInterfaceCreationTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    EnablePrimaryIpv6: NotRequired[bool]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]
    Operator: NotRequired[OperatorRequestTypeDef]
    Description: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    Groups: NotRequired[Sequence[str]]
    PrivateIpAddresses: NotRequired[Sequence[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    Ipv6AddressCount: NotRequired[int]
    DryRun: NotRequired[bool]


class CreateNetworkInterfaceRequestServiceResourceCreateNetworkInterfaceTypeDef(TypedDict):
    SubnetId: str
    Ipv4Prefixes: NotRequired[Sequence[Ipv4PrefixSpecificationRequestTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[Sequence[Ipv6PrefixSpecificationRequestTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    InterfaceType: NotRequired[NetworkInterfaceCreationTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    EnablePrimaryIpv6: NotRequired[bool]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]
    Operator: NotRequired[OperatorRequestTypeDef]
    Description: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    Groups: NotRequired[Sequence[str]]
    PrivateIpAddresses: NotRequired[Sequence[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    Ipv6AddressCount: NotRequired[int]
    DryRun: NotRequired[bool]


class CreateNetworkInterfaceRequestSubnetCreateNetworkInterfaceTypeDef(TypedDict):
    Ipv4Prefixes: NotRequired[Sequence[Ipv4PrefixSpecificationRequestTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[Sequence[Ipv6PrefixSpecificationRequestTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    InterfaceType: NotRequired[NetworkInterfaceCreationTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    EnablePrimaryIpv6: NotRequired[bool]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]
    Operator: NotRequired[OperatorRequestTypeDef]
    Description: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    Groups: NotRequired[Sequence[str]]
    PrivateIpAddresses: NotRequired[Sequence[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    Ipv6AddressCount: NotRequired[int]
    DryRun: NotRequired[bool]


class CreatePlacementGroupRequestRequestTypeDef(TypedDict):
    PartitionCount: NotRequired[int]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    SpreadLevel: NotRequired[SpreadLevelType]
    DryRun: NotRequired[bool]
    GroupName: NotRequired[str]
    Strategy: NotRequired[PlacementStrategyType]


class CreatePlacementGroupRequestServiceResourceCreatePlacementGroupTypeDef(TypedDict):
    PartitionCount: NotRequired[int]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    SpreadLevel: NotRequired[SpreadLevelType]
    DryRun: NotRequired[bool]
    GroupName: NotRequired[str]
    Strategy: NotRequired[PlacementStrategyType]


class CreatePublicIpv4PoolRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    NetworkBorderGroup: NotRequired[str]


class CreateReplaceRootVolumeTaskRequestRequestTypeDef(TypedDict):
    InstanceId: str
    SnapshotId: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ImageId: NotRequired[str]
    DeleteReplacedRootVolume: NotRequired[bool]


class CreateRestoreImageTaskRequestRequestTypeDef(TypedDict):
    Bucket: str
    ObjectKey: str
    Name: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateRouteTableRequestRequestTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateRouteTableRequestServiceResourceCreateRouteTableTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateRouteTableRequestVpcCreateRouteTableTypeDef(TypedDict):
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]


class CreateSecurityGroupRequestRequestTypeDef(TypedDict):
    Description: str
    GroupName: str
    VpcId: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateSecurityGroupRequestServiceResourceCreateSecurityGroupTypeDef(TypedDict):
    Description: str
    GroupName: str
    VpcId: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateSecurityGroupRequestVpcCreateSecurityGroupTypeDef(TypedDict):
    Description: str
    GroupName: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateSnapshotRequestRequestTypeDef(TypedDict):
    VolumeId: str
    Description: NotRequired[str]
    OutpostArn: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    Location: NotRequired[SnapshotLocationEnumType]
    DryRun: NotRequired[bool]


class CreateSnapshotRequestServiceResourceCreateSnapshotTypeDef(TypedDict):
    VolumeId: str
    Description: NotRequired[str]
    OutpostArn: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    Location: NotRequired[SnapshotLocationEnumType]
    DryRun: NotRequired[bool]


class CreateSnapshotRequestVolumeCreateSnapshotTypeDef(TypedDict):
    Description: NotRequired[str]
    OutpostArn: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    Location: NotRequired[SnapshotLocationEnumType]
    DryRun: NotRequired[bool]


class CreateSnapshotsRequestRequestTypeDef(TypedDict):
    InstanceSpecification: InstanceSpecificationTypeDef
    Description: NotRequired[str]
    OutpostArn: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    CopyTagsFromSource: NotRequired[Literal["volume"]]
    Location: NotRequired[SnapshotLocationEnumType]


class CreateSubnetCidrReservationRequestRequestTypeDef(TypedDict):
    SubnetId: str
    Cidr: str
    ReservationType: SubnetCidrReservationTypeType
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateSubnetRequestRequestTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    CidrBlock: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    OutpostArn: NotRequired[str]
    Ipv6Native: NotRequired[bool]
    Ipv4IpamPoolId: NotRequired[str]
    Ipv4NetmaskLength: NotRequired[int]
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    DryRun: NotRequired[bool]


class CreateSubnetRequestServiceResourceCreateSubnetTypeDef(TypedDict):
    VpcId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    CidrBlock: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    OutpostArn: NotRequired[str]
    Ipv6Native: NotRequired[bool]
    Ipv4IpamPoolId: NotRequired[str]
    Ipv4NetmaskLength: NotRequired[int]
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    DryRun: NotRequired[bool]


class CreateSubnetRequestVpcCreateSubnetTypeDef(TypedDict):
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    AvailabilityZone: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    CidrBlock: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    OutpostArn: NotRequired[str]
    Ipv6Native: NotRequired[bool]
    Ipv4IpamPoolId: NotRequired[str]
    Ipv4NetmaskLength: NotRequired[int]
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    DryRun: NotRequired[bool]


class CreateTrafficMirrorFilterRequestRequestTypeDef(TypedDict):
    Description: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


CreateTrafficMirrorFilterRuleRequestRequestTypeDef = TypedDict(
    "CreateTrafficMirrorFilterRuleRequestRequestTypeDef",
    {
        "TrafficMirrorFilterId": str,
        "TrafficDirection": TrafficDirectionType,
        "RuleNumber": int,
        "RuleAction": TrafficMirrorRuleActionType,
        "DestinationCidrBlock": str,
        "SourceCidrBlock": str,
        "DestinationPortRange": NotRequired[TrafficMirrorPortRangeRequestTypeDef],
        "SourcePortRange": NotRequired[TrafficMirrorPortRangeRequestTypeDef],
        "Protocol": NotRequired[int],
        "Description": NotRequired[str],
        "DryRun": NotRequired[bool],
        "ClientToken": NotRequired[str],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
    },
)


class CreateTrafficMirrorSessionRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    TrafficMirrorTargetId: str
    TrafficMirrorFilterId: str
    SessionNumber: int
    PacketLength: NotRequired[int]
    VirtualNetworkId: NotRequired[int]
    Description: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class CreateTrafficMirrorTargetRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: NotRequired[str]
    NetworkLoadBalancerArn: NotRequired[str]
    Description: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    GatewayLoadBalancerEndpointId: NotRequired[str]


class CreateTransitGatewayConnectPeerRequestRequestTypeDef(TypedDict):
    TransitGatewayAttachmentId: str
    PeerAddress: str
    InsideCidrBlocks: Sequence[str]
    TransitGatewayAddress: NotRequired[str]
    BgpOptions: NotRequired[TransitGatewayConnectRequestBgpOptionsTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayConnectRequestRequestTypeDef(TypedDict):
    TransportTransitGatewayAttachmentId: str
    Options: CreateTransitGatewayConnectRequestOptionsTypeDef
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayMulticastDomainRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    Options: NotRequired[CreateTransitGatewayMulticastDomainRequestOptionsTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayPeeringAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    PeerTransitGatewayId: str
    PeerAccountId: str
    PeerRegion: str
    Options: NotRequired[CreateTransitGatewayPeeringAttachmentRequestOptionsTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayPolicyTableRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayRequestRequestTypeDef(TypedDict):
    Description: NotRequired[str]
    Options: NotRequired[TransitGatewayRequestOptionsTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayRouteTableAnnouncementRequestRequestTypeDef(TypedDict):
    TransitGatewayRouteTableId: str
    PeeringAttachmentId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayRouteTableRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateTransitGatewayVpcAttachmentRequestRequestTypeDef(TypedDict):
    TransitGatewayId: str
    VpcId: str
    SubnetIds: Sequence[str]
    Options: NotRequired[CreateTransitGatewayVpcAttachmentRequestOptionsTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class CreateVerifiedAccessGroupRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    Description: NotRequired[str]
    PolicyDocument: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationRequestTypeDef]


class CreateVerifiedAccessInstanceRequestRequestTypeDef(TypedDict):
    Description: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    FIPSEnabled: NotRequired[bool]
    CidrEndpointsCustomSubDomain: NotRequired[str]


class CreateVerifiedAccessTrustProviderRequestRequestTypeDef(TypedDict):
    TrustProviderType: TrustProviderTypeType
    PolicyReferenceName: str
    UserTrustProviderType: NotRequired[UserTrustProviderTypeType]
    DeviceTrustProviderType: NotRequired[DeviceTrustProviderTypeType]
    OidcOptions: NotRequired[CreateVerifiedAccessTrustProviderOidcOptionsTypeDef]
    DeviceOptions: NotRequired[CreateVerifiedAccessTrustProviderDeviceOptionsTypeDef]
    Description: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationRequestTypeDef]
    NativeApplicationOidcOptions: NotRequired[
        CreateVerifiedAccessNativeApplicationOidcOptionsTypeDef
    ]


class CreateVolumeRequestRequestTypeDef(TypedDict):
    AvailabilityZone: str
    Encrypted: NotRequired[bool]
    Iops: NotRequired[int]
    KmsKeyId: NotRequired[str]
    OutpostArn: NotRequired[str]
    Size: NotRequired[int]
    SnapshotId: NotRequired[str]
    VolumeType: NotRequired[VolumeTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    MultiAttachEnabled: NotRequired[bool]
    Throughput: NotRequired[int]
    ClientToken: NotRequired[str]
    Operator: NotRequired[OperatorRequestTypeDef]
    DryRun: NotRequired[bool]


class CreateVolumeRequestServiceResourceCreateVolumeTypeDef(TypedDict):
    AvailabilityZone: str
    Encrypted: NotRequired[bool]
    Iops: NotRequired[int]
    KmsKeyId: NotRequired[str]
    OutpostArn: NotRequired[str]
    Size: NotRequired[int]
    SnapshotId: NotRequired[str]
    VolumeType: NotRequired[VolumeTypeType]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    MultiAttachEnabled: NotRequired[bool]
    Throughput: NotRequired[int]
    ClientToken: NotRequired[str]
    Operator: NotRequired[OperatorRequestTypeDef]
    DryRun: NotRequired[bool]


class CreateVpcBlockPublicAccessExclusionRequestRequestTypeDef(TypedDict):
    InternetGatewayExclusionMode: InternetGatewayExclusionModeType
    DryRun: NotRequired[bool]
    SubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


CreateVpcEndpointRequestRequestTypeDef = TypedDict(
    "CreateVpcEndpointRequestRequestTypeDef",
    {
        "VpcId": str,
        "DryRun": NotRequired[bool],
        "VpcEndpointType": NotRequired[VpcEndpointTypeType],
        "ServiceName": NotRequired[str],
        "PolicyDocument": NotRequired[str],
        "RouteTableIds": NotRequired[Sequence[str]],
        "SubnetIds": NotRequired[Sequence[str]],
        "SecurityGroupIds": NotRequired[Sequence[str]],
        "IpAddressType": NotRequired[IpAddressTypeType],
        "DnsOptions": NotRequired[DnsOptionsSpecificationTypeDef],
        "ClientToken": NotRequired[str],
        "PrivateDnsEnabled": NotRequired[bool],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "SubnetConfigurations": NotRequired[Sequence[SubnetConfigurationTypeDef]],
        "ServiceNetworkArn": NotRequired[str],
        "ResourceConfigurationArn": NotRequired[str],
        "ServiceRegion": NotRequired[str],
    },
)


class CreateVpcEndpointServiceConfigurationRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    AcceptanceRequired: NotRequired[bool]
    PrivateDnsName: NotRequired[str]
    NetworkLoadBalancerArns: NotRequired[Sequence[str]]
    GatewayLoadBalancerArns: NotRequired[Sequence[str]]
    SupportedIpAddressTypes: NotRequired[Sequence[str]]
    SupportedRegions: NotRequired[Sequence[str]]
    ClientToken: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateVpcPeeringConnectionRequestRequestTypeDef(TypedDict):
    VpcId: str
    PeerRegion: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    PeerVpcId: NotRequired[str]
    PeerOwnerId: NotRequired[str]


class CreateVpcPeeringConnectionRequestServiceResourceCreateVpcPeeringConnectionTypeDef(TypedDict):
    VpcId: str
    PeerRegion: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    PeerVpcId: NotRequired[str]
    PeerOwnerId: NotRequired[str]


class CreateVpcPeeringConnectionRequestVpcRequestVpcPeeringConnectionTypeDef(TypedDict):
    PeerRegion: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    PeerVpcId: NotRequired[str]
    PeerOwnerId: NotRequired[str]


class CreateVpcRequestRequestTypeDef(TypedDict):
    CidrBlock: NotRequired[str]
    Ipv6Pool: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    Ipv4IpamPoolId: NotRequired[str]
    Ipv4NetmaskLength: NotRequired[int]
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    Ipv6CidrBlockNetworkBorderGroup: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    InstanceTenancy: NotRequired[TenancyType]
    AmazonProvidedIpv6CidrBlock: NotRequired[bool]


class CreateVpcRequestServiceResourceCreateVpcTypeDef(TypedDict):
    CidrBlock: NotRequired[str]
    Ipv6Pool: NotRequired[str]
    Ipv6CidrBlock: NotRequired[str]
    Ipv4IpamPoolId: NotRequired[str]
    Ipv4NetmaskLength: NotRequired[int]
    Ipv6IpamPoolId: NotRequired[str]
    Ipv6NetmaskLength: NotRequired[int]
    Ipv6CidrBlockNetworkBorderGroup: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    InstanceTenancy: NotRequired[TenancyType]
    AmazonProvidedIpv6CidrBlock: NotRequired[bool]


CreateVpnGatewayRequestRequestTypeDef = TypedDict(
    "CreateVpnGatewayRequestRequestTypeDef",
    {
        "Type": Literal["ipsec.1"],
        "AvailabilityZone": NotRequired[str],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "AmazonSideAsn": NotRequired[int],
        "DryRun": NotRequired[bool],
    },
)


class ExportImageRequestRequestTypeDef(TypedDict):
    DiskImageFormat: DiskImageFormatType
    ImageId: str
    S3ExportLocation: ExportTaskS3LocationRequestTypeDef
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    RoleName: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class ImportKeyPairRequestRequestTypeDef(TypedDict):
    KeyName: str
    PublicKeyMaterial: BlobTypeDef
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class ImportKeyPairRequestServiceResourceImportKeyPairTypeDef(TypedDict):
    KeyName: str
    PublicKeyMaterial: BlobTypeDef
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class ProvisionByoipCidrRequestRequestTypeDef(TypedDict):
    Cidr: str
    CidrAuthorizationContext: NotRequired[CidrAuthorizationContextTypeDef]
    PubliclyAdvertisable: NotRequired[bool]
    Description: NotRequired[str]
    DryRun: NotRequired[bool]
    PoolTagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    MultiRegion: NotRequired[bool]
    NetworkBorderGroup: NotRequired[str]


class PurchaseCapacityBlockRequestRequestTypeDef(TypedDict):
    CapacityBlockOfferingId: str
    InstancePlatform: CapacityReservationInstancePlatformType
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class PurchaseHostReservationRequestRequestTypeDef(TypedDict):
    HostIdSet: Sequence[str]
    OfferingId: str
    ClientToken: NotRequired[str]
    CurrencyCode: NotRequired[Literal["USD"]]
    LimitPrice: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class StartDeclarativePoliciesReportRequestRequestTypeDef(TypedDict):
    S3Bucket: str
    TargetId: str
    DryRun: NotRequired[bool]
    S3Prefix: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class StartNetworkInsightsAccessScopeAnalysisRequestRequestTypeDef(TypedDict):
    NetworkInsightsAccessScopeId: str
    ClientToken: str
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class StartNetworkInsightsAnalysisRequestRequestTypeDef(TypedDict):
    NetworkInsightsPathId: str
    ClientToken: str
    AdditionalAccounts: NotRequired[Sequence[str]]
    FilterInArns: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


TagSpecificationUnionTypeDef = Union[TagSpecificationTypeDef, TagSpecificationOutputTypeDef]


class CreateTrafficMirrorSessionResultTypeDef(TypedDict):
    TrafficMirrorSession: TrafficMirrorSessionTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrafficMirrorSessionsResultTypeDef(TypedDict):
    TrafficMirrorSessions: list[TrafficMirrorSessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyTrafficMirrorSessionResultTypeDef(TypedDict):
    TrafficMirrorSession: TrafficMirrorSessionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrafficMirrorTargetResultTypeDef(TypedDict):
    TrafficMirrorTarget: TrafficMirrorTargetTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrafficMirrorTargetsResultTypeDef(TypedDict):
    TrafficMirrorTargets: list[TrafficMirrorTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateTransitGatewayPolicyTableResultTypeDef(TypedDict):
    TransitGatewayPolicyTable: TransitGatewayPolicyTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayPolicyTableResultTypeDef(TypedDict):
    TransitGatewayPolicyTable: TransitGatewayPolicyTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayPolicyTablesResultTypeDef(TypedDict):
    TransitGatewayPolicyTables: list[TransitGatewayPolicyTableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateTransitGatewayRouteTableAnnouncementResultTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncement: TransitGatewayRouteTableAnnouncementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayRouteTableAnnouncementResultTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncement: TransitGatewayRouteTableAnnouncementTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayRouteTableAnnouncementsResultTypeDef(TypedDict):
    TransitGatewayRouteTableAnnouncements: list[TransitGatewayRouteTableAnnouncementTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateTransitGatewayRouteTableResultTypeDef(TypedDict):
    TransitGatewayRouteTable: TransitGatewayRouteTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayRouteTableResultTypeDef(TypedDict):
    TransitGatewayRouteTable: TransitGatewayRouteTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayRouteTablesResultTypeDef(TypedDict):
    TransitGatewayRouteTables: list[TransitGatewayRouteTableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AssociateTrunkInterfaceResultTypeDef(TypedDict):
    InterfaceAssociation: TrunkInterfaceAssociationTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrunkInterfaceAssociationsResultTypeDef(TypedDict):
    InterfaceAssociations: list[TrunkInterfaceAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateVpcBlockPublicAccessExclusionResultTypeDef(TypedDict):
    VpcBlockPublicAccessExclusion: VpcBlockPublicAccessExclusionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcBlockPublicAccessExclusionResultTypeDef(TypedDict):
    VpcBlockPublicAccessExclusion: VpcBlockPublicAccessExclusionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcBlockPublicAccessExclusionsResultTypeDef(TypedDict):
    VpcBlockPublicAccessExclusions: list[VpcBlockPublicAccessExclusionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVpcBlockPublicAccessExclusionResultTypeDef(TypedDict):
    VpcBlockPublicAccessExclusion: VpcBlockPublicAccessExclusionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcClassicLinkResultTypeDef(TypedDict):
    Vpcs: list[VpcClassicLinkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExplanationTypeDef(TypedDict):
    Acl: NotRequired[AnalysisComponentTypeDef]
    AclRule: NotRequired[AnalysisAclRuleTypeDef]
    Address: NotRequired[str]
    Addresses: NotRequired[list[str]]
    AttachedTo: NotRequired[AnalysisComponentTypeDef]
    AvailabilityZones: NotRequired[list[str]]
    Cidrs: NotRequired[list[str]]
    Component: NotRequired[AnalysisComponentTypeDef]
    CustomerGateway: NotRequired[AnalysisComponentTypeDef]
    Destination: NotRequired[AnalysisComponentTypeDef]
    DestinationVpc: NotRequired[AnalysisComponentTypeDef]
    Direction: NotRequired[str]
    ExplanationCode: NotRequired[str]
    IngressRouteTable: NotRequired[AnalysisComponentTypeDef]
    InternetGateway: NotRequired[AnalysisComponentTypeDef]
    LoadBalancerArn: NotRequired[str]
    ClassicLoadBalancerListener: NotRequired[AnalysisLoadBalancerListenerTypeDef]
    LoadBalancerListenerPort: NotRequired[int]
    LoadBalancerTarget: NotRequired[AnalysisLoadBalancerTargetTypeDef]
    LoadBalancerTargetGroup: NotRequired[AnalysisComponentTypeDef]
    LoadBalancerTargetGroups: NotRequired[list[AnalysisComponentTypeDef]]
    LoadBalancerTargetPort: NotRequired[int]
    ElasticLoadBalancerListener: NotRequired[AnalysisComponentTypeDef]
    MissingComponent: NotRequired[str]
    NatGateway: NotRequired[AnalysisComponentTypeDef]
    NetworkInterface: NotRequired[AnalysisComponentTypeDef]
    PacketField: NotRequired[str]
    VpcPeeringConnection: NotRequired[AnalysisComponentTypeDef]
    Port: NotRequired[int]
    PortRanges: NotRequired[list[PortRangeTypeDef]]
    PrefixList: NotRequired[AnalysisComponentTypeDef]
    Protocols: NotRequired[list[str]]
    RouteTableRoute: NotRequired[AnalysisRouteTableRouteTypeDef]
    RouteTable: NotRequired[AnalysisComponentTypeDef]
    SecurityGroup: NotRequired[AnalysisComponentTypeDef]
    SecurityGroupRule: NotRequired[AnalysisSecurityGroupRuleTypeDef]
    SecurityGroups: NotRequired[list[AnalysisComponentTypeDef]]
    SourceVpc: NotRequired[AnalysisComponentTypeDef]
    State: NotRequired[str]
    Subnet: NotRequired[AnalysisComponentTypeDef]
    SubnetRouteTable: NotRequired[AnalysisComponentTypeDef]
    Vpc: NotRequired[AnalysisComponentTypeDef]
    VpcEndpoint: NotRequired[AnalysisComponentTypeDef]
    VpnConnection: NotRequired[AnalysisComponentTypeDef]
    VpnGateway: NotRequired[AnalysisComponentTypeDef]
    TransitGateway: NotRequired[AnalysisComponentTypeDef]
    TransitGatewayRouteTable: NotRequired[AnalysisComponentTypeDef]
    TransitGatewayRouteTableRoute: NotRequired[TransitGatewayRouteTableRouteTypeDef]
    TransitGatewayAttachment: NotRequired[AnalysisComponentTypeDef]
    ComponentAccount: NotRequired[str]
    ComponentRegion: NotRequired[str]
    FirewallStatelessRule: NotRequired[FirewallStatelessRuleTypeDef]
    FirewallStatefulRule: NotRequired[FirewallStatefulRuleTypeDef]


class AdvertiseByoipCidrResultTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeprovisionByoipCidrResultTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeByoipCidrsResultTypeDef(TypedDict):
    ByoipCidrs: list[ByoipCidrTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MoveByoipCidrToIpamResultTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ProvisionByoipCidrResultTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class WithdrawByoipCidrResultTypeDef(TypedDict):
    ByoipCidr: ByoipCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClientVpnTargetNetworksResultTypeDef(TypedDict):
    ClientVpnTargetNetworks: list[TargetNetworkTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RouteTableTypeDef(TypedDict):
    Associations: NotRequired[list[RouteTableAssociationTypeDef]]
    PropagatingVgws: NotRequired[list[PropagatingVgwTypeDef]]
    RouteTableId: NotRequired[str]
    Routes: NotRequired[list[RouteTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    VpcId: NotRequired[str]
    OwnerId: NotRequired[str]


class IntegrateServicesTypeDef(TypedDict):
    AthenaIntegrations: NotRequired[Sequence[AthenaIntegrationTypeDef]]


class LaunchTemplateInstanceMarketOptionsRequestTypeDef(TypedDict):
    MarketType: NotRequired[MarketTypeType]
    SpotOptions: NotRequired[LaunchTemplateSpotMarketOptionsRequestTypeDef]


class DescribeScheduledInstanceAvailabilityRequestPaginateTypeDef(TypedDict):
    FirstSlotStartTimeRange: SlotDateTimeRangeRequestTypeDef
    Recurrence: ScheduledInstanceRecurrenceRequestTypeDef
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxSlotDurationInHours: NotRequired[int]
    MinSlotDurationInHours: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScheduledInstanceAvailabilityRequestRequestTypeDef(TypedDict):
    FirstSlotStartTimeRange: SlotDateTimeRangeRequestTypeDef
    Recurrence: ScheduledInstanceRecurrenceRequestTypeDef
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    MaxSlotDurationInHours: NotRequired[int]
    MinSlotDurationInHours: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeScheduledInstancesRequestPaginateTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    ScheduledInstanceIds: NotRequired[Sequence[str]]
    SlotStartTimeRange: NotRequired[SlotStartTimeRangeRequestTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeScheduledInstancesRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ScheduledInstanceIds: NotRequired[Sequence[str]]
    SlotStartTimeRange: NotRequired[SlotStartTimeRangeRequestTypeDef]


class InstanceMarketOptionsRequestTypeDef(TypedDict):
    MarketType: NotRequired[MarketTypeType]
    SpotOptions: NotRequired[SpotMarketOptionsTypeDef]


class CreateVpnGatewayResultTypeDef(TypedDict):
    VpnGateway: VpnGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpnGatewaysResultTypeDef(TypedDict):
    VpnGateways: list[VpnGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class NetworkInterfaceAttachmentTypeDef(TypedDict):
    AttachTime: NotRequired[datetime]
    AttachmentId: NotRequired[str]
    DeleteOnTermination: NotRequired[bool]
    DeviceIndex: NotRequired[int]
    NetworkCardIndex: NotRequired[int]
    InstanceId: NotRequired[str]
    InstanceOwnerId: NotRequired[str]
    Status: NotRequired[AttachmentStatusType]
    EnaSrdSpecification: NotRequired[AttachmentEnaSrdSpecificationTypeDef]


class GetDeclarativePoliciesReportSummaryResultTypeDef(TypedDict):
    ReportId: str
    S3Bucket: str
    S3Prefix: str
    TargetId: str
    StartTime: datetime
    EndTime: datetime
    NumberOfAccounts: int
    NumberOfFailedAccounts: int
    AttributeSummaries: list[AttributeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DhcpOptionsTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    DhcpOptionsId: NotRequired[str]
    DhcpConfigurations: NotRequired[list[DhcpConfigurationTypeDef]]


class DescribeClientVpnAuthorizationRulesResultTypeDef(TypedDict):
    AuthorizationRules: list[AuthorizationRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeAvailabilityZonesResultTypeDef(TypedDict):
    AvailabilityZones: list[AvailabilityZoneTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class HostTypeDef(TypedDict):
    AutoPlacement: NotRequired[AutoPlacementType]
    AvailabilityZone: NotRequired[str]
    AvailableCapacity: NotRequired[AvailableCapacityTypeDef]
    ClientToken: NotRequired[str]
    HostId: NotRequired[str]
    HostProperties: NotRequired[HostPropertiesTypeDef]
    HostReservationId: NotRequired[str]
    Instances: NotRequired[list[HostInstanceTypeDef]]
    State: NotRequired[AllocationStateType]
    AllocationTime: NotRequired[datetime]
    ReleaseTime: NotRequired[datetime]
    Tags: NotRequired[list[TagTypeDef]]
    HostRecovery: NotRequired[HostRecoveryType]
    AllowsMultipleInstanceTypes: NotRequired[AllowsMultipleInstanceTypesType]
    OwnerId: NotRequired[str]
    AvailabilityZoneId: NotRequired[str]
    MemberOfServiceLinkedResourceGroup: NotRequired[bool]
    OutpostArn: NotRequired[str]
    HostMaintenance: NotRequired[HostMaintenanceType]
    AssetId: NotRequired[str]


S3StorageUnionTypeDef = Union[S3StorageTypeDef, S3StorageOutputTypeDef]


class CreateImageRequestInstanceCreateImageTypeDef(TypedDict):
    Name: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    NoReboot: NotRequired[bool]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]


class CreateImageRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Name: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    NoReboot: NotRequired[bool]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]


class ImageAttributeTypeDef(TypedDict):
    Description: AttributeValueTypeDef
    KernelId: AttributeValueTypeDef
    RamdiskId: AttributeValueTypeDef
    SriovNetSupport: AttributeValueTypeDef
    BootMode: AttributeValueTypeDef
    TpmSupport: AttributeValueTypeDef
    UefiData: AttributeValueTypeDef
    LastLaunchedTime: AttributeValueTypeDef
    ImdsSupport: AttributeValueTypeDef
    DeregistrationProtection: AttributeValueTypeDef
    ImageId: str
    LaunchPermissions: list[LaunchPermissionTypeDef]
    ProductCodes: list[ProductCodeTypeDef]
    BlockDeviceMappings: list[BlockDeviceMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImageTypeDef(TypedDict):
    PlatformDetails: NotRequired[str]
    UsageOperation: NotRequired[str]
    BlockDeviceMappings: NotRequired[list[BlockDeviceMappingTypeDef]]
    Description: NotRequired[str]
    EnaSupport: NotRequired[bool]
    Hypervisor: NotRequired[HypervisorTypeType]
    ImageOwnerAlias: NotRequired[str]
    Name: NotRequired[str]
    RootDeviceName: NotRequired[str]
    RootDeviceType: NotRequired[DeviceTypeType]
    SriovNetSupport: NotRequired[str]
    StateReason: NotRequired[StateReasonTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    VirtualizationType: NotRequired[VirtualizationTypeType]
    BootMode: NotRequired[BootModeValuesType]
    TpmSupport: NotRequired[Literal["v2.0"]]
    DeprecationTime: NotRequired[str]
    ImdsSupport: NotRequired[Literal["v2.0"]]
    SourceInstanceId: NotRequired[str]
    DeregistrationProtection: NotRequired[str]
    LastLaunchedTime: NotRequired[str]
    ImageAllowed: NotRequired[bool]
    SourceImageId: NotRequired[str]
    SourceImageRegion: NotRequired[str]
    ImageId: NotRequired[str]
    ImageLocation: NotRequired[str]
    State: NotRequired[ImageStateType]
    OwnerId: NotRequired[str]
    CreationDate: NotRequired[str]
    Public: NotRequired[bool]
    ProductCodes: NotRequired[list[ProductCodeTypeDef]]
    Architecture: NotRequired[ArchitectureValuesType]
    ImageType: NotRequired[ImageTypeValuesType]
    KernelId: NotRequired[str]
    RamdiskId: NotRequired[str]
    Platform: NotRequired[Literal["windows"]]


class RegisterImageRequestRequestTypeDef(TypedDict):
    Name: str
    ImageLocation: NotRequired[str]
    BillingProducts: NotRequired[Sequence[str]]
    BootMode: NotRequired[BootModeValuesType]
    TpmSupport: NotRequired[Literal["v2.0"]]
    UefiData: NotRequired[str]
    ImdsSupport: NotRequired[Literal["v2.0"]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    Architecture: NotRequired[ArchitectureValuesType]
    KernelId: NotRequired[str]
    RamdiskId: NotRequired[str]
    RootDeviceName: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    VirtualizationType: NotRequired[str]
    SriovNetSupport: NotRequired[str]
    EnaSupport: NotRequired[bool]


class RegisterImageRequestServiceResourceRegisterImageTypeDef(TypedDict):
    Name: str
    ImageLocation: NotRequired[str]
    BillingProducts: NotRequired[Sequence[str]]
    BootMode: NotRequired[BootModeValuesType]
    TpmSupport: NotRequired[Literal["v2.0"]]
    UefiData: NotRequired[str]
    ImdsSupport: NotRequired[Literal["v2.0"]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    Architecture: NotRequired[ArchitectureValuesType]
    KernelId: NotRequired[str]
    RamdiskId: NotRequired[str]
    RootDeviceName: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    VirtualizationType: NotRequired[str]
    SriovNetSupport: NotRequired[str]
    EnaSupport: NotRequired[bool]


class CancelCapacityReservationFleetsResultTypeDef(TypedDict):
    SuccessfulFleetCancellations: list[CapacityReservationFleetCancellationStateTypeDef]
    FailedFleetCancellations: list[FailedCapacityReservationFleetCancellationResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CancelSpotFleetRequestsResponseTypeDef(TypedDict):
    SuccessfulFleetRequests: list[CancelSpotFleetRequestsSuccessItemTypeDef]
    UnsuccessfulFleetRequests: list[CancelSpotFleetRequestsErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCapacityReservationBillingRequestsResultTypeDef(TypedDict):
    CapacityReservationBillingRequests: list[CapacityReservationBillingRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateCapacityReservationBySplittingResultTypeDef(TypedDict):
    SourceCapacityReservation: CapacityReservationTypeDef
    DestinationCapacityReservation: CapacityReservationTypeDef
    InstanceCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCapacityReservationResultTypeDef(TypedDict):
    CapacityReservation: CapacityReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCapacityReservationsResultTypeDef(TypedDict):
    CapacityReservations: list[CapacityReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class MoveCapacityReservationInstancesResultTypeDef(TypedDict):
    SourceCapacityReservation: CapacityReservationTypeDef
    DestinationCapacityReservation: CapacityReservationTypeDef
    InstanceCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class PurchaseCapacityBlockResultTypeDef(TypedDict):
    CapacityReservation: CapacityReservationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCapacityReservationFleetsResultTypeDef(TypedDict):
    CapacityReservationFleets: list[CapacityReservationFleetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyInstanceCapacityReservationAttributesRequestRequestTypeDef(TypedDict):
    InstanceId: str
    CapacityReservationSpecification: CapacityReservationSpecificationTypeDef
    DryRun: NotRequired[bool]


class DescribeClassicLinkInstancesResultTypeDef(TypedDict):
    Instances: list[ClassicLinkInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


ClassicLoadBalancersConfigUnionTypeDef = Union[
    ClassicLoadBalancersConfigTypeDef, ClassicLoadBalancersConfigOutputTypeDef
]


class CreateClientVpnEndpointRequestRequestTypeDef(TypedDict):
    ClientCidrBlock: str
    ServerCertificateArn: str
    AuthenticationOptions: Sequence[ClientVpnAuthenticationRequestTypeDef]
    ConnectionLogOptions: ConnectionLogOptionsTypeDef
    DnsServers: NotRequired[Sequence[str]]
    TransportProtocol: NotRequired[TransportProtocolType]
    VpnPort: NotRequired[int]
    Description: NotRequired[str]
    SplitTunnel: NotRequired[bool]
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    VpcId: NotRequired[str]
    SelfServicePortal: NotRequired[SelfServicePortalType]
    ClientConnectOptions: NotRequired[ClientConnectOptionsTypeDef]
    SessionTimeoutHours: NotRequired[int]
    ClientLoginBannerOptions: NotRequired[ClientLoginBannerOptionsTypeDef]


class ClientVpnEndpointTypeDef(TypedDict):
    ClientVpnEndpointId: NotRequired[str]
    Description: NotRequired[str]
    Status: NotRequired[ClientVpnEndpointStatusTypeDef]
    CreationTime: NotRequired[str]
    DeletionTime: NotRequired[str]
    DnsName: NotRequired[str]
    ClientCidrBlock: NotRequired[str]
    DnsServers: NotRequired[list[str]]
    SplitTunnel: NotRequired[bool]
    VpnProtocol: NotRequired[Literal["openvpn"]]
    TransportProtocol: NotRequired[TransportProtocolType]
    VpnPort: NotRequired[int]
    AssociatedTargetNetworks: NotRequired[list[AssociatedTargetNetworkTypeDef]]
    ServerCertificateArn: NotRequired[str]
    AuthenticationOptions: NotRequired[list[ClientVpnAuthenticationTypeDef]]
    ConnectionLogOptions: NotRequired[ConnectionLogResponseOptionsTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    SecurityGroupIds: NotRequired[list[str]]
    VpcId: NotRequired[str]
    SelfServicePortalUrl: NotRequired[str]
    ClientConnectOptions: NotRequired[ClientConnectResponseOptionsTypeDef]
    SessionTimeoutHours: NotRequired[int]
    ClientLoginBannerOptions: NotRequired[ClientLoginBannerResponseOptionsTypeDef]


class DescribeClientVpnConnectionsResultTypeDef(TypedDict):
    Connections: list[ClientVpnConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TerminateClientVpnConnectionsResultTypeDef(TypedDict):
    ClientVpnEndpointId: str
    Username: str
    ConnectionStatuses: list[TerminateConnectionStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeClientVpnRoutesResultTypeDef(TypedDict):
    Routes: list[ClientVpnRouteTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVpnTunnelOptionsSpecificationTypeDef(TypedDict):
    TunnelInsideCidr: NotRequired[str]
    TunnelInsideIpv6Cidr: NotRequired[str]
    PreSharedKey: NotRequired[str]
    Phase1LifetimeSeconds: NotRequired[int]
    Phase2LifetimeSeconds: NotRequired[int]
    RekeyMarginTimeSeconds: NotRequired[int]
    RekeyFuzzPercentage: NotRequired[int]
    ReplayWindowSize: NotRequired[int]
    DPDTimeoutSeconds: NotRequired[int]
    DPDTimeoutAction: NotRequired[str]
    Phase1EncryptionAlgorithms: NotRequired[
        Sequence[Phase1EncryptionAlgorithmsRequestListValueTypeDef]
    ]
    Phase2EncryptionAlgorithms: NotRequired[
        Sequence[Phase2EncryptionAlgorithmsRequestListValueTypeDef]
    ]
    Phase1IntegrityAlgorithms: NotRequired[
        Sequence[Phase1IntegrityAlgorithmsRequestListValueTypeDef]
    ]
    Phase2IntegrityAlgorithms: NotRequired[
        Sequence[Phase2IntegrityAlgorithmsRequestListValueTypeDef]
    ]
    Phase1DHGroupNumbers: NotRequired[Sequence[Phase1DHGroupNumbersRequestListValueTypeDef]]
    Phase2DHGroupNumbers: NotRequired[Sequence[Phase2DHGroupNumbersRequestListValueTypeDef]]
    IKEVersions: NotRequired[Sequence[IKEVersionsRequestListValueTypeDef]]
    StartupAction: NotRequired[str]
    LogOptions: NotRequired[VpnTunnelLogOptionsSpecificationTypeDef]
    EnableTunnelLifecycleControl: NotRequired[bool]


class VpnTunnelOptionsSpecificationTypeDef(TypedDict):
    TunnelInsideCidr: NotRequired[str]
    TunnelInsideIpv6Cidr: NotRequired[str]
    PreSharedKey: NotRequired[str]
    Phase1LifetimeSeconds: NotRequired[int]
    Phase2LifetimeSeconds: NotRequired[int]
    RekeyMarginTimeSeconds: NotRequired[int]
    RekeyFuzzPercentage: NotRequired[int]
    ReplayWindowSize: NotRequired[int]
    DPDTimeoutSeconds: NotRequired[int]
    DPDTimeoutAction: NotRequired[str]
    Phase1EncryptionAlgorithms: NotRequired[
        Sequence[Phase1EncryptionAlgorithmsRequestListValueTypeDef]
    ]
    Phase2EncryptionAlgorithms: NotRequired[
        Sequence[Phase2EncryptionAlgorithmsRequestListValueTypeDef]
    ]
    Phase1IntegrityAlgorithms: NotRequired[
        Sequence[Phase1IntegrityAlgorithmsRequestListValueTypeDef]
    ]
    Phase2IntegrityAlgorithms: NotRequired[
        Sequence[Phase2IntegrityAlgorithmsRequestListValueTypeDef]
    ]
    Phase1DHGroupNumbers: NotRequired[Sequence[Phase1DHGroupNumbersRequestListValueTypeDef]]
    Phase2DHGroupNumbers: NotRequired[Sequence[Phase2DHGroupNumbersRequestListValueTypeDef]]
    IKEVersions: NotRequired[Sequence[IKEVersionsRequestListValueTypeDef]]
    StartupAction: NotRequired[str]
    LogOptions: NotRequired[VpnTunnelLogOptionsSpecificationTypeDef]
    EnableTunnelLifecycleControl: NotRequired[bool]


class TunnelOptionTypeDef(TypedDict):
    OutsideIpAddress: NotRequired[str]
    TunnelInsideCidr: NotRequired[str]
    TunnelInsideIpv6Cidr: NotRequired[str]
    PreSharedKey: NotRequired[str]
    Phase1LifetimeSeconds: NotRequired[int]
    Phase2LifetimeSeconds: NotRequired[int]
    RekeyMarginTimeSeconds: NotRequired[int]
    RekeyFuzzPercentage: NotRequired[int]
    ReplayWindowSize: NotRequired[int]
    DpdTimeoutSeconds: NotRequired[int]
    DpdTimeoutAction: NotRequired[str]
    Phase1EncryptionAlgorithms: NotRequired[list[Phase1EncryptionAlgorithmsListValueTypeDef]]
    Phase2EncryptionAlgorithms: NotRequired[list[Phase2EncryptionAlgorithmsListValueTypeDef]]
    Phase1IntegrityAlgorithms: NotRequired[list[Phase1IntegrityAlgorithmsListValueTypeDef]]
    Phase2IntegrityAlgorithms: NotRequired[list[Phase2IntegrityAlgorithmsListValueTypeDef]]
    Phase1DHGroupNumbers: NotRequired[list[Phase1DHGroupNumbersListValueTypeDef]]
    Phase2DHGroupNumbers: NotRequired[list[Phase2DHGroupNumbersListValueTypeDef]]
    IkeVersions: NotRequired[list[IKEVersionsListValueTypeDef]]
    StartupAction: NotRequired[str]
    LogOptions: NotRequired[VpnTunnelLogOptionsTypeDef]
    EnableTunnelLifecycleControl: NotRequired[bool]


class BaselinePerformanceFactorsOutputTypeDef(TypedDict):
    Cpu: NotRequired[CpuPerformanceFactorOutputTypeDef]


CpuPerformanceFactorUnionTypeDef = Union[
    CpuPerformanceFactorTypeDef, CpuPerformanceFactorOutputTypeDef
]


class BaselinePerformanceFactorsRequestTypeDef(TypedDict):
    Cpu: NotRequired[CpuPerformanceFactorRequestTypeDef]


class NetworkAclTypeDef(TypedDict):
    Associations: NotRequired[list[NetworkAclAssociationTypeDef]]
    Entries: NotRequired[list[NetworkAclEntryTypeDef]]
    IsDefault: NotRequired[bool]
    NetworkAclId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    VpcId: NotRequired[str]
    OwnerId: NotRequired[str]


class CreateVerifiedAccessEndpointRequestRequestTypeDef(TypedDict):
    VerifiedAccessGroupId: str
    EndpointType: VerifiedAccessEndpointTypeType
    AttachmentType: Literal["vpc"]
    DomainCertificateArn: NotRequired[str]
    ApplicationDomain: NotRequired[str]
    EndpointDomainPrefix: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    LoadBalancerOptions: NotRequired[CreateVerifiedAccessEndpointLoadBalancerOptionsTypeDef]
    NetworkInterfaceOptions: NotRequired[CreateVerifiedAccessEndpointEniOptionsTypeDef]
    Description: NotRequired[str]
    PolicyDocument: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationRequestTypeDef]
    RdsOptions: NotRequired[CreateVerifiedAccessEndpointRdsOptionsTypeDef]
    CidrOptions: NotRequired[CreateVerifiedAccessEndpointCidrOptionsTypeDef]


class ModifySnapshotAttributeRequestRequestTypeDef(TypedDict):
    SnapshotId: str
    Attribute: NotRequired[SnapshotAttributeNameType]
    CreateVolumePermission: NotRequired[CreateVolumePermissionModificationsTypeDef]
    GroupNames: NotRequired[Sequence[str]]
    OperationType: NotRequired[OperationTypeType]
    UserIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class ModifySnapshotAttributeRequestSnapshotModifyAttributeTypeDef(TypedDict):
    Attribute: NotRequired[SnapshotAttributeNameType]
    CreateVolumePermission: NotRequired[CreateVolumePermissionModificationsTypeDef]
    GroupNames: NotRequired[Sequence[str]]
    OperationType: NotRequired[OperationTypeType]
    UserIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class GetAwsNetworkPerformanceDataResultTypeDef(TypedDict):
    DataResponses: list[DataResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DeleteFleetsResultTypeDef(TypedDict):
    SuccessfulFleetDeletions: list[DeleteFleetSuccessItemTypeDef]
    UnsuccessfulFleetDeletions: list[DeleteFleetErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLaunchTemplateVersionsResultTypeDef(TypedDict):
    SuccessfullyDeletedLaunchTemplateVersions: list[
        DeleteLaunchTemplateVersionsResponseSuccessItemTypeDef
    ]
    UnsuccessfullyDeletedLaunchTemplateVersions: list[
        DeleteLaunchTemplateVersionsResponseErrorItemTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteQueuedReservedInstancesResultTypeDef(TypedDict):
    SuccessfulQueuedPurchaseDeletions: list[SuccessfulQueuedPurchaseDeletionTypeDef]
    FailedQueuedPurchaseDeletions: list[FailedQueuedPurchaseDeletionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePrincipalIdFormatResultTypeDef(TypedDict):
    Principals: list[PrincipalIdFormatTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFastLaunchImagesResultTypeDef(TypedDict):
    FastLaunchImages: list[DescribeFastLaunchImagesSuccessItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFlowLogsResultTypeDef(TypedDict):
    FlowLogs: list[FlowLogTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DisableFastSnapshotRestoreErrorItemTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    FastSnapshotRestoreStateErrors: NotRequired[
        list[DisableFastSnapshotRestoreStateErrorItemTypeDef]
    ]


class ImportInstanceTaskDetailsTypeDef(TypedDict):
    Description: NotRequired[str]
    InstanceId: NotRequired[str]
    Platform: NotRequired[Literal["windows"]]
    Volumes: NotRequired[list[ImportInstanceVolumeDetailItemTypeDef]]


class DescribeVpcEndpointAssociationsResultTypeDef(TypedDict):
    VpcEndpointAssociations: list[VpcEndpointAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeVpcEndpointConnectionsResultTypeDef(TypedDict):
    VpcEndpointConnections: list[VpcEndpointConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyInstanceAttributeRequestInstanceModifyAttributeTypeDef(TypedDict):
    SourceDestCheck: NotRequired[AttributeBooleanValueTypeDef]
    DisableApiStop: NotRequired[AttributeBooleanValueTypeDef]
    DryRun: NotRequired[bool]
    Attribute: NotRequired[InstanceAttributeNameType]
    Value: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[InstanceBlockDeviceMappingSpecificationTypeDef]]
    DisableApiTermination: NotRequired[AttributeBooleanValueTypeDef]
    InstanceType: NotRequired[AttributeValueTypeDef]
    Kernel: NotRequired[AttributeValueTypeDef]
    Ramdisk: NotRequired[AttributeValueTypeDef]
    UserData: NotRequired[BlobAttributeValueTypeDef]
    InstanceInitiatedShutdownBehavior: NotRequired[AttributeValueTypeDef]
    Groups: NotRequired[Sequence[str]]
    EbsOptimized: NotRequired[AttributeBooleanValueTypeDef]
    SriovNetSupport: NotRequired[AttributeValueTypeDef]
    EnaSupport: NotRequired[AttributeBooleanValueTypeDef]


class ModifyInstanceAttributeRequestRequestTypeDef(TypedDict):
    InstanceId: str
    SourceDestCheck: NotRequired[AttributeBooleanValueTypeDef]
    DisableApiStop: NotRequired[AttributeBooleanValueTypeDef]
    DryRun: NotRequired[bool]
    Attribute: NotRequired[InstanceAttributeNameType]
    Value: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[InstanceBlockDeviceMappingSpecificationTypeDef]]
    DisableApiTermination: NotRequired[AttributeBooleanValueTypeDef]
    InstanceType: NotRequired[AttributeValueTypeDef]
    Kernel: NotRequired[AttributeValueTypeDef]
    Ramdisk: NotRequired[AttributeValueTypeDef]
    UserData: NotRequired[BlobAttributeValueTypeDef]
    InstanceInitiatedShutdownBehavior: NotRequired[AttributeValueTypeDef]
    Groups: NotRequired[Sequence[str]]
    EbsOptimized: NotRequired[AttributeBooleanValueTypeDef]
    SriovNetSupport: NotRequired[AttributeValueTypeDef]
    EnaSupport: NotRequired[AttributeBooleanValueTypeDef]


class InstanceBlockDeviceMappingTypeDef(TypedDict):
    DeviceName: NotRequired[str]
    Ebs: NotRequired[EbsInstanceBlockDeviceTypeDef]


class DeleteLaunchTemplateResultTypeDef(TypedDict):
    LaunchTemplate: LaunchTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLaunchTemplatesResultTypeDef(TypedDict):
    LaunchTemplates: list[LaunchTemplateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyLaunchTemplateResultTypeDef(TypedDict):
    LaunchTemplate: LaunchTemplateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEgressOnlyInternetGatewayResultTypeDef(TypedDict):
    ClientToken: str
    EgressOnlyInternetGateway: EgressOnlyInternetGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEgressOnlyInternetGatewaysResultTypeDef(TypedDict):
    EgressOnlyInternetGateways: list[EgressOnlyInternetGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateInternetGatewayResultTypeDef(TypedDict):
    InternetGateway: InternetGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInternetGatewaysResultTypeDef(TypedDict):
    InternetGateways: list[InternetGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeElasticGpusResultTypeDef(TypedDict):
    ElasticGpuSet: list[ElasticGpusTypeDef]
    MaxResults: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceNetworkInterfaceSpecificationOutputTypeDef(TypedDict):
    AssociatePublicIpAddress: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Description: NotRequired[str]
    DeviceIndex: NotRequired[int]
    Groups: NotRequired[list[str]]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[list[InstanceIpv6AddressTypeDef]]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddresses: NotRequired[list[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    SubnetId: NotRequired[str]
    AssociateCarrierIpAddress: NotRequired[bool]
    InterfaceType: NotRequired[str]
    NetworkCardIndex: NotRequired[int]
    Ipv4Prefixes: NotRequired[list[Ipv4PrefixSpecificationRequestTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[list[Ipv6PrefixSpecificationRequestTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    PrimaryIpv6: NotRequired[bool]
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationRequestTypeDef]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]


class InstanceNetworkInterfaceSpecificationTypeDef(TypedDict):
    AssociatePublicIpAddress: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Description: NotRequired[str]
    DeviceIndex: NotRequired[int]
    Groups: NotRequired[Sequence[str]]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddresses: NotRequired[Sequence[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    SubnetId: NotRequired[str]
    AssociateCarrierIpAddress: NotRequired[bool]
    InterfaceType: NotRequired[str]
    NetworkCardIndex: NotRequired[int]
    Ipv4Prefixes: NotRequired[Sequence[Ipv4PrefixSpecificationRequestTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[Sequence[Ipv6PrefixSpecificationRequestTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    PrimaryIpv6: NotRequired[bool]
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationRequestTypeDef]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]


class LaunchTemplateInstanceNetworkInterfaceSpecificationRequestTypeDef(TypedDict):
    AssociateCarrierIpAddress: NotRequired[bool]
    AssociatePublicIpAddress: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Description: NotRequired[str]
    DeviceIndex: NotRequired[int]
    Groups: NotRequired[Sequence[str]]
    InterfaceType: NotRequired[str]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressRequestTypeDef]]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddresses: NotRequired[Sequence[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    SubnetId: NotRequired[str]
    NetworkCardIndex: NotRequired[int]
    Ipv4Prefixes: NotRequired[Sequence[Ipv4PrefixSpecificationRequestTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[Sequence[Ipv6PrefixSpecificationRequestTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    PrimaryIpv6: NotRequired[bool]
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationRequestTypeDef]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]


class AttachNetworkInterfaceRequestNetworkInterfaceAttachTypeDef(TypedDict):
    InstanceId: str
    DeviceIndex: int
    NetworkCardIndex: NotRequired[int]
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationTypeDef]
    DryRun: NotRequired[bool]


class AttachNetworkInterfaceRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    InstanceId: str
    DeviceIndex: int
    NetworkCardIndex: NotRequired[int]
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationTypeDef]
    DryRun: NotRequired[bool]


class ModifyNetworkInterfaceAttributeRequestNetworkInterfaceModifyAttributeTypeDef(TypedDict):
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationTypeDef]
    EnablePrimaryIpv6: NotRequired[bool]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]
    AssociatePublicIpAddress: NotRequired[bool]
    DryRun: NotRequired[bool]
    Description: NotRequired[AttributeValueTypeDef]
    SourceDestCheck: NotRequired[AttributeBooleanValueTypeDef]
    Groups: NotRequired[Sequence[str]]
    Attachment: NotRequired[NetworkInterfaceAttachmentChangesTypeDef]


class ModifyNetworkInterfaceAttributeRequestRequestTypeDef(TypedDict):
    NetworkInterfaceId: str
    EnaSrdSpecification: NotRequired[EnaSrdSpecificationTypeDef]
    EnablePrimaryIpv6: NotRequired[bool]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationRequestTypeDef]
    AssociatePublicIpAddress: NotRequired[bool]
    DryRun: NotRequired[bool]
    Description: NotRequired[AttributeValueTypeDef]
    SourceDestCheck: NotRequired[AttributeBooleanValueTypeDef]
    Groups: NotRequired[Sequence[str]]
    Attachment: NotRequired[NetworkInterfaceAttachmentChangesTypeDef]


class EnableFastSnapshotRestoreErrorItemTypeDef(TypedDict):
    SnapshotId: NotRequired[str]
    FastSnapshotRestoreStateErrors: NotRequired[
        list[EnableFastSnapshotRestoreStateErrorItemTypeDef]
    ]


class DescribeFleetHistoryResultTypeDef(TypedDict):
    HistoryRecords: list[HistoryRecordEntryTypeDef]
    LastEvaluatedTime: datetime
    FleetId: str
    StartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSpotFleetRequestHistoryResponseTypeDef(TypedDict):
    HistoryRecords: list[HistoryRecordTypeDef]
    LastEvaluatedTime: datetime
    SpotFleetRequestId: str
    StartTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeExportImageTasksResultTypeDef(TypedDict):
    ExportImageTasks: list[ExportImageTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateInstanceExportTaskResultTypeDef(TypedDict):
    ExportTask: ExportTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeExportTasksResultTypeDef(TypedDict):
    ExportTasks: list[ExportTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


NetworkInsightsPathTypeDef = TypedDict(
    "NetworkInsightsPathTypeDef",
    {
        "NetworkInsightsPathId": NotRequired[str],
        "NetworkInsightsPathArn": NotRequired[str],
        "CreatedDate": NotRequired[datetime],
        "Source": NotRequired[str],
        "Destination": NotRequired[str],
        "SourceArn": NotRequired[str],
        "DestinationArn": NotRequired[str],
        "SourceIp": NotRequired[str],
        "DestinationIp": NotRequired[str],
        "Protocol": NotRequired[ProtocolType],
        "DestinationPort": NotRequired[int],
        "Tags": NotRequired[list[TagTypeDef]],
        "FilterAtSource": NotRequired[PathFilterTypeDef],
        "FilterAtDestination": NotRequired[PathFilterTypeDef],
    },
)


class SpotOptionsRequestTypeDef(TypedDict):
    AllocationStrategy: NotRequired[SpotAllocationStrategyType]
    MaintenanceStrategies: NotRequired[FleetSpotMaintenanceStrategiesRequestTypeDef]
    InstanceInterruptionBehavior: NotRequired[SpotInstanceInterruptionBehaviorType]
    InstancePoolsToUseCount: NotRequired[int]
    SingleInstanceType: NotRequired[bool]
    SingleAvailabilityZone: NotRequired[bool]
    MinTargetCapacity: NotRequired[int]
    MaxTotalPrice: NotRequired[str]


class SpotOptionsTypeDef(TypedDict):
    AllocationStrategy: NotRequired[SpotAllocationStrategyType]
    MaintenanceStrategies: NotRequired[FleetSpotMaintenanceStrategiesTypeDef]
    InstanceInterruptionBehavior: NotRequired[SpotInstanceInterruptionBehaviorType]
    InstancePoolsToUseCount: NotRequired[int]
    SingleInstanceType: NotRequired[bool]
    SingleAvailabilityZone: NotRequired[bool]
    MinTargetCapacity: NotRequired[int]
    MaxTotalPrice: NotRequired[str]


class FpgaInfoTypeDef(TypedDict):
    Fpgas: NotRequired[list[FpgaDeviceInfoTypeDef]]
    TotalFpgaMemoryInMiB: NotRequired[int]


class DescribeFpgaImageAttributeResultTypeDef(TypedDict):
    FpgaImageAttribute: FpgaImageAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyFpgaImageAttributeResultTypeDef(TypedDict):
    FpgaImageAttribute: FpgaImageAttributeTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFpgaImagesResultTypeDef(TypedDict):
    FpgaImages: list[FpgaImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GpuInfoTypeDef(TypedDict):
    Gpus: NotRequired[list[GpuDeviceInfoTypeDef]]
    TotalGpuMemoryInMiB: NotRequired[int]


class AssociateIamInstanceProfileResultTypeDef(TypedDict):
    IamInstanceProfileAssociation: IamInstanceProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIamInstanceProfileAssociationsResultTypeDef(TypedDict):
    IamInstanceProfileAssociations: list[IamInstanceProfileAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DisassociateIamInstanceProfileResultTypeDef(TypedDict):
    IamInstanceProfileAssociation: IamInstanceProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReplaceIamInstanceProfileAssociationResultTypeDef(TypedDict):
    IamInstanceProfileAssociation: IamInstanceProfileAssociationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyImageAttributeRequestImageModifyAttributeTypeDef(TypedDict):
    Attribute: NotRequired[str]
    Description: NotRequired[AttributeValueTypeDef]
    LaunchPermission: NotRequired[LaunchPermissionModificationsTypeDef]
    OperationType: NotRequired[OperationTypeType]
    ProductCodes: NotRequired[Sequence[str]]
    UserGroups: NotRequired[Sequence[str]]
    UserIds: NotRequired[Sequence[str]]
    Value: NotRequired[str]
    OrganizationArns: NotRequired[Sequence[str]]
    OrganizationalUnitArns: NotRequired[Sequence[str]]
    ImdsSupport: NotRequired[AttributeValueTypeDef]
    DryRun: NotRequired[bool]


class ModifyImageAttributeRequestRequestTypeDef(TypedDict):
    ImageId: str
    Attribute: NotRequired[str]
    Description: NotRequired[AttributeValueTypeDef]
    LaunchPermission: NotRequired[LaunchPermissionModificationsTypeDef]
    OperationType: NotRequired[OperationTypeType]
    ProductCodes: NotRequired[Sequence[str]]
    UserGroups: NotRequired[Sequence[str]]
    UserIds: NotRequired[Sequence[str]]
    Value: NotRequired[str]
    OrganizationArns: NotRequired[Sequence[str]]
    OrganizationalUnitArns: NotRequired[Sequence[str]]
    ImdsSupport: NotRequired[AttributeValueTypeDef]
    DryRun: NotRequired[bool]


class ImportImageRequestRequestTypeDef(TypedDict):
    Architecture: NotRequired[str]
    ClientData: NotRequired[ClientDataTypeDef]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    DiskContainers: NotRequired[Sequence[ImageDiskContainerTypeDef]]
    DryRun: NotRequired[bool]
    Encrypted: NotRequired[bool]
    Hypervisor: NotRequired[str]
    KmsKeyId: NotRequired[str]
    LicenseType: NotRequired[str]
    Platform: NotRequired[str]
    RoleName: NotRequired[str]
    LicenseSpecifications: NotRequired[Sequence[ImportImageLicenseConfigurationRequestTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    UsageOperation: NotRequired[str]
    BootMode: NotRequired[BootModeValuesType]


class ImportSnapshotRequestRequestTypeDef(TypedDict):
    ClientData: NotRequired[ClientDataTypeDef]
    ClientToken: NotRequired[str]
    Description: NotRequired[str]
    DiskContainer: NotRequired[SnapshotDiskContainerTypeDef]
    DryRun: NotRequired[bool]
    Encrypted: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    RoleName: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateLocalGatewayRouteTableResultTypeDef(TypedDict):
    LocalGatewayRouteTable: LocalGatewayRouteTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteLocalGatewayRouteTableResultTypeDef(TypedDict):
    LocalGatewayRouteTable: LocalGatewayRouteTableTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLocalGatewayRouteTablesResultTypeDef(TypedDict):
    LocalGatewayRouteTables: list[LocalGatewayRouteTableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ImportInstanceRequestRequestTypeDef(TypedDict):
    Platform: Literal["windows"]
    DryRun: NotRequired[bool]
    Description: NotRequired[str]
    LaunchSpecification: NotRequired[ImportInstanceLaunchSpecificationTypeDef]
    DiskImages: NotRequired[Sequence[DiskImageTypeDef]]


class InferenceAcceleratorInfoTypeDef(TypedDict):
    Accelerators: NotRequired[list[InferenceDeviceInfoTypeDef]]
    TotalInferenceMemoryInMiB: NotRequired[int]


class InstanceNetworkInterfaceAttachmentTypeDef(TypedDict):
    AttachTime: NotRequired[datetime]
    AttachmentId: NotRequired[str]
    DeleteOnTermination: NotRequired[bool]
    DeviceIndex: NotRequired[int]
    Status: NotRequired[AttachmentStatusType]
    NetworkCardIndex: NotRequired[int]
    EnaSrdSpecification: NotRequired[InstanceAttachmentEnaSrdSpecificationTypeDef]


class DescribeInstanceImageMetadataResultTypeDef(TypedDict):
    InstanceImageMetadata: list[InstanceImageMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartInstancesResultTypeDef(TypedDict):
    StartingInstances: list[InstanceStateChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StopInstancesResultTypeDef(TypedDict):
    StoppingInstances: list[InstanceStateChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TerminateInstancesResultTypeDef(TypedDict):
    TerminatingInstances: list[InstanceStateChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class MonitorInstancesResultTypeDef(TypedDict):
    InstanceMonitorings: list[InstanceMonitoringTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UnmonitorInstancesResultTypeDef(TypedDict):
    InstanceMonitorings: list[InstanceMonitoringTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class InstanceStatusTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    OutpostArn: NotRequired[str]
    Operator: NotRequired[OperatorResponseTypeDef]
    Events: NotRequired[list[InstanceStatusEventTypeDef]]
    InstanceId: NotRequired[str]
    InstanceState: NotRequired[InstanceStateTypeDef]
    InstanceStatus: NotRequired[InstanceStatusSummaryTypeDef]
    SystemStatus: NotRequired[InstanceStatusSummaryTypeDef]
    AttachedEbsStatus: NotRequired[EbsStatusSummaryTypeDef]


class RevokeSecurityGroupEgressResultTypeDef(TypedDict):
    Return: bool
    UnknownIpPermissions: list[IpPermissionOutputTypeDef]
    RevokedSecurityGroupRules: list[RevokedSecurityGroupRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RevokeSecurityGroupIngressResultTypeDef(TypedDict):
    Return: bool
    UnknownIpPermissions: list[IpPermissionOutputTypeDef]
    RevokedSecurityGroupRules: list[RevokedSecurityGroupRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class SecurityGroupTypeDef(TypedDict):
    GroupId: NotRequired[str]
    IpPermissionsEgress: NotRequired[list[IpPermissionOutputTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    VpcId: NotRequired[str]
    SecurityGroupArn: NotRequired[str]
    OwnerId: NotRequired[str]
    GroupName: NotRequired[str]
    Description: NotRequired[str]
    IpPermissions: NotRequired[list[IpPermissionOutputTypeDef]]


class AuthorizeSecurityGroupEgressRequestSecurityGroupAuthorizeEgressTypeDef(TypedDict):
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIp: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]


class AuthorizeSecurityGroupIngressRequestRequestTypeDef(TypedDict):
    CidrIp: NotRequired[str]
    FromPort: NotRequired[int]
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    IpProtocol: NotRequired[str]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    ToPort: NotRequired[int]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class AuthorizeSecurityGroupIngressRequestSecurityGroupAuthorizeIngressTypeDef(TypedDict):
    CidrIp: NotRequired[str]
    FromPort: NotRequired[int]
    GroupName: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    IpProtocol: NotRequired[str]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    ToPort: NotRequired[int]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


IpPermissionUnionTypeDef = Union[IpPermissionTypeDef, IpPermissionOutputTypeDef]


class RevokeSecurityGroupEgressRequestRequestTypeDef(TypedDict):
    GroupId: str
    SecurityGroupRuleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIp: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]


class RevokeSecurityGroupEgressRequestSecurityGroupRevokeEgressTypeDef(TypedDict):
    SecurityGroupRuleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIp: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]


class RevokeSecurityGroupIngressRequestRequestTypeDef(TypedDict):
    CidrIp: NotRequired[str]
    FromPort: NotRequired[int]
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    IpProtocol: NotRequired[str]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    ToPort: NotRequired[int]
    SecurityGroupRuleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class RevokeSecurityGroupIngressRequestSecurityGroupRevokeIngressTypeDef(TypedDict):
    CidrIp: NotRequired[str]
    FromPort: NotRequired[int]
    GroupName: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    IpProtocol: NotRequired[str]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    ToPort: NotRequired[int]
    SecurityGroupRuleIds: NotRequired[Sequence[str]]
    DryRun: NotRequired[bool]


class UpdateSecurityGroupRuleDescriptionsEgressRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    SecurityGroupRuleDescriptions: NotRequired[Sequence[SecurityGroupRuleDescriptionTypeDef]]


class UpdateSecurityGroupRuleDescriptionsIngressRequestRequestTypeDef(TypedDict):
    DryRun: NotRequired[bool]
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionTypeDef]]
    SecurityGroupRuleDescriptions: NotRequired[Sequence[SecurityGroupRuleDescriptionTypeDef]]


class StaleSecurityGroupTypeDef(TypedDict):
    Description: NotRequired[str]
    GroupId: NotRequired[str]
    GroupName: NotRequired[str]
    StaleIpPermissions: NotRequired[list[StaleIpPermissionTypeDef]]
    StaleIpPermissionsEgress: NotRequired[list[StaleIpPermissionTypeDef]]
    VpcId: NotRequired[str]


class GetIpamDiscoveredAccountsResultTypeDef(TypedDict):
    IpamDiscoveredAccounts: list[IpamDiscoveredAccountTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetIpamDiscoveredResourceCidrsResultTypeDef(TypedDict):
    IpamDiscoveredResourceCidrs: list[IpamDiscoveredResourceCidrTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetIpamResourceCidrsResultTypeDef(TypedDict):
    IpamResourceCidrs: list[IpamResourceCidrTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyIpamResourceCidrResultTypeDef(TypedDict):
    IpamResourceCidr: IpamResourceCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIpamResultTypeDef(TypedDict):
    Ipam: IpamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIpamResultTypeDef(TypedDict):
    Ipam: IpamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamsResultTypeDef(TypedDict):
    Ipams: list[IpamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyIpamResultTypeDef(TypedDict):
    Ipam: IpamTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIpamResourceDiscoveryResultTypeDef(TypedDict):
    IpamResourceDiscovery: IpamResourceDiscoveryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIpamResourceDiscoveryResultTypeDef(TypedDict):
    IpamResourceDiscovery: IpamResourceDiscoveryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamResourceDiscoveriesResultTypeDef(TypedDict):
    IpamResourceDiscoveries: list[IpamResourceDiscoveryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyIpamResourceDiscoveryResultTypeDef(TypedDict):
    IpamResourceDiscovery: IpamResourceDiscoveryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeprovisionIpamPoolCidrResultTypeDef(TypedDict):
    IpamPoolCidr: IpamPoolCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIpamPoolCidrsResultTypeDef(TypedDict):
    IpamPoolCidrs: list[IpamPoolCidrTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ProvisionIpamPoolCidrResultTypeDef(TypedDict):
    IpamPoolCidr: IpamPoolCidrTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIpamPoolResultTypeDef(TypedDict):
    IpamPool: IpamPoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIpamPoolResultTypeDef(TypedDict):
    IpamPool: IpamPoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpamPoolsResultTypeDef(TypedDict):
    IpamPools: list[IpamPoolTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyIpamPoolResultTypeDef(TypedDict):
    IpamPool: IpamPoolTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class IpamDiscoveredPublicAddressTypeDef(TypedDict):
    IpamResourceDiscoveryId: NotRequired[str]
    AddressRegion: NotRequired[str]
    Address: NotRequired[str]
    AddressOwnerId: NotRequired[str]
    AddressAllocationId: NotRequired[str]
    AssociationStatus: NotRequired[IpamPublicAddressAssociationStatusType]
    AddressType: NotRequired[IpamPublicAddressTypeType]
    Service: NotRequired[IpamPublicAddressAwsServiceType]
    ServiceResource: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetId: NotRequired[str]
    PublicIpv4PoolId: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    NetworkInterfaceDescription: NotRequired[str]
    InstanceId: NotRequired[str]
    Tags: NotRequired[IpamPublicAddressTagsTypeDef]
    NetworkBorderGroup: NotRequired[str]
    SecurityGroups: NotRequired[list[IpamPublicAddressSecurityGroupTypeDef]]
    SampleTime: NotRequired[datetime]


class DescribeIpv6PoolsResultTypeDef(TypedDict):
    Ipv6Pools: list[Ipv6PoolTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LaunchTemplateInstanceNetworkInterfaceSpecificationTypeDef(TypedDict):
    AssociateCarrierIpAddress: NotRequired[bool]
    AssociatePublicIpAddress: NotRequired[bool]
    DeleteOnTermination: NotRequired[bool]
    Description: NotRequired[str]
    DeviceIndex: NotRequired[int]
    Groups: NotRequired[list[str]]
    InterfaceType: NotRequired[str]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[list[InstanceIpv6AddressTypeDef]]
    NetworkInterfaceId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddresses: NotRequired[list[PrivateIpAddressSpecificationTypeDef]]
    SecondaryPrivateIpAddressCount: NotRequired[int]
    SubnetId: NotRequired[str]
    NetworkCardIndex: NotRequired[int]
    Ipv4Prefixes: NotRequired[list[Ipv4PrefixSpecificationResponseTypeDef]]
    Ipv4PrefixCount: NotRequired[int]
    Ipv6Prefixes: NotRequired[list[Ipv6PrefixSpecificationResponseTypeDef]]
    Ipv6PrefixCount: NotRequired[int]
    PrimaryIpv6: NotRequired[bool]
    EnaSrdSpecification: NotRequired[LaunchTemplateEnaSrdSpecificationTypeDef]
    ConnectionTrackingSpecification: NotRequired[ConnectionTrackingSpecificationTypeDef]


class ModifyFpgaImageAttributeRequestRequestTypeDef(TypedDict):
    FpgaImageId: str
    DryRun: NotRequired[bool]
    Attribute: NotRequired[FpgaImageAttributeNameType]
    OperationType: NotRequired[OperationTypeType]
    UserIds: NotRequired[Sequence[str]]
    UserGroups: NotRequired[Sequence[str]]
    ProductCodes: NotRequired[Sequence[str]]
    LoadPermission: NotRequired[LoadPermissionModificationsTypeDef]
    Description: NotRequired[str]
    Name: NotRequired[str]


class MediaAcceleratorInfoTypeDef(TypedDict):
    Accelerators: NotRequired[list[MediaDeviceInfoTypeDef]]
    TotalMediaMemoryInMiB: NotRequired[int]


class ReservedInstancesModificationTypeDef(TypedDict):
    ClientToken: NotRequired[str]
    CreateDate: NotRequired[datetime]
    EffectiveDate: NotRequired[datetime]
    ModificationResults: NotRequired[list[ReservedInstancesModificationResultTypeDef]]
    ReservedInstancesIds: NotRequired[list[ReservedInstancesIdTypeDef]]
    ReservedInstancesModificationId: NotRequired[str]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    UpdateDate: NotRequired[datetime]


class ModifyVerifiedAccessEndpointRequestRequestTypeDef(TypedDict):
    VerifiedAccessEndpointId: str
    VerifiedAccessGroupId: NotRequired[str]
    LoadBalancerOptions: NotRequired[ModifyVerifiedAccessEndpointLoadBalancerOptionsTypeDef]
    NetworkInterfaceOptions: NotRequired[ModifyVerifiedAccessEndpointEniOptionsTypeDef]
    Description: NotRequired[str]
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    RdsOptions: NotRequired[ModifyVerifiedAccessEndpointRdsOptionsTypeDef]
    CidrOptions: NotRequired[ModifyVerifiedAccessEndpointCidrOptionsTypeDef]


class CreateVerifiedAccessGroupResultTypeDef(TypedDict):
    VerifiedAccessGroup: VerifiedAccessGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVerifiedAccessGroupResultTypeDef(TypedDict):
    VerifiedAccessGroup: VerifiedAccessGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVerifiedAccessGroupsResultTypeDef(TypedDict):
    VerifiedAccessGroups: list[VerifiedAccessGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVerifiedAccessGroupResultTypeDef(TypedDict):
    VerifiedAccessGroup: VerifiedAccessGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNatGatewayResultTypeDef(TypedDict):
    ClientToken: str
    NatGateway: NatGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNatGatewaysResultTypeDef(TypedDict):
    NatGateways: list[NatGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateNetworkInterfacePermissionResultTypeDef(TypedDict):
    InterfacePermission: NetworkInterfacePermissionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNetworkInterfacePermissionsResultTypeDef(TypedDict):
    NetworkInterfacePermissions: list[NetworkInterfacePermissionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class NeuronInfoTypeDef(TypedDict):
    NeuronDevices: NotRequired[list[NeuronDeviceInfoTypeDef]]
    TotalNeuronDeviceMemoryInMiB: NotRequired[int]


class CreateVerifiedAccessTrustProviderResultTypeDef(TypedDict):
    VerifiedAccessTrustProvider: VerifiedAccessTrustProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVerifiedAccessTrustProviderResultTypeDef(TypedDict):
    VerifiedAccessTrustProvider: VerifiedAccessTrustProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVerifiedAccessTrustProvidersResultTypeDef(TypedDict):
    VerifiedAccessTrustProviders: list[VerifiedAccessTrustProviderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVerifiedAccessTrustProviderResultTypeDef(TypedDict):
    VerifiedAccessTrustProvider: VerifiedAccessTrustProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreateNetworkInsightsPathRequestRequestTypeDef = TypedDict(
    "CreateNetworkInsightsPathRequestRequestTypeDef",
    {
        "Source": str,
        "Protocol": ProtocolType,
        "ClientToken": str,
        "SourceIp": NotRequired[str],
        "DestinationIp": NotRequired[str],
        "Destination": NotRequired[str],
        "DestinationPort": NotRequired[int],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "DryRun": NotRequired[bool],
        "FilterAtSource": NotRequired[PathRequestFilterTypeDef],
        "FilterAtDestination": NotRequired[PathRequestFilterTypeDef],
    },
)


class AccessScopePathRequestTypeDef(TypedDict):
    Source: NotRequired[PathStatementRequestTypeDef]
    Destination: NotRequired[PathStatementRequestTypeDef]
    ThroughResources: NotRequired[Sequence[ThroughResourcesStatementRequestTypeDef]]


class AccessScopePathTypeDef(TypedDict):
    Source: NotRequired[PathStatementTypeDef]
    Destination: NotRequired[PathStatementTypeDef]
    ThroughResources: NotRequired[list[ThroughResourcesStatementTypeDef]]


class CancelReservedInstancesListingResultTypeDef(TypedDict):
    ReservedInstancesListings: list[ReservedInstancesListingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReservedInstancesListingResultTypeDef(TypedDict):
    ReservedInstancesListings: list[ReservedInstancesListingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReservedInstancesListingsResultTypeDef(TypedDict):
    ReservedInstancesListings: list[ReservedInstancesListingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePublicIpv4PoolsResultTypeDef(TypedDict):
    PublicIpv4Pools: list[PublicIpv4PoolTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeReservedInstancesOfferingsResultTypeDef(TypedDict):
    ReservedInstancesOfferings: list[ReservedInstancesOfferingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeReservedInstancesResultTypeDef(TypedDict):
    ReservedInstances: list[ReservedInstancesTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AuthorizeSecurityGroupEgressResultTypeDef(TypedDict):
    Return: bool
    SecurityGroupRules: list[SecurityGroupRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AuthorizeSecurityGroupIngressResultTypeDef(TypedDict):
    Return: bool
    SecurityGroupRules: list[SecurityGroupRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSecurityGroupRulesResultTypeDef(TypedDict):
    SecurityGroupRules: list[SecurityGroupRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BundleTaskTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    BundleId: NotRequired[str]
    State: NotRequired[BundleTaskStateType]
    StartTime: NotRequired[datetime]
    UpdateTime: NotRequired[datetime]
    Storage: NotRequired[StorageOutputTypeDef]
    Progress: NotRequired[str]
    BundleTaskError: NotRequired[BundleTaskErrorTypeDef]


class DescribeScheduledInstanceAvailabilityResultTypeDef(TypedDict):
    ScheduledInstanceAvailabilitySet: list[ScheduledInstanceAvailabilityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeScheduledInstancesResultTypeDef(TypedDict):
    ScheduledInstanceSet: list[ScheduledInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PurchaseScheduledInstancesResultTypeDef(TypedDict):
    ScheduledInstanceSet: list[ScheduledInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ScheduledInstancesLaunchSpecificationTypeDef(TypedDict):
    ImageId: str
    BlockDeviceMappings: NotRequired[Sequence[ScheduledInstancesBlockDeviceMappingTypeDef]]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[ScheduledInstancesIamInstanceProfileTypeDef]
    InstanceType: NotRequired[str]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[ScheduledInstancesMonitoringTypeDef]
    NetworkInterfaces: NotRequired[Sequence[ScheduledInstancesNetworkInterfaceTypeDef]]
    Placement: NotRequired[ScheduledInstancesPlacementTypeDef]
    RamdiskId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SubnetId: NotRequired[str]
    UserData: NotRequired[str]


class ModifySecurityGroupRulesRequestRequestTypeDef(TypedDict):
    GroupId: str
    SecurityGroupRules: Sequence[SecurityGroupRuleUpdateTypeDef]
    DryRun: NotRequired[bool]


class DescribeVpcEndpointServicesResultTypeDef(TypedDict):
    ServiceNames: list[str]
    ServiceDetails: list[ServiceDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateVpcEndpointServiceConfigurationResultTypeDef(TypedDict):
    ServiceConfiguration: ServiceConfigurationTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcEndpointServiceConfigurationsResultTypeDef(TypedDict):
    ServiceConfigurations: list[ServiceConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ImportImageResultTypeDef(TypedDict):
    Architecture: str
    Description: str
    Encrypted: bool
    Hypervisor: str
    ImageId: str
    ImportTaskId: str
    KmsKeyId: str
    LicenseType: str
    Platform: str
    Progress: str
    SnapshotDetails: list[SnapshotDetailTypeDef]
    Status: str
    StatusMessage: str
    LicenseSpecifications: list[ImportImageLicenseConfigurationResponseTypeDef]
    Tags: list[TagTypeDef]
    UsageOperation: str
    ResponseMetadata: ResponseMetadataTypeDef


class ImportImageTaskTypeDef(TypedDict):
    Architecture: NotRequired[str]
    Description: NotRequired[str]
    Encrypted: NotRequired[bool]
    Hypervisor: NotRequired[str]
    ImageId: NotRequired[str]
    ImportTaskId: NotRequired[str]
    KmsKeyId: NotRequired[str]
    LicenseType: NotRequired[str]
    Platform: NotRequired[str]
    Progress: NotRequired[str]
    SnapshotDetails: NotRequired[list[SnapshotDetailTypeDef]]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    LicenseSpecifications: NotRequired[list[ImportImageLicenseConfigurationResponseTypeDef]]
    UsageOperation: NotRequired[str]
    BootMode: NotRequired[BootModeValuesType]


class ImportSnapshotResultTypeDef(TypedDict):
    Description: str
    ImportTaskId: str
    SnapshotTaskDetail: SnapshotTaskDetailTypeDef
    Tags: list[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImportSnapshotTaskTypeDef(TypedDict):
    Description: NotRequired[str]
    ImportTaskId: NotRequired[str]
    SnapshotTaskDetail: NotRequired[SnapshotTaskDetailTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class CreateSpotDatafeedSubscriptionResultTypeDef(TypedDict):
    SpotDatafeedSubscription: SpotDatafeedSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSpotDatafeedSubscriptionResultTypeDef(TypedDict):
    SpotDatafeedSubscription: SpotDatafeedSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayMulticastDomainAssociationsResultTypeDef(TypedDict):
    MulticastDomainAssociations: list[TransitGatewayMulticastDomainAssociationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AcceptTransitGatewayMulticastDomainAssociationsResultTypeDef(TypedDict):
    Associations: TransitGatewayMulticastDomainAssociationsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateTransitGatewayMulticastDomainResultTypeDef(TypedDict):
    Associations: TransitGatewayMulticastDomainAssociationsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateTransitGatewayMulticastDomainResultTypeDef(TypedDict):
    Associations: TransitGatewayMulticastDomainAssociationsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RejectTransitGatewayMulticastDomainAssociationsResultTypeDef(TypedDict):
    Associations: TransitGatewayMulticastDomainAssociationsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateSubnetCidrBlockResultTypeDef(TypedDict):
    Ipv6CidrBlockAssociation: SubnetIpv6CidrBlockAssociationTypeDef
    SubnetId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateSubnetCidrBlockResultTypeDef(TypedDict):
    Ipv6CidrBlockAssociation: SubnetIpv6CidrBlockAssociationTypeDef
    SubnetId: str
    ResponseMetadata: ResponseMetadataTypeDef


class SubnetTypeDef(TypedDict):
    AvailabilityZoneId: NotRequired[str]
    EnableLniAtDeviceIndex: NotRequired[int]
    MapCustomerOwnedIpOnLaunch: NotRequired[bool]
    CustomerOwnedIpv4Pool: NotRequired[str]
    OwnerId: NotRequired[str]
    AssignIpv6AddressOnCreation: NotRequired[bool]
    Ipv6CidrBlockAssociationSet: NotRequired[list[SubnetIpv6CidrBlockAssociationTypeDef]]
    Tags: NotRequired[list[TagTypeDef]]
    SubnetArn: NotRequired[str]
    OutpostArn: NotRequired[str]
    EnableDns64: NotRequired[bool]
    Ipv6Native: NotRequired[bool]
    PrivateDnsNameOptionsOnLaunch: NotRequired[PrivateDnsNameOptionsOnLaunchTypeDef]
    BlockPublicAccessStates: NotRequired[BlockPublicAccessStatesTypeDef]
    SubnetId: NotRequired[str]
    State: NotRequired[SubnetStateType]
    VpcId: NotRequired[str]
    CidrBlock: NotRequired[str]
    AvailableIpAddressCount: NotRequired[int]
    AvailabilityZone: NotRequired[str]
    DefaultForAz: NotRequired[bool]
    MapPublicIpOnLaunch: NotRequired[bool]


class CreateVpcEndpointResultTypeDef(TypedDict):
    VpcEndpoint: VpcEndpointTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcEndpointsResultTypeDef(TypedDict):
    VpcEndpoints: list[VpcEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetReservedInstancesExchangeQuoteResultTypeDef(TypedDict):
    CurrencyCode: str
    IsValidExchange: bool
    OutputReservedInstancesWillExpireAt: datetime
    PaymentDue: str
    ReservedInstanceValueRollup: ReservationValueTypeDef
    ReservedInstanceValueSet: list[ReservedInstanceReservationValueTypeDef]
    TargetConfigurationValueRollup: ReservationValueTypeDef
    TargetConfigurationValueSet: list[TargetReservationValueTypeDef]
    ValidationFailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class LoadBalancersConfigOutputTypeDef(TypedDict):
    ClassicLoadBalancersConfig: NotRequired[ClassicLoadBalancersConfigOutputTypeDef]
    TargetGroupsConfig: NotRequired[TargetGroupsConfigOutputTypeDef]


TargetGroupsConfigUnionTypeDef = Union[TargetGroupsConfigTypeDef, TargetGroupsConfigOutputTypeDef]


class CreateTrafficMirrorFilterRuleResultTypeDef(TypedDict):
    TrafficMirrorFilterRule: TrafficMirrorFilterRuleTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrafficMirrorFilterRulesResultTypeDef(TypedDict):
    TrafficMirrorFilterRules: list[TrafficMirrorFilterRuleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyTrafficMirrorFilterRuleResultTypeDef(TypedDict):
    TrafficMirrorFilterRule: TrafficMirrorFilterRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TrafficMirrorFilterTypeDef(TypedDict):
    TrafficMirrorFilterId: NotRequired[str]
    IngressFilterRules: NotRequired[list[TrafficMirrorFilterRuleTypeDef]]
    EgressFilterRules: NotRequired[list[TrafficMirrorFilterRuleTypeDef]]
    NetworkServices: NotRequired[list[Literal["amazon-dns"]]]
    Description: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class DescribeTransitGatewayAttachmentsResultTypeDef(TypedDict):
    TransitGatewayAttachments: list[TransitGatewayAttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class TransitGatewayConnectPeerTypeDef(TypedDict):
    TransitGatewayAttachmentId: NotRequired[str]
    TransitGatewayConnectPeerId: NotRequired[str]
    State: NotRequired[TransitGatewayConnectPeerStateType]
    CreationTime: NotRequired[datetime]
    ConnectPeerConfiguration: NotRequired[TransitGatewayConnectPeerConfigurationTypeDef]
    Tags: NotRequired[list[TagTypeDef]]


class CreateTransitGatewayConnectResultTypeDef(TypedDict):
    TransitGatewayConnect: TransitGatewayConnectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayConnectResultTypeDef(TypedDict):
    TransitGatewayConnect: TransitGatewayConnectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayConnectsResultTypeDef(TypedDict):
    TransitGatewayConnects: list[TransitGatewayConnectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateTransitGatewayMulticastDomainResultTypeDef(TypedDict):
    TransitGatewayMulticastDomain: TransitGatewayMulticastDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayMulticastDomainResultTypeDef(TypedDict):
    TransitGatewayMulticastDomain: TransitGatewayMulticastDomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayMulticastDomainsResultTypeDef(TypedDict):
    TransitGatewayMulticastDomains: list[TransitGatewayMulticastDomainTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateTransitGatewayResultTypeDef(TypedDict):
    TransitGateway: TransitGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayResultTypeDef(TypedDict):
    TransitGateway: TransitGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewaysResultTypeDef(TypedDict):
    TransitGateways: list[TransitGatewayTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyTransitGatewayResultTypeDef(TypedDict):
    TransitGateway: TransitGatewayTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptTransitGatewayPeeringAttachmentResultTypeDef(TypedDict):
    TransitGatewayPeeringAttachment: TransitGatewayPeeringAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransitGatewayPeeringAttachmentResultTypeDef(TypedDict):
    TransitGatewayPeeringAttachment: TransitGatewayPeeringAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayPeeringAttachmentResultTypeDef(TypedDict):
    TransitGatewayPeeringAttachment: TransitGatewayPeeringAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayPeeringAttachmentsResultTypeDef(TypedDict):
    TransitGatewayPeeringAttachments: list[TransitGatewayPeeringAttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RejectTransitGatewayPeeringAttachmentResultTypeDef(TypedDict):
    TransitGatewayPeeringAttachment: TransitGatewayPeeringAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class TransitGatewayPolicyTableEntryTypeDef(TypedDict):
    PolicyRuleNumber: NotRequired[str]
    PolicyRule: NotRequired[TransitGatewayPolicyRuleTypeDef]
    TargetRouteTableId: NotRequired[str]


class CreateTransitGatewayPrefixListReferenceResultTypeDef(TypedDict):
    TransitGatewayPrefixListReference: TransitGatewayPrefixListReferenceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayPrefixListReferenceResultTypeDef(TypedDict):
    TransitGatewayPrefixListReference: TransitGatewayPrefixListReferenceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTransitGatewayPrefixListReferencesResultTypeDef(TypedDict):
    TransitGatewayPrefixListReferences: list[TransitGatewayPrefixListReferenceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyTransitGatewayPrefixListReferenceResultTypeDef(TypedDict):
    TransitGatewayPrefixListReference: TransitGatewayPrefixListReferenceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransitGatewayRouteResultTypeDef(TypedDict):
    Route: TransitGatewayRouteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayRouteResultTypeDef(TypedDict):
    Route: TransitGatewayRouteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReplaceTransitGatewayRouteResultTypeDef(TypedDict):
    Route: TransitGatewayRouteTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class SearchTransitGatewayRoutesResultTypeDef(TypedDict):
    Routes: list[TransitGatewayRouteTypeDef]
    AdditionalRoutesAvailable: bool
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptTransitGatewayVpcAttachmentResultTypeDef(TypedDict):
    TransitGatewayVpcAttachment: TransitGatewayVpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransitGatewayVpcAttachmentResultTypeDef(TypedDict):
    TransitGatewayVpcAttachment: TransitGatewayVpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayVpcAttachmentResultTypeDef(TypedDict):
    TransitGatewayVpcAttachment: TransitGatewayVpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayVpcAttachmentsResultTypeDef(TypedDict):
    TransitGatewayVpcAttachments: list[TransitGatewayVpcAttachmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyTransitGatewayVpcAttachmentResultTypeDef(TypedDict):
    TransitGatewayVpcAttachment: TransitGatewayVpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RejectTransitGatewayVpcAttachmentResultTypeDef(TypedDict):
    TransitGatewayVpcAttachment: TransitGatewayVpcAttachmentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceCreditSpecificationResultTypeDef(TypedDict):
    SuccessfulInstanceCreditSpecifications: list[SuccessfulInstanceCreditSpecificationItemTypeDef]
    UnsuccessfulInstanceCreditSpecifications: list[
        UnsuccessfulInstanceCreditSpecificationItemTypeDef
    ]
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptVpcEndpointConnectionsResultTypeDef(TypedDict):
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFlowLogsResultTypeDef(TypedDict):
    ClientToken: str
    FlowLogIds: list[str]
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFlowLogsResultTypeDef(TypedDict):
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcEndpointConnectionNotificationsResultTypeDef(TypedDict):
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcEndpointServiceConfigurationsResultTypeDef(TypedDict):
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcEndpointsResultTypeDef(TypedDict):
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyHostsResultTypeDef(TypedDict):
    Successful: list[str]
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RejectVpcEndpointConnectionsResultTypeDef(TypedDict):
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ReleaseHostsResultTypeDef(TypedDict):
    Successful: list[str]
    Unsuccessful: list[UnsuccessfulItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


CreateLaunchTemplateResultTypeDef = TypedDict(
    "CreateLaunchTemplateResultTypeDef",
    {
        "LaunchTemplate": LaunchTemplateTypeDef,
        "Warning": ValidationWarningTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class VerifiedAccessEndpointTypeDef(TypedDict):
    VerifiedAccessInstanceId: NotRequired[str]
    VerifiedAccessGroupId: NotRequired[str]
    VerifiedAccessEndpointId: NotRequired[str]
    ApplicationDomain: NotRequired[str]
    EndpointType: NotRequired[VerifiedAccessEndpointTypeType]
    AttachmentType: NotRequired[Literal["vpc"]]
    DomainCertificateArn: NotRequired[str]
    EndpointDomain: NotRequired[str]
    DeviceValidationDomain: NotRequired[str]
    SecurityGroupIds: NotRequired[list[str]]
    LoadBalancerOptions: NotRequired[VerifiedAccessEndpointLoadBalancerOptionsTypeDef]
    NetworkInterfaceOptions: NotRequired[VerifiedAccessEndpointEniOptionsTypeDef]
    Status: NotRequired[VerifiedAccessEndpointStatusTypeDef]
    Description: NotRequired[str]
    CreationTime: NotRequired[str]
    LastUpdatedTime: NotRequired[str]
    DeletionTime: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]
    SseSpecification: NotRequired[VerifiedAccessSseSpecificationResponseTypeDef]
    RdsOptions: NotRequired[VerifiedAccessEndpointRdsOptionsTypeDef]
    CidrOptions: NotRequired[VerifiedAccessEndpointCidrOptionsTypeDef]


class ExportVerifiedAccessInstanceClientConfigurationResultTypeDef(TypedDict):
    Version: str
    VerifiedAccessInstanceId: str
    Region: str
    DeviceTrustProviders: list[DeviceTrustProviderTypeType]
    UserTrustProvider: VerifiedAccessInstanceUserTrustProviderClientConfigurationTypeDef
    OpenVpnConfigurations: list[VerifiedAccessInstanceOpenVpnClientConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachVerifiedAccessTrustProviderResultTypeDef(TypedDict):
    VerifiedAccessTrustProvider: VerifiedAccessTrustProviderTypeDef
    VerifiedAccessInstance: VerifiedAccessInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVerifiedAccessInstanceResultTypeDef(TypedDict):
    VerifiedAccessInstance: VerifiedAccessInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVerifiedAccessInstanceResultTypeDef(TypedDict):
    VerifiedAccessInstance: VerifiedAccessInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVerifiedAccessInstancesResultTypeDef(TypedDict):
    VerifiedAccessInstances: list[VerifiedAccessInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DetachVerifiedAccessTrustProviderResultTypeDef(TypedDict):
    VerifiedAccessTrustProvider: VerifiedAccessTrustProviderTypeDef
    VerifiedAccessInstance: VerifiedAccessInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVerifiedAccessInstanceResultTypeDef(TypedDict):
    VerifiedAccessInstance: VerifiedAccessInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VerifiedAccessLogsTypeDef(TypedDict):
    S3: NotRequired[VerifiedAccessLogS3DestinationTypeDef]
    CloudWatchLogs: NotRequired[VerifiedAccessLogCloudWatchLogsDestinationTypeDef]
    KinesisDataFirehose: NotRequired[VerifiedAccessLogKinesisDataFirehoseDestinationTypeDef]
    LogVersion: NotRequired[str]
    IncludeTrustContext: NotRequired[bool]


class ModifyVerifiedAccessInstanceLoggingConfigurationRequestRequestTypeDef(TypedDict):
    VerifiedAccessInstanceId: str
    AccessLogs: VerifiedAccessLogOptionsTypeDef
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]


class DescribeVolumesResultTypeDef(TypedDict):
    Volumes: list[VolumeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class VolumeStatusItemTypeDef(TypedDict):
    Actions: NotRequired[list[VolumeStatusActionTypeDef]]
    AvailabilityZone: NotRequired[str]
    OutpostArn: NotRequired[str]
    Events: NotRequired[list[VolumeStatusEventTypeDef]]
    VolumeId: NotRequired[str]
    VolumeStatus: NotRequired[VolumeStatusInfoTypeDef]
    AttachmentStatuses: NotRequired[list[VolumeStatusAttachmentStatusTypeDef]]


class AssociateVpcCidrBlockResultTypeDef(TypedDict):
    Ipv6CidrBlockAssociation: VpcIpv6CidrBlockAssociationTypeDef
    CidrBlockAssociation: VpcCidrBlockAssociationTypeDef
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateVpcCidrBlockResultTypeDef(TypedDict):
    Ipv6CidrBlockAssociation: VpcIpv6CidrBlockAssociationTypeDef
    CidrBlockAssociation: VpcCidrBlockAssociationTypeDef
    VpcId: str
    ResponseMetadata: ResponseMetadataTypeDef


class VpcTypeDef(TypedDict):
    OwnerId: NotRequired[str]
    InstanceTenancy: NotRequired[TenancyType]
    Ipv6CidrBlockAssociationSet: NotRequired[list[VpcIpv6CidrBlockAssociationTypeDef]]
    CidrBlockAssociationSet: NotRequired[list[VpcCidrBlockAssociationTypeDef]]
    IsDefault: NotRequired[bool]
    Tags: NotRequired[list[TagTypeDef]]
    BlockPublicAccessStates: NotRequired[BlockPublicAccessStatesTypeDef]
    VpcId: NotRequired[str]
    State: NotRequired[VpcStateType]
    CidrBlock: NotRequired[str]
    DhcpOptionsId: NotRequired[str]


class VpcPeeringConnectionTypeDef(TypedDict):
    AccepterVpcInfo: NotRequired[VpcPeeringConnectionVpcInfoTypeDef]
    ExpirationTime: NotRequired[datetime]
    RequesterVpcInfo: NotRequired[VpcPeeringConnectionVpcInfoTypeDef]
    Status: NotRequired[VpcPeeringConnectionStateReasonTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    VpcPeeringConnectionId: NotRequired[str]


class AssociateInstanceEventWindowResultTypeDef(TypedDict):
    InstanceEventWindow: InstanceEventWindowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInstanceEventWindowResultTypeDef(TypedDict):
    InstanceEventWindow: InstanceEventWindowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInstanceEventWindowsResultTypeDef(TypedDict):
    InstanceEventWindows: list[InstanceEventWindowTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DisassociateInstanceEventWindowResultTypeDef(TypedDict):
    InstanceEventWindow: InstanceEventWindowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceEventWindowResultTypeDef(TypedDict):
    InstanceEventWindow: InstanceEventWindowTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AcceptAddressTransferRequestRequestTypeDef(TypedDict):
    Address: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationUnionTypeDef]]
    DryRun: NotRequired[bool]


PathComponentTypeDef = TypedDict(
    "PathComponentTypeDef",
    {
        "SequenceNumber": NotRequired[int],
        "AclRule": NotRequired[AnalysisAclRuleTypeDef],
        "AttachedTo": NotRequired[AnalysisComponentTypeDef],
        "Component": NotRequired[AnalysisComponentTypeDef],
        "DestinationVpc": NotRequired[AnalysisComponentTypeDef],
        "OutboundHeader": NotRequired[AnalysisPacketHeaderTypeDef],
        "InboundHeader": NotRequired[AnalysisPacketHeaderTypeDef],
        "RouteTableRoute": NotRequired[AnalysisRouteTableRouteTypeDef],
        "SecurityGroupRule": NotRequired[AnalysisSecurityGroupRuleTypeDef],
        "SourceVpc": NotRequired[AnalysisComponentTypeDef],
        "Subnet": NotRequired[AnalysisComponentTypeDef],
        "Vpc": NotRequired[AnalysisComponentTypeDef],
        "AdditionalDetails": NotRequired[list[AdditionalDetailTypeDef]],
        "TransitGateway": NotRequired[AnalysisComponentTypeDef],
        "TransitGatewayRouteTableRoute": NotRequired[TransitGatewayRouteTableRouteTypeDef],
        "Explanations": NotRequired[list[ExplanationTypeDef]],
        "ElasticLoadBalancerListener": NotRequired[AnalysisComponentTypeDef],
        "FirewallStatelessRule": NotRequired[FirewallStatelessRuleTypeDef],
        "FirewallStatefulRule": NotRequired[FirewallStatefulRuleTypeDef],
        "ServiceName": NotRequired[str],
    },
)


class CreateRouteTableResultTypeDef(TypedDict):
    RouteTable: RouteTableTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRouteTablesResultTypeDef(TypedDict):
    RouteTables: list[RouteTableTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetFlowLogsIntegrationTemplateRequestRequestTypeDef(TypedDict):
    FlowLogId: str
    ConfigDeliveryS3DestinationArn: str
    IntegrateServices: IntegrateServicesTypeDef
    DryRun: NotRequired[bool]


class DescribeNetworkInterfaceAttributeResultTypeDef(TypedDict):
    Attachment: NetworkInterfaceAttachmentTypeDef
    Description: AttributeValueTypeDef
    Groups: list[GroupIdentifierTypeDef]
    NetworkInterfaceId: str
    SourceDestCheck: AttributeBooleanValueTypeDef
    AssociatePublicIpAddress: bool
    ResponseMetadata: ResponseMetadataTypeDef


class NetworkInterfaceTypeDef(TypedDict):
    Association: NotRequired[NetworkInterfaceAssociationTypeDef]
    Attachment: NotRequired[NetworkInterfaceAttachmentTypeDef]
    AvailabilityZone: NotRequired[str]
    ConnectionTrackingConfiguration: NotRequired[ConnectionTrackingConfigurationTypeDef]
    Description: NotRequired[str]
    Groups: NotRequired[list[GroupIdentifierTypeDef]]
    InterfaceType: NotRequired[NetworkInterfaceTypeType]
    Ipv6Addresses: NotRequired[list[NetworkInterfaceIpv6AddressTypeDef]]
    MacAddress: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    OutpostArn: NotRequired[str]
    OwnerId: NotRequired[str]
    PrivateDnsName: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddresses: NotRequired[list[NetworkInterfacePrivateIpAddressTypeDef]]
    Ipv4Prefixes: NotRequired[list[Ipv4PrefixSpecificationTypeDef]]
    Ipv6Prefixes: NotRequired[list[Ipv6PrefixSpecificationTypeDef]]
    RequesterId: NotRequired[str]
    RequesterManaged: NotRequired[bool]
    SourceDestCheck: NotRequired[bool]
    Status: NotRequired[NetworkInterfaceStatusType]
    SubnetId: NotRequired[str]
    TagSet: NotRequired[list[TagTypeDef]]
    VpcId: NotRequired[str]
    DenyAllIgwTraffic: NotRequired[bool]
    Ipv6Native: NotRequired[bool]
    Ipv6Address: NotRequired[str]
    Operator: NotRequired[OperatorResponseTypeDef]


class CreateDhcpOptionsResultTypeDef(TypedDict):
    DhcpOptions: DhcpOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDhcpOptionsResultTypeDef(TypedDict):
    DhcpOptions: list[DhcpOptionsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeHostsResultTypeDef(TypedDict):
    Hosts: list[HostTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StorageTypeDef(TypedDict):
    S3: NotRequired[S3StorageUnionTypeDef]


class DescribeImagesResultTypeDef(TypedDict):
    Images: list[ImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeClientVpnEndpointsResultTypeDef(TypedDict):
    ClientVpnEndpoints: list[ClientVpnEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVpnTunnelOptionsRequestRequestTypeDef(TypedDict):
    VpnConnectionId: str
    VpnTunnelOutsideIpAddress: str
    TunnelOptions: ModifyVpnTunnelOptionsSpecificationTypeDef
    DryRun: NotRequired[bool]
    SkipTunnelReplacement: NotRequired[bool]


class VpnConnectionOptionsSpecificationTypeDef(TypedDict):
    EnableAcceleration: NotRequired[bool]
    TunnelInsideIpVersion: NotRequired[TunnelInsideIpVersionType]
    TunnelOptions: NotRequired[Sequence[VpnTunnelOptionsSpecificationTypeDef]]
    LocalIpv4NetworkCidr: NotRequired[str]
    RemoteIpv4NetworkCidr: NotRequired[str]
    LocalIpv6NetworkCidr: NotRequired[str]
    RemoteIpv6NetworkCidr: NotRequired[str]
    OutsideIpAddressType: NotRequired[str]
    TransportTransitGatewayAttachmentId: NotRequired[str]
    StaticRoutesOnly: NotRequired[bool]


class VpnConnectionOptionsTypeDef(TypedDict):
    EnableAcceleration: NotRequired[bool]
    StaticRoutesOnly: NotRequired[bool]
    LocalIpv4NetworkCidr: NotRequired[str]
    RemoteIpv4NetworkCidr: NotRequired[str]
    LocalIpv6NetworkCidr: NotRequired[str]
    RemoteIpv6NetworkCidr: NotRequired[str]
    OutsideIpAddressType: NotRequired[str]
    TransportTransitGatewayAttachmentId: NotRequired[str]
    TunnelInsideIpVersion: NotRequired[TunnelInsideIpVersionType]
    TunnelOptions: NotRequired[list[TunnelOptionTypeDef]]


class InstanceRequirementsOutputTypeDef(TypedDict):
    VCpuCount: NotRequired[VCpuCountRangeTypeDef]
    MemoryMiB: NotRequired[MemoryMiBTypeDef]
    CpuManufacturers: NotRequired[list[CpuManufacturerType]]
    MemoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuTypeDef]
    ExcludedInstanceTypes: NotRequired[list[str]]
    InstanceGenerations: NotRequired[list[InstanceGenerationType]]
    SpotMaxPricePercentageOverLowestPrice: NotRequired[int]
    OnDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    BareMetal: NotRequired[BareMetalType]
    BurstablePerformance: NotRequired[BurstablePerformanceType]
    RequireHibernateSupport: NotRequired[bool]
    NetworkInterfaceCount: NotRequired[NetworkInterfaceCountTypeDef]
    LocalStorage: NotRequired[LocalStorageType]
    LocalStorageTypes: NotRequired[list[LocalStorageTypeType]]
    TotalLocalStorageGB: NotRequired[TotalLocalStorageGBTypeDef]
    BaselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsTypeDef]
    AcceleratorTypes: NotRequired[list[AcceleratorTypeType]]
    AcceleratorCount: NotRequired[AcceleratorCountTypeDef]
    AcceleratorManufacturers: NotRequired[list[AcceleratorManufacturerType]]
    AcceleratorNames: NotRequired[list[AcceleratorNameType]]
    AcceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBTypeDef]
    NetworkBandwidthGbps: NotRequired[NetworkBandwidthGbpsTypeDef]
    AllowedInstanceTypes: NotRequired[list[str]]
    MaxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]
    BaselinePerformanceFactors: NotRequired[BaselinePerformanceFactorsOutputTypeDef]


class BaselinePerformanceFactorsTypeDef(TypedDict):
    Cpu: NotRequired[CpuPerformanceFactorUnionTypeDef]


class InstanceRequirementsRequestTypeDef(TypedDict):
    VCpuCount: VCpuCountRangeRequestTypeDef
    MemoryMiB: MemoryMiBRequestTypeDef
    CpuManufacturers: NotRequired[Sequence[CpuManufacturerType]]
    MemoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuRequestTypeDef]
    ExcludedInstanceTypes: NotRequired[Sequence[str]]
    InstanceGenerations: NotRequired[Sequence[InstanceGenerationType]]
    SpotMaxPricePercentageOverLowestPrice: NotRequired[int]
    OnDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    BareMetal: NotRequired[BareMetalType]
    BurstablePerformance: NotRequired[BurstablePerformanceType]
    RequireHibernateSupport: NotRequired[bool]
    NetworkInterfaceCount: NotRequired[NetworkInterfaceCountRequestTypeDef]
    LocalStorage: NotRequired[LocalStorageType]
    LocalStorageTypes: NotRequired[Sequence[LocalStorageTypeType]]
    TotalLocalStorageGB: NotRequired[TotalLocalStorageGBRequestTypeDef]
    BaselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsRequestTypeDef]
    AcceleratorTypes: NotRequired[Sequence[AcceleratorTypeType]]
    AcceleratorCount: NotRequired[AcceleratorCountRequestTypeDef]
    AcceleratorManufacturers: NotRequired[Sequence[AcceleratorManufacturerType]]
    AcceleratorNames: NotRequired[Sequence[AcceleratorNameType]]
    AcceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBRequestTypeDef]
    NetworkBandwidthGbps: NotRequired[NetworkBandwidthGbpsRequestTypeDef]
    AllowedInstanceTypes: NotRequired[Sequence[str]]
    MaxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]
    BaselinePerformanceFactors: NotRequired[BaselinePerformanceFactorsRequestTypeDef]


class CreateNetworkAclResultTypeDef(TypedDict):
    NetworkAcl: NetworkAclTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNetworkAclsResultTypeDef(TypedDict):
    NetworkAcls: list[NetworkAclTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DisableFastSnapshotRestoresResultTypeDef(TypedDict):
    Successful: list[DisableFastSnapshotRestoreSuccessItemTypeDef]
    Unsuccessful: list[DisableFastSnapshotRestoreErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ConversionTaskTypeDef(TypedDict):
    ConversionTaskId: NotRequired[str]
    ExpirationTime: NotRequired[str]
    ImportInstance: NotRequired[ImportInstanceTaskDetailsTypeDef]
    ImportVolume: NotRequired[ImportVolumeTaskDetailsTypeDef]
    State: NotRequired[ConversionTaskStateType]
    StatusMessage: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class InstanceAttributeTypeDef(TypedDict):
    BlockDeviceMappings: list[InstanceBlockDeviceMappingTypeDef]
    DisableApiTermination: AttributeBooleanValueTypeDef
    EnaSupport: AttributeBooleanValueTypeDef
    EnclaveOptions: EnclaveOptionsTypeDef
    EbsOptimized: AttributeBooleanValueTypeDef
    InstanceId: str
    InstanceInitiatedShutdownBehavior: AttributeValueTypeDef
    InstanceType: AttributeValueTypeDef
    KernelId: AttributeValueTypeDef
    ProductCodes: list[ProductCodeTypeDef]
    RamdiskId: AttributeValueTypeDef
    RootDeviceName: AttributeValueTypeDef
    SourceDestCheck: AttributeBooleanValueTypeDef
    SriovNetSupport: AttributeValueTypeDef
    UserData: AttributeValueTypeDef
    DisableApiStop: AttributeBooleanValueTypeDef
    Groups: list[GroupIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class LaunchSpecificationTypeDef(TypedDict):
    UserData: NotRequired[str]
    AddressingType: NotRequired[str]
    BlockDeviceMappings: NotRequired[list[BlockDeviceMappingTypeDef]]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    NetworkInterfaces: NotRequired[list[InstanceNetworkInterfaceSpecificationOutputTypeDef]]
    Placement: NotRequired[SpotPlacementTypeDef]
    RamdiskId: NotRequired[str]
    SubnetId: NotRequired[str]
    SecurityGroups: NotRequired[list[GroupIdentifierTypeDef]]
    Monitoring: NotRequired[RunInstancesMonitoringEnabledTypeDef]


InstanceNetworkInterfaceSpecificationUnionTypeDef = Union[
    InstanceNetworkInterfaceSpecificationTypeDef, InstanceNetworkInterfaceSpecificationOutputTypeDef
]


class RunInstancesRequestServiceResourceCreateInstancesTypeDef(TypedDict):
    MaxCount: int
    MinCount: int
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[RunInstancesMonitoringEnabledTypeDef]
    Placement: NotRequired[PlacementTypeDef]
    RamdiskId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    SubnetId: NotRequired[str]
    UserData: NotRequired[str]
    ElasticGpuSpecification: NotRequired[Sequence[ElasticGpuSpecificationTypeDef]]
    ElasticInferenceAccelerators: NotRequired[Sequence[ElasticInferenceAcceleratorTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    InstanceMarketOptions: NotRequired[InstanceMarketOptionsRequestTypeDef]
    CreditSpecification: NotRequired[CreditSpecificationRequestTypeDef]
    CpuOptions: NotRequired[CpuOptionsRequestTypeDef]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationTypeDef]
    HibernationOptions: NotRequired[HibernationOptionsRequestTypeDef]
    LicenseSpecifications: NotRequired[Sequence[LicenseConfigurationRequestTypeDef]]
    MetadataOptions: NotRequired[InstanceMetadataOptionsRequestTypeDef]
    EnclaveOptions: NotRequired[EnclaveOptionsRequestTypeDef]
    PrivateDnsNameOptions: NotRequired[PrivateDnsNameOptionsRequestTypeDef]
    MaintenanceOptions: NotRequired[InstanceMaintenanceOptionsRequestTypeDef]
    DisableApiStop: NotRequired[bool]
    EnablePrimaryIpv6: NotRequired[bool]
    NetworkPerformanceOptions: NotRequired[InstanceNetworkPerformanceOptionsRequestTypeDef]
    Operator: NotRequired[OperatorRequestTypeDef]
    DryRun: NotRequired[bool]
    DisableApiTermination: NotRequired[bool]
    InstanceInitiatedShutdownBehavior: NotRequired[ShutdownBehaviorType]
    PrivateIpAddress: NotRequired[str]
    ClientToken: NotRequired[str]
    AdditionalInfo: NotRequired[str]
    NetworkInterfaces: NotRequired[Sequence[InstanceNetworkInterfaceSpecificationTypeDef]]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    EbsOptimized: NotRequired[bool]


class RunInstancesRequestSubnetCreateInstancesTypeDef(TypedDict):
    MaxCount: int
    MinCount: int
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[RunInstancesMonitoringEnabledTypeDef]
    Placement: NotRequired[PlacementTypeDef]
    RamdiskId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    UserData: NotRequired[str]
    ElasticGpuSpecification: NotRequired[Sequence[ElasticGpuSpecificationTypeDef]]
    ElasticInferenceAccelerators: NotRequired[Sequence[ElasticInferenceAcceleratorTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    InstanceMarketOptions: NotRequired[InstanceMarketOptionsRequestTypeDef]
    CreditSpecification: NotRequired[CreditSpecificationRequestTypeDef]
    CpuOptions: NotRequired[CpuOptionsRequestTypeDef]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationTypeDef]
    HibernationOptions: NotRequired[HibernationOptionsRequestTypeDef]
    LicenseSpecifications: NotRequired[Sequence[LicenseConfigurationRequestTypeDef]]
    MetadataOptions: NotRequired[InstanceMetadataOptionsRequestTypeDef]
    EnclaveOptions: NotRequired[EnclaveOptionsRequestTypeDef]
    PrivateDnsNameOptions: NotRequired[PrivateDnsNameOptionsRequestTypeDef]
    MaintenanceOptions: NotRequired[InstanceMaintenanceOptionsRequestTypeDef]
    DisableApiStop: NotRequired[bool]
    EnablePrimaryIpv6: NotRequired[bool]
    NetworkPerformanceOptions: NotRequired[InstanceNetworkPerformanceOptionsRequestTypeDef]
    Operator: NotRequired[OperatorRequestTypeDef]
    DryRun: NotRequired[bool]
    DisableApiTermination: NotRequired[bool]
    InstanceInitiatedShutdownBehavior: NotRequired[ShutdownBehaviorType]
    PrivateIpAddress: NotRequired[str]
    ClientToken: NotRequired[str]
    AdditionalInfo: NotRequired[str]
    NetworkInterfaces: NotRequired[Sequence[InstanceNetworkInterfaceSpecificationTypeDef]]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    EbsOptimized: NotRequired[bool]


class EnableFastSnapshotRestoresResultTypeDef(TypedDict):
    Successful: list[EnableFastSnapshotRestoreSuccessItemTypeDef]
    Unsuccessful: list[EnableFastSnapshotRestoreErrorItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNetworkInsightsPathResultTypeDef(TypedDict):
    NetworkInsightsPath: NetworkInsightsPathTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNetworkInsightsPathsResultTypeDef(TypedDict):
    NetworkInsightsPaths: list[NetworkInsightsPathTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceNetworkInterfaceTypeDef(TypedDict):
    Association: NotRequired[InstanceNetworkInterfaceAssociationTypeDef]
    Attachment: NotRequired[InstanceNetworkInterfaceAttachmentTypeDef]
    Description: NotRequired[str]
    Groups: NotRequired[list[GroupIdentifierTypeDef]]
    Ipv6Addresses: NotRequired[list[InstanceIpv6AddressTypeDef]]
    MacAddress: NotRequired[str]
    NetworkInterfaceId: NotRequired[str]
    OwnerId: NotRequired[str]
    PrivateDnsName: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PrivateIpAddresses: NotRequired[list[InstancePrivateIpAddressTypeDef]]
    SourceDestCheck: NotRequired[bool]
    Status: NotRequired[NetworkInterfaceStatusType]
    SubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    InterfaceType: NotRequired[str]
    Ipv4Prefixes: NotRequired[list[InstanceIpv4PrefixTypeDef]]
    Ipv6Prefixes: NotRequired[list[InstanceIpv6PrefixTypeDef]]
    ConnectionTrackingConfiguration: NotRequired[ConnectionTrackingSpecificationResponseTypeDef]
    Operator: NotRequired[OperatorResponseTypeDef]


class DescribeInstanceStatusResultTypeDef(TypedDict):
    InstanceStatuses: list[InstanceStatusTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSecurityGroupsResultTypeDef(TypedDict):
    SecurityGroups: list[SecurityGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AuthorizeSecurityGroupEgressRequestRequestTypeDef(TypedDict):
    GroupId: str
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]
    SourceSecurityGroupName: NotRequired[str]
    SourceSecurityGroupOwnerId: NotRequired[str]
    IpProtocol: NotRequired[str]
    FromPort: NotRequired[int]
    ToPort: NotRequired[int]
    CidrIp: NotRequired[str]
    IpPermissions: NotRequired[Sequence[IpPermissionUnionTypeDef]]


class DescribeStaleSecurityGroupsResultTypeDef(TypedDict):
    StaleSecurityGroupSet: list[StaleSecurityGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetIpamDiscoveredPublicAddressesResultTypeDef(TypedDict):
    IpamDiscoveredPublicAddresses: list[IpamDiscoveredPublicAddressTypeDef]
    OldestSampleTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeReservedInstancesModificationsResultTypeDef(TypedDict):
    ReservedInstancesModifications: list[ReservedInstancesModificationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class InstanceTypeInfoTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    CurrentGeneration: NotRequired[bool]
    FreeTierEligible: NotRequired[bool]
    SupportedUsageClasses: NotRequired[list[UsageClassTypeType]]
    SupportedRootDeviceTypes: NotRequired[list[RootDeviceTypeType]]
    SupportedVirtualizationTypes: NotRequired[list[VirtualizationTypeType]]
    BareMetal: NotRequired[bool]
    Hypervisor: NotRequired[InstanceTypeHypervisorType]
    ProcessorInfo: NotRequired[ProcessorInfoTypeDef]
    VCpuInfo: NotRequired[VCpuInfoTypeDef]
    MemoryInfo: NotRequired[MemoryInfoTypeDef]
    InstanceStorageSupported: NotRequired[bool]
    InstanceStorageInfo: NotRequired[InstanceStorageInfoTypeDef]
    EbsInfo: NotRequired[EbsInfoTypeDef]
    NetworkInfo: NotRequired[NetworkInfoTypeDef]
    GpuInfo: NotRequired[GpuInfoTypeDef]
    FpgaInfo: NotRequired[FpgaInfoTypeDef]
    PlacementGroupInfo: NotRequired[PlacementGroupInfoTypeDef]
    InferenceAcceleratorInfo: NotRequired[InferenceAcceleratorInfoTypeDef]
    HibernationSupported: NotRequired[bool]
    BurstablePerformanceSupported: NotRequired[bool]
    DedicatedHostsSupported: NotRequired[bool]
    AutoRecoverySupported: NotRequired[bool]
    SupportedBootModes: NotRequired[list[BootModeTypeType]]
    NitroEnclavesSupport: NotRequired[NitroEnclavesSupportType]
    NitroTpmSupport: NotRequired[NitroTpmSupportType]
    NitroTpmInfo: NotRequired[NitroTpmInfoTypeDef]
    MediaAcceleratorInfo: NotRequired[MediaAcceleratorInfoTypeDef]
    NeuronInfo: NotRequired[NeuronInfoTypeDef]
    PhcSupport: NotRequired[PhcSupportType]


class CreateNetworkInsightsAccessScopeRequestRequestTypeDef(TypedDict):
    ClientToken: str
    MatchPaths: NotRequired[Sequence[AccessScopePathRequestTypeDef]]
    ExcludePaths: NotRequired[Sequence[AccessScopePathRequestTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    DryRun: NotRequired[bool]


class NetworkInsightsAccessScopeContentTypeDef(TypedDict):
    NetworkInsightsAccessScopeId: NotRequired[str]
    MatchPaths: NotRequired[list[AccessScopePathTypeDef]]
    ExcludePaths: NotRequired[list[AccessScopePathTypeDef]]


class BundleInstanceResultTypeDef(TypedDict):
    BundleTask: BundleTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CancelBundleTaskResultTypeDef(TypedDict):
    BundleTask: BundleTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBundleTasksResultTypeDef(TypedDict):
    BundleTasks: list[BundleTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RunScheduledInstancesRequestRequestTypeDef(TypedDict):
    LaunchSpecification: ScheduledInstancesLaunchSpecificationTypeDef
    ScheduledInstanceId: str
    ClientToken: NotRequired[str]
    DryRun: NotRequired[bool]
    InstanceCount: NotRequired[int]


class DescribeImportImageTasksResultTypeDef(TypedDict):
    ImportImageTasks: list[ImportImageTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeImportSnapshotTasksResultTypeDef(TypedDict):
    ImportSnapshotTasks: list[ImportSnapshotTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateDefaultSubnetResultTypeDef(TypedDict):
    Subnet: SubnetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSubnetResultTypeDef(TypedDict):
    Subnet: SubnetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSubnetsResultTypeDef(TypedDict):
    Subnets: list[SubnetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class LoadBalancersConfigTypeDef(TypedDict):
    ClassicLoadBalancersConfig: NotRequired[ClassicLoadBalancersConfigUnionTypeDef]
    TargetGroupsConfig: NotRequired[TargetGroupsConfigUnionTypeDef]


class CreateTrafficMirrorFilterResultTypeDef(TypedDict):
    TrafficMirrorFilter: TrafficMirrorFilterTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTrafficMirrorFiltersResultTypeDef(TypedDict):
    TrafficMirrorFilters: list[TrafficMirrorFilterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyTrafficMirrorFilterNetworkServicesResultTypeDef(TypedDict):
    TrafficMirrorFilter: TrafficMirrorFilterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTransitGatewayConnectPeerResultTypeDef(TypedDict):
    TransitGatewayConnectPeer: TransitGatewayConnectPeerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTransitGatewayConnectPeerResultTypeDef(TypedDict):
    TransitGatewayConnectPeer: TransitGatewayConnectPeerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTransitGatewayConnectPeersResultTypeDef(TypedDict):
    TransitGatewayConnectPeers: list[TransitGatewayConnectPeerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetTransitGatewayPolicyTableEntriesResultTypeDef(TypedDict):
    TransitGatewayPolicyTableEntries: list[TransitGatewayPolicyTableEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVerifiedAccessEndpointResultTypeDef(TypedDict):
    VerifiedAccessEndpoint: VerifiedAccessEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVerifiedAccessEndpointResultTypeDef(TypedDict):
    VerifiedAccessEndpoint: VerifiedAccessEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVerifiedAccessEndpointsResultTypeDef(TypedDict):
    VerifiedAccessEndpoints: list[VerifiedAccessEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVerifiedAccessEndpointResultTypeDef(TypedDict):
    VerifiedAccessEndpoint: VerifiedAccessEndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class VerifiedAccessInstanceLoggingConfigurationTypeDef(TypedDict):
    VerifiedAccessInstanceId: NotRequired[str]
    AccessLogs: NotRequired[VerifiedAccessLogsTypeDef]


class DescribeVolumeStatusResultTypeDef(TypedDict):
    VolumeStatuses: list[VolumeStatusItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateDefaultVpcResultTypeDef(TypedDict):
    Vpc: VpcTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcResultTypeDef(TypedDict):
    Vpc: VpcTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcsResultTypeDef(TypedDict):
    Vpcs: list[VpcTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AcceptVpcPeeringConnectionResultTypeDef(TypedDict):
    VpcPeeringConnection: VpcPeeringConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcPeeringConnectionResultTypeDef(TypedDict):
    VpcPeeringConnection: VpcPeeringConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcPeeringConnectionsResultTypeDef(TypedDict):
    VpcPeeringConnections: list[VpcPeeringConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class AccessScopeAnalysisFindingTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: NotRequired[str]
    NetworkInsightsAccessScopeId: NotRequired[str]
    FindingId: NotRequired[str]
    FindingComponents: NotRequired[list[PathComponentTypeDef]]


class NetworkInsightsAnalysisTypeDef(TypedDict):
    NetworkInsightsAnalysisId: NotRequired[str]
    NetworkInsightsAnalysisArn: NotRequired[str]
    NetworkInsightsPathId: NotRequired[str]
    AdditionalAccounts: NotRequired[list[str]]
    FilterInArns: NotRequired[list[str]]
    StartDate: NotRequired[datetime]
    Status: NotRequired[AnalysisStatusType]
    StatusMessage: NotRequired[str]
    WarningMessage: NotRequired[str]
    NetworkPathFound: NotRequired[bool]
    ForwardPathComponents: NotRequired[list[PathComponentTypeDef]]
    ReturnPathComponents: NotRequired[list[PathComponentTypeDef]]
    Explanations: NotRequired[list[ExplanationTypeDef]]
    AlternatePathHints: NotRequired[list[AlternatePathHintTypeDef]]
    SuggestedAccounts: NotRequired[list[str]]
    Tags: NotRequired[list[TagTypeDef]]


class CreateNetworkInterfaceResultTypeDef(TypedDict):
    NetworkInterface: NetworkInterfaceTypeDef
    ClientToken: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeNetworkInterfacesResultTypeDef(TypedDict):
    NetworkInterfaces: list[NetworkInterfaceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class BundleInstanceRequestRequestTypeDef(TypedDict):
    InstanceId: str
    Storage: StorageTypeDef
    DryRun: NotRequired[bool]


CreateVpnConnectionRequestRequestTypeDef = TypedDict(
    "CreateVpnConnectionRequestRequestTypeDef",
    {
        "CustomerGatewayId": str,
        "Type": str,
        "VpnGatewayId": NotRequired[str],
        "TransitGatewayId": NotRequired[str],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "DryRun": NotRequired[bool],
        "Options": NotRequired[VpnConnectionOptionsSpecificationTypeDef],
    },
)
VpnConnectionTypeDef = TypedDict(
    "VpnConnectionTypeDef",
    {
        "Category": NotRequired[str],
        "TransitGatewayId": NotRequired[str],
        "CoreNetworkArn": NotRequired[str],
        "CoreNetworkAttachmentArn": NotRequired[str],
        "GatewayAssociationState": NotRequired[GatewayAssociationStateType],
        "Options": NotRequired[VpnConnectionOptionsTypeDef],
        "Routes": NotRequired[list[VpnStaticRouteTypeDef]],
        "Tags": NotRequired[list[TagTypeDef]],
        "VgwTelemetry": NotRequired[list[VgwTelemetryTypeDef]],
        "VpnConnectionId": NotRequired[str],
        "State": NotRequired[VpnStateType],
        "CustomerGatewayConfiguration": NotRequired[str],
        "Type": NotRequired[Literal["ipsec.1"]],
        "CustomerGatewayId": NotRequired[str],
        "VpnGatewayId": NotRequired[str],
    },
)


class FleetLaunchTemplateOverridesTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    MaxPrice: NotRequired[str]
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    WeightedCapacity: NotRequired[float]
    Priority: NotRequired[float]
    Placement: NotRequired[PlacementResponseTypeDef]
    InstanceRequirements: NotRequired[InstanceRequirementsOutputTypeDef]
    ImageId: NotRequired[str]


class LaunchTemplateOverridesOutputTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    SpotPrice: NotRequired[str]
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    WeightedCapacity: NotRequired[float]
    Priority: NotRequired[float]
    InstanceRequirements: NotRequired[InstanceRequirementsOutputTypeDef]


class ResponseLaunchTemplateDataTypeDef(TypedDict):
    KernelId: NotRequired[str]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[LaunchTemplateIamInstanceProfileSpecificationTypeDef]
    BlockDeviceMappings: NotRequired[list[LaunchTemplateBlockDeviceMappingTypeDef]]
    NetworkInterfaces: NotRequired[list[LaunchTemplateInstanceNetworkInterfaceSpecificationTypeDef]]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[LaunchTemplatesMonitoringTypeDef]
    Placement: NotRequired[LaunchTemplatePlacementTypeDef]
    RamDiskId: NotRequired[str]
    DisableApiTermination: NotRequired[bool]
    InstanceInitiatedShutdownBehavior: NotRequired[ShutdownBehaviorType]
    UserData: NotRequired[str]
    TagSpecifications: NotRequired[list[LaunchTemplateTagSpecificationTypeDef]]
    ElasticGpuSpecifications: NotRequired[list[ElasticGpuSpecificationResponseTypeDef]]
    ElasticInferenceAccelerators: NotRequired[
        list[LaunchTemplateElasticInferenceAcceleratorResponseTypeDef]
    ]
    SecurityGroupIds: NotRequired[list[str]]
    SecurityGroups: NotRequired[list[str]]
    InstanceMarketOptions: NotRequired[LaunchTemplateInstanceMarketOptionsTypeDef]
    CreditSpecification: NotRequired[CreditSpecificationTypeDef]
    CpuOptions: NotRequired[LaunchTemplateCpuOptionsTypeDef]
    CapacityReservationSpecification: NotRequired[
        LaunchTemplateCapacityReservationSpecificationResponseTypeDef
    ]
    LicenseSpecifications: NotRequired[list[LaunchTemplateLicenseConfigurationTypeDef]]
    HibernationOptions: NotRequired[LaunchTemplateHibernationOptionsTypeDef]
    MetadataOptions: NotRequired[LaunchTemplateInstanceMetadataOptionsTypeDef]
    EnclaveOptions: NotRequired[LaunchTemplateEnclaveOptionsTypeDef]
    InstanceRequirements: NotRequired[InstanceRequirementsOutputTypeDef]
    PrivateDnsNameOptions: NotRequired[LaunchTemplatePrivateDnsNameOptionsTypeDef]
    MaintenanceOptions: NotRequired[LaunchTemplateInstanceMaintenanceOptionsTypeDef]
    DisableApiStop: NotRequired[bool]
    Operator: NotRequired[OperatorResponseTypeDef]
    NetworkPerformanceOptions: NotRequired[LaunchTemplateNetworkPerformanceOptionsTypeDef]


class SpotFleetLaunchSpecificationOutputTypeDef(TypedDict):
    AddressingType: NotRequired[str]
    BlockDeviceMappings: NotRequired[list[BlockDeviceMappingTypeDef]]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[SpotFleetMonitoringTypeDef]
    NetworkInterfaces: NotRequired[list[InstanceNetworkInterfaceSpecificationOutputTypeDef]]
    Placement: NotRequired[SpotPlacementTypeDef]
    RamdiskId: NotRequired[str]
    SpotPrice: NotRequired[str]
    SubnetId: NotRequired[str]
    UserData: NotRequired[str]
    WeightedCapacity: NotRequired[float]
    TagSpecifications: NotRequired[list[SpotFleetTagSpecificationOutputTypeDef]]
    InstanceRequirements: NotRequired[InstanceRequirementsOutputTypeDef]
    SecurityGroups: NotRequired[list[GroupIdentifierTypeDef]]


BaselinePerformanceFactorsUnionTypeDef = Union[
    BaselinePerformanceFactorsTypeDef, BaselinePerformanceFactorsOutputTypeDef
]


class FleetLaunchTemplateOverridesRequestTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    MaxPrice: NotRequired[str]
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    WeightedCapacity: NotRequired[float]
    Priority: NotRequired[float]
    Placement: NotRequired[PlacementTypeDef]
    InstanceRequirements: NotRequired[InstanceRequirementsRequestTypeDef]
    ImageId: NotRequired[str]


class GetInstanceTypesFromInstanceRequirementsRequestPaginateTypeDef(TypedDict):
    ArchitectureTypes: Sequence[ArchitectureTypeType]
    VirtualizationTypes: Sequence[VirtualizationTypeType]
    InstanceRequirements: InstanceRequirementsRequestTypeDef
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetInstanceTypesFromInstanceRequirementsRequestRequestTypeDef(TypedDict):
    ArchitectureTypes: Sequence[ArchitectureTypeType]
    VirtualizationTypes: Sequence[VirtualizationTypeType]
    InstanceRequirements: InstanceRequirementsRequestTypeDef
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class InstanceRequirementsWithMetadataRequestTypeDef(TypedDict):
    ArchitectureTypes: NotRequired[Sequence[ArchitectureTypeType]]
    VirtualizationTypes: NotRequired[Sequence[VirtualizationTypeType]]
    InstanceRequirements: NotRequired[InstanceRequirementsRequestTypeDef]


class RequestLaunchTemplateDataTypeDef(TypedDict):
    KernelId: NotRequired[str]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[LaunchTemplateIamInstanceProfileSpecificationRequestTypeDef]
    BlockDeviceMappings: NotRequired[Sequence[LaunchTemplateBlockDeviceMappingRequestTypeDef]]
    NetworkInterfaces: NotRequired[
        Sequence[LaunchTemplateInstanceNetworkInterfaceSpecificationRequestTypeDef]
    ]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[LaunchTemplatesMonitoringRequestTypeDef]
    Placement: NotRequired[LaunchTemplatePlacementRequestTypeDef]
    RamDiskId: NotRequired[str]
    DisableApiTermination: NotRequired[bool]
    InstanceInitiatedShutdownBehavior: NotRequired[ShutdownBehaviorType]
    UserData: NotRequired[str]
    TagSpecifications: NotRequired[Sequence[LaunchTemplateTagSpecificationRequestTypeDef]]
    ElasticGpuSpecifications: NotRequired[Sequence[ElasticGpuSpecificationTypeDef]]
    ElasticInferenceAccelerators: NotRequired[
        Sequence[LaunchTemplateElasticInferenceAcceleratorTypeDef]
    ]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    InstanceMarketOptions: NotRequired[LaunchTemplateInstanceMarketOptionsRequestTypeDef]
    CreditSpecification: NotRequired[CreditSpecificationRequestTypeDef]
    CpuOptions: NotRequired[LaunchTemplateCpuOptionsRequestTypeDef]
    CapacityReservationSpecification: NotRequired[
        LaunchTemplateCapacityReservationSpecificationRequestTypeDef
    ]
    LicenseSpecifications: NotRequired[Sequence[LaunchTemplateLicenseConfigurationRequestTypeDef]]
    HibernationOptions: NotRequired[LaunchTemplateHibernationOptionsRequestTypeDef]
    MetadataOptions: NotRequired[LaunchTemplateInstanceMetadataOptionsRequestTypeDef]
    EnclaveOptions: NotRequired[LaunchTemplateEnclaveOptionsRequestTypeDef]
    InstanceRequirements: NotRequired[InstanceRequirementsRequestTypeDef]
    PrivateDnsNameOptions: NotRequired[LaunchTemplatePrivateDnsNameOptionsRequestTypeDef]
    MaintenanceOptions: NotRequired[LaunchTemplateInstanceMaintenanceOptionsRequestTypeDef]
    DisableApiStop: NotRequired[bool]
    Operator: NotRequired[OperatorRequestTypeDef]
    NetworkPerformanceOptions: NotRequired[LaunchTemplateNetworkPerformanceOptionsRequestTypeDef]


class DescribeConversionTasksResultTypeDef(TypedDict):
    ConversionTasks: list[ConversionTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImportInstanceResultTypeDef(TypedDict):
    ConversionTask: ConversionTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ImportVolumeResultTypeDef(TypedDict):
    ConversionTask: ConversionTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


SpotInstanceRequestTypeDef = TypedDict(
    "SpotInstanceRequestTypeDef",
    {
        "ActualBlockHourlyPrice": NotRequired[str],
        "AvailabilityZoneGroup": NotRequired[str],
        "BlockDurationMinutes": NotRequired[int],
        "CreateTime": NotRequired[datetime],
        "Fault": NotRequired[SpotInstanceStateFaultTypeDef],
        "InstanceId": NotRequired[str],
        "LaunchGroup": NotRequired[str],
        "LaunchSpecification": NotRequired[LaunchSpecificationTypeDef],
        "LaunchedAvailabilityZone": NotRequired[str],
        "ProductDescription": NotRequired[RIProductDescriptionType],
        "SpotInstanceRequestId": NotRequired[str],
        "SpotPrice": NotRequired[str],
        "State": NotRequired[SpotInstanceStateType],
        "Status": NotRequired[SpotInstanceStatusTypeDef],
        "Tags": NotRequired[list[TagTypeDef]],
        "Type": NotRequired[SpotInstanceTypeType],
        "ValidFrom": NotRequired[datetime],
        "ValidUntil": NotRequired[datetime],
        "InstanceInterruptionBehavior": NotRequired[InstanceInterruptionBehaviorType],
    },
)


class RequestSpotLaunchSpecificationTypeDef(TypedDict):
    SecurityGroupIds: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    AddressingType: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[RunInstancesMonitoringEnabledTypeDef]
    NetworkInterfaces: NotRequired[Sequence[InstanceNetworkInterfaceSpecificationUnionTypeDef]]
    Placement: NotRequired[SpotPlacementTypeDef]
    RamdiskId: NotRequired[str]
    SubnetId: NotRequired[str]
    UserData: NotRequired[str]


class RunInstancesRequestRequestTypeDef(TypedDict):
    MaxCount: int
    MinCount: int
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    Ipv6AddressCount: NotRequired[int]
    Ipv6Addresses: NotRequired[Sequence[InstanceIpv6AddressTypeDef]]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[RunInstancesMonitoringEnabledTypeDef]
    Placement: NotRequired[PlacementTypeDef]
    RamdiskId: NotRequired[str]
    SecurityGroupIds: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    SubnetId: NotRequired[str]
    UserData: NotRequired[str]
    ElasticGpuSpecification: NotRequired[Sequence[ElasticGpuSpecificationTypeDef]]
    ElasticInferenceAccelerators: NotRequired[Sequence[ElasticInferenceAcceleratorTypeDef]]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]
    LaunchTemplate: NotRequired[LaunchTemplateSpecificationTypeDef]
    InstanceMarketOptions: NotRequired[InstanceMarketOptionsRequestTypeDef]
    CreditSpecification: NotRequired[CreditSpecificationRequestTypeDef]
    CpuOptions: NotRequired[CpuOptionsRequestTypeDef]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationTypeDef]
    HibernationOptions: NotRequired[HibernationOptionsRequestTypeDef]
    LicenseSpecifications: NotRequired[Sequence[LicenseConfigurationRequestTypeDef]]
    MetadataOptions: NotRequired[InstanceMetadataOptionsRequestTypeDef]
    EnclaveOptions: NotRequired[EnclaveOptionsRequestTypeDef]
    PrivateDnsNameOptions: NotRequired[PrivateDnsNameOptionsRequestTypeDef]
    MaintenanceOptions: NotRequired[InstanceMaintenanceOptionsRequestTypeDef]
    DisableApiStop: NotRequired[bool]
    EnablePrimaryIpv6: NotRequired[bool]
    NetworkPerformanceOptions: NotRequired[InstanceNetworkPerformanceOptionsRequestTypeDef]
    Operator: NotRequired[OperatorRequestTypeDef]
    DryRun: NotRequired[bool]
    DisableApiTermination: NotRequired[bool]
    InstanceInitiatedShutdownBehavior: NotRequired[ShutdownBehaviorType]
    PrivateIpAddress: NotRequired[str]
    ClientToken: NotRequired[str]
    AdditionalInfo: NotRequired[str]
    NetworkInterfaces: NotRequired[Sequence[InstanceNetworkInterfaceSpecificationUnionTypeDef]]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    EbsOptimized: NotRequired[bool]


class InstanceTypeDef(TypedDict):
    Architecture: NotRequired[ArchitectureValuesType]
    BlockDeviceMappings: NotRequired[list[InstanceBlockDeviceMappingTypeDef]]
    ClientToken: NotRequired[str]
    EbsOptimized: NotRequired[bool]
    EnaSupport: NotRequired[bool]
    Hypervisor: NotRequired[HypervisorTypeType]
    IamInstanceProfile: NotRequired[IamInstanceProfileTypeDef]
    InstanceLifecycle: NotRequired[InstanceLifecycleTypeType]
    ElasticGpuAssociations: NotRequired[list[ElasticGpuAssociationTypeDef]]
    ElasticInferenceAcceleratorAssociations: NotRequired[
        list[ElasticInferenceAcceleratorAssociationTypeDef]
    ]
    NetworkInterfaces: NotRequired[list[InstanceNetworkInterfaceTypeDef]]
    OutpostArn: NotRequired[str]
    RootDeviceName: NotRequired[str]
    RootDeviceType: NotRequired[DeviceTypeType]
    SecurityGroups: NotRequired[list[GroupIdentifierTypeDef]]
    SourceDestCheck: NotRequired[bool]
    SpotInstanceRequestId: NotRequired[str]
    SriovNetSupport: NotRequired[str]
    StateReason: NotRequired[StateReasonTypeDef]
    Tags: NotRequired[list[TagTypeDef]]
    VirtualizationType: NotRequired[VirtualizationTypeType]
    CpuOptions: NotRequired[CpuOptionsTypeDef]
    CapacityReservationId: NotRequired[str]
    CapacityReservationSpecification: NotRequired[CapacityReservationSpecificationResponseTypeDef]
    HibernationOptions: NotRequired[HibernationOptionsTypeDef]
    Licenses: NotRequired[list[LicenseConfigurationTypeDef]]
    MetadataOptions: NotRequired[InstanceMetadataOptionsResponseTypeDef]
    EnclaveOptions: NotRequired[EnclaveOptionsTypeDef]
    BootMode: NotRequired[BootModeValuesType]
    PlatformDetails: NotRequired[str]
    UsageOperation: NotRequired[str]
    UsageOperationUpdateTime: NotRequired[datetime]
    PrivateDnsNameOptions: NotRequired[PrivateDnsNameOptionsResponseTypeDef]
    Ipv6Address: NotRequired[str]
    TpmSupport: NotRequired[str]
    MaintenanceOptions: NotRequired[InstanceMaintenanceOptionsTypeDef]
    CurrentInstanceBootMode: NotRequired[InstanceBootModeValuesType]
    NetworkPerformanceOptions: NotRequired[InstanceNetworkPerformanceOptionsTypeDef]
    Operator: NotRequired[OperatorResponseTypeDef]
    InstanceId: NotRequired[str]
    ImageId: NotRequired[str]
    State: NotRequired[InstanceStateTypeDef]
    PrivateDnsName: NotRequired[str]
    PublicDnsName: NotRequired[str]
    StateTransitionReason: NotRequired[str]
    KeyName: NotRequired[str]
    AmiLaunchIndex: NotRequired[int]
    ProductCodes: NotRequired[list[ProductCodeTypeDef]]
    InstanceType: NotRequired[InstanceTypeType]
    LaunchTime: NotRequired[datetime]
    Placement: NotRequired[PlacementTypeDef]
    KernelId: NotRequired[str]
    RamdiskId: NotRequired[str]
    Platform: NotRequired[Literal["windows"]]
    Monitoring: NotRequired[MonitoringTypeDef]
    SubnetId: NotRequired[str]
    VpcId: NotRequired[str]
    PrivateIpAddress: NotRequired[str]
    PublicIpAddress: NotRequired[str]


class DescribeInstanceTypesResultTypeDef(TypedDict):
    InstanceTypes: list[InstanceTypeInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateNetworkInsightsAccessScopeResultTypeDef(TypedDict):
    NetworkInsightsAccessScope: NetworkInsightsAccessScopeTypeDef
    NetworkInsightsAccessScopeContent: NetworkInsightsAccessScopeContentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNetworkInsightsAccessScopeContentResultTypeDef(TypedDict):
    NetworkInsightsAccessScopeContent: NetworkInsightsAccessScopeContentTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


LoadBalancersConfigUnionTypeDef = Union[
    LoadBalancersConfigTypeDef, LoadBalancersConfigOutputTypeDef
]


class DescribeVerifiedAccessInstanceLoggingConfigurationsResultTypeDef(TypedDict):
    LoggingConfigurations: list[VerifiedAccessInstanceLoggingConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ModifyVerifiedAccessInstanceLoggingConfigurationResultTypeDef(TypedDict):
    LoggingConfiguration: VerifiedAccessInstanceLoggingConfigurationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetNetworkInsightsAccessScopeAnalysisFindingsResultTypeDef(TypedDict):
    NetworkInsightsAccessScopeAnalysisId: str
    AnalysisStatus: AnalysisStatusType
    AnalysisFindings: list[AccessScopeAnalysisFindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeNetworkInsightsAnalysesResultTypeDef(TypedDict):
    NetworkInsightsAnalyses: list[NetworkInsightsAnalysisTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartNetworkInsightsAnalysisResultTypeDef(TypedDict):
    NetworkInsightsAnalysis: NetworkInsightsAnalysisTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpnConnectionResultTypeDef(TypedDict):
    VpnConnection: VpnConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpnConnectionsResultTypeDef(TypedDict):
    VpnConnections: list[VpnConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpnConnectionOptionsResultTypeDef(TypedDict):
    VpnConnection: VpnConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpnConnectionResultTypeDef(TypedDict):
    VpnConnection: VpnConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpnTunnelCertificateResultTypeDef(TypedDict):
    VpnConnection: VpnConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyVpnTunnelOptionsResultTypeDef(TypedDict):
    VpnConnection: VpnConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class FleetLaunchTemplateConfigTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[FleetLaunchTemplateSpecificationTypeDef]
    Overrides: NotRequired[list[FleetLaunchTemplateOverridesTypeDef]]


class LaunchTemplateAndOverridesResponseTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[FleetLaunchTemplateSpecificationTypeDef]
    Overrides: NotRequired[FleetLaunchTemplateOverridesTypeDef]


class LaunchTemplateConfigOutputTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[FleetLaunchTemplateSpecificationTypeDef]
    Overrides: NotRequired[list[LaunchTemplateOverridesOutputTypeDef]]


class GetLaunchTemplateDataResultTypeDef(TypedDict):
    LaunchTemplateData: ResponseLaunchTemplateDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LaunchTemplateVersionTypeDef(TypedDict):
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    VersionNumber: NotRequired[int]
    VersionDescription: NotRequired[str]
    CreateTime: NotRequired[datetime]
    CreatedBy: NotRequired[str]
    DefaultVersion: NotRequired[bool]
    LaunchTemplateData: NotRequired[ResponseLaunchTemplateDataTypeDef]
    Operator: NotRequired[OperatorResponseTypeDef]


class InstanceRequirementsTypeDef(TypedDict):
    VCpuCount: NotRequired[VCpuCountRangeTypeDef]
    MemoryMiB: NotRequired[MemoryMiBTypeDef]
    CpuManufacturers: NotRequired[Sequence[CpuManufacturerType]]
    MemoryGiBPerVCpu: NotRequired[MemoryGiBPerVCpuTypeDef]
    ExcludedInstanceTypes: NotRequired[Sequence[str]]
    InstanceGenerations: NotRequired[Sequence[InstanceGenerationType]]
    SpotMaxPricePercentageOverLowestPrice: NotRequired[int]
    OnDemandMaxPricePercentageOverLowestPrice: NotRequired[int]
    BareMetal: NotRequired[BareMetalType]
    BurstablePerformance: NotRequired[BurstablePerformanceType]
    RequireHibernateSupport: NotRequired[bool]
    NetworkInterfaceCount: NotRequired[NetworkInterfaceCountTypeDef]
    LocalStorage: NotRequired[LocalStorageType]
    LocalStorageTypes: NotRequired[Sequence[LocalStorageTypeType]]
    TotalLocalStorageGB: NotRequired[TotalLocalStorageGBTypeDef]
    BaselineEbsBandwidthMbps: NotRequired[BaselineEbsBandwidthMbpsTypeDef]
    AcceleratorTypes: NotRequired[Sequence[AcceleratorTypeType]]
    AcceleratorCount: NotRequired[AcceleratorCountTypeDef]
    AcceleratorManufacturers: NotRequired[Sequence[AcceleratorManufacturerType]]
    AcceleratorNames: NotRequired[Sequence[AcceleratorNameType]]
    AcceleratorTotalMemoryMiB: NotRequired[AcceleratorTotalMemoryMiBTypeDef]
    NetworkBandwidthGbps: NotRequired[NetworkBandwidthGbpsTypeDef]
    AllowedInstanceTypes: NotRequired[Sequence[str]]
    MaxSpotPriceAsPercentageOfOptimalOnDemandPrice: NotRequired[int]
    BaselinePerformanceFactors: NotRequired[BaselinePerformanceFactorsUnionTypeDef]


class FleetLaunchTemplateConfigRequestTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[FleetLaunchTemplateSpecificationRequestTypeDef]
    Overrides: NotRequired[Sequence[FleetLaunchTemplateOverridesRequestTypeDef]]


class GetSpotPlacementScoresRequestPaginateTypeDef(TypedDict):
    TargetCapacity: int
    InstanceTypes: NotRequired[Sequence[str]]
    TargetCapacityUnitType: NotRequired[TargetCapacityUnitTypeType]
    SingleAvailabilityZone: NotRequired[bool]
    RegionNames: NotRequired[Sequence[str]]
    InstanceRequirementsWithMetadata: NotRequired[InstanceRequirementsWithMetadataRequestTypeDef]
    DryRun: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetSpotPlacementScoresRequestRequestTypeDef(TypedDict):
    TargetCapacity: int
    InstanceTypes: NotRequired[Sequence[str]]
    TargetCapacityUnitType: NotRequired[TargetCapacityUnitTypeType]
    SingleAvailabilityZone: NotRequired[bool]
    RegionNames: NotRequired[Sequence[str]]
    InstanceRequirementsWithMetadata: NotRequired[InstanceRequirementsWithMetadataRequestTypeDef]
    DryRun: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class CreateLaunchTemplateRequestRequestTypeDef(TypedDict):
    LaunchTemplateName: str
    LaunchTemplateData: RequestLaunchTemplateDataTypeDef
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    VersionDescription: NotRequired[str]
    Operator: NotRequired[OperatorRequestTypeDef]
    TagSpecifications: NotRequired[Sequence[TagSpecificationTypeDef]]


class CreateLaunchTemplateVersionRequestRequestTypeDef(TypedDict):
    LaunchTemplateData: RequestLaunchTemplateDataTypeDef
    DryRun: NotRequired[bool]
    ClientToken: NotRequired[str]
    LaunchTemplateId: NotRequired[str]
    LaunchTemplateName: NotRequired[str]
    SourceVersion: NotRequired[str]
    VersionDescription: NotRequired[str]
    ResolveAlias: NotRequired[bool]


class DescribeSpotInstanceRequestsResultTypeDef(TypedDict):
    SpotInstanceRequests: list[SpotInstanceRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RequestSpotInstancesResultTypeDef(TypedDict):
    SpotInstanceRequests: list[SpotInstanceRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


RequestSpotInstancesRequestRequestTypeDef = TypedDict(
    "RequestSpotInstancesRequestRequestTypeDef",
    {
        "LaunchSpecification": NotRequired[RequestSpotLaunchSpecificationTypeDef],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "InstanceInterruptionBehavior": NotRequired[InstanceInterruptionBehaviorType],
        "DryRun": NotRequired[bool],
        "SpotPrice": NotRequired[str],
        "ClientToken": NotRequired[str],
        "InstanceCount": NotRequired[int],
        "Type": NotRequired[SpotInstanceTypeType],
        "ValidFrom": NotRequired[TimestampTypeDef],
        "ValidUntil": NotRequired[TimestampTypeDef],
        "LaunchGroup": NotRequired[str],
        "AvailabilityZoneGroup": NotRequired[str],
        "BlockDurationMinutes": NotRequired[int],
    },
)


class ReservationResponseTypeDef(TypedDict):
    ReservationId: str
    OwnerId: str
    RequesterId: str
    Groups: list[GroupIdentifierTypeDef]
    Instances: list[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ReservationTypeDef(TypedDict):
    ReservationId: NotRequired[str]
    OwnerId: NotRequired[str]
    RequesterId: NotRequired[str]
    Groups: NotRequired[list[GroupIdentifierTypeDef]]
    Instances: NotRequired[list[InstanceTypeDef]]


class CreateFleetErrorTypeDef(TypedDict):
    LaunchTemplateAndOverrides: NotRequired[LaunchTemplateAndOverridesResponseTypeDef]
    Lifecycle: NotRequired[InstanceLifecycleType]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class CreateFleetInstanceTypeDef(TypedDict):
    LaunchTemplateAndOverrides: NotRequired[LaunchTemplateAndOverridesResponseTypeDef]
    Lifecycle: NotRequired[InstanceLifecycleType]
    InstanceIds: NotRequired[list[str]]
    InstanceType: NotRequired[InstanceTypeType]
    Platform: NotRequired[Literal["windows"]]


class DescribeFleetErrorTypeDef(TypedDict):
    LaunchTemplateAndOverrides: NotRequired[LaunchTemplateAndOverridesResponseTypeDef]
    Lifecycle: NotRequired[InstanceLifecycleType]
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]


class DescribeFleetsInstancesTypeDef(TypedDict):
    LaunchTemplateAndOverrides: NotRequired[LaunchTemplateAndOverridesResponseTypeDef]
    Lifecycle: NotRequired[InstanceLifecycleType]
    InstanceIds: NotRequired[list[str]]
    InstanceType: NotRequired[InstanceTypeType]
    Platform: NotRequired[Literal["windows"]]


SpotFleetRequestConfigDataOutputTypeDef = TypedDict(
    "SpotFleetRequestConfigDataOutputTypeDef",
    {
        "IamFleetRole": str,
        "TargetCapacity": int,
        "AllocationStrategy": NotRequired[AllocationStrategyType],
        "OnDemandAllocationStrategy": NotRequired[OnDemandAllocationStrategyType],
        "SpotMaintenanceStrategies": NotRequired[SpotMaintenanceStrategiesTypeDef],
        "ClientToken": NotRequired[str],
        "ExcessCapacityTerminationPolicy": NotRequired[ExcessCapacityTerminationPolicyType],
        "FulfilledCapacity": NotRequired[float],
        "OnDemandFulfilledCapacity": NotRequired[float],
        "LaunchSpecifications": NotRequired[list[SpotFleetLaunchSpecificationOutputTypeDef]],
        "LaunchTemplateConfigs": NotRequired[list[LaunchTemplateConfigOutputTypeDef]],
        "SpotPrice": NotRequired[str],
        "OnDemandTargetCapacity": NotRequired[int],
        "OnDemandMaxTotalPrice": NotRequired[str],
        "SpotMaxTotalPrice": NotRequired[str],
        "TerminateInstancesWithExpiration": NotRequired[bool],
        "Type": NotRequired[FleetTypeType],
        "ValidFrom": NotRequired[datetime],
        "ValidUntil": NotRequired[datetime],
        "ReplaceUnhealthyInstances": NotRequired[bool],
        "InstanceInterruptionBehavior": NotRequired[InstanceInterruptionBehaviorType],
        "LoadBalancersConfig": NotRequired[LoadBalancersConfigOutputTypeDef],
        "InstancePoolsToUseCount": NotRequired[int],
        "Context": NotRequired[str],
        "TargetCapacityUnitType": NotRequired[TargetCapacityUnitTypeType],
        "TagSpecifications": NotRequired[list[TagSpecificationOutputTypeDef]],
    },
)
CreateLaunchTemplateVersionResultTypeDef = TypedDict(
    "CreateLaunchTemplateVersionResultTypeDef",
    {
        "LaunchTemplateVersion": LaunchTemplateVersionTypeDef,
        "Warning": ValidationWarningTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DescribeLaunchTemplateVersionsResultTypeDef(TypedDict):
    LaunchTemplateVersions: list[LaunchTemplateVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


InstanceRequirementsUnionTypeDef = Union[
    InstanceRequirementsTypeDef, InstanceRequirementsOutputTypeDef
]
CreateFleetRequestRequestTypeDef = TypedDict(
    "CreateFleetRequestRequestTypeDef",
    {
        "LaunchTemplateConfigs": Sequence[FleetLaunchTemplateConfigRequestTypeDef],
        "TargetCapacitySpecification": TargetCapacitySpecificationRequestTypeDef,
        "DryRun": NotRequired[bool],
        "ClientToken": NotRequired[str],
        "SpotOptions": NotRequired[SpotOptionsRequestTypeDef],
        "OnDemandOptions": NotRequired[OnDemandOptionsRequestTypeDef],
        "ExcessCapacityTerminationPolicy": NotRequired[FleetExcessCapacityTerminationPolicyType],
        "TerminateInstancesWithExpiration": NotRequired[bool],
        "Type": NotRequired[FleetTypeType],
        "ValidFrom": NotRequired[TimestampTypeDef],
        "ValidUntil": NotRequired[TimestampTypeDef],
        "ReplaceUnhealthyInstances": NotRequired[bool],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationTypeDef]],
        "Context": NotRequired[str],
    },
)


class ModifyFleetRequestRequestTypeDef(TypedDict):
    FleetId: str
    DryRun: NotRequired[bool]
    ExcessCapacityTerminationPolicy: NotRequired[FleetExcessCapacityTerminationPolicyType]
    LaunchTemplateConfigs: NotRequired[Sequence[FleetLaunchTemplateConfigRequestTypeDef]]
    TargetCapacitySpecification: NotRequired[TargetCapacitySpecificationRequestTypeDef]
    Context: NotRequired[str]


class DescribeInstancesResultTypeDef(TypedDict):
    Reservations: list[ReservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateFleetResultTypeDef(TypedDict):
    FleetId: str
    Errors: list[CreateFleetErrorTypeDef]
    Instances: list[CreateFleetInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


FleetDataTypeDef = TypedDict(
    "FleetDataTypeDef",
    {
        "ActivityStatus": NotRequired[FleetActivityStatusType],
        "CreateTime": NotRequired[datetime],
        "FleetId": NotRequired[str],
        "FleetState": NotRequired[FleetStateCodeType],
        "ClientToken": NotRequired[str],
        "ExcessCapacityTerminationPolicy": NotRequired[FleetExcessCapacityTerminationPolicyType],
        "FulfilledCapacity": NotRequired[float],
        "FulfilledOnDemandCapacity": NotRequired[float],
        "LaunchTemplateConfigs": NotRequired[list[FleetLaunchTemplateConfigTypeDef]],
        "TargetCapacitySpecification": NotRequired[TargetCapacitySpecificationTypeDef],
        "TerminateInstancesWithExpiration": NotRequired[bool],
        "Type": NotRequired[FleetTypeType],
        "ValidFrom": NotRequired[datetime],
        "ValidUntil": NotRequired[datetime],
        "ReplaceUnhealthyInstances": NotRequired[bool],
        "SpotOptions": NotRequired[SpotOptionsTypeDef],
        "OnDemandOptions": NotRequired[OnDemandOptionsTypeDef],
        "Tags": NotRequired[list[TagTypeDef]],
        "Errors": NotRequired[list[DescribeFleetErrorTypeDef]],
        "Instances": NotRequired[list[DescribeFleetsInstancesTypeDef]],
        "Context": NotRequired[str],
    },
)


class SpotFleetRequestConfigTypeDef(TypedDict):
    ActivityStatus: NotRequired[ActivityStatusType]
    CreateTime: NotRequired[datetime]
    SpotFleetRequestConfig: NotRequired[SpotFleetRequestConfigDataOutputTypeDef]
    SpotFleetRequestId: NotRequired[str]
    SpotFleetRequestState: NotRequired[BatchStateType]
    Tags: NotRequired[list[TagTypeDef]]


class LaunchTemplateOverridesTypeDef(TypedDict):
    InstanceType: NotRequired[InstanceTypeType]
    SpotPrice: NotRequired[str]
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    WeightedCapacity: NotRequired[float]
    Priority: NotRequired[float]
    InstanceRequirements: NotRequired[InstanceRequirementsUnionTypeDef]


class SpotFleetLaunchSpecificationTypeDef(TypedDict):
    AddressingType: NotRequired[str]
    BlockDeviceMappings: NotRequired[Sequence[BlockDeviceMappingTypeDef]]
    EbsOptimized: NotRequired[bool]
    IamInstanceProfile: NotRequired[IamInstanceProfileSpecificationTypeDef]
    ImageId: NotRequired[str]
    InstanceType: NotRequired[InstanceTypeType]
    KernelId: NotRequired[str]
    KeyName: NotRequired[str]
    Monitoring: NotRequired[SpotFleetMonitoringTypeDef]
    NetworkInterfaces: NotRequired[Sequence[InstanceNetworkInterfaceSpecificationUnionTypeDef]]
    Placement: NotRequired[SpotPlacementTypeDef]
    RamdiskId: NotRequired[str]
    SpotPrice: NotRequired[str]
    SubnetId: NotRequired[str]
    UserData: NotRequired[str]
    WeightedCapacity: NotRequired[float]
    TagSpecifications: NotRequired[Sequence[SpotFleetTagSpecificationUnionTypeDef]]
    InstanceRequirements: NotRequired[InstanceRequirementsUnionTypeDef]
    SecurityGroups: NotRequired[Sequence[GroupIdentifierTypeDef]]


class DescribeFleetsResultTypeDef(TypedDict):
    Fleets: list[FleetDataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeSpotFleetRequestsResponseTypeDef(TypedDict):
    SpotFleetRequestConfigs: list[SpotFleetRequestConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


LaunchTemplateOverridesUnionTypeDef = Union[
    LaunchTemplateOverridesTypeDef, LaunchTemplateOverridesOutputTypeDef
]
SpotFleetLaunchSpecificationUnionTypeDef = Union[
    SpotFleetLaunchSpecificationTypeDef, SpotFleetLaunchSpecificationOutputTypeDef
]


class LaunchTemplateConfigTypeDef(TypedDict):
    LaunchTemplateSpecification: NotRequired[FleetLaunchTemplateSpecificationTypeDef]
    Overrides: NotRequired[Sequence[LaunchTemplateOverridesUnionTypeDef]]


LaunchTemplateConfigUnionTypeDef = Union[
    LaunchTemplateConfigTypeDef, LaunchTemplateConfigOutputTypeDef
]


class ModifySpotFleetRequestRequestRequestTypeDef(TypedDict):
    SpotFleetRequestId: str
    LaunchTemplateConfigs: NotRequired[Sequence[LaunchTemplateConfigUnionTypeDef]]
    OnDemandTargetCapacity: NotRequired[int]
    Context: NotRequired[str]
    TargetCapacity: NotRequired[int]
    ExcessCapacityTerminationPolicy: NotRequired[ExcessCapacityTerminationPolicyType]


SpotFleetRequestConfigDataTypeDef = TypedDict(
    "SpotFleetRequestConfigDataTypeDef",
    {
        "IamFleetRole": str,
        "TargetCapacity": int,
        "AllocationStrategy": NotRequired[AllocationStrategyType],
        "OnDemandAllocationStrategy": NotRequired[OnDemandAllocationStrategyType],
        "SpotMaintenanceStrategies": NotRequired[SpotMaintenanceStrategiesTypeDef],
        "ClientToken": NotRequired[str],
        "ExcessCapacityTerminationPolicy": NotRequired[ExcessCapacityTerminationPolicyType],
        "FulfilledCapacity": NotRequired[float],
        "OnDemandFulfilledCapacity": NotRequired[float],
        "LaunchSpecifications": NotRequired[Sequence[SpotFleetLaunchSpecificationUnionTypeDef]],
        "LaunchTemplateConfigs": NotRequired[Sequence[LaunchTemplateConfigUnionTypeDef]],
        "SpotPrice": NotRequired[str],
        "OnDemandTargetCapacity": NotRequired[int],
        "OnDemandMaxTotalPrice": NotRequired[str],
        "SpotMaxTotalPrice": NotRequired[str],
        "TerminateInstancesWithExpiration": NotRequired[bool],
        "Type": NotRequired[FleetTypeType],
        "ValidFrom": NotRequired[TimestampTypeDef],
        "ValidUntil": NotRequired[TimestampTypeDef],
        "ReplaceUnhealthyInstances": NotRequired[bool],
        "InstanceInterruptionBehavior": NotRequired[InstanceInterruptionBehaviorType],
        "LoadBalancersConfig": NotRequired[LoadBalancersConfigUnionTypeDef],
        "InstancePoolsToUseCount": NotRequired[int],
        "Context": NotRequired[str],
        "TargetCapacityUnitType": NotRequired[TargetCapacityUnitTypeType],
        "TagSpecifications": NotRequired[Sequence[TagSpecificationUnionTypeDef]],
    },
)


class RequestSpotFleetRequestRequestTypeDef(TypedDict):
    SpotFleetRequestConfig: SpotFleetRequestConfigDataTypeDef
    DryRun: NotRequired[bool]

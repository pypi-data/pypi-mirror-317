# Dell Unity Family Unisphere Management REST API Resource Types

This document provides a comprehensive list of all resource types available in the Dell Unity Unisphere Management REST API, organized by functional categories.

## Storage Resources

Core storage management and provisioning resources:

- **Storage Resource** (`/api/types/storageResource/instances`)
  - Primary resource for managing storage entities
  - Handles LUNs, filesystems, and VMware datastores

- **Filesystem** (`/api/types/filesystem/instances`)
  - File-based storage management
  - Supports SMB/CIFS and NFS protocols

- **LUN** (`/api/types/lun/instances`)
  - Block storage management
  - iSCSI and Fibre Channel support

- **Pool** (`/api/types/pool/instances`)
  - Storage pool management
  - Capacity and RAID configuration

- **Pool Unit** (`/api/types/poolUnit/instances`)
  - Individual units within storage pools
  - Physical storage allocation

- **Disk Group** (`/api/types/diskGroup/instances`)
  - Disk grouping and management
  - RAID configuration

- **Disk** (`/api/types/disk/instances`)
  - Physical disk management
  - Health monitoring and statistics

## File Sharing Services

Resources for file sharing and protocol management:

- **NAS Server** (`/api/types/nasServer/instances`)
  - File sharing server management
  - Protocol and network configuration

- **CIFS Server** (`/api/types/cifsServer/instances`)
  - Windows file sharing (SMB) configuration
  - Active Directory integration

- **NFS Share** (`/api/types/nfsShare/instances`)
  - Unix/Linux file sharing configuration
  - Export management

- **Quota Configuration** (`/api/types/quotaConfig/instances`)
  - Storage quota settings
  - Usage limits and monitoring

- **Tree Quota** (`/api/types/treeQuota/instances`)
  - Directory-based quotas
  - Hierarchical storage management

- **User Quota** (`/api/types/userQuota/instances`)
  - User-based storage limits
  - Resource allocation control

## Network and Security

Network configuration and security management:

- **DNS Server** (`/api/types/dnsServer/instances`)
  - Domain name resolution
  - Network naming services

- **Kerberos Server** (`/api/types/fileKerberosServer/instances`)
  - Authentication services
  - Security token management

- **LDAP Server** (`/api/types/fileLDAPServer/instances`)
  - Directory services integration
  - User authentication and mapping

- **iSCSI Portal** (`/api/types/iscsiPortal/instances`)
  - iSCSI network endpoints
  - Block storage networking

- **iSCSI Settings** (`/api/types/iscsiSettings/instances`)
  - iSCSI protocol configuration
  - Target and initiator settings

- **Management Interface** (`/api/types/mqmtInterface/instances`)
  - System management networking
  - Administrative access

## Host Management

Host system integration and access control:

- **Host** (`/api/types/host/instances`)
  - Host system registration
  - Access configuration

- **Host Group** (`/api/types/hostGroup/instances`)
  - Host clustering
  - Shared resource access

- **Host IP Port** (`/api/types/hostIPPort/instances`)
  - Network port configuration
  - Connectivity management

- **Host Initiator** (`/api/types/hostInitiator/instances`)
  - Storage access points
  - Protocol endpoints

- **Virtual Machine** (`/api/types/vm/instances`)
  - VM integration
  - Virtual infrastructure management

- **VM Disk** (`/api/types/vmDisk/instances`)
  - Virtual disk management
  - Storage mapping

## System Management

System-wide configuration and monitoring:

- **SNMP Target** (`/api/types/alertConfigSNMPTarget/instances`)
  - SNMP monitoring configuration
  - Alert destinations

- **Email Configuration** (`/api/types/alertEmailConfig/instances`)
  - Email alert settings
  - Notification management

- **Job** (`/api/types/job/instances`)
  - Task management
  - Operation tracking

- **System Capacity** (`/api/types/systemCapacity/instances`)
  - Storage capacity monitoring
  - Resource utilization

## Authentication and Access Control

User and tenant management:

- **ACL User** (`/api/types/aclUser/instances`)
  - Access control lists
  - User permissions

- **Tenant** (`/api/types/tenant/instances`)
  - Multi-tenancy support
  - Resource isolation

## Backup and Protection

Data protection and backup services:

- **NDMP Server** (`/api/types/fileNDMPServer/instances`)
  - Network backup protocol
  - Tape backup integration

- **CHAP Settings** (`/api/types/rpChapSettings/instances`)
  - Authentication for iSCSI
  - Security configuration

## Performance and Optimization

System optimization and performance management:

- **FAST VP** (`/api/types/fastVP/instances`)
  - Automated storage tiering
  - Performance optimization

- **File Events Pool** (`/api/types/fileEventsPool/instances`)
  - File system event monitoring
  - Activity tracking

## Additional Resources

Other specialized resource types:

- **Pool Consumer** (`/api/types/poolConsumer/instances`)
  - Storage resource usage tracking
  - Capacity management

- **Pool Consumer Allocation** (`/api/types/poolConsumerAllocation/instances`)
  - Detailed allocation tracking
  - Resource distribution

- **RAID Group** (`/api/types/raidGroup/instances`)
  - RAID configuration
  - Disk organization

- **DAE** (`/api/types/dae/instances`)
  - Disk Array Enclosure management
  - Hardware monitoring

Each resource type supports standard REST operations (GET, POST, DELETE) as appropriate, with specific endpoints for instance management, queries, and modifications. Refer to the main API documentation for detailed information about supported operations, parameters, and response formats for each resource type.

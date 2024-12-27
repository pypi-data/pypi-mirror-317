# Table of Contents

1) ### [Goals](#Goals)
2) ### [Utilities Structure](#Utilities-Structure)
3) ### [Defining a Holder](#Defining-a-Holder)
4) ### [Final Class Designs](#Final-Class-Designs)
5) ### [File Design](#File-Design)
6) ### [Process](#Process)
7) ### [Requirements List](#Requirements-List)

# Goals

* Play with default class functions
* Play with Enums
* Play with decorative functions (@)
  * A logging decorator
  * Using class decorators (classmethod, staticmethod, attribute, setter)
  * Using dataclass decorator for simple data structures
* Play with creating environments through JSON/YAML files
* Play with passing filepaths as arguments
* Play with hash tables
* Play with "updating" terminal outputs
* Play with load balancing CAs
* Play with auto-generating environments
* Play with testing
* Play with package files
* Play with documentation
* Play with using dataclasses for messages
* Play with AsciiDoc
* Play with TLA+?
* Play with git pushes and signed commits

# Utilities Structure

## Functionality should exist for-

* The Certificate Authority
  * Both Root and Intermediate
* The Certificate Subject and Relying Party
* Certificate Signing Requests
* Certificate Chains
* The Registration Authority
* Renewing and Revoking Certificates
* Certificate Revocation Lists, OCSP, and real-time validation
* Temporary Certificate Local Caching
* General Communication supported by above PKI functionality

The Certificate Authority should be able to keep a database of certificates

## A certificate object should have-

* My own custom certificate object.
* A certificate object from the Cryptography library. - May not be needed anymore
* The holder's unique ID.
* The certificate authority's unique ID.

## Info on certificate content and signing-

* https://www.ssl.com/faqs/what-is-an-x-509-certificate/
* https://learn.microsoft.com/en-us/azure/iot-hub/reference-x509-certificates
* https://medium.com/@kennch/introduction-to-pki-public-key-infrastructure-e7863c9232f9
* https://www.nist.gov/identity-access-management/personal-identity-verification-piv
* https://www.youtube.com/watch?v=5OqgYSXWYQM

## The certificate itself includes-

* The name of the certificate
* Subject Information
  * Country
  * State/Province
  * Locality
  * Organization
  * Organization Unit
  * Common name of the Subject's URL
  * Contact email address
* Issuer Information
  * Country
  * State/Province
  * Locality
  * Organization
  * Common name of Issuing CA certificate
* Certificate Information
  * Unique Serial Number
  * X.509 Version
  * Signature (Hash) Algorithm
  * Validity Range (Exclusive Edges)
* Public Key Information
  * Encryption Algorithm
  * Public Key
  * Key Size
  * Key Usage Cases
* Certificate Signature

# Defining a Holder

## Possible Holders

A holder can be anything that holds a certificate. This includes-

1) Account
   1) User
      1) Guest
      2) Personal
      3) Enterprise
   2) Admin
      1) Domain Admin
      2) Schema Admin
      3) Server Admin
      4) Network Admin
      5) Cloud Admin
      6) Database Admin 
      7) Auditor
2) Operating System
   1) Microsoft
      1) Windows
         1) Windows 2000
            1) Professional
            2) Server
            3) Advanced Server
            4) Datacenter Server
         2) Windows XP
            1) Home
            2) Professional
         3) Windows Vista
            1) Starter
            2) Home Basic
            3) Home Premium
            4) Business
            5) Enterprise
            6) Ultimate
         4) Windows 7
            1) Starter
            2) Home Basic
            3) Home Premium
            4) Business
            5) Enterprise
            6) Ultimate
         5) Windows 8
            1) Home
            2) Pro
            3) Enterprise
         6) Windows 10
            1) Home
            2) Pro
            3) Educational
            4) Enterprise
         7) Windows 11
            1) Home
            2) Pro
            3) Educational
            4) Enterprise
      2) Windows Server
         1) Windows Server 2003
            1) Web
            2) Standard
            3) Enterprise
            4) Datacenter
         2) Windows Server 2008
            1) Web
            2) Standard
            3) Enterprise
            4) Datacenter
            5) Itanium
            6) Foundation
            7) HPC
         3) Windows Server 2012
            1) Foundation
            2) Essentials
            3) Standard
            4) Datacenter
         4) Windows Server 2016
            1) Standard
            2) Datacenter
         5) Windows Server 2019
            1) Standard
            2) Datacenter
         6) Windows Server 2022
            1) Standard
            2) Datacenter
            3) Datacenter Azure
   2) Unix
      1) Linux
         1) Debian
            1) Ubuntu
            2) Linux Mint
            3) Kali Linux
            4) Raspberry Pi
            5) MX Linux
            6) Debian
         2) Red Hat
            1) Red Hat
            2) Fedora
            3) Cent OS
         3) Arch Linux
         4) Gentoo
         5) SUSE
            1) openSUSE
            2) SUSE Linux Enterprise
         6) Alpine
         7) Nix OS
         8) Qubes OS
         9) Ubuntu Server
      2) BSD
         1) FreeBSD
         2) OpenBSD
         3) NetBSD
      3) Solaris
      4) Mac OS X
         1) Leopard
         2) Snow Leopard
         3) Lion
         4) Mountain Lion
         5) Mavericks
         6) Yosemite
         7) El Capitan
         8) Sierra
         9) High Sierra
         10) Mojave
         11) Catalina
         12) Big Sur
         13) Monterey
         14) Ventura
         15) Sonoma
         16) Sequoia
   3) Mobile
      1) iOS
      2) Android
         1) Android Nougat
         2) Android Oreo
         3) Android Pie
         4) Android 10
         5) Android 11
         6) Android 12
         7) Android 13
         8) Android 14
         9) Android 15
         10) Android 16
   4) Routing
      1) ONIE (Open Network Install Environment)
      2) ONL (Open Network Linux)
      3) OPX (OpenSwitch)
      4) DNOS (Dell Network OS)
      5) Junos OS
      6) FBOSS (Facebook Open Switching System)
      7) SONiC (Software for Open Networking in the Cloud)
      8) ArubaOS
      9) Cisco IOS
      10) NX-OS (Nexus NOS)
      11) OpenWrt
3) Hardware
   1) Endpoint
      1) Desktop
         1) Hewlett-Packard
         2) Acer
         3) Dell
         4) Lenovo
         5) Toshiba
         6) IBM
         7) Fujitsu
         8) NEC
         9) Apple
      2) Laptop
         1) Samsung
         2) Razer
         3) Microsoft
         4) MSI
         5) Asus
         6) Acer
         7) Dell
         8) Lenovo
         9) Hewlett-Packard
         10) Apple
      3) Phone
         1) Samsung
         2) Apple
         3) Huawei
         4) Sony
         5) Google
         6) Microsoft
         7) Toshiba
         8) Dell
      4) Server
         1) Dell
         2) Hewlett-Packard
         3) Supermicro
         4) Inspur
         5) Lenovo
         6) Huawei
         7) IBM
         8) Fukitsu
         9) Cisco
      5) IoT
         1) Advantech
         2) Raspberry Pi
         3) Arduino
         4) Nvidia
         5) BeagleBoard
         6) Udoo
         7) OnLogic
         8) Kontron
         9) Arbor
         10) Axiomtek
   2) Network
      1) Router
         1) Cisco
         2) Peplink
         3) Advantech
         4) Netgear
         5) TP-Link
      2) Switch
         1) Anchor
         2) Honeywell
         3) Philips
         4) Siemens
         5) Cisco
         6) HPL
      3) Access Point
         1) Cisco
         2) Fortinet
         3) Netgear
         4) Zyxel
         5) TP-Link
         6) EnGenius
   3) Appliance
      1) Firewall
         1) Bitdefender
         2) Cisco
         3) Fortinet
         4) Palo Alto
         5) Netgate
         6) WatchGuard
         7) SonicWall
      2) UTM Device (i.e. IDS/IPS, DLP, AC, Proxy)
         1) SonicWall
         2) Fortigate
         3) Barracuda
         4) Juniper
         5) Trellix
         6) Palo Alto
   4) Peripheral
      1) USB Key
         1) Samsung
         2) SanDisk
         3) Corsiar
         4) Kingston
         5) PNY
      2) Smart Card
         1) Thales
         2) NXP Semiconductors
         3) CardLogix
         4) Infineon
      3) External Storage
         1) Seagate
         2) Western Digital
         3) SanDisk
         4) Transcend
         5) LaCie

## Holder Identifier

{Hardware Type}.{OS}.{App, Person, or Service}

Short-hand example: Dell.Windows_10.Personal

Long-hand example: Endpoint_Desktop_Dell.Microsoft_Windows_Windows_10.User_Personal

Exceptions include when the OS or Device itself is the Holder, but they still need a unique identifier.

## A Holder Object should have-

* Their Holder type information
* Their Authority information
* Anything required to create a certificate without extensions
* A link that they can be accessed by the simulated network
  * Don't try to use an actual network, just a bunch of fake addresses should work. 
* A hash generated from object content that can used to organize certificates into load balancing CAs.
* Certificates stored on the holder, multiple for CAs.

## Holder CA Status

A holder's device can also be an authority, the status should be attached to the end.

1) Not Authority (Not_Auth)
2) Intermediate Authority (Inter_Auth)
3) Root Authority (Root_Auth)

Short-hand example: Dell.Windows_10.Personal.Not_Auth

Long-hand example: Endpoint_Desktop_Dell.Microsoft_Windows_Windows_10.User_Personal.Not_Auth

## Holder Actions

A holder can perform the following actions-

* All holders
  * Create Key Pairs
  * Create CSRs and send them to registration authorities
  * Request Signing CA's public key and validate certificates
  * Communicate regularly with other entities
* Certificate Authorities Only
  * If Root CA
    * Self-sign own certificate
    * Auto-load own certificate onto all other hardware/software/accounts
  * Return certificates to lower hierarchical respondees
  * Host lower hierarchical certificates on device
  * Registration Duties
    * Accept CSRs
    * Analyze CSRs for basic validity
    * Forward Valid CSRs to corresponding CAs
  * Revocation Duties
    * Routinely check certificates for age

# Final Class Designs

\* = create a requirement to accommodate this

## Certificate Class

### Parameters

* cert_name (str) - Unique Identifier of the certificate

* subject_common_name (str) - Common Domain Name of Subject
* subject_country (str) - Country of Subject
* subject_state (str) - State/Region of Subject
* subject_local (str) - City/Town/Locality of Subject
* subject_org (str) - Organization of Subject
* subject_org_unit (str) - Organizational Unit of Subject
* subject_email (str) - Email of the Subject
* subject_url (str) - Internet Address of the Subject

* issuer_common_name (str) - Common Domain Name of Issuer
* issuer_country (str) - Country of Issuer
* issuer_state (str) - State/Region of Issuer
* issuer_local (str) - City/Town/Locality of Issuer
* issuer_org (str) - Organization of Issuer
* issuer_cert_url (str) - Internet Address of the Issuer

* cert_serial (str) - Unique Serial Number
* cert_x509_ver (int) * - X.509 Version Number
* cert_sig_hash_alg (str) * - Certificate Signature Hashing Algorithm
* cert_not_valid_before (datetime) * - Beginning of Valid Period (Exclusive)
* cert_not_valid_after (datatime) * - End of Valid Period (Exclusive)

* pubkey_encrypt_alg (str) * (Enum, Setup) - Asymmetric Encryption Algorithm
* pubkey_params (dict) * - Asymmetric Encryption Parameters
* pubkey_key (str) * - Asymmetric Encryption Public Key

* cert_signature (str or None) - Digital Signature
* cert_chain (list from top down) - Top Down Certificate Chain

### Methods

* init - creates a certificate
* create_signature - hashes content into a signature

## Holder Class

### Parameters

* holder_name (str) - Unique Identifier of the holder

* holder_env_info (dataclass) - Environment Information
  * holder_level (str) - Holder's Hierarchical Level
  * holder_uid_hash (str) - Holder's UID Hashing Algorithm
  * holder_sig_hash (str) - Holder's Signature Hashing Algorithm
  * holder_encrypt_alg (dict) - Holder's Encryption Algorithm & Params
    * algorithm (str) - Algorithm used
    * params (dict) - Parameters for algorithm
  * revoc_prob (float) - Holder's Revocation Probability
  * cert_valid_dur (datetime or int) - Holder's Certificate Validity Duration
  * cache_dur (datetime or int) - Holder's Regular Cache Duration
  * cooldown_time (datetime or int) - Holder's Cooldown Time
  * timeout_time (datetime or int) - Holder's Wait Time
  * holder_network (HolderNetwork) - Holder's Network

* holder_type_info (dataclass) - Holder's Type Information
  * hardware_type (str) - Holder's Hardware Type
  * hardware_subtype (str) - Holder's Hardware Subtype
  * hardware_brand (str) - Holder's Hardware Brand
  * os_category (str) - Holder's Operating System Category
  * os_subcategory (str) - Holder's Operating System Subcategory
  * os_dist (str) - Holder's Operating System Distribution
  * os_subdist (str) - Holder's Operating System Sub-distribution
  * account_type (str) - Holder's Account Type
  * account_subtype (str) - Holder's Account Subtype
  * ca_status (str) - Holder's Certificate Authority Status
* short_type_name (str) - Holder's Short Type Name
* long_type_name (str) - Holder's Long Type Name

* holder_info (dataclass) - Holder's Information
  * common_name (str) - Holder's Common Domain Name
  * country (str) - Holder's Country
  * state (str) - Holder's State/Region
  * local (str) - Holder's City/Town/Locality
  * org (str) - Holder's Organization
  * org_unit (str) - Holder's Organizational Unit
  * email (str) - Holder's Email
  * url (str) - Holder's Internet Address
* holder_hash (str) - Holder's Hash from Information

* privkey (str) - Holder's Private Key
* pubkey (str) - Holder's Public Key
* holder_certificate (Certificate or None) - Holder's Certificate
* root_certificates (immutable dictionary) - Holder's Root Certificate List
* cached_certificates (mutable dictionary) - Holder's Regular Certificate Cache

* csr_port (queue) - Queue for anything related to Certificate Signing Requests
* message_port (queue) - Queue for anything related to Messages
* oscp_port (queue) - Queue for anything related to OCSP Communications

* has_root_certs (bool) - Holder has root certificates
* has_cert (bool) - Holder has a certificate
* cache_empty (bool) - Holder's regular cache is empty
* waiting_for_csr_response (bool) - Holder is waiting for a CSR response
* waiting_to_send_csr (bool) - Holder's CSR has failed and now is waiting
* waiting_for_response (bool) - Holder is waiting for a response
* waiting_to_send_message (bool) - Holder's response has failed and now is waiting
* waiting_for_revoc_check (bool) - Holder is waiting for a revocation check
* need_new_certificate (bool) - Holder needs a new certificate

### Methods

* init - creates a holder
* hash_identity - hashes all information related to holder identity and returns a hex digest
* send_cert_request - sends a certificate signing request to assigned CA
* receive_csr_response_listener - {may not need this}
* send_data - sends a message to another non-CA holder
* receive_data_listener - {may not need this}
* cache_cert - save a validated cert to cache for a limited amount of time
* check_cache - check if a cert is in the regular cache
* check_root_cache - check if a cert is in the root cache
* check_cert_valid - contact CAs to check if a certificate is valid
* check_csr_port - check if a CSR message is in the queue
* check_message_port - check if a regular message is in the queue
* check_ocsp_port - check if an OCSP message is in the queue
* check_expiration - check if a certificate has expired
* send_self_revoc - send a self revocation message to assigned CA

## CertAuthority Class (Extends Holder)

Needs added functionality for returning certificates, returning certificate responses, checking certificate revocation
statuses, and checking certificate statuses for lower levels.

### Parameters

* valid_cert_list (dict) - Valid Certificate List
* cert_revok_list (dict) - Certificate Revocation List

### Methods

* check_revo_list - checks if a certificate sent is in revocation list
* validate_cert - check if a certificate sent is valid
* send_revoc - send a revocation message to lower level

## HolderNetwork Class

### Parameters

* network_name (str) - Network Name

* network_level_count (str) - Number of Levels in Network Hierarchy
* network_count_by_level (list) - Number of Holders at each level
* network_total_count (int) - Total Number of Holders

* uid_hash (str) - UID Hashing Algorithm
* sig_hash (str) - Signature Hashing Algorithm
* encrypt_alg (dict) - Encryption Algorithm & Params
  * algorithm (str) - Algorithm used
  * params (dict) - Parameters for algorithm
* revoc_probs (list) - Revocation Probabilities for each level
* cert_valid_durs (list) - Certificate Validity Durations for each level
* cache_durs (list) - Regular Cache Duration for each level
* cooldown_durs (list) - Cooldown Time for each level
* timeout_durs (list) - Wait Time for each level

* network (dict) - Network Hierarchy
* network_log (list) - Network Log

### Methods

* init - creates a network
* add_to_network - adds a holder to the network
* contact_holder - bridge between holder
* add_to_log - adds a message to the network log
* save_log - saves the network log to file

# File Design

## Auto

* Number of Root CAs: {enter number here}
* Number of Inter CA levels: {enter number here}
* Number of Inter CAs at each level: {enter list of numbers here}
* Number of Communicating Non-CA devices: {enter number here}

# Process

1) The file contents are read into memory.
   1) If auto, the hierarchical structure is read in first.
      1) The number of root CAs is first.
      2) The number of Inter CA levels is next.
      3) The array of number of Inter CAs at each level is next.
      4) The number of non-CAs is last.
   2) The hashing function used for creating holder hashes is read in.
   3) The hashing function used for creating digital signatures is read in.
   4) The asymmetrical encryption function used throughout the environment is read in.
      1) The parameters needed for the asymmetrical encryption.
   5) The random revocation probabilities for each layer are read in.
   6) The duration of root CA certificates, intermediate CA certificates, and end certificates are read in. 
      1) Formatted in hours, minutes, and seconds for each layer.
   7) The cache duration of intermediate CAs and non-CAs are read in.
      1) Formatted in minutes, and seconds, for each layer.
   8) The CSR cooldown time, or the time to wait if a CSR attempt as failed, is read in.
      1) Formatted in seconds.
   9) The CSR wait time, or the time to wait until a request times out, is read in.
      1) Formatted in seconds.
   10) If manual, the hierarchical structure is read in last.
      1) The number of layers is first.
      2) The list of CAs and non-CAs is next.
2) For each holder read or created-
   1) Phase one
      1) The name of the object is generated as random alphabet characters or loaded in.
      2) The parameters are read through the enums to load the hardware/software/account information.
      3) By default, the extension "Not_Auth" is added as the CA status of the holder
      4) The short and long type names are dynamically created from the information in the above step.
      5) The holder information used for certificates are then loaded in as well.
      6) Everything previously established is then hashed with a hashing function.
      7) The level stated in the file for the holder is read in.
      8) If not root CA-
         1) The holder's hash is then used to determine who they should communicate with on above row.
      9) The encryption key pairs are then generated.
      10) The holder is added to the global network depending on the holder's level.
   2) Phase two
      1) A message cache is created.
      2) If root CA-
         1) A self-signed certificate is created.
      3) If not root CA-
         1) All root certificates are saved to a root cache through the global network.
         2) An empty regular certificate cache is created.
      4) If CA-
         1) An empty certificate revocation list is created.
         2) An empty lower level certificate store is created.
      5) If intermediate CA-
         1) All root certificates are saved to a root cache.
         2) A CSR is submitted to the assigned above CA.
         3) The holder waits for a response and/or certificate from the above CA.
         4) The holder tries again if needed.
      6) If intermediate CA at level 3 or more (meaning they are not directly connected to root CA)-
         1) Add the certificates from the assigned above CA to the regular cache.
   3) Phase three
      1) Non-CA holders communicate random encrypted data with each other.
         1) If the holder does not have a valid certificate, they should first send a CSR to their assigned CA. The 
            holder should then wait for their response and send another if the response fails after a while.
         2) If the holder does have a valid certificate, they are allowed to send the data in a message containing the
            certificate to the recipient's message cache. They must wait for a response to know if the other side
            read the message or not.
         3) If the holder receives a message to their message cache, they shall use the certificate sent inside to
            validate that certificate, using public keys, chains, and other checks. They must send a confirmation or
            rejection message to whoever sent it.
         4) If a holder receives a message rejection response, they must double-check their certificate with their CA
            before trying again.
         5) If a holder receives a message confirmed response, then yippie!
      2) Owners of a certificate (excluding root) can randomly decide whether their certificate is no longer valid and
         request their CA to revoke the status.
         1) This process can be used for renewals with a new coat of paint.
      3) CAs can randomly go through their certificates and randomly decide whether a certificate is no longer valid and
         let their lower-level owner know to make a new one.
         1) This process can be used for renewals with a new coat of paint.
      4) This goes on forever and ever, with all details being logged to file.

# Requirements List

1) Project SHALL simulate an environment where general communication is supported a Public Key Infrastructure to
   provide non-repudiation of encrypted traffic.
2) Project SHALL take JSON or YAML files for designating a hierarchy of root layer CAs, intermediate layer(s) CAs, and
   regular endpoint devices.
   1) Project SHALL pass the desired filepath as a command line argument.
   2) File at filepath SHALL conform to one of two design standards that can be handled by the project.
      1) The first design standard is "auto" and SHALL list how many entities exist at each level of the PKI
         hierarchy.
         1) The auto standard's inputs SHALL be selected in a way that when the numbers of entities per layer are
            arranged from top to bottom in sequential order, all numbers before a given number x are less than x, and
            all numbers after a given number x are greater than x.
         2) The auto standard SHALL automatically generate entities using a predetermined list of values and random
            inputs when names and unique identifiers are needed.
            1) The auto standard SHALL recognize when specific hardware requires specific software and NOT choose
               unrealistic software.
            2) The auto standard SHALL recognize when specific software requires specific accounts and NOT choose
               unrealistic accounts.
            3) The auto standard SHALL recognize when an entity is NOT a non-CA and NOT choose unrealistic hardware,
               software, and accounts.
            4) The auto standard SHALL use enums to conduct this process.
         3) The auto standard SHALL return a timestamped JSON and YAML file of the created hierarchy during the 
            project's runtime.
      2) The second design standard is "manual" and SHALL list out manually created entities, where all relevant 
         fields are present for the entity in question and are either filled or contain an empty string.
      3) There SHALL be default files for both in both JSON and YAML for other users to test. 
      4) Both standards SHALL outline the encryption and hashing algorithms used by the environment.
         1) The chosen encryption algorithm SHALL be an asymmetric encryption algorithm.
         2) Both chosen algorithms SHALL be algorithms recognized as currently viable by NIST or some other valid 
            agency.
      5) Both standards SHALL outline the revocation probability, or the chance that a holder will suddenly decide
         a certificate is no longer valid or usable. This SHALL be used in place of simulating unusual events (i.e.
         compromise of holder in cyberattack).
      6) Both standards SHALL outline the cached time limit, or the amount of time a recently verified certificate
         can stay local to an entity before needing to be reevaluated again.
   3) Any errors that are caused by incorrect files or filepaths being passed into the project SHALL be handled
      gracefully by the project.
   4) In the case where no filepath is passed by the user, the project SHALL have a built-in auto standard setup that
      can run.
      1) The project SHALL inform the user that they must pass the file next time before starting the built-in auto
         standard setup.
   5) All strings used in the configuration file should be lowercase and treated as such explicity.
3) Project SHALL recognize all entities as "holders" that can hold or work with "certificates" to some degree.
   1) Project SHALL have a parsing mechanism to derive the hardware, the operating system (if needed), and the user (if 
      needed) of the holder. 
   2) Project SHALL have a parsing mechanism to assign a holder class or child class depending on the holder's 
      information.
   3) Project SHALL automatically create asymmetric key pairs when creating a holder object.
   4) Project SHALL deem the holder object's name using the syntax shown in the Holder Identifier section if the name
      is NOT already manually established or an empty string.
   5) Project SHALL make any values that are related to identity immutable.
   6) Project SHALL make any functions that do not need to be accessed outside the object private.
4) Project SHALL set up load balancing at all levels, where connections are determined at environment creation.
   1) The load balancing algorithm SHALL use a hash organization method that assigns each CA a hash range. The
      hashes of holder information in the lower level SHALL be used to determine where they will do their PKI 
      communications.
5) Project SHALL have some decorator function method to log the entire runtime, including every distinct action done by 
   the program or the holders.
6) Project SHALL have custom functionality created for the default class methods.
7) Project SHALL satisfy requirements 1-6 above at runtime before even starting the environment simulation.
8) Project SHALL have a test folder that can be used to conduct automatic testing.
9) Project SHALL utilize threading to run all holders at once.
   1) All holders SHALL have mechanisms, flags, and setter functions to facilitate communications.
      1) All holders SHALL be able to "cache" valid certificates and uncache revoked or old-ish certificates.
         1) The parameter to determine how long a certificate can stay cached SHALL be established in environment
            creation.
      2) All holders SHALL have a root cache of certificates from all root CAs.
         1) A holder's root cache SHALL be immutable and without time limit once set up.
      3) All holders SHALL use timestamps set in the future, instead of counters, to determine any sort of expirations.
      4) All holders SHALL check root, then normal caches before checking global index for holders.
   2) All holders that are not CAs SHALL engage in general communication sending random encrypted data from 
      "applications" and "services."
      1) All messages sent between non-CA holders SHALL be signed and endorsed using the PKI architecture.
         1) Non-CA holders SHALL create CSRs to submit before starting communication at all and SHALL have explicit
            measures to prevent such communication.
         2) Non-CA holders who send messages SHALL be responsible for sending a certificate along with it.
         3) Non-CA holders who receive messages SHALL drop any message without a certificate along with it.
      2) The message generation strategy used SHALL recognize when some holders realistically cannot send certain
         types of data and generate accordingly.
   3) All holders that have a certificate SHALL periodically check whether that certificate is valid.
      1) Revoke Decision by holder SHALL have a random chance to take place. This random chance SHALL be established in 
         environment creation.
      2) Holders SHALL communicate this decision with assigned CA and expect a response using a flag and/or other
         measures to help wait safely.
   4) Holders that are CAs SHALL have multiple threads to handle distinct functions.
      1) Holders that are CAs SHALL have a thread for analyzing and responding to CSR requests.
         1) CSR requests that are not being attended to SHALL sit in a dedicated queue for the CA.
         2) Respondees waiting on CA responses SHALL use flags and a dedicated space of their own to handle waiting.
         3) CSR requests SHALL have a small random chance of being rejected. This random chance SHALL be established
            in environment creation.
      2) Holders that are CAs SHALL have a thread for periodically analyzing if certificates need to be revoked.
         1) Certificate revocation analysis SHALL analyze if certificates a) fall outside the expiration date, b) has,
            for some reason, be decided by the CA or the lower-level holder that the certificate no longer works.
            1) Revoke Decision by CA or lower-level holder SHALL have a random chance to take place. This random
               chance SHALL be established in environment creation.
      3) Holders that are CAs SHALL have a thread for responding to certificate revocation checks.
      4) In all threads, Holders that are CAs SHALL always send some response back down to the lower level.
   5) Holders that are root CAs SHALL be excluded from having to communicate outside certain scenarios.
      1) Root CAs SHALL still send public keys when lower levels need to decrypt signatures.
      2) Root CAs SHALL explicitly be excluded from the random chance revoke decision through some measure.

## Depreciated Requirements

* (2.2.X) Both standards SHALL automatically create Registration Authorities for each layer, where RA's would be
   responsible for handling CSRs from lower hierarchical levels.
   1) The top-most root layer SHALL create a RA for each Root CA.
   2) All other layers SHALL have ceil(n / r) RAs, where n is the number of CAs in a given layer, r is the number
      of CAs that SHALL share an RA, and ceil is a function that takes the result and raises the result to the
      nearest whole number that is greater than the result.
   3) The RA ratio factor r SHALL be defined in both standards.

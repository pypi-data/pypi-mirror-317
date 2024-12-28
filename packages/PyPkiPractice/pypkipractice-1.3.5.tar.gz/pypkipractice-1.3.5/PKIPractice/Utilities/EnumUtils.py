"""
This file contains enums used in the program along with functions to retrieve information.
"""

from enum import Enum
from typing import Union


class SUPPORTED_HASH_ALGS(Enum):
    """
    This class contains all supported hash algorithms.
    It is used in both the autoconfiguration and manual configuration to set hashing algorithms.
    """
    SHA224 = 'sha224'
    SHA256 = 'sha256'
    SHA384 = 'sha384'
    SHA512 = 'sha512'
    SHA3_224 = 'sha3_224'
    SHA3_256 = 'sha3_256'
    SHA3_384 = 'sha3_384'
    SHA3_512 = 'sha3_512'
    BLAKE2B = 'blake2b'
    BLAKE2S = 'blake2s'


class SUPPORTED_ENCRYPT_ALGS(Enum):
    """
    This class contains all supported encryption algorithms.
    It is used in both the autoconfiguration and manual configuration to set encryption algorithms.
    """
    RSA = 'rsa'
    ECC = 'ecc'


class SUPPORTED_ECC_CURVES(Enum):
    """
    This class contains all supported curves for eliptic curve cryptography.
    It is used in both the autoconfiguration and manual configuration to set the curve for ECC.
    """
    SECP256R1 = 'secp256r1'
    SECP384R1 = 'secp384r1'
    SECP521R1 = 'secp521r1'
    SECP224R1 = 'secp224r1'
    SECP192R1 = 'secp192r1'
    SECP256K1 = 'secp256k1'


class COMMON_USERS(Enum):
    """
    This class contains all supported user types by default.
    It is used in the manual configuration file to specify user types.
    """
    GUEST = 'guest'
    PERSONAL = 'personal'
    ENTERPRISE = 'enterprise'


class COMMON_ADMINS(Enum):
    """
    This class contains all supported admin types by default.
    It is used in the manual configuration file to specify admin types.
    """
    DOMAIN_ADMIN = 'domain_admin'
    SCHEMA_ADMIN = 'schema_admin'
    SERVER_ADMIN = 'server_admin'
    NETWORK_ADMIN = 'network_admin'
    CLOUD_ADMIN = 'cloud_admin'
    DATABASE_ADMIN = 'database_admin'
    AUDITOR = 'auditor'


class COMMON_ACCOUNTS(Enum):
    """
    This class contains all supported account types by default.
    It is used in the manual configuration file to specify account types.
    """
    USER = 'user'
    ADMIN = 'admin'


class COMMON_WINDOWS(Enum):
    """
    This class contains all supported Windows versions by default.
    It is used in the manual configuration file to specify Windows versions.
    """
    WINDOWS_2000 = ('Professional', 'Server', 'Advanced Server', 'Datacenter Server')
    WINDOWS_XP = ('Home', 'Professional')
    WINDOWS_VISTA = ('Starter', 'Home Basic', 'Home Premium', 'Business', 'Enterprise', 'Ultimate')
    WINDOWS_7 = ('Starter', 'Home Basic', 'Home Premium', 'Business', 'Enterprise', 'Ultimate')
    WINDOWS_8 = ('Home', 'Pro', 'Enterprise')
    WINDOWS_10 = ('Home', 'Pro', 'Educational', 'Enterprise')
    WINDOWS_11 = ('Home', 'Pro', 'Educational', 'Enterprise')


class COMMON_WINDOWS_SERVER(Enum):
    """
    This class contains all supported Windows Server versions by default.
    It is used in the manual configuration file to specify Windows Server versions.
    """
    WINDOWS_SERVER_2003 = ('Web', 'Standard', 'Enterprise', 'Datacenter')
    WINDOWS_SERVER_2008 = ('Web', 'Standard', 'Enterprise', 'Datacenter', 'Itanium', 'Foundation', 'HPC')
    WINDOWS_SERVER_2012 = ('Foundation', 'Essentials', 'Standard', 'Datacenter')
    WINDOWS_SERVER_2016 = ('Standard', 'Datacenter')
    WINDOWS_SERVER_2019 = ('Standard', 'Datacenter')
    WINDOWS_SERVER_2022 = ('Standard', 'Datacenter', 'Datacenter Azure')


class COMMON_MICROSOFT(Enum):
    """
    This class contains all supported Microsoft products by default.
    It is used in the manual configuration file to specify Microsoft products.
    """
    WINDOWS = 'windows'
    WINDOWS_SERVER = 'windows_server'


class COMMON_LINUX(Enum):
    """
    This class contains all supported Linux distributions by default.
    It is used in the manual configuration file to specify Linux distributions.
    """
    DEBIAN = ('Debian', 'Linux Mint', 'Kali Linux', 'Raspberry Pi', 'MX Linux', 'Debian')
    RED_HAT = ('Red Hat', 'Fedora', 'Cent OS')
    ARCH_LINUX = 'Arch Linux'
    GENTOO = 'Gentoo'
    SUSE = ('SUSE Linux Enterprise', 'openSUSE')
    ALPINE = 'Alpine Linux'
    NIX_OS = 'Nix OS'
    QUBES_OS = 'Qubes OS'
    UBUNTU_SERVER = 'Ubuntu Server'


class COMMON_BSD(Enum):
    """
    This class contains all supported BSD distributions by default.
    It is used in the manual configuration file to specify BSD distributions.
    """
    FREE_BSD = 'free_bsd'
    OPEN_BSD = 'open_bsd'
    NET_BSD = 'net_bsd'


class COMMON_MAC_OS_X(Enum):
    """
    This class contains all supported Mac OS X versions by default.
    It is used in the manual configuration file to specify Mac OS X versions.
    """
    LEOPARD = 'leopard'
    SNOW_LEOPARD = 'snow_leopard'
    LION = 'lion'
    MOUNTAIN_LION = 'mountain_lion'
    MAVERICKS = 'mavericks'
    YOSEMITE = 'yosemite'
    EL_CAPITAN = 'el_capitan'
    SIERRA = 'sierra'
    HIGH_SIERRA = 'high_sierra'
    MOJAVE = 'mojave'
    CATALINA = 'catalina'
    BIG_SUR = 'big_sur'
    MONTEREY = 'monterey'
    VENTURA = 'ventura'
    SONOMA = 'sonoma'
    SEQUOIA = 'sequoia'


class COMMON_UNIX(Enum):
    """
    This class contains all supported Unix flavors by default.
    It is used in the manual configuration file to specify Unix flavors.
    """
    LINUX = 'linux'
    BSD = 'bsd'
    SOLARIS = 'solaris'
    MAC_OS_X = 'mac_os_x'


class COMMON_MOBILE(Enum):
    """
    This class contains all supported mobile operating system families by default.
    It is used in the manual configuration file to specify mobile operating system families.
    """
    IOS = 'iOS'
    ANDROID = ('Nougat', 'Oreo', 'Pie', '10', '11', '12', '13', '14', '15', '16')


class COMMON_ROUTING(Enum):
    """
    This class contains all supported routing platforms by default.
    It is used in the manual configuration file to specify routing platforms.
    """
    ONIE = 'Open Network Install Environment'
    ONL = 'Open Network Linux'
    OPX = 'OpenSwitch'
    DNOS = 'Dell Network OS'
    JUNOS = 'Junos OS'
    FBOSS = 'Facebook Open Switching System'
    SONIC = 'Software for Open Networking in the Cloud'
    ARUBA = 'ArubaOS'
    CISCO = 'Cisco IOS'
    NXOS = 'Nexus NOS'
    OPENWRT = 'OpenWrt'


class COMMON_OS(Enum):
    """
    This class contains all supported operating system types by default.
    It is used in the manual configuration file to specify operating system types.
    """
    MICROSOFT = 'microsoft'
    UNIX = 'unix'
    MOBILE = 'mobile'
    ROUTING = 'routing'


class COMMON_ENDPOINT(Enum):
    """
    This class contains all supported endpoint hardware manufacturers by default.
    It is used in the manual configuration file to specify endpoint hardware manufacturers.
    """
    DESKTOP = ('Hewlett-Packard', 'Acer', 'Dell', 'Lenovo', 'Toshiba', 'IBM', 'Fujitsu', 'NEC', 'Apple')
    LAPTOP = ('Samsung', 'Razer', 'Microsoft', 'MSI', 'Asus', 'Acer', 'Dell', 'Lenovo', 'Hewlett-Packard', 'Apple')
    PHONE = ('Samsung', 'Apple', 'Huawei', 'Sony', 'Google', 'Microsoft', 'Toshiba', 'Dell')
    SERVER = ('Dell', 'Hewlett-Packard', 'Supermicro', 'Inspur', 'Lenovo', 'Huawei', 'IBM', 'Fukitsu', 'Cisco')
    IOT = (
        'Advantech', 'Raspberry Pi', 'Arudino', 'Nvidia', 'BeagleBoard',
        'Udoo', 'OnLogic', 'Kontron', 'Arbor', 'Axiomtek'
    )


class COMMON_NETWORK(Enum):
    """
    This class contains all supported network hardware manufacturers by default.
    It is used in the manual configuration file to specify network hardware manufacturers.
    """
    ROUTER = ('Cisco', 'Peplink', 'Advantech', 'Netgear', 'TP-Link')
    SWITCH = ('Anchor', 'Honeywell', 'Philips', 'Siemens', 'Cisco', 'HPL')
    ACCESS_POINT = ('Cisco', 'Fortinet', 'Netgear', 'Zyxel', 'TP-Link', 'EnGenius')


class COMMON_APPLIANCE(Enum):
    """
    This class contains all supported appliance hardware manufacturers by default.
    It is used in the manual configuration file to specify appliance hardware manufacturers.
    """
    FIREWALL = ('Bitdefender', 'Cisco', 'Fortinet', 'Palo Alto', 'Netgate', 'WatchGuard', 'SonicWall')
    UTM_DEVICE = ('SonicWall', 'Fortigate', 'Barracuda', 'Juniper', 'Trellix', 'Palo Alto')


class COMMON_PERIPHERALS(Enum):
    """
    This class contains all supported peripheral hardware manufacturers by default.
    It is used in the manual configuration file to specify peripheral hardware manufacturers.
    """
    USB_KEY = ('Samsung', 'SanDisk', 'Corsiar', 'Kingston', 'PNY')
    SMART_CARD = ('Thales', 'NXP', 'CardLogix', 'Infineon')
    EXTERNAL_STORAGE = ('Seagate', 'Western Digital', 'SanDisk', 'Transcend', 'LaCie')


class COMMON_HARDWARE(Enum):
    """
    This class contains all supported hardware types by default.
    It is used in the manual configuration file to specify hardware types.
    """
    ENDPOINT = 'endpoint'
    NETWORK = 'network'
    APPLIANCE = 'appliance'
    PERIPHERAL = 'peripheral'


def has_value(enum_class, value: str) -> bool:
    """
    Check if a given value exists in the specified enum class.

    Args:
        enum_class: The enum class to check.
        value (str): The value to check.

    Returns:
        bool: True if the value exists in the enum class, False otherwise.
    """
    return value in (item.value for item in enum_class)


def get_all_items(enum_class, verbose: bool = False) -> Union[dict, list]:
    """
    Return the versions of an enum class.
    If verbose is True, return the versions as a dictionary with names and values.
    If verbose is False, return the versions as a list with names only.

    Args:
        enum_class: The enum class to get the versions from.
        verbose (bool): If True, return the versions as a dictionary with names and values.
                        If False, return the versions as a list with names only.

    Returns:
        dict | list: The versions of the enum class.
    """
    if verbose:
        return {item.name: item.value for item in enum_class}
    else:
        return [item.name for item in enum_class]

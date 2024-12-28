"""
This file contains enums used in the program along with functions to retrieve information.
"""

from enum import Enum, StrEnum, auto


class SUPPORTED_HASH_ALGS(StrEnum):
    """
    This class contains all supported hash algorithms.
    It is used in both the autoconfiguration and manual configuration to set hashing algorithms.
    """
    SHA224 = auto()
    SHA256 = auto()
    SHA384 = auto()
    SHA512 = auto()
    SHA3_224 = auto()
    SHA3_256 = auto()
    SHA3_384 = auto()
    SHA3_512 = auto()
    BLAKE2B = auto()
    BLAKE2S = auto()


class SUPPORTED_ENCRYPT_ALGS(StrEnum):
    """
    This class contains all supported encryption algorithms.
    It is used in both the autoconfiguration and manual configuration to set encryption algorithms.
    """
    RSA = auto()
    ECC = auto()


class SUPPORTED_ECC_CURVES(StrEnum):
    """
    This class contains all supported curves for eliptic curve cryptography.
    It is used in both the autoconfiguration and manual configuration to set the curve for ECC.
    """
    SECP256R1 = auto()
    SECP384R1 = auto()
    SECP521R1 = auto()
    SECP224R1 = auto()
    SECP192R1 = auto()
    SECP256K1 = auto()


class COMMON_USERS(StrEnum):
    """
    This class contains all supported user types by default.
    It is used in the manual configuration file to specify user types.
    """
    GUEST = auto()
    PERSONAL = auto()
    ENTERPRISE = auto()


class COMMON_ADMINS(StrEnum):
    """
    This class contains all supported admin types by default.
    It is used in the manual configuration file to specify admin types.
    """
    DOMAIN_ADMIN = auto()
    SCHEMA_ADMIN = auto()
    SERVER_ADMIN = auto()
    NETWORK_ADMIN = auto()
    CLOUD_ADMIN = auto()
    DATABASE_ADMIN = auto()
    AUDITOR = auto()


class COMMON_ACCOUNTS(StrEnum):
    """
    This class contains all supported account types by default.
    It is used in the manual configuration file to specify account types.
    """
    USER = auto()
    ADMIN = auto()


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


class COMMON_MICROSOFT(StrEnum):
    """
    This class contains all supported Microsoft products by default.
    It is used in the manual configuration file to specify Microsoft products.
    """
    WINDOWS = auto()
    WINDOWS_SERVER = auto()


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


class COMMON_BSD(StrEnum):
    """
    This class contains all supported BSD distributions by default.
    It is used in the manual configuration file to specify BSD distributions.
    """
    FREE_BSD = auto()
    OPEN_BSD = auto()
    NET_BSD = auto()


class COMMON_MAC_OS_X(StrEnum):
    """
    This class contains all supported Mac OS X versions by default.
    It is used in the manual configuration file to specify Mac OS X versions.
    """
    LEOPARD = auto()
    SNOW_LEOPARD = auto()
    LION = auto()
    MOUNTAIN_LION = auto()
    MAVERICKS = auto()
    YOSEMITE = auto()
    EL_CAPITAN = auto()
    SIERRA = auto()
    HIGH_SIERRA = auto()
    MOJAVE = auto()
    CATALINA = auto()
    BIG_SUR = auto()
    MONTEREY = auto()
    VENTURA = auto()
    SONOMA = auto()
    SEQUOIA = auto()


class COMMON_UNIX(StrEnum):
    """
    This class contains all supported Unix flavors by default.
    It is used in the manual configuration file to specify Unix flavors.
    """
    LINUX = auto()
    BSD = auto()
    SOLARIS = auto()
    MAC_OS_X = auto()


class COMMON_MOBILE(Enum):
    """
    This class contains all supported mobile operating system families by default.
    It is used in the manual configuration file to specify mobile operating system families.
    """
    IOS = 'iOS'
    ANDROID = ('Nougat', 'Oreo', 'Pie', '10', '11', '12', '13', '14', '15', '16')


class COMMON_ROUTING(StrEnum):
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


class COMMON_OS(StrEnum):
    """
    This class contains all supported operating system types by default.
    It is used in the manual configuration file to specify operating system types.
    """
    MICROSOFT = auto()
    UNIX = auto()
    MOBILE = auto()
    ROUTING = auto()


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


class COMMON_HARDWARE(StrEnum):
    """
    This class contains all supported hardware types by default.
    It is used in the manual configuration file to specify hardware types.
    """
    ENDPOINT = auto()
    NETWORK = auto()
    APPLIANCE = auto()
    PERIPHERAL = auto()


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


def get_all_items(enum_class, verbose: bool = False) -> dict | list:
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

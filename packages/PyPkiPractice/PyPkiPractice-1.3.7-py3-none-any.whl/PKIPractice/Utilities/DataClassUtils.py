from dataclasses import dataclass


@dataclass
class HOLDER_ENV_INFO:
    level: int
    uid_hash: str
    sig_hash: str
    encrypt_alg: dict
    revoc_prob: float
    cert_valid_dur: str
    cache_dur: str
    cooldown_dur: str
    timeout_dur: str


@dataclass
class HOLDER_TYPE_INFO:
    hardware_type: str
    hardware_subtype: str
    hardware_brand: str
    os_category: str
    os_subcategory: str
    os_dist: str
    os_subdist: str
    account_type: str
    account_subtype: str
    ca_status: str

    def __post_init__(self):
        self.hardware_type = self.hardware_type.lower().replace(" ", "_").replace("-", "_")
        self.hardware_subtype = self.hardware_subtype.lower().replace(" ", "_").replace("-", "_")
        self.hardware_brand = self.hardware_brand.lower().replace(" ", "_").replace("-", "_")
        self.os_category = self.os_category.lower().replace(" ", "_").replace("-", "_")
        self.os_subcategory = self.os_subcategory.lower().replace(" ", "_").replace("-", "_")
        self.os_dist = self.os_dist.lower().replace(" ", "_").replace("-", "_")
        self.os_subdist = self.os_subdist.lower().replace(" ", "_").replace("-", "_")
        self.account_type = self.account_type.lower().replace(" ", "_").replace("-", "_")
        self.account_subtype = self.account_subtype.lower().replace(" ", "_").replace("-", "_")
        self.ca_status = self.ca_status.lower().replace(" ", "_").replace("-", "_")

    @property
    def long_name(self):
        return f'{self.hardware_type}_{self.hardware_subtype}_{self.hardware_brand}.' \
               f'{self.os_category}_{self.os_subcategory}_{self.os_dist}_{self.os_subdist}.' \
               f'{self.account_type}_{self.account_subtype}.{self.ca_status}'

    @property
    def short_name(self):
        return f'{self.hardware_brand}.{self.os_subdist}.{self.account_subtype}.{self.ca_status}'


@dataclass
class HOLDER_INFO:
    common_name: str
    country: str
    state: str
    local: str
    org: str
    org_unit: str
    email: str
    url: str

    @property
    def hash_content(self):
        return f'{self.common_name}' \
               f'{self.country}{self.state}{self.local}' \
               f'{self.org}{self.org_unit}{self.email}{self.url}'

import sys
from .IngestUtils import parse_config_auto, parse_config_manual


def get_default_auto() -> dict:
    """
    Retrieve the default autoconfiguration

    Returns:
        dict: The default autoconfiguration
    """
    auto_config: dict = {
        "level_count": 4,
        "count_by_level": [1, 2, 4, 8],
        "uid_hash": "sha256",
        "sig_hash": "sha256",
        "encrypt_alg": {
            "alg": "rsa",
            "params": {
                "pub_exp": 65537,
                "key_size": 2048
            }
        },
        "revoc_probs": [0.0, 0.0001, 0.001, 0.01],
        "cert_valid_durs": ["none", "00:15:00", "00:10:00", "00:05:00"],
        "cache_durs": ["none", "11:00", "06:00", "01:00"],
        "cooldown_durs": ["none", "5", "5", "5"],
        "timeout_durs": ["none", "20", "20", "20"]
    }

    return auto_config


def get_default_manual() -> dict:
    """
    Retrieve the default manual configuration

    Returns:
        dict: The default manual configuration
    """
    manual_config: dict = {
        "default_root_ca": {
            "location": {
                "level": 1,
                "holder": 1
            },
            "env_overrides": {
                "uid_hash": "sha3_512",
                "sig_hash": "sha3_512",
                "encrypt_alg": {
                    "alg": "ecc",
                    "params": {
                        "curve": "secp256r1"
                    }
                },
                "revoc_prob": 0.0,
                "cert_valid_dur": "none",
                "cache_dur": "none",
                "cooldown_dur": "none",
                "timeout_dur": "none"
            },
            "holder_type_info": {
                "hardware_type": "Endpoint",
                "hardware_subtype": "Server",
                "hardware_brand": "Dell",
                "os_category": "Microsoft",
                "os_subcategory": "Windows Server",
                "os_dist": "Windows Server 2019",
                "os_subdist": "Standard",
                "account_type": "Admin",
                "account_subtype": "Domain Admin",
                "ca_status": "Root_Auth"
            },
            "holder_info": {
                "common_name": "Root Enterprises Root CA",
                "country": "US",
                "state": "CA",
                "locality": "San Francisco",
                "org": "Root Enterprises",
                "org_unit": "Certificates",
                "email": "root_ca_team@root_enterprises.com",
                "url": "root_enterprises.com/root_ca"
            }
        },
        "second_lvl_ca_one": {
            "location": {
                "level": 2,
                "holder": 1
            },
            "env_overrides": {
                "uid_hash": "sha512",
                "sig_hash": "sha512",
                "encrypt_alg": {
                    "alg": "ecc",
                    "params": {
                        "curve": "secp256r1"
                    }
                }
            },
            "holder_type_info": {
                "os_category": "Unix",
                "os_subcategory": "Linux",
                "os_dist": "Ubuntu Server"
            }
        },
        "second_lvl_ca_two": {
            "location": {
                "level": 2,
                "holder": 2
            },
            "env_overrides": {
                "uid_hash": "sha512",
                "sig_hash": "sha512",
                "encrypt_alg": {
                    "alg": "ecc",
                    "params": {
                        "curve": "secp256r1"
                    }
                }
            },
            "holder_type_info": {
                "os_category": "Unix",
                "os_subcategory": "Linux",
                "os_dist": "Ubuntu Server"
            }
        },
        "third_lvl_ca_one": {
            "location": {
                "level": 3,
                "holder": 1
            },
            "env_overrides": {
                "uid_hash": "sha512",
                "sig_hash": "sha512"
            },
            "holder_info": {
                "common_name": "Cert Incorporated South America CA",
                "country": "PE",
                "state": "Lima",
                "locality": "Ventanilla",
                "org": "Cert Incorporated",
                "org_unit": "South American Certificates",
                "email": "certs_sa@cert_incorporated.com",
                "url": "cert_incorporated.com/peru/intermediate_ca"
            }
        },
        "third_lvl_ca_two": {
            "location": {
                "level": 3,
                "holder": 2
            },
            "env_overrides": {
                "uid_hash": "sha512",
                "sig_hash": "sha512"
            },
            "holder_info": {
                "common_name": "CloudCert Inc West Africa CA",
                "country": "Nigeria",
                "state": "Oyo",
                "locality": "Ibadan",
                "org": "CloudCert Inc",
                "org_unit": "West African Certificates",
                "email": "certs_africa@cloudcert.com",
                "url": "cloudcert.com/nigeria/intermediate_ca"
            }
        },
        "third_lvl_ca_three": {
            "location": {
                "level": 3,
                "holder": 3
            },
            "env_overrides": {
                "uid_hash": "sha512",
                "sig_hash": "sha512"
            },
            "holder_info": {
                "common_name": "EuroPass International Norway CA",
                "country": "NO",
                "state": "Bergen",
                "locality": "Kokstad",
                "org": "EuroPass International",
                "org_unit": "Western European Certificates",
                "email": "certs_europe@europass.com",
                "url": "europass.com/norway_intermediate_ca"
            }
        },
        "third_lvl_ca_four": {
            "location": {
                "level": 3,
                "holder": 4
            },
            "env_overrides": {
                "uid_hash": "sha512",
                "sig_hash": "sha512"
            },
            "holder_info": {
                "common_name": "Lone Star Networking Houston CA",
                "country": "US",
                "state": "Texas",
                "locality": "Houston",
                "org": "Lone Star Networking",
                "org_unit": "North American Certificates",
                "email": "lone_star_certs@lonestarnet.com",
                "url": "lonestarnet.com/us/houston/intermediate_ca"
            }
        },
        "fourth_level_one": {
            "location": {
                "level": 4,
                "holder": 1
            },
            "holder_type_info": {
                "hardware_type": "Network",
                "hardware_subtype": "Access Point",
                "hardware_brand": "Cisco",
                "os_category": "Routing",
                "os_subcategory": "OpenWrt",
                "os_dist": "OpenWrt",
                "os_subdist": "OpenWrt",
                "account_type": "Admin",
                "account_subtype": "Network Admin"
            }
        },
        "fourth_level_two": {
            "location": {
                "level": 4,
                "holder": 2
            },
            "holder_type_info": {
                "hardware_type": "Endpoint",
                "hardware_subtype": "Laptop",
                "hardware_brand": "Asus",
                "os_category": "Microsoft",
                "os_subcategory": "Windows",
                "os_dist": "Windows 10",
                "os_subdist": "Home",
                "account_type": "User",
                "account_subtype": "Personal"
            }
        },
        "fourth_level_three": {
            "location": {
                "level": 4,
                "holder": 3
            },
            "holder_type_info": {
                "hardware_type": "Peripheral",
                "hardware_subtype": "Smart Card",
                "account_type": "User",
                "account_subtype": "Enterprise"
            }
        },
        "fourth_level_four": {
            "location": {
                "level": 4,
                "holder": 4
            },
            "holder_type_info": {
                "hardware_type": "Endpoint",
                "hardware_subtype": "Mobile",
                "account_type": "User"
            }
        },
        "fourth_level_five": {
            "location": {
                "level": 4,
                "holder": 5
            },
            "holder_type_info": {
                "hardware_type": "Appliance",
                "hardware_subtype": "UTM",
                "hardware_brand": "Barracuda",
                "account_type": "Admin",
                "account_subtype": "Network Admin"
            }
        },
        "fourth_level_six": {
            "location": {
                "level": 4,
                "holder": 6
            },
            "holder_type_info": {
                "hardware_type": "Endpoint",
                "hardware_subtype": "Desktop",
                "os_category": "Unix",
                "os_subcategory": "Solaris",
                "account_subtype": "Cloud Admin"
            }
        },
        "fourth_level_seven": {
            "location": {
                "level": 4,
                "holder": 7
            },
            "holder_type_info": {
                "hardware_type": "Endpoint",
                "hardware_subtype": "IoT",
                "hardware_brand": "Arduino",
                "os_category": "Unix",
                "os_subcategory": "Linux",
                "os_dist": "Alpine",
                "os_subdist": "Alpine",
                "account_type": "User",
                "account_subtype": "Guest"
            }
        },
        "fourth_level_eight": {
            "location": {
                "level": 4,
                "holder": 8
            },
            "holder_type_info": {
                "os_subcategory": "Mac OS X"
            }
        }
    }

    return manual_config


def start_program(args: list, default: bool = False) -> None:
    """
    Starts the program using the command-line arguments.

    Args:
        args (list): A list of command-line arguments.
        default (bool, optional): If True, use the default configuration files. Defaults to False.
    """
    # Check if there is a proper argument for the auto generation
    assert 'auto' in args[1] or default, (
        'Invalid configuration filepath provided.\n'
        '\t   Please provide a proper auto configuration file by '
        'passing the filepath of your file as an command-line argument.\n'
        '\t   Example: python Main.py Default_Configs/default_auto.yaml\n'
    )

    # Check if there is a proper argument for the manual settings or if it's just one argument
    only_auto: bool = len(args) == 2
    if only_auto:
        manual_exists: bool = True
    else:
        manual_exists: bool = 'manual' in args[2]
    assert manual_exists is True, (
        'Invalid configuration filepath provided.\n'
        '\t   Please provide a proper manual configuration file by '
        'passing the filepath of your file as an command-line argument.\n'
        '\t   Example: python Main.py Default_Configs/default_auto.yaml Default_Configs/default_manual.yaml\n'
    )

    # Warn if there are more than the two arguments that have been checked
    if len(args) > 3:
        print('Warning: More than two command-line argument provided.\n'
              '\t Please provide a configuration file by '
              'passing the filepath of your file as an command-line argument.\n'
              '\t   Example: python Main.py Default_Configs/default_auto.yaml '
              'Default_Configs/default_manual.yaml\n')

    # Pass auto argument to ingestion utilities
    if default:
        env_auto_settings: dict | None = get_default_auto()
    else:
        env_auto_settings: dict | None = parse_config_auto(args[1])

    # Pass manual argument to ingestion utilities
    if default:
        env_manual_settings: dict | None = get_default_manual()
    else:
        if len(args) > 2:
            env_manual_settings: dict | None = parse_config_manual(args[2])
        else:
            env_manual_settings: dict | None = None

    # Check the return values for both
    assert env_auto_settings is not None, (
        'Unparseable autoconfiguration file provided.\n'
        '\t   Please ensure that your configuration file exists or are properly created.\n'
        '\t   Use the default configuration files provided in the Default_Configs folder as a guide.\n'
    )

    if len(args) > 2:
        assert env_manual_settings is not None, (
            'Unparseable manual configuration file provided.\n'
            '\t   Please ensure that your configuration file exists or are properly created.\n'
            '\t   Use the default configuration files provided in the Default_Configs folder as a guide.\n'
        )

    print('Was able to print both.')


def basic_check() -> None:
    try:
        # Check if there are more than one argument
        assert len(sys.argv) > 1, (
            'No configuration file provided.\n' 
            '\t   Please provide a configuration file by '
            'passing the filepath of your file as an command-line argument.\n'
            '\t   Example: python Main.py Default_Configs/default_auto.yaml\n'
        )

        # Check if there is a help flag
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(
                '   Help flag detected.\n'
                '   Welcome to PKI Practice!\n'
                '   This is not really meant for much, I just wanted to practice PKI architecture.\n'
                '   However, that does not mean that it should not be fun to play with.\n'
                '\n'
                '   In terms of command-line usage, you need to provide only to files.\n'
                '   The first is a configuration file for the auto generation of the environment.\n'
                '   The second is a configuration file for the manual configuration of the environment.\n'
                '   The second file is optional to run the program, but the first can be run without the second.\n'
                '\n'
                '   Structure: python Main.py [-h | --help] [<autoconfig filepath>] [<manualconfig filepath>]\n'
                '   Example without second: python Main.py Default_Configs/default_auto.yaml\n'
                '   Example with second: python Main.py Default_Configs/default_auto.yaml '
                'Default_Configs/default_manual.yaml\n'
                '\n'
                '   For more details, please check the README file.\n'
            )

        # Check if there is a default flag
        elif sys.argv[1] == '-d' or sys.argv[1] == '--default':
            print(
                '   Default flag detected.\n'
                '   Welcome to PKI Practice!\n'
                '   This is not really meant for much, I just wanted to practice PKI architecture.\n'
                '   However, that does not mean that it should not be fun to play with.\n'
                '\n'
                '   In terms of command-line usage, you need to provide only to files.\n'
                '   The first is a configuration file for the auto generation of the environment.\n'
                '   The second is a configuration file for the manual configuration of the environment.\n'
                '   The second file is optional to run the program, but the first can be run without the second.\n'
                '\n'
                '   Structure: python Main.py [-h | --help] [<autoconfig filepath>] [<manualconfig filepath>]\n'
                '   Example without second: python Main.py Default_Configs/default_auto.yaml\n'
                '   Example with second: python Main.py Default_Configs/default_auto.yaml '
                'Default_Configs/default_manual.yaml\n'
                '\n'
                '   For more details, please check the README file.\n'
                '\n'
                '   For now though, here is a default run of the program using the default yaml files.\n'
            )

            start_program(sys.argv, default=True)

        # No options apply, so just start the program
        else:
            start_program(sys.argv)

    # Ultimate error escape
    except AssertionError as e:
        print(f'\nException: {e}')

"""
This file contains functions for parsing configuration files and validating their input.
"""

import yaml
import json
import xmltodict
import tomllib
import re
from .EnumUtils import *


def adjust_types_auto(settings: dict) -> dict or None:
    """
    Adjusts the data types and format of the settings dictionary.

    Args:
        settings (dict): The dictionary to be modified and wrangled.

    Returns:
        dict: The tailored dictionary.
    """

    try:
        settings['level_count'] = int(settings['level_count'])
        settings['count_by_level'] = list(map(int, settings['count_by_level']))
        settings['uid_hash'] = settings['uid_hash'].lower().replace('-', '_')
        settings['sig_hash'] = settings['sig_hash'].lower().replace('-', '_')
        settings['encrypt_alg']['alg'] = settings['encrypt_alg']['alg'].lower()

        if settings['encrypt_alg']['alg'] == 'rsa':
            settings['encrypt_alg']['params']['pub_exp'] = int(settings['encrypt_alg']['params']['pub_exp'])
            settings['encrypt_alg']['params']['key_size'] = int(settings['encrypt_alg']['params']['key_size'])
        if settings['encrypt_alg']['alg'] == 'ecc':
            settings['encrypt_alg']['params']['curve'] = settings['encrypt_alg']['params']['curve'].lower()

        settings['revoc_probs'] = list(map(float, settings['revoc_probs']))
    except (KeyError, TypeError, ValueError) as e:
        topic = re.search(r"'(.*?)'", str(e)).group(1)
        print(f'Either "{topic}" is a missing key word, or "{topic}" is not the correct data type.\nIf the former is '
              'true, please add it to the configuration file.\nIf the latter is true, look for where it is used in '
              'the autoconfiguration file, as that is likely the problem.')
        return None

    return settings


def validate_settings_auto(settings: dict) -> bool:
    """
    Validates the settings dictionary.

    Args:
        settings (dict): The dictionary to be validated.

    Returns:
        bool: True if the settings are valid, False otherwise.
    """

    # Checking the existence and lengths of lists
    try:
        for setting in [
            settings['count_by_level'], settings['revoc_probs'], settings['cert_valid_durs'],
            settings['cache_durs'], settings['cooldown_durs'], settings['timeout_durs']
        ]:
            if not isinstance(setting, list):
                print(f'The value {setting} is not a list. Please fix this in the autoconfiguration file.')
                return False
            if len(setting) != settings['level_count']:
                print(f'The number of values in the list {setting} must match the level_count parameter. '
                      'Please fix this in the autoconfiguration file.')
                return False
    except KeyError as e:
        print(f'{e} is a missing key required in the autoconfiguration file. Please add it.')
        return False

    # Checking existence of untouched strings
    if not settings['uid_hash'] or not settings['sig_hash'] or not settings['encrypt_alg']['alg']:
        print('uid_hash, sig_hash, and encrypt_alg.alg are missing from the autoconfiguration file. Please add them.')
        return False

    # Checking durations for correct formats
    for dur in settings['cert_valid_durs']:
        if not (re.match(r'^[0-9]+:[0-9]{2}:[0-9]{2}$', dur) or dur == 'none'):
            print(f'"{dur}" is not a valid input for cert_valid_durs. Please fix this in the autoconfiguration file.')
            return False

    for dur in settings['cache_durs']:
        if not (re.match(r'^[0-9]{2}:[0-9]{2}$', dur) or dur == 'none'):
            print(f'"{dur}" is not a valid input for cache_durs. Please fix this in the autoconfiguration file.')
            return False

    for dur in settings['cooldown_durs']:
        if not (re.match(r'^[0-9]+$', dur) or dur == 'none'):
            print(f'"{dur}" is not a valid input for cooldown_durs. Please fix this in the autoconfiguration file.')
            return False

    for dur in settings['timeout_durs']:
        if not (re.match(r'^[0-9]+$', dur) or dur == 'none'):
            print(f'"{dur}" is not a valid input for timeout_durs. Please fix this in the autoconfiguration file.')
            return False

    # Checking if revoc_probs are between 0 and 1 inclusive
    for prob in settings['revoc_probs']:
        if prob < 0.0 or prob > 1.0:
            print(f'"{prob}" is not a valid input for revoc_probs and must be between 0 and 1. '
                  'Please fix this in the autoconfiguration file.')
            return False

    # Checking if parameters for hashing and encryption are valid
    if not has_value(SUPPORTED_HASH_ALGS, settings['uid_hash']):
        print(f'"{settings["uid_hash"]}" is not a valid input for uid_hash. Please fix this in the autoconfiguration ' 
              'file.')
        return False

    if not has_value(SUPPORTED_HASH_ALGS, settings['sig_hash']):
        print(f'"{settings["sig_hash"]}" is not a valid input for sig_hash. Please fix this in the autoconfiguration '
              'file.')
        return False

    if not has_value(SUPPORTED_ENCRYPT_ALGS, settings['encrypt_alg']['alg']):
        print(f'"{settings["encrypt_alg"]["alg"]}" is not a valid input for encrypt_alg.alg. Please fix this in the '
              'autoconfiguration file.')
        return False

    if settings['encrypt_alg']['alg'] == 'ecc':
        if not has_value(SUPPORTED_ECC_CURVES, settings['encrypt_alg']['params']['curve']):
            print(f'"{settings["encrypt_alg"]["params"]["curve"]}" is not a valid input for '
                  'encrypt_alg.params.curve. Please fix this in the autoconfiguration file.')
            return False

    return True


def parse_config_auto(filepath: str) -> dict or None:
    """
    Parses an autoconfiguration file given its file path.

    Args:
        filepath (str): The path to the configuration file to be parsed.

    Returns:
        dict: A dictionary containing the parsed configuration data.
    """

    settings: dict | None = None

    # Check file type
    assert any(ext in filepath for ext in ['.yaml', '.yml', '.json', '.xml', '.toml']), (
        'Invalid autoconfiguration configuration file provided.\n'
        '\t   Please provide a configuration file that is a YAML, JSON, XML, or TOML file.\n'
        '\t   Look in the Default_Configs folder for examples.\n'
    )

    # File type tree
    try:
        if filepath.endswith('.yaml') or filepath.endswith('.yml'):
            with open(filepath, 'r') as file:
                settings = yaml.load(file, Loader=yaml.Loader)
        elif filepath.endswith('.json'):
            with open(filepath, 'r') as file:
                settings = json.load(file)
        elif filepath.endswith('.xml'):
            with open(filepath, 'r') as file:
                settings = xmltodict.parse(file.read())
                settings = settings['config']
        elif filepath.endswith('.toml'):
            with open(filepath, 'rb') as file:
                settings = tomllib.load(file)
    except Exception as e:
        print(f'Ingestion libraries experienced an error: "{str(e).title()}"')
        return settings

    # Type adjustment
    settings = adjust_types_auto(settings)
    assert settings is not None, (
        'Ingested autoconfiguration settings were not able to be adjusted due to incorrect configuration format.\n'
        '\t   Please ensure your configuration file is correctly created.\n'
        '\t   Use the default configuration file as a template.\n'
    )

    # Settings validation
    assert validate_settings_auto(settings) is True, (
        'Ingested autoconfiguration settings were not found to be valid.\n'
        '\t   Please ensure your configuration file is correctly created.\n'
        '\t   Use the default configuration file as a template.\n'
    )

    return settings


def search_for_typecast_manual(settings: dict) -> dict or None:
    """
    Adjusts the data types and format of the settings dictionary.

    Args:
        settings (dict): The dictionary to be modified and wrangled.

    Returns:
        dict: The tailored dictionary.
    """

    try:
        for key, value in settings.items():
            if key in ['level', 'holder', 'pub_exp', 'key_size']:
                settings[key] = int(value)
            elif key in ['revoc_prob']:
                settings[key] = float(value)
            elif isinstance(value, dict):
                settings[key] = search_for_typecast_manual(value)
                assert settings[key] is not None, (
                    'Ingested manual configuration settings were not able to be adjusted '
                    'due to incorrect configuration format.\n'
                    '\t   Please ensure your configuration file is correctly created.\n'
                    '\t   Use the default configuration file as a template.\n'
                )
        return settings
    except (KeyError, TypeError, ValueError) as e:
        print(e)
        print(f'Look for where "{re.search(r"'(.*?)'", str(e)).group(1)}" '
              'is used in the manual configuration file, as that is likely the problem.')
        return None


def parse_config_manual(filepath: str) -> dict or None:
    """
    Parses a manual configuration file given its file path.

    Args:
        filepath (str): The path to the configuration file to be parsed.

    Returns:
        dict: A dictionary containing the parsed configuration data.
    """

    settings: dict | None = None

    # Check file type
    assert any(ext in filepath for ext in ['.yaml', '.yml', '.json', '.xml', '.toml']), (
        'Invalid manual configuration file provided.\n'
        '\t   Please provide a configuration file that is a YAML, JSON, XML, or TOML file.\n'
        '\t   Look in the Default_Configs folder for examples.\n'
    )

    # File type tree
    try:
        if filepath.endswith('.yaml') or filepath.endswith('.yml'):
            with open(filepath, 'r') as file:
                settings = yaml.load(file, Loader=yaml.Loader)
        elif filepath.endswith('.json'):
            with open(filepath, 'r') as file:
                settings = json.load(file)
        elif filepath.endswith('.xml'):
            with open(filepath, 'r') as file:
                settings = xmltodict.parse(file.read())
                settings = settings['config']
        elif filepath.endswith('.toml'):
            with open(filepath, 'rb') as file:
                settings = tomllib.load(file)
    except Exception as e:
        print(f'Ingestion libraries experienced an error: "{str(e).title()}"')
        return settings

    # Type adjustment
    settings = search_for_typecast_manual(settings)
    assert settings is not None, (
        'Ingested manual configuration settings were not able to be adjusted due to unparsable configuration params.\n'
        '\t   Please ensure your configuration file is correctly created.\n'
        '\t   Use the default configuration file as a template.\n'
    )

    return settings

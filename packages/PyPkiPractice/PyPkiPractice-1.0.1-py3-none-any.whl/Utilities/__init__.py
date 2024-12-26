"""
This module provides utilities for parsing configuration files and working with enums.

Utilities:
    parse_config_auto: Parses an autoconfiguration file in JSON, YAML, XML, or TOML format.
    parse_config_manual: Parses a manual configuration file in JSON, YAML, XML, or TOML format.
    EnumUtils: Utilities for working with enums.
"""

__all__ = ["parse_config_auto", "parse_config_manual", "EnumUtils", "basic_check"]

from .IngestUtils import parse_config_auto, parse_config_manual
from . import EnumUtils
from .CLIUtils import basic_check

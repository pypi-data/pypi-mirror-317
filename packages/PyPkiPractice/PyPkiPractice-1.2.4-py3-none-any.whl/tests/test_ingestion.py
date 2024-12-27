import unittest

# Append the parent directory to the sys.path
import sys
from os.path import curdir, abspath, basename, join, dirname
sys.path.append(abspath(join(dirname(__file__), '..')))

# Personal Modules must be imported after the system path is modified.
from ..Utilities import parse_config_auto, parse_config_manual


class TestIngestion(unittest.TestCase):
    def setUp(self):
        current_dir = basename(abspath(curdir))
        if current_dir in ['PKI_Practice', 'PKI Practice']:
            self.dc_dir = './'
        elif current_dir == 'PKIPractice':
            self.dc_dir = '../'
        elif current_dir == 'tests':
            self.dc_dir = '../../'
        else:
            self.dc_dir = './'
            
    def test_key_count_auto(self) -> None:
        """
        Checks if the number of keys in the auto config files is consistent across all formats.
        """
        def total_keys(test_dict: dict) -> int:
            return 0 if not isinstance(test_dict, dict) else len(test_dict) + sum(
                total_keys(val) for val in test_dict.values())

        config_json: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.json')
        config_yaml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.yaml')
        config_xml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.xml')
        config_toml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.toml')

        count_yaml: int = total_keys(config_yaml)
        count_json: int = total_keys(config_json)
        count_xml: int = total_keys(config_xml)
        count_toml: int = total_keys(config_toml)

        self.assertNotEqual(count_yaml, 0)
        self.assertNotEqual(count_json, 0)
        self.assertNotEqual(count_xml, 0)
        self.assertNotEqual(count_toml, 0)

        self.assertEqual(count_yaml, count_json)
        self.assertEqual(count_yaml, count_xml)
        self.assertEqual(count_yaml, count_toml)

    def test_key_count_manual(self) -> None:
        """
        Checks if the number of keys in the manual config files is consistent across all formats.
        """
        def total_keys(test_dict: dict) -> int:
            return 0 if not isinstance(test_dict, dict) else len(test_dict) + sum(
                total_keys(val) for val in test_dict.values())

        config_json: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.json')
        config_yaml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.yaml')
        config_xml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.xml')
        config_toml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.toml')

        count_yaml: int = total_keys(config_yaml)
        count_json: int = total_keys(config_json)
        count_xml: int = total_keys(config_xml)
        count_toml: int = total_keys(config_toml)

        self.assertNotEqual(count_yaml, 0)
        self.assertNotEqual(count_json, 0)
        self.assertNotEqual(count_xml, 0)
        self.assertNotEqual(count_toml, 0)

        self.assertEqual(count_yaml, count_json)
        self.assertEqual(count_yaml, count_xml)
        self.assertEqual(count_yaml, count_toml)

    def test_key_types_auto(self) -> None:
        """
        Checks if the key types in the auto config files are consistent across all formats.
        """
        config_json: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.json')
        config_yaml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.yaml')
        config_xml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.xml')
        config_toml: dict = parse_config_auto(f'{self.dc_dir}Default_Configs/default_auto.toml')

        self.assertEqual(config_yaml, config_json)
        self.assertEqual(config_yaml, config_xml)
        self.assertEqual(config_yaml, config_toml)

    def test_key_types_manual(self) -> None:
        """
        Checks if the key types in the manual config files are consistent across all formats.
        """
        config_json: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.json')
        config_yaml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.yaml')
        config_xml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.xml')
        config_toml: dict = parse_config_manual(f'{self.dc_dir}Default_Configs/default_manual.toml')

        self.assertEqual(config_yaml, config_json)
        self.assertEqual(config_yaml, config_xml)
        self.assertEqual(config_yaml, config_toml)


if __name__ == '__main__':
    unittest.main()

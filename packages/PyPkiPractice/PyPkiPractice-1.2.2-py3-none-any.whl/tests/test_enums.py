import unittest
import inspect

# Append the parent directory to the sys.path
import sys
from os.path import curdir, abspath, basename, join, dirname
sys.path.append(abspath(join(dirname(__file__), '..')))

# Personal Modules must be imported after the system path is modified.
from ..Utilities import EnumUtils


class TestEnums(unittest.TestCase):
    def test_enum_retrieval(self):
        def get_classes_from_module(module):
            return [cls for name, cls in inspect.getmembers(module, inspect.isclass) if
                    cls.__module__ == module.__name__]

        enums = get_classes_from_module(EnumUtils)
        for enum in enums:
            self.assertIsNotNone(EnumUtils.get_all_items(enum))
            self.assertIsNotNone(EnumUtils.get_all_items(enum, True))

    def test_enum_default_values(self):
        def get_classes_from_module(module):
            return [cls for name, cls in inspect.getmembers(module, inspect.isclass) if
                    cls.__module__ == module.__name__]

        enums = get_classes_from_module(EnumUtils)
        for enum in enums:
            info = EnumUtils.get_all_items(enum, True)
            for name, value in info.items():
                self.assertEqual(value, enum[name].value)

    def test_enum_value_type(self):
        def get_classes_from_module(module):
            return [cls for name, cls in inspect.getmembers(module, inspect.isclass) if
                    cls.__module__ == module.__name__]

        enums = get_classes_from_module(EnumUtils)
        for enum in enums:
            info = EnumUtils.get_all_items(enum, True)
            for name, value in info.items():
                self.assertIsInstance(value, tuple | str)

                if isinstance(value, tuple):
                    for v in value:
                        self.assertIsInstance(
                            v,
                            str,
                            f'{v} is not a string, it is a {type(v)}. This is in the {name} enum for the '
                            f'{enum.__name__} class.'
                        )


if __name__ == '__main__':
    unittest.main()

import sys
from os.path import curdir, abspath, basename
from .IngestUtils import parse_config_auto, parse_config_manual


def start_program(args: list) -> None:
    """
    Starts the program using the command-line arguments.

    Args:
        args (list): A list of command-line arguments.
    """
    # Check if there is a proper argument for the auto generation
    assert 'auto' in args[1], (
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
    env_auto_settings: dict | None = parse_config_auto(args[1])

    # Pass manual argument to ingestion utilities
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
            current_dir = basename(abspath(curdir))
            if current_dir == 'Utilities':
                start_program([
                    sys.argv[0],
                    '../../Default_Configs/default_auto.yaml',
                    '../../Default_Configs/default_manual.yaml'
                ])
            elif current_dir == 'PKIPractice':
                start_program([
                    sys.argv[0],
                    '../Default_Configs/default_auto.yaml',
                    '../Default_Configs/default_manual.yaml'
                ])
            elif current_dir in ['PKI Practice', 'PKI_Practice']:
                start_program([
                    sys.argv[0],
                    'Default_Configs/default_auto.yaml',
                    'Default_Configs/default_manual.yaml'
                ])
            else:
                print(
                    '   Something went wrong with the default run of the program.\n'
                    '   A common folder was not detected.\n'
                )
        else:
            start_program(sys.argv)

    # Ultimate error escape
    except AssertionError as e:
        print(f'\nException: {e}')

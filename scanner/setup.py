from setuptools import setup, find_packages

setup(
    name='ip_scanner_project',
    version='1.0.0',
    author='Barton Elles',
    description=('Provides an IP scanner library and CLI wrapper. Checks if '
    'given IP addresses match specified software (nginx and IIS) and versions, ' 
    'and if they have a directory listing available at the root directory. '
    'Wrapper can be ran with ip-scanner-project-cli --ips <ip> <ip>'),
    packages=['', 'cli'],
    install_requires=[
        'requests==2.31.0',
        'termcolor==2.3.0'
    ],
    entry_points={
        'console_scripts': [
            'ip-scanner-project-cli=cli.cli_wrapper:main'
        ]
    },
)

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='tranzit',
    packages=['tranzit'],
    install_requires=[
        'aiohttp==2.3.10',
        'aiohttp_session==2.2.0',
        'pyyaml==5.4',
        'cryptography==2.2.2'
    ],
    version='0.1.1',
    description='asynchronous http web framework based on '
                'aiohttp providing websocket server functionality',
    keywords='async http web framework websocket server',
    url='https://github.com/artkra/tranzit',
    download_url='https://github.com/artkra/tranzit/archive/0.1.tar.gz',
    author='Art Krasnyy',
    author_email='artkrasnyy@gmail.com',
    license='GPL-2.0',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    entry_points={
        'console_scripts':
            ['tranzit = tranzit:cli_handler']
    }
)
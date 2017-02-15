try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'basic console based chat server',
    'author': 'Tyrone Lagore',
    'url': '',
    'download_url': 'https://github.com/tlagore/chitter_chat',
    'author_email': 'tyronelagore@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['cc_server', 'cc_client'],
    'scripts': [],
    'name': 'chitter_chat'
}

setup(**config)

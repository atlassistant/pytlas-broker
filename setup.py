# pylint: disable=C0111

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

with open('pytlas_broker/__about__.py') as about_file:
    ABOUT = {}
    exec(about_file.read(), ABOUT) # pylint: disable=W0122

setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__summary__'],
    long_description=README,
    url=ABOUT['__github_url__'],
    project_urls={
        "Documentation": ABOUT['__doc_url__'],
        "Source": ABOUT['__github_url__'],
        "Tracker": ABOUT['__tracker_url__'],
    },
    author=ABOUT['__author__'],
    author_email=ABOUT['__email__'],
    license=ABOUT['__license__'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'pytlas[snips]~=5.0',
        'paho-mqtt~=1.4.0',
    ],
    extras_require={
        'test': [
            'nose~=1.3.7',
            'sure~=1.4.11',
            'coverage~=4.5.4',
        ],
    },
    entry_points={
        'console_scripts': [
            'pytlas-broker-server = pytlas_broker.cli.server:main',
            'pytlas-broker-client = pytlas_broker.cli.client:main',
        ]
    },
)

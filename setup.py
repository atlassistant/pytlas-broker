from setuptools import setup, find_packages
import os

with open('README.rst', encoding='utf-8') as f:
  readme = f.read()

with open('pytlas_broker/version.py') as f:
  version = f.readline().strip()[15:-1]

setup(
  name='pytlas-broker',
  version=version,
  description='Library and CLI to communicate with the pytlas open-source assistant using MQTT',
  long_description=readme,
  url='https://github.com/atlassistant/pytlas-broker',
  author='Julien LEICHER',
  license='GPL-3.0',
  packages=find_packages(),
  include_package_data=True,
  classifiers=[
    "Programming Language :: Python :: 3",
  ],
  install_requires=[
    'pytlas~=4.0.5',
    'paho-mqtt~=1.4.0',
  ],
  extras_require={
    'test': [
      'nose~=1.3.7',
      'sure~=1.4.11',
      'coverage~=4.5.1',
    ],
  },
  entry_points={
    'console_scripts': [
      'pytlas-broker-server = pytlas_broker.cli.server:main',
      'pytlas-broker-client = pytlas_broker.cli.client:main',
    ]
  },
)
import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='zoom-utils',
    version='0.1',
    packages=[],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'UW-RestClients-Zoom>=0.1.4,<2.0',
        'UW-RestClients-GWS>=2.2.2,<3.0',
    ],
    license='Apache License, Version 2.0',
    description=('AXDD Zoom utilities'),
    url='https://github.com/uw-it-aca/zoom-utils',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)

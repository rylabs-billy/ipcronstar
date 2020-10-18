# setup.py
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name='ipcronstar',
    version='1.0.6',
    description='Add additional IPV4 and IPv6 addresses to Linux',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/rylabs-billy/ipcronstar',
    author='Billy Thompson',
    author_email='rylabs@protonmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['ipcronstar'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ipcronstar=ipcronstar.__main__:main',
        ]
    },
)
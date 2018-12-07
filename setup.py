from distutils.text_file import TextFile
from io import open
from os import path
from pathlib import Path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def parse_requirements(filename: str):
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return TextFile(filename=str(Path(__file__).with_name(filename))).readlines()


setup(
    name='Dispono',
    version='0.1.0',
    url='https://github.com/Viatorus/seejeepee',
    license='MIT',

    author='Toni Neubert',
    author_email='lutztonineubert@gmail.com',

    description='Dispono is a synchronization program between your browser IDE and your local machine.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=find_packages(exclude=('tests',)),
    include_package_data=True,

    install_requires=parse_requirements('requirements.txt'),

    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ],
)

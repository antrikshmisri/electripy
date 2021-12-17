from os import path

from setuptools import setup

from electripy import __version__ as version

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='electripy',
    version=version,
    description='Python UI package powered by Electron and React',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/antrikshmisri/electripy',
    author='Antriksh Misri',
    author_email='antrikshmisri@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['UI', 'Electron', 'React', 'Electripy', 'Python'],
    include_package_data=True,
    packages=['electripy'],
)
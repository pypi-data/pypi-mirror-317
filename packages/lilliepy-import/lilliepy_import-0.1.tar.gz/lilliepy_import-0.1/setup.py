from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text()

setup(
    name='lilliepy-import',
    version='0.1',
    packages=['lilliepy_import'],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='dynamic importer for LilliePy framework',
    keywords=[
        "lilliepy", "lilliepy-importer", 'reactpy'
    ],
    url='https://github.com/websitedeb/lilliepy-import',
    author='Sarthak Ghoshal',
    author_email='sarthak22.ghoshal@gmail.com',
    license='MIT',
    python_requires='>=3.6',
)
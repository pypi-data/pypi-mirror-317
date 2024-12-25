from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text()

setup(
    name='lilliepy-query',
    version='0.1',
    packages=['lilliepy_query'],
    install_requires=[
        'reactpy',
        'asyncio',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='fetching library for fetching and caching data for the Lilliepy Framework',
    keywords=[
        "lilliepy", "lilliepy-query", "reactpy"
    ],
    url='https://github.com/websitedeb/lilliepy-query',
    author='Sarthak Ghoshal',
    author_email='sarthak22.ghoshal@gmail.com',
    license='MIT',
    python_requires='>=3.6',
)

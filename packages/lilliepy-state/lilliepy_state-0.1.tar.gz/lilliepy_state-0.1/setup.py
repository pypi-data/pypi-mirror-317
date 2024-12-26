from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text()

setup(
    name='lilliepy-state',
    version='0.1',
    packages=['lilliepy_state'],
    install_requires=[
        'reactpy'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='state manager for lilliepy framework',
    keywords=[
        "lilliepy", "lilliepy-state", "reactpy"
    ],
    url='https://github.com/websitedeb/lilliepy-state',
    author='Sarthak Ghoshal',
    author_email='sarthak22.ghoshal@gmail.com',
    license='MIT',
    python_requires='>=3.6',
)
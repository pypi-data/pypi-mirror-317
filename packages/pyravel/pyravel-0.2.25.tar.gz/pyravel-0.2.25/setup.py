from setuptools import setup, find_packages

setup(
    name='pyravel',  # Changed name to match command
    version='0.2.25',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package that builds files from the command line.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyravel=pyravel.cli:main',
        ],
    },
    install_requires=[
        'questionary',
        'rich',
    ],
    python_requires=">=3.12",
)

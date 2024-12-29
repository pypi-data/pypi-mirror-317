from setuptools import find_packages, setup

from setuptools import setup, find_packages

setup(
    name='aij_team',  # Name of your library
    version='1.0.0',  # Version of your library
    author='AIJ Team',  # Your name or team name
    author_email='python.bot.0909@gmail.com',  # Your email
    description='A library that does some math-based equations',  # Short description
    long_description=open("README.md").read(),  # Detailed description from README
    long_description_content_type='text/markdown',  # Type of long description
    packages=find_packages(),  # Include only specified packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)

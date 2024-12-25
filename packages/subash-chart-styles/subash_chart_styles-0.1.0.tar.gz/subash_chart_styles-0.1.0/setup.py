# setup.py
from setuptools import setup, find_packages

setup(
    name='subash_chart_styles',  # Name of the package
    version='0.1.0',             # Version of the package
    description='A Python package for generating styled market cap charts',
    long_description=open('README.md').read(),  # Read the long description from the README
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/subash_chart_styles',  # Replace with your GitHub URL
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'matplotlib',  # Required dependencies
        'psycopg2',    # For PostgreSQL access
        'slugify',     # For creating slugs
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

setup(
    name='skufpkg',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'skufpkg=skufpkg.cli:main',
        ],
    },
    install_requires=[
        'requests',
        'flask',
    ],
    description='A simple package manager for Linux',
    author='Zahar Balashov',
    author_email='zaharb840@gmail.com',
)


from setuptools import setup

setup(
    name="SECEdgar-Python",
    version="0.0.1",
    description="A simple to work with library to interact and get information from the SEC edgar Data",
    install_requires=[
        'os>=2.1.4',
        'pandas>=2.2.3',
        'requests>=2.32.3',
        'bs4>=0.0.2'
    ]
)
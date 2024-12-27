from setuptools import setup, find_packages

setup(
    name='CypherPilot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'neo4j>=4.4.0',
    ],
    author='Yaki Naftali',
    author_email='yaki.naftali@accenture.com',
    description='Python Library for Database Interaction with Neo4j',
    long_description_content_type='text/markdown'
)

from setuptools import setup, find_packages

with open('README.md', mode='r') as f:
    description = f.read()

setup(
    name='danteai',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'torch',
        'tensorflow',
        'datasets',
    ],
    long_description=description,
    long_description_content_type='text/markdown'
)
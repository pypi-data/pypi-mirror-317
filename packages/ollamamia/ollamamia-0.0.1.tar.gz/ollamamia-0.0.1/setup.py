from setuptools import setup, find_packages

setup(
    name='ollamamia',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'ollama==0.4.4',
        'tqdm==4.66.4',
        'readchar==4.0.5',
        'termcolor==2.5.0',
        "setuptools==69.5.1"
    ],
)
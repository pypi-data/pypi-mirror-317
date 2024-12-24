from setuptools import setup, find_packages

setup(
    name='ollamamia',
    version='0.0.0',
    author_email='yuda03979@gmail.com',
    description='simple communicate with ollama',
    long_description_content_type='text/markdown',
    long_description=open('README.md', mode="r", encoding="utf-8").read(),
    packages=find_packages(),
    install_requires=[
    ]
)
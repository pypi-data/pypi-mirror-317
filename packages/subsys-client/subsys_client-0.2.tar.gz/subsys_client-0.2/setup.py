   # setup.py
from setuptools import setup, find_packages

setup(
       name='subsys_client',
       version='0.2',
       packages=find_packages(),
       description='The subsys_client Python library facilitates communication and management of subsystems or APIs through a client interface, typically for distributed systems.',
       author='patschu200',
       author_email='patschu@gmail.com',  # Optional: Deine Projekt-URL
       classifiers=[
           'Programming Language :: Python :: 3',
           'License :: OSI Approved :: MIT License',
           'Operating System :: OS Independent',
       ],
       python_requires='>=3.6',
)
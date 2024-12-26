from setuptools import setup, find_packages
with open("README.md","r") as f:
    descrip = f.read()
setup(
name='model_measure',
version='0.0.1',
author='Dhivya Nagasubramanian',
author_email='nagas021@alumni.umn.edu',
description='Machine learning model measurement',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
long_description = descrip,
long_description_content_type='text/markdown',
)
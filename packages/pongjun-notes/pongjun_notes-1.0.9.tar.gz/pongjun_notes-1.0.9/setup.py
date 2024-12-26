from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pongjun-notes',
    version='1.0.9',
    packages=find_packages(include=['notes', 'notes.*']),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',  # Specify the Django version your app supports
    ],
    description='A Django app for managing notes',
    long_description=long_description,  # Add the README content
    long_description_content_type="text/markdown",  # Specify the format
    author='i2x',
    author_email='s6601012610067@kmutnb.ac.com',
    url='https://github.com/i2x/notes',  # Replace with your project URL
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

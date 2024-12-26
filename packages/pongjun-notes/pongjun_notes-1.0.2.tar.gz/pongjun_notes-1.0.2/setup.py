from setuptools import setup, find_packages

setup(
    name='pongjun-notes',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',  # Specify the Django version your app supports
    ],
    description='A Django app for managing notes',
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

from setuptools import setup, find_packages

setup(
    name='pongjun-notes',
    version='0.1.6',
    packages=find_packages(),  # Automatically include all Python packages
    include_package_data=True,  # Include non-Python files like templates and static files
    license='MIT',
    description='A reusable Django app for managing notes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/i2x/notes',  # Replace with your GitHub URL
    author='Pongjun',
    author_email='s6601012610067@kmutnb.ac.th',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'Django>=4.0',
    ],
)

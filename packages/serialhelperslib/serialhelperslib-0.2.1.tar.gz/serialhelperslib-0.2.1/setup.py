from setuptools import setup, find_packages

setup(
    name='serialhelperslib',  # Your package name (must be unique on PyPI)
    version='0.2.1',    # Start with a low version number and increment with releases
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    long_description=open('README.md').read(), # Use your README as long description
    long_description_content_type='text/markdown',  # Specify the type of long description
    url='https://github.com/yourusername/my_package', # Link to your project's repo
    packages=find_packages(), # Automatically find your package modules
    install_requires=[     # List any dependencies your package needs
        'requests',
        'numpy>=1.20.0',
    ],
    classifiers=[          # Metadata for PyPI to categorize your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose an appropriate license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10', # Specify minimum Python version supported
)
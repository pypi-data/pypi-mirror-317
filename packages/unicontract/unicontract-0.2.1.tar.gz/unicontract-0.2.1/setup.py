from setuptools import setup, find_packages
import os

# Read the contents of requirements.txt to install the dependencies
def read_requirements():
    # Read the 'requirements.txt' file
    requirements_file = 'requirements.txt'
    if os.path.exists(requirements_file):
        with open(requirements_file) as f:
            return f.read().splitlines()
    else:
        return []
    
# Setup function to package and distribute the Python project.
setup(
    name='unicontract',  # The name of the package. This is what users will install via pip.
    version='0.2.1',     # The version of the package, update as needed.
    
    # Automatically discover all the sub-packages (directories with __init__.py files).
    packages=find_packages(),  

    # List of dependencies that need to be installed for this package to work properly.
    install_requires=read_requirements(),  # Read dependencies from requirements.txt,

    # Entry points define how the CLI tool is called from the command line.
    entry_points={
        'console_scripts': [
            'unicontract = unicontract.__main__:main',  # When 'unicontract' is run, it will call the main() function from 'unicontract.__main__'.
        ],
    },

    # Read the contents of the README.md to display it on PyPI and in other tools.
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # The format of the long description is Markdown.

    # Classifiers help users find your package on PyPI by categorizing it.
    classifiers=[
        'Programming Language :: Python :: 3',           # The package supports Python 3.
        'License :: OSI Approved :: Apache Software License',  # The license is Apache 2.0.
        'Operating System :: OS Independent',            # The package is platform-independent.
    ],

    # The license for this package. We use the Apache 2.0 license here.
    license='Apache-2.0',  # License for the package, which is Apache License 2.0. The full text should be in the LICENSE file.

    # Include the LICENSE file in the distribution package.
    include_package_data=True,  # This will include the LICENSE file and other non-Python files in the package.
    package_data={
        'unicontract': [
            './*',
            'elements/*',
            'emitters/*',
            'grammar/*',
            'grammar/.antlr/*',
            'linters/*',
            ],
    },
)
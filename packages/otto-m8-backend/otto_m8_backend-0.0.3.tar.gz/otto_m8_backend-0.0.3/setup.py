from setuptools import setup, find_packages

with open('./src/requirements.txt') as f:
    install_requires = f.read().splitlines()
    
    
long_description = """
# Otto-m8 Backend

Otto-m8 Backend is a backend engine for [otto-m8](https://github.com/farhan0167/otto-m8), a low code tool to build and deploy AI/ML workloads.
This package does not need to be installed directly since it is installed via otto-m8's toolkit package.
"""

setup(
    name='otto_m8_backend',
    version='0.0.3',
    description='Backend engine for otto-m8, a low code tool to build and deploy AI/ML workloads.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='farhan0167',
    author_email='ahmadfarhanishraq@gmail.com',
    url='https://github.com/farhan0167/otto-m8',  # URL to your project, if available
    packages=['db', 'db.models'],
    package_dir={'': 'src'},
    install_requires=install_requires,
    python_requires='>=3.10',  # Specify Python version compatibility
)
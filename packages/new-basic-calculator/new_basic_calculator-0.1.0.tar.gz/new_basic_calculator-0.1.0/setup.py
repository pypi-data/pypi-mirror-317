from setuptools import setup, find_packages

setup(
    name='new_basic_calculator',
    version='0.1.0',
    description='A basic calculator SDK',
    author='snowffer',
    author_email='snowffer@xxx.com',
    packages=find_packages(where='./src'),
    package_dir={'': './src'},
    install_requires=[
        'pandas',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
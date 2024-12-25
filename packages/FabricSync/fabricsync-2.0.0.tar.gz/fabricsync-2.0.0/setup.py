from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '2.0.0'

setup(
    name='FabricSync',
    version=version,
    author='Microsoft GBBs North America',  
    author_email='chriprice@microsoft.com',
    description='Fabric Data Sync Utility',
    packages=find_packages(),
    install_requires=requirements,
    project_urls={
        "Documentation": "https://github.com/microsoft/FabricBQSync#README",
        "Source": "https://github.com/microsoft/FabricBQSync",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    package_data={
        'fabricsync': ['fabricsync.png'],
    },
)
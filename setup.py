try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ansibly-idiot_ag",
    version="0.0.1",
    author="Maheshkrishna A G",
    author_email="maheshkrishnagopal@gmail.com",
    description="Ansibly is an Ansible Playbook and Roles generator with vast information on Ansible Modules.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maheshkrishnagopal/Ansibly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        'pymongo',
        'platform',
        'sys',
        'os',
    ]
)

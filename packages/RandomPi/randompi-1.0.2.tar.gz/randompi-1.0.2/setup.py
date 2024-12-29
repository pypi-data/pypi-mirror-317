from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="RandomPi",
    url="https://github.com/realendie/RandomPy/tree/PIP",
    author="Wyatt Johnson",
    author_email="enderprooffical@gmail.com",
    license="Appache 2.0",
    license_files="LICENSE",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4==4.12.3",
        "bs4==0.0.2",
        "certifi==2024.12.14",
        "charset-normalizer==3.4.1",
        "idna==3.10",
        "requests==2.32.3",
        "setuptools==75.6.0",
        "soupsieve==2.6",
        "urllib3==2.3.0",
    ],
    keywords=["python", "random", "pypi", "package", "random package"],
    short_description="RandomPi is a simple package that uses the PyPi api to get a random python package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "get_random_pi = RandomPi:get_random_pi",
            "get_randompi = RandomPi:get_random_pi",
        ]
    },
)

#  python setup.py sdist bdist_wheel
#  twine upload dist/*

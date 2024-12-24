import setuptools
import re
import requests
from bs4 import BeautifulSoup

package_name = "enumer"

VERSION = None


def curr_version():
    global VERSION
    if VERSION is None:
        with open('VERSION', 'r', encoding = 'utf-8') as f:
            VERSION = f.read()
    return VERSION


def get_version():
    return curr_version()
    '''
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", curr_version())
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))

    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    new_version_str = f"{major}.{minor}.{patch}"
    return new_version_str
    '''


def upload():
    with open("README.md", "r", encoding = 'utf-8') as fh:
        long_description = fh.read()
    with open('requirements.txt', 'r', encoding = 'utf-8') as f:
        required = f.read().splitlines()

    setuptools.setup(
        name=package_name,
        version=get_version(),
        author="Astrageldon",
        author_email="astrageldon@gmail.com",
        description="Residue class enumeration given partial information of either end.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/enumer/",
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.9',
        install_requires=required,
    )


def write_curr_version():
    print("Current VERSION:", curr_version())
    with open("VERSION", "w", encoding = 'utf-8') as version_f:
        version_f.write(get_version())


def main():
    try:
        upload()
        print("Upload success, Current VERSION:", curr_version())
    except Exception as e:
        raise Exception("Upload package error", e)
    
    write_curr_version()


if __name__ == '__main__':
    main()
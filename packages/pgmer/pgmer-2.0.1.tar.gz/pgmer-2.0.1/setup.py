import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.0.1'
DESCRIPTION = 'Tools for front-end engineering'
LONG_DESCRIPTION = 'Tools for front-end engineering'

# Setting up
setup(
    name="pgmer",
    version=VERSION,
    author="小鱼程序员",
    author_email="732355054@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'websockets',
        'requests',
        'loguru',
        'websocket-client'
    ],
    keywords=['python', 'front-end engineering', 'pyzjr', 'windows', 'mac', 'linux'],
    classifiers=[
        "Development Status :: 4 - Beta",  # 更改开发状态
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8'
)
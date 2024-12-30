from setuptools import setup, find_packages
import os
import codecs

VERSION = '0.0.1'
DESCRIPTION = "A Python package to send messages and images to Telegram groups using 'requests' package only."
LONG_DESCRIPTION = ""

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()


# Setting up
setup(
    name="telegramy",
    version=VERSION,
    author="Yan Sido",
    author_email="yansido1@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'telegram', 'telegram-sender', 'telegram sender', 'telegramy', 'telegramy sender', 'telegramy python', 'telegramy sender python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
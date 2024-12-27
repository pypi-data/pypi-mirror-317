from setuptools import setup, find_packages

classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.12",
]

setup(
name = "custom_print",
version = "0.0.5",
author = "Miguel Angel Aguilar Cuesta",
author_email = "acma.mex@gmail.com",
description = "Print a list type as a table style",
long_description = open("README.md").read(),
long_description_content_type = "text/markdown",
url = "https://github.com/acma82/Custom_Print",
license = "EveryOneCanUseIt",
packages = find_packages(),
install_requires = [''],
classifiers=classifiers,
keywords="custom_print"
)

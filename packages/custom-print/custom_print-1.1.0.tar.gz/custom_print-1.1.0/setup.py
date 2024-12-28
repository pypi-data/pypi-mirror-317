from setuptools import setup, find_packages

setup(
name = "custom_print",
version = "1.1.0",
author = "Miguel Angel Aguilar Cuesta",
author_email = "acma.mex@gmail.com",
description = "Customized Print Style",
long_description = open("README.md").read(),
long_description_content_type = "text/markdown",
url = "https://github.com/acma82/Custom_Print",
license = "Everyone Can Use It",
packages = find_packages(),
install_requires = [''],
keywords = ["print","custom print","fancy print", "fancy message", "font style"],
classifiers = [ "Topic :: Utilities",
                "Programming Language :: Python :: 3.12",
                "Operating System :: Unix",
                "Operating System :: Microsoft :: Windows"],
entry_points = {"console_scripts": ["custom_print = custom_print.cmdl:main"]}
      )

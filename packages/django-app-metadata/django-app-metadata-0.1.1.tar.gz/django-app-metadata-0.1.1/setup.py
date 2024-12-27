# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages
from django_app_metadata import version

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires if x.strip()]


setup(
    name="django-app-metadata",
    version=version.VERSION,
    description="Django数据字典管理应用。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rRR0VrFP",
    maintainer="rRR0VrFP",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django-app-metadata", "django"],
    install_requires=requires,
    packages=find_packages(
        ".",
        exclude=[
            "django_app_metadata_demo",
            "django_app_metadata_example",
            "django_app_metadata_example.migrations",
        ],
    ),
    zip_safe=False,
    include_package_data=True,
)

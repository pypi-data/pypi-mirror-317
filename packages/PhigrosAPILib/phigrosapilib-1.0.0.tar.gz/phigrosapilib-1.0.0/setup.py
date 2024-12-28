from setuptools import setup, find_packages

setup(
  name="PhigrosAPILib",
  version="1.0.0",
  author="Nekitori17",
  author_email="cuongnguyen286641@gmail.com",
  description="A library for accessing Phigros API",
  long_description=open("README.md", "r", encoding="utf-8").read(),
  long_description_content_type="text/markdown",
  license="GNU General Public License v3 (GPLv3)",
  url="https://github.com/Nekitori17/phigrs-api-lib",
  keywords=["Phigros", "API"],
  packages=find_packages(include=["PhigrosAPILib", "PhigrosAPILib.*", "PhigrosAPILib."]),
  install_requires=["click", "requests", "pycryptodome"],
  package_data={"PhigrosAPILib": ["data/*.json"]},
  entry_points={
    "console_scripts": [
      "updatePhiDB=PhigrosAPILib.Cli:main"
    ]
  },
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10"
  ],
  python_requires=">=3.7",
)

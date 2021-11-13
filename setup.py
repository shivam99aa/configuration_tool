from setuptools import setup, find_packages

setup(
    name="configzz",
    version="0.0.1",
    description="config tool for configuring debian machines.",
    author="shivam shukla",
    author_email="shivam99aa@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(
        where="src"
    ),
    entry_points={
        "console_scripts": [
            "configzz=configzz.main:main"
        ]
    }
)
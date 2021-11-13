from setuptools import setup

setup(
    name="configzz",
    version="0.0.1",
    description="config tool for configuring debian machines.",
    author="shivam shukla",
    author_email="shivam99aa@gmail.com",
    entry_points={
        "console_scripts": [
            "configzz=configzz.main:main"
        ]
    }
)
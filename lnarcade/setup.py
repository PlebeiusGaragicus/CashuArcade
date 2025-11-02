from setuptools import setup

setup(
    name="lnarcade",
    version="1.0.0",
    packages=["lnarcade"],
    package_dir={"lnarcade": "."},
    install_requires=[
        "pygame",
    ],
    python_requires=">=3.7",
)

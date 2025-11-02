from setuptools import setup

setup(
    name="gamelib",
    version="1.0.0",
    packages=["gamelib"],
    package_dir={"gamelib": "."},
    install_requires=[
        "pygame",
    ],
    python_requires=">=3.7",
)

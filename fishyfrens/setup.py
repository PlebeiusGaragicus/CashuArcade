from setuptools import setup

setup(
    name="fishyfrens",
    version="1.0.0",
    packages=["fishyfrens"],
    package_dir={"fishyfrens": "."},
    install_requires=[
        "pygame",
        "numpy",
        "icecream",
    ],
    python_requires=">=3.7",
)

from setuptools import setup

setup(
    name="slots",
    version="1.0.0",
    description="Casino Slots - A classic slot machine game",
    author="CashuArcade",
    packages=["slots"],
    package_dir={"slots": "."},
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "slots=slots.__main__:main",
        ],
    },
    python_requires=">=3.7",
)

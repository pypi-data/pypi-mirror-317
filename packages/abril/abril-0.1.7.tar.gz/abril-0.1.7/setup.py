from setuptools import setup

setup(
    name="abril",
    version="0.1.7",
    package_dir={"": "src"},
    packages=["abril"],
    install_requires=[
        "torch>=1.7.1",
        "pillow>=7.1.2",
        "numpy>=1.18.5",
        "clip",  # Just specify clip as a regular dependency
    ],
    dependency_links=[
        "https://github.com/openai/CLIP/tarball/master#egg=clip"  # Use this format for git dependencies
    ],
)

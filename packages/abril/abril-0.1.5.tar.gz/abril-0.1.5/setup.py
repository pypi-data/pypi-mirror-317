from setuptools import setup

setup(
    name="abril",
    version="0.1.5",
    package_dir={"": "src"},
    packages=["abril"],
    install_requires=[
        "torch>=1.7.1",
        "pillow>=7.1.2",
        "numpy>=1.18.5",
        "clip @ git+https://github.com/openai/CLIP.git@v0.1.3",
    ],
)

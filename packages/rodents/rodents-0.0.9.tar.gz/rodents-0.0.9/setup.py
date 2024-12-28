from setuptools import setup, find_packages

setup(
    name="rodents",
    version="0.0.9",
    packages=find_packages(),
    entry_points={"console_scripts": ["rodents = rodents.jiggler:run_jiggler"]},
    install_requires=open("requirements.txt", encoding="utf-8").readlines(),
)

from setuptools import setup, find_packages

setup(
    name="inference",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["inference", "utils"],
    install_requires=["xgboost", "pandas", "numpy"],
)

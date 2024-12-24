from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name="coocoo",
    version="0.1.0",
    author="eyadrealhim",
    description="A simple io game simulator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eyadrealhim/coocoo",
    ext_modules=cythonize(
        [  # This compiles your Cython code
            Extension("coocoo.module", ["coocoo/module.pyx"])
        ]
    ),
    packages=["coocoo"],
    classifiers=[],
    install_requires=[],  # Any dependencies can be listed here
    python_requires=">=3.6",
)

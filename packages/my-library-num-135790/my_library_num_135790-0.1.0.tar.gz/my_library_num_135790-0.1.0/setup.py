from setuptools import setup, find_packages

setup(
    name="my_library_num_135790",
    version="0.1.0",
    test_suite='tests',
    packages=find_packages(),
    install_requires=[],
    author="Седохин Даниил",
    author_email="sedokhin.daniil@gmail.com",
    description="Библиотека направленная на работу с текстом и математическими вычислениями",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Daniil2234/lab04-Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)

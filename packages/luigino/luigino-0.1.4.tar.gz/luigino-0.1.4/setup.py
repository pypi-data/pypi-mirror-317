from setuptools import setup, find_packages

setup(
    name="luigino",
    version="0.1.4",
    author="Jung JinYoung",
    author_email="bungker@gmail.com",
    description="Utilities package for Luigi tasks with Celery integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyjung/luigino",
    packages=find_packages(),
    install_requires=[
        "luigi",
        "celery",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
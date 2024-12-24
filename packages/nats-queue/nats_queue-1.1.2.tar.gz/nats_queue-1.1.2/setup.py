from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="nats_queue",
    version="1.1.2",
    author="k.shishkina",
    author_email="klikklok2017@gmail.com",
    license="MIT",
    description="This is my first module for queue_nats",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/qwejid/nats_queue",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["requests>=2.25.1", "setuptools>=42", "nats-py>=2.9.0"],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="python nats",
    python_requires=">=3.9",
)

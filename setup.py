import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tg",
    version="0.0.1",
    author="Aleksi Anisimov",
    author_email="a.aleksu@gmail.com",
    description="Very basic stuff for Telegram client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaleksu/tg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

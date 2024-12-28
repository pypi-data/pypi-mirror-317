from setuptools import setup, find_packages

setup(
    name="fagflag",
    version="1.0.9",
    description="Generate pride flags as bitmap or vector images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="disuko",
    author_email="disuko@redpandastudios.net",
    url="https://github.com/Red-Panda-Studios/fagflag",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Pillow"],
    entry_points={
        "console_scripts": [
            "fagflag=fagflag.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

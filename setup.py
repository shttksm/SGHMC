import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SGHMC_bs",
    version="0.0.1",
    author="Boyao Li, Shota Takeshima",
    author_email="boyao.li@duke.edu, shota.takeshima@duke.edu",
    description="Python implementation of SGHMC as STA663 Final Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shttksm/SGHMC/",
    project_urls={
        "Bug Tracker": "https://github.com/shttksm/SGHMC/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

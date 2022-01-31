import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kube_kombu",
    version="v1.0.4",
    install_requires=[
        "kombu==5.2.3",
    ],
    author="Anmol Porwal",
    author_email="anmolporwal@ymail.com",
    description="Running kombu consumers with support of liveness probe for kubernetes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Anmol-Porwal18/kube_kombu",
    platforms=["any"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(exclude=("sample",)),
    python_requires=">=3.7",
    keywords=["kubernetes", "kombu", "consumer", "liveness probe"],
)

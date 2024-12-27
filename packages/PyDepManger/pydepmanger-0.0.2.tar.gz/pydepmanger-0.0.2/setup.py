import setuptools

setuptools.setup(
    name="PyDepManger",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abuawadd/PyDepManger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy==2.2.0",
        "pandas==2.2.3",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.2",
        "scipy==1.14.1",
        "six==1.17.0",
        "tzdata==2024.2",
    ],
    packages=setuptools.find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
